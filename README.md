# Description

The goal of the project is to allow automated subtitling of videos.

# Technical Work

Here are the different components of the project:
- Whisper is used to timestamp the text of a video.
- GPT-4o then assembles the timestamps using a script.
- Once this assembling is done, the timestamps are parsed to create an srt file.
- This srt file then allows through the moviepy library subtitling of the video.

# Setup

Create yourself a config.yaml file with your openai api key.

Have the openai api key noted as OPENAI_API_KEY.

Only three libraries are required : openai, pyyaml and moviepy.

# Image Magick and Ffmpeg

You also need to install Image Magick within your system for the process to work.

A link that can be useful: http://www.imagemagick.org/script/binary-releases.php

You also need ffmpeg which can be found here: https://ffmpeg.org/download.html

# Subtitling a video

To subtitle a video after all previous steps are down, have a script.txt file and a video.mp4 file.

Then launch the subtitling notebook, and the magic should happen.

# Results

This process has been tested on a 2:30 min video with success. No guarantee for beyond 5 minutes.