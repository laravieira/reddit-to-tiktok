from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, ImageClip
from moviepy.video.fx import FadeOut, Resize, CrossFadeIn
import pysrt
import os

audioTitle = AudioFileClip('assets/inputs/title.wav')
audioContent = AudioFileClip('assets/inputs/content.wav')

clip = (
    VideoFileClip('assets/inputs/background.mp4')
        .subclipped(0, audioTitle.duration+audioContent.duration)
        .without_audio()
)

def build_subtitles(video):
    subs = pysrt.open('assets/inputs/subtitles.srt', encoding='utf-8')
    subs.shift(milliseconds=-120)
    subtitles = []
    for sub in subs:
        start = sub.start.ordinal/1000
        end = sub.end.ordinal/1000
        duration = end - start
        clip = (
            TextClip(
                text=sub.text.strip('-.,— '),
                font='assets/fonts/RedditSans-Bold.ttf',
                font_size=60,
                color='white',
                stroke_color="black",
                stroke_width=5,
                text_align='center',
                duration=duration,
                method='caption',
                size=(video.size[0]-24*2, video.size[1]),
                margin=(0, 0)
            )
            .with_start(start)
            .with_effects([CrossFadeIn(.05)])
        )
        subtitles.append(clip)
    return CompositeVideoClip(subtitles)

thumbnail = (
    ImageClip('assets/output/thumbnail.png')
        .with_position('center', 'center')
        .with_duration(audioTitle.duration)
        .with_audio(audioTitle)
        .with_effects([Resize(width=clip.size[0]-32), FadeOut(.1)])
)

subtitles = (
    build_subtitles(clip)
        .with_position('center', 'center')
        .with_duration(audioContent.duration)
        .with_audio(audioContent)
        .with_start(audioTitle.duration)
)

result = CompositeVideoClip([clip, thumbnail, subtitles])
result.write_videofile(
    filename='assets/output/video.mp4',
    codec=os.getenv('VIDEO_CODEC', 'h264'),
    preset=os.getenv('VIDEO_PRESET', 'slow'),
    bitrate=os.getenv('VIDEO_BITRATE', None),
    fps=int(os.getenv('VIDEO_FPS', 30)),
)