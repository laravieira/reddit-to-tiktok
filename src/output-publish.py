from TikTokUploader.uploader import uploadVideo
import os
import json

if __name__ == '__main__':
    post_title = ''

    with open('assets/inputs/post.json', 'r', encoding='utf-8') as file:
        post = json.load(file)
        post_title = post['title']

    uploadVideo(
        session_id=os.getenv('TIKTOK_SESSION_ID'),
        video='assets/output/video.mp4',
        title=post_title,
        tags=os.getenv('TIKTOK_TAGS', 'reddit').split(','),
        schedule_time=int(os.getenv('TIKTOK_SCHEDULE_TIMESTAMP', 0)),
        url_prefix=os.getenv('TIKTOK_URL_PREFIX', 'www'),
    )