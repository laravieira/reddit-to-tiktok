from minio import Minio
import os

files = [
    (os.getenv('OBJECT_NAME_BACKGROUND_VIDEO',  'background.mp4'), 'assets/inputs/background.mp4'),
    (os.getenv('OBJECT_NAME_SUBREDDIT_PICTURE', 'subreddit.png'),  'assets/inputs/subreddit.png'),
    (os.getenv('OBJECT_NAME_POST_FILE',         'post.json'),      'assets/inputs/post.json'),
    (os.getenv('OBJECT_NAME_TITLE_AUDIO',       'title.wav'),      'assets/inputs/title.wav'),
    (os.getenv('OBJECT_NAME_CONTENT_AUDIO',     'content.wav'),    'assets/inputs/content.wav'),
    (os.getenv('OBJECT_NAME_SUBTITLES_FILE',    'subtitles.srt'),  'assets/inputs/subtitles.srt'),
]

if __name__ == '__main__':
    minio = Minio(
        endpoint=os.getenv('MINIO_ENDPOINT'),
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=os.getenv('MINIO_SECURE', 'false').lower() == 'true',
    )
    bucket_name = os.getenv('BUCKET_NAME', 'reddit-to-tiktok')

    for object_name, file_path in files:
        minio.fget_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path
        )
        print(f"{object_name} downloaded.")