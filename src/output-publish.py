import os
import requests
import json
import time
import datetime
from urllib.parse import urlencode

from TikTokUploader.x_bogus_ import get_x_bogus
from TikTokUploader.util import assertSuccess, printError, getTagsExtra, uploadToTikTok, log, getCreationId


UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'

def uploadVideo(session_id, video, title, tags, users=[], url_prefix='us', schedule_time: int = 0, proxy: dict = None):
    # In the TikTok web version, the schedule must be as least 15 minutes in the future, and a maximum of 10 days, also the minutes in schedule_time must be multiple of 5
    tiktok_min_margin_schedule_time =  900  # 15 minutes
    tiktok_max_margin_schedule_time = 864000  # 10 days
    margin_to_upload_video = 300  # 5 minutes

    min_schedule_time = datetime.datetime.now(datetime.UTC) + tiktok_min_margin_schedule_time + margin_to_upload_video
    max_schedule_time = datetime.datetime.now(datetime.UTC) + tiktok_max_margin_schedule_time

    if schedule_time == 0:
        pass
    elif schedule_time < min_schedule_time:
        print(f"[-] Can not schedule video in less than {(tiktok_min_margin_schedule_time + margin_to_upload_video) // 60} minutes")
        return False
    elif schedule_time > max_schedule_time:
        print(f"[-] Can not schedule video in more than {tiktok_max_margin_schedule_time // 86400} days")
        return False

    session = requests.Session()

    if proxy:
        session.proxies.update(proxy)
    session.cookies.set('sessionid', session_id, domain='.tiktok.com')
    session.verify = True
    headers = {
        'User-Agent': UA
    }
    url = f"https://{url_prefix}.tiktok.com/upload/"
    r = session.get(url, headers=headers)
    if not assertSuccess(url, r):
        return False
    creationid = getCreationId()
    url = f"https://{url_prefix}.tiktok.com/api/v1/web/project/create/?creation_id={creationid}&type=1&aid=1988"
    headers = {
        'X-Secsdk-Csrf-Request': '1',
        'X-Secsdk-Csrf-Version': '1.2.8'
    }
    r = session.post(url, headers=headers)
    if not assertSuccess(url, r):
        return False
    try:
        tempInfo = r.json()['project']
    except KeyError:
        print(f"[-] An error occured while reaching {url}")
        print("[-] Please try to change the --url_server argument to the adapted prefix for your account")
        return False
    creationID = tempInfo['creationID']
    projectID = tempInfo['project_id']
    # 获取账号信息
    url = f"https://{url_prefix}.tiktok.com/passport/web/account/info/"
    r = session.get(url)
    if not assertSuccess(url, r):
        return False
    # user_id = r.json()["data"]["user_id_str"]
    log('Start uploading video')
    video_id = uploadToTikTok(video, session)
    if not video_id:
        log('Video upload failed')
        return False
    log('Video uploaded successfully')
    time.sleep(2)
    result = getTagsExtra(title, tags, users, session, url_prefix)
    time.sleep(3)
    title = result[0]
    text_extra = result[1]
    markup_text = result[2]
    postQuery = {
        'app_name': 'tiktok_web',
        'channel': 'tiktok_web',
        'device_platform': 'web',
        'aid': 1988
    }
    data = {
        "post_common_info": {
            "creation_id": creationID,
            "enter_post_page_from": 1,
            "post_type": 3
        },
        "feature_common_info_list": [
            {
                "geofencing_regions": [],
                "playlist_name": "",
                "playlist_id": "",
                "tcm_params": "{\"commerce_toggle_info\":{}}",
                "sound_exemption": 0,
                "anchors": [],
                "vedit_common_info": {
                    "draft": "",
                    "video_id": video_id
                },
                "privacy_setting_info": {
                    "visibility_type": 0,
                    "allow_duet": 1,
                    "allow_stitch": 1,
                    "allow_comment": 1
                }
            }
        ],
        "single_post_req_list": [
            {
                "batch_index": 0,
                "video_id": video_id,
                "is_long_video": 0,
                "single_post_feature_info": {
                    "text": title,
                    "text_extra": text_extra,
                    "markup_text": markup_text,
                    "music_info": {},
                    "poster_delay": 0,
                }
            }
        ]
    }
    if schedule_time == 0:
        pass
    elif schedule_time > min_schedule_time:
        # Confirm again because the video upload can be very long
        data["feature_common_info_list"][0]["schedule_time"] = schedule_time
    else:
        log(f"Video schedule time is less than {tiktok_min_margin_schedule_time // 60} minutes in the future, the upload process took more than"
            f"the {margin_to_upload_video // 60} minutes of margin to upload the video")
        return False
    postQuery['X-Bogus'] = get_x_bogus(urlencode(postQuery), json.dumps(data, separators=(',', ':')), UA)
    url = f'https://{url_prefix}.tiktok.com/tiktok/web/project/post/v1/'
    headers = {
        'Host': f'{url_prefix}.tiktok.com',
        'content-type': 'application/json',
        'user-agent': UA,
        'origin': 'https://www.tiktok.com',
        'referer': 'https://www.tiktok.com/'
    }
    r = session.post(url, params=postQuery, data=json.dumps(data, separators=(',', ':')), headers=headers)
    if not assertSuccess(url, r):
        log("Publish failed")
        printError(url, r)
        return False
    if r.json()["status_code"] == 0:
        log(f"Published successfully {'| Scheduled for ' + str(schedule_time) if schedule_time else ''}")
    else:
        log("Publish failed")
        printError(url, r)
        return False

    return True

if __name__ == '__main__':
    if os.getenv('TIKTOK_PUBLISH_ENABLE', 'false').lower() != 'true':
        print('Publishing to TikTok is disabled. Set TIKTOK_PUBLISH_ENABLE to true to enable.')
        exit(0)

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