import requests
import os
import time
from src import config

current_frame_number = ""
total_frames = ""
pimage = ""
cimage = ""
timestamp = ""
padding = ""
dummy_response = {"id": "123456789", "post_id": "987654321_123456789"}


def initialize(_current_frame_number, _total_frames, _pimage, _cimage):
    global current_frame_number
    current_frame_number = _current_frame_number
    global total_frames
    total_frames = _total_frames
    global pimage
    pimage = _pimage
    global cimage
    cimage = _cimage
    global padding
    padding = len(str(_total_frames))
    base_filename = os.path.basename(_pimage)
    filename_without_ext = os.path.splitext(base_filename)[0]
    frame_pts = int(filename_without_ext.split("_")[1].lstrip("0"))
    global timestamp
    timestamp = time.strftime(f"%Mm:%Ss.{(frame_pts % 1000):03}ms", time.gmtime(frame_pts / 1000.0))


def post_caption():
    newline = "\n"
    msg = (
        # f"Some anime\n"
        # f"Episode 01 of 12\n"
        f"Frame {current_frame_number:0{padding}} of {total_frames}\n"
        f"Timestamp: {timestamp}"
        # f"\nTag: ABCXX_E1F{current_frame_number}"
    )
    if config.verbose:
        print(f"defined post caption:{newline}{msg}")

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
    newline = "\n"
    msg = (
        # f"Episode number - "
        f"{current_frame_number:0{padding}}/{total_frames:0{padding}} - {timestamp}\n"
        f"Original post: https://www.facebook.com/{post_id}"
    )
    if config.verbose:
        print(f"defined album_post caption:{newline}{msg}")

    return msg


def make_post():
    caption = post_caption()
    url = (
        f"https://graph.facebook.com/{config.page_id}/photos?"
        f"caption={caption}&access_token={config.token}"
    )
    files = {
        'image': open(pimage, "rb")
    }
    if config.dry_run:
        return dummy_response
    response = requests.post(url, files=files)
    return response.json()


def make_comment(post_id):
    message = comment_caption()
    url = (
        f"https://graph.facebook.com/{post_id}/comments?"
        f"message={message}&access_token={config.token}"
    )

    files = {
        'image': open(cimage, "rb")
    }
    if config.dry_run:
        return dummy_response
    response = requests.post(url, files=files)
    return response.json()


def make_album_post(post_id, album_id, caller):
    caption = album_post_caption(post_id)
    url = (
        f"https://graph.facebook.com/{album_id}/photos?"
        f"caption={caption}&access_token={config.token}"
    )
    if caller == "p":
        image = pimage
    else:
        image = cimage
    files = {
        'image': open(image, "rb")
    }
    if config.dry_run:
        return dummy_response
    response = requests.post(url, files=files)
    return response.json()
