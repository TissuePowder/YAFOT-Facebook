import argparse
import os
import sys
from src import config


def process_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--page-id", required=True, help="your facebook page-id")
    parser.add_argument("--pdir", required=True, help="directory of frames for main posts")
    parser.add_argument("--cdir", help="directory of frames to post as comments under main posts")
    parser.add_argument("--palbum-id", help="album-id to post frames from --pdir")
    parser.add_argument("--calbum-id", help="album-id to post frames from --cdir")
    parser.add_argument("--token", required=True, help="your facebook page access-token")
    parser.add_argument("--start", type=int, required=True, help="starting number of the frame to post")
    parser.add_argument("--count", type=int, help="how many frames to post starting from --start")
    parser.add_argument("--delay", type=int, help="delay between two frame-posts in seconds")
    parser.add_argument("-v", "--verbose", action="store_true", help="turns on verbosity")
    parser.add_argument("-n", "--dry-run", action="store_true", help="offline testing, no web request made")
    args = parser.parse_args()

    config.page_id = args.page_id
    config.pdir = args.pdir
    config.cdir = args.cdir
    config.palbum_id = args.palbum_id
    config.calbum_id = args.calbum_id
    config.token = args.token
    config.start = args.start
    config.count = args.count
    config.delay = args.delay
    config.verbose = args.verbose
    config.dry_run = args.dry_run

    if config.dry_run:
        config.verbose = True
        print("DRY RUN MODE")
        print("no web request will be made, a dummy response will be returned for offline app testing\n")

    if not os.path.isdir(config.pdir):
        print("Photo-frames directory is not valid.")
        sys.exit(1)

    if config.cdir:
        if not os.path.isdir(config.cdir):
            print("Comment-frames directory is not valid.")
            sys.exit(1)

    if not config.count:
        config.count = len(os.listdir(config.pdir)) - config.start + 1
        if config.count < 0:
            print(f"invalid start-number. there are less than {config.start} frames in your directory.")
            sys.exit(1)

    if not config.delay:
        config.delay = 120

    if config.verbose:

        print(f"page-id: {config.page_id}")
        print(f"access_token: {config.token}")
        print(f"photo-frames directory: {config.pdir}")

        if config.cdir:
            print(f"comment-frames directory: {config.cdir}")
        else:
            print("warning: comment-frames directory is not provided, nothing will be posted in comments.")

        if config.palbum_id:
            print(f"album-id for photo-frames: {config.palbum_id}")
        else:
            print("warning: album-id for photo-frames is not provided, photo-frames will not be added to album")

        if config.calbum_id:
            if not config.cdir:
                print("ERROR: comment-frames directory not provided, not possible to post in album.")
                sys.exit(1)
            else:
                print(f"album-id for comment-frames: {config.calbum_id}")
        else:
            print("warning: album-id for comment-frames is not provided, comment-frames will not be added to album")

        print(f"starting frame-number: {config.start}")
        print(f"number of frames to post: {config.count}")
        print(f"delay: {config.delay} seconds")


