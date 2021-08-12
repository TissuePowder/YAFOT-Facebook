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
# Dummy response to return in dry-run mode
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
    # Zero pad the frame-number upto the number of total frames
    padding = len(str(_total_frames))

    # Filename is expected in "FrameNumber_FramePTSinMilliseconds.ext" format to include timestamps
    # Follow the ffmpeg frame-extraction tutorial if you don't know how to include frame_pts in filename
    base_filename = os.path.basename(_pimage)  # Get base filename without directory parts
    filename_without_ext = os.path.splitext(base_filename)[0]  # Get filename without extension
    frame_pts_split = filename_without_ext.split("_")

    # If framepts is included in filename
    if len(frame_pts_split) > 1:
        frame_pts = int(frame_pts_split[1].lstrip("0"))  # Get the frame_pts part from filename

        global timestamp
        # Convert the milliseconds into sexagesimal format (hh:mm:ss.ms)
        timestamp = time.strftime(f"%Hh:%Mm:%Ss.{(frame_pts % 1000):03}ms", time.gmtime(frame_pts / 1000.0))
        # Most episodes are below 1 hour, so keeping 00h in timestamp is uselsess
        # 00h: is ripped from timestamp as default
        if timestamp[:2] == '00':
            timestamp = timestamp[4:]


def post_caption():
    newline = "\n"
    timestamp_msg = ""
    if timestamp:
        timestamp_msg = f"\nTimestamp: {timestamp}"
    # Add your desired post-caption here
    # It is recommended to execute the script in dry-run mode first to check the post captions and text formats
    msg = (
        # f"Some anime\n"
        # f"Episode 01 of 12\n"
        f"Frame {current_frame_number:0{padding}} of {total_frames}"
        # Comment out the following line if you aren't using timestamp
        f"{timestamp_msg}"
        # f"\nTag: ABCXX_E1F{current_frame_number}"
    )
    if config.verbose:
        print(f"Defined post caption:{newline}{msg}")

    return msg


def comment_caption():
    newline = "\n"
    msg = (
        f"Raw frame without subtitles"
    )
    if config.verbose:
        print(f"Defined comment caption:{newline}{msg}")

    return msg


def album_post_caption(post_id):
    newline = "\n"
    timestamp_msg = ""
    if timestamp:
        timestamp_msg = f" - {timestamp}"
    msg = (
        # f"Episode number - "
        f"{current_frame_number:0{padding}}/{total_frames}"
        # Comment out the following line if you aren't using timestamp
        f"{timestamp_msg}\n"
        f"Original post: https://www.facebook.com/{post_id}"
    )
    if config.verbose:
        print(f"Defined album_post caption:{newline}{msg}")

    return msg


def make_post():
    caption = post_caption()
    # URL format and fields are according to facebook's API documentation
    # Since no API version is explicitly given in the link, requests will always use the latest API version
    url = (
        f"https://graph.facebook.com/{config.page_id}/photos?"
        f"caption={caption}&access_token={config.token}"
    )
    files = {
        'image': open(pimage, "rb")
    }
    if config.dry_run:
        return dummy_response
    # Send http POST request to /page-id/photos to make the post
    response = requests.post(url, files=files)
    return response.json()


def make_comment(post_id):
    message = comment_caption()
    # URL format and fields are according to facebook's API documentation
    # Since no API version is explicitly given in the link, requests will always use the latest API version
    url = (
        f"https://graph.facebook.com/{post_id}/comments?"
        f"message={message}&access_token={config.token}"
    )

    files = {
        'image': open(cimage, "rb")
    }
    if config.dry_run:
        return dummy_response
    # Send http POST request to /post-id/comments to make a comment under the previously made post
    response = requests.post(url, files=files)
    return response.json()


def make_album_post(post_id, album_id, caller):
    caption = album_post_caption(post_id)
    # URL format and fields are according to facebook's API documentation
    # Since no API version is explicitly given in the link, requests will always use the latest API version
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
    # Send http POST request to /album-id/photos to add the frame in the album
    response = requests.post(url, files=files)
    return response.json()
