# reddit-to-tiktok
###### This project is only the rendering and publishing part of a bigger project to create TikTok videos from Reddit posts.
### Follow on TikTok account to see the results: [@reddittotiktoklaravieira](https://www.tiktok.com/@reddittotiktoklaravieira)

## Overview
This project is a Python rendering and publishing pipeline that takes Reddit posts data and converts them into TikTok videos. The pipeline includes downloading assets from a MinIO server, generating a thumbnail, creating a video with audio and subtitles, and finally uploading the video to TikTok.
#### Thumbnail
The thumbnail is generated using the subreddit community icon and the post data. It has the fix width and the height is calculated based on the title length.
![thumbnail.png](assets/readme/thumbnail.png)
#### Video
The video is generated using the background video, TTS audio of the post title and content, and subtitles. The video has a fixed width and the height is calculated based on the background video aspect ratio (its optimized for TikTok, 1080x1920).
[![Watch the video](https://img.youtube.com/vi/N_YoukvxIaE/hqdefault.jpg)](https://www.youtube.com/embed/N_YoukvxIaE)

## Requirements
To run this project, you need to have already done:
- `assets/inputs/post.json` File with the raw reddit-api post data;
- `assets/inputs/subreddit.png` Subreddit community icon;
- `assets/inputs/title.wav` TTS audio of the post title;
- `assets/inputs/content.wav` TTS audio of the post content;
- `assets/inputs/subtitle.srt` Subtitle file of the post content;
- `assets/inputs/background.mp4` Background video for the TikTok;

To run this project, you need to have installed:
- `python>=3.10`
- `minio>=7.2.15`
- `moviepy>=2.1.2`
- `pillow>=10.4.0`
- `pysrt>=1.1.2`
- `requests>=2.31.0`
- `requests-auth-aws-sigv4>=0.7`

You can install the required packages using:
```bash
pip install -r requirements.txt
```

## Configuration
You need to set the environment variables for the MinIO connection:
```bash
export MINIO_ENDPOINT=
export MINIO_ACCESS_KEY=
export MINIO_SECRET_KEY=
export MINIO_SECURE=true
export MINIO_BUCKET=
export OBJECT_NAME_BACKGROUND_VIDEO=backgrounds/minecraft-1.mp4
export OBJECT_NAME_SUBREDDIT_PICTURE=subreddit.png
export OBJECT_NAME_POST_FILE=post.json
export OBJECT_NAME_TITLE_AUDIO=title.wav
export OBJECT_NAME_CONTENT_AUDIO=content.wav
export OBJECT_NAME_SUBTITLES_FILE=subtitles.srt
export OBJECT_NAME_THUMBNAIL=thumbnail.png
export OBJECT_NAME_VIDEO=video.mp4
```
You need to set the environment variable for the TikTok API:
```bash
export TIKTOK_PUBLISH_ENABLE=true
export TIKTOK_SESSION_ID=
export TIKTOK_TAGS=reddit,reddit-to-tiktok
export TIKTOK_SCHEDULE_TIMESTAMP=0
export TIKTOK_URL_PREFIX=www
```
You need to set the environment variables for the video rendering:
```bash
export VIDEO_CODEC=h264
export VIDEO_PRESET=slow
export VIDEO_BITRATE=4000k
export VIDEO_FPS=30
```

## Usage
1. Get files from MinIO:
```bash
python3 src/input-download.py
```
2. Generate the title thumbnail:
```bash
python3 src/thumbnail-generator.py
```
3. Generate the video:
```bash
python3 src/video-generator.py
```
4. Upload the video and thumbnail to MinIO:
```bash
python3 src/output-upload.py
```
5. Publish the video to TikTok:
```bash
python3 src/output-publish.py
```

## Credits
Credits to [546200350](https://github.com/546200350) for the [TikTokUploader](https://github.com/546200350/TikTokUploder) project.