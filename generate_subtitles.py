import re 
import yaml
from openai import OpenAI

def read_config(config_path: str) -> dict:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = read_config('config.yaml')
api_key = config['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)

def read_script(script_path:str) -> str:
    with open(script_path, "r", encoding="utf-8") as file:
        script = file.read()
    return script

def transcribe_video(video_path:str) -> str:
    audio_file = open(video_path, "rb")
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )
    return transcript

def create_timestamping_prompt(script:str, transcript:str) -> str:
    timestamping_prompt = f"""You are being given this whisper output, which is the transcript of a video.
    Here is the script of this video: <script> {script} </script>
    Here is the whisper transcript: <transcript> {transcript.words} </transcript>
    Output in format: "(timestamp) - (group of words)" using the lines of the script, splitting into chunks of at most 4 words like I was subtitling the video.
    Output your timestamping answer between <output> and </output> tags.
    Output:"""
    return timestamping_prompt

def timestamp_transcript(script:str, transcript:str) -> str:
    openai_prompt = create_timestamping_prompt(script, transcript)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": openai_prompt
            }
        ]
    )
    output_text = completion.choices[0].message.content
    timestamped_subtitles = re.match(r".*<output>(.*)</output>.*", output_text, re.DOTALL).group(1)
    return timestamped_subtitles

def parse_lyrics(input_text:str) -> tuple:
    pattern = r'\(([\d.]+)\)\s*-\s*(.+)'
    matches = re.findall(pattern, input_text)
    timestamps = []
    lines = []
    for match in matches:
        timestamp = float(match[0]) 
        line = match[1].strip()
        timestamps.append(timestamp)
        lines.append(line)
    n_sec_per_word = (timestamps[-1] - timestamps[-2])/len(lines[-2].split())
    final_timestamp = timestamps[-1] + n_sec_per_word*len(lines[-1].split())
    timestamps.append(final_timestamp)
    return timestamps, lines

def create_srt_file(timestamps:list, lines:list, output_file:str='subtitles.srt') -> None:
    with open(output_file, 'w') as f:
        for i, (start, end, text) in enumerate(zip(timestamps[:-1], timestamps[1:], lines), 1):
            # Format start and end time to srt's hour:minute:second,millisecond
            start_time = format_time(start, is_start=1)
            end_time = format_time(end, is_start=0)
            f.write(f"{i}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

def format_time(seconds:float, is_start:bool) -> str:
    millisec = int((seconds % 1  + 0.1*is_start) * 1000)
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{sec:02},{millisec:03}"

def generate_subtitles(video_path:str, script_path:str, output_file='subtitles_2.srt') -> None:
    script = read_script(script_path)
    transcript = transcribe_video(video_path)
    timestamped_transcript = timestamp_transcript(script, transcript)
    timestamps, lines = parse_lyrics(timestamped_transcript)
    create_srt_file(timestamps, lines, output_file)
