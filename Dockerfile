FROM python:3.13-bullseye

ENV MINIO_ENDPOINT ''
ENV MINIO_ACCESS_KEY ''
ENV MINIO_SECRET_KEY ''
ENV MINIO_SECURE 'true'
ENV MINIO_BUCKET ''

ENV OBJECT_NAME_BACKGROUND_VIDEO 'backgrounds/minecraft-1.mp4'
ENV OBJECT_NAME_SUBREDDIT_PICTURE 'subreddit.png'
ENV OBJECT_NAME_POST_FILE 'post.json'
ENV OBJECT_NAME_TITLE_AUDIO 'title.wav'
ENV OBJECT_NAME_CONTENT_AUDIO 'content.wav'
ENV OBJECT_NAME_SUBTITLES_FILE 'subtitles.srt'

ENV OBJECT_NAME_THUMBNAIL 'thumbnail.png'
ENV OBJECT_NAME_VIDEO 'video.mp4'

ENV VIDEO_CODEC 'h264'
ENV VIDEO_PRESET 'slow'
ENV VIDEO_BITRATE '4000k'
ENV VIDEO_FPS '30'

WORKDIR /app
COPY requirements.txt requirements.txt
COPY src .
COPY assets/fonts assets/fonts

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]