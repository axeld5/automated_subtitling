import json
from moviepy.editor import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip

def read_subtitle_config(config_path: str) -> dict:
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

def subtitle_video(
        video_path:str, 
        subtitle_path:str, 
        output_path:str, 
        subtitle_config_path:str="subtitle_config.json",
    ) -> None:
    video = VideoFileClip(video_path)
    subtitle_config = read_subtitle_config(subtitle_config_path)
    text_config = subtitle_config["TEXT"]
    pos_config = subtitle_config["POSITION"]
    generator = lambda txt: TextClip(txt, **text_config)
    subtitles = SubtitlesClip(subtitle_path, generator)
    result = CompositeVideoClip([video, subtitles.set_pos((pos_config["x"], pos_config["y"]), relative=True)])
    result.write_videofile(output_path, codec="libx264",audio_codec="aac", fps=video.fps,)
