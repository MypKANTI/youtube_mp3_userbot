from pytubefix import YouTube


def download_video_youtube(url: str):
    yt = YouTube(url)
    audio_stream = yt.streams.get_audio_only()

    title = yt.title
    author = yt.author
    length = yt.length
    views = yt.views
    likes = yt.likes
    publish_date = yt.publish_date

    path = audio_stream.download(
        output_path="music", filename=title.replace(".mp3", "") + ".mp3"
    )

    return {
        "path_audio": path,
        "title": title,
        "author": author,
        "length": length,
        "info": {
            "views": views,
            "likes": likes,
            "publish_date": publish_date,
        },
    }
