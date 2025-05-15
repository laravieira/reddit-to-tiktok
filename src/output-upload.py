from minio import Minio
import os

files = [
    (os.getenv('OBJECT_NAME_THUMBNAIL', 'thumbnail.png'), 'assets/output/thumbnail.png'),
    (os.getenv('OBJECT_NAME_VIDEO',     'video.mp4'),     'assets/output/video.mp4'),
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
        minio.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path
        )
        print(f"{object_name} uploaded.")