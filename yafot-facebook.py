import os
import sys
import time
from src import commandline
from src import config
from src import bot
from src import logger


def main():
    try:
        # Parse arguments from commandline
        commandline.process_arguments()

        # Store all the frames from the directory in a list in alphabetically sorted order
        # It is because the frame-number i isn't taken from the filename, rather it's the i-th file in the directory
        # Caution: Do not keep any other file or sub-directory in the directory except the frames
        pframes = sorted(os.listdir(config.pdir))
        cframes = []
        if config.cdir:
            cframes = sorted(os.listdir(config.cdir))

        total_frames = len(pframes)
        start = config.start
        end = config.start + config.count  # Loop is run in [start, end) range, so +1 isn't necessary

        # Loop body. Each iteration does four tasks related to a single frame
        # Namely, post, comment, add post-photo in album, add comment-photo in album
        for curren_frame in range(start, end):

            # Only base filenames without the directory parts are stored in the list
            # Base-filenames must be joined back with their directory part
            pimage_basename = pframes[curren_frame - 1]  # Get the i-th file from the list
            pimage = f"{config.pdir}/{pimage_basename}"  # filename = directory/ + basename
            if config.cdir:
                cimage_basename = cframes[curren_frame - 1]
                cimage = f"{config.cdir}/{cimage_basename}"
            else:
                cimage = ""

            # Initialize the bot with variables for this loop
            bot.initialize(curren_frame, total_frames, pimage, cimage)

            comment_id = ""
            palbum_id = ""
            calbum_id = ""

            # Ask the bot to make the post
            post_response = bot.make_post()
            error_counter = 0

            while "error" in post_response.keys():
                if error_counter >= 10:
                    print("error still unresolved after 10 tries, bot exiting")
                    logger.log_error("unresolved error while requesting at /page-id/photos")
                    sys.exit(1)
                error_counter += 1
                print(post_response)
                logger.log_error(post_response)
                print("trying again after 10 seconds")
                time.sleep(10)
                post_response = bot.make_post()

            post_id = post_response["post_id"]  # Get the post-id from json response

            if config.cdir:
                comment_response = bot.make_comment(post_id)
                error_counter = 0
                while "error" in comment_response.keys():
                    if error_counter >= 10:
                        print("error still unresolved after 10 tries, bot exiting")
                        logger.log_error("unresolved error while requesting at /post-id/comments")
                        sys.exit(1)
                    error_counter += 1
                    print(comment_response)
                    logger.log_error(comment_response)
                    print("trying again after 10 seconds")
                    time.sleep(10)
                    comment_response = bot.make_comment(post_id)

                comment_id = comment_response["id"]  # Get the comment-id from json response

            if config.palbum_id:
                palbum_response = bot.make_album_post(post_id, config.palbum_id, "p")
                error_counter = 0
                while "error" in palbum_response.keys():
                    if error_counter >= 10:
                        print("error still unresolved after 10 tries, bot exiting")
                        logger.log_error("unresolved error while posting at /palbum-id/photos")
                        sys.exit(1)
                    error_counter += 1
                    print(palbum_response)
                    logger.log_error(palbum_response)
                    print("trying again after 10 seconds")
                    time.sleep(10)
                    palbum_response = bot.make_album_post(post_id, config.palbum_id, "p")

                palbum_id = palbum_response["post_id"]  # Get the photo-album-post-id from json response

            if config.calbum_id:
                calbum_response = bot.make_album_post(comment_id, config.calbum_id, "c")
                error_counter = 0
                while "error" in calbum_response.keys():
                    if error_counter >= 10:
                        print("error still unresolved after 10 tries, bot exiting")
                        logger.log_error("unresolved error while posting at /calbum-id/photos")
                        sys.exit(1)
                    error_counter += 1
                    print(calbum_response)
                    logger.log_error(calbum_response)
                    print("trying again after 10 seconds")
                    time.sleep(10)
                    calbum_response = bot.make_album_post(comment_id, config.calbum_id, "c")

                calbum_id = calbum_response["post_id"]  # Get the comment-album-post-id from json response

            # Log the id's of the posts
            logger.log_posts(curren_frame, post_id, comment_id, palbum_id, calbum_id)

            # Wait for some time before going into the next loop
            if config.verbose:
                print(f"Sleeping for {config.delay} seconds")
            time.sleep(config.delay)

    except Exception as e:
        print(e)
        logger.log_error(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
