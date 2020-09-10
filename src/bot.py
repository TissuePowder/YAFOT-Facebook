import requests
import os
import time
import config

current_frame_number = ""
total_frames = ""
image = ""
timestamp = ""
padding = ""
dummy_response = {"id": "123456789", "post_id": "987654321_123456789"}


def initialize(_current_frame_number, _total_frames, _image):
    global current_frame_number
    current_frame_number = _current_frame_number
    global total_frames
    total_frames = _total_frames
    global image
    image = _image
    global padding
    padding = len(str(_total_frames))
    base_filename = os.path.basename(_image)
    filename_without_ext = os.path.splitext(base_filename)[0]
    frame_pts = int(filename_without_ext.split("_")[1].lstrip("0"))
    global timestamp
    timestamp = time.strftime(f"%Mm:%Ss.{(frame_pts % 1000):03}ms", time.gmtime(frame_pts / 1000.0))


def post_caption():
    msg: str = (
        ""
        # f"Some anime\n"
        # f"Episode 01 of 12\n"
    )
    msg += (
        f"Frame {current_frame_number:0{padding}} of {total_frames:0{padding}}\n"
        f"Timestamp: {timestamp}"
        # f"\nTag: ABCXX_E1F{current_frame_number}"
    )
    if config.verbose:
        print(f"defined post caption:\n{msg}")

    return msg


def comment_caption():
    msg = (
        ""
        # f"Raw frame without subtitles
    )
    if config.verbose:
        print(f"defined comment caption:\n{msg}")

    return msg


def album_post_caption(post_id):
    msg = (
        # f"Episode number - "
        f"{current_frame_number:0{padding}}/{total_frames:0{padding}} - {timestamp}\n"
        f"Original post: https://www.facebook.com/{post_id}"
    )
    if config.verbose:
        print(f"defines album_post caption:\n{msg}")

    return msg


def make_post():
    if config.dry_run:
        return dummy_response
    caption = post_caption()
    url = (
        f"https://graph.facebook.com/{config.page_id}/photos?"
        f"caption={caption}&access_token={config.token}"
    )
    files = {
        'image': open(image, "rb")
    }
    response = requests.post(url, files=files)
    return response.json()


def make_comment(post_id):
    if config.dry_run:
        return dummy_response
    message = comment_caption()
    url = (
        f"https://graph.facebook.com/{post_id}/comments?"
        f"message={message}&access_token={config.token}"
    )

    files = {
        'image': open(image, "rb")
    }
    response = requests.post(url, files=files)
    return response.json()


def make_album_post(post_id, album_id):
    if config.dry_run:
        return dummy_response
    caption = album_post_caption(post_id)
    url = (
        f"https://graph.facebook.com/{album_id}/photos?"
        f"caption={caption}&access_token={config.token}"
    )
    files = {
        'image': open(image, "rb")
    }
    response = requests.post(url, files=files)
    return response.json()
