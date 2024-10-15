from moviepy.editor import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip


# Load the video file
def subtitle_video(video_path:str, subtitle_path:str, output_path:str) -> None:
    video = VideoFileClip(video_path)
    generator = lambda txt: TextClip(txt, font='Comic-Sans-MS-Bold-Italic', fontsize=50, color='yellow', stroke_color='black', stroke_width=2)
    subtitles = SubtitlesClip(subtitle_path, generator)
    result = CompositeVideoClip([video, subtitles.set_pos(("center", 0.7), relative=True)])
    result.write_videofile(output_path, codec="libx264",audio_codec="aac", fps=video.fps,)