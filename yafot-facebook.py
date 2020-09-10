import os
import sys
import time
from src import commandline
from src import config
from src import bot
from src import logger


def main():
    try:
        commandline.process_arguments()
        pframes = sorted(os.listdir(config.pdir))
        cframes = []
        if config.cdir:
            cframes = sorted(os.listdir(config.cdir))
        total_frames = len(pframes)
        start = config.start
        end = config.start + config.count
        for curren_frame in range(start, end):
            pimage_basename = pframes[curren_frame - 1]
            pimage = f"{config.pdir}/{pimage_basename}"
            if config.cdir:
                cimage_basename = cframes[curren_frame - 1]
                cimage = f"{config.cdir}/{cimage_basename}"
            else:
                cimage = ""

            bot.initialize(curren_frame, total_frames, pimage, cimage)

            comment_id = ""
            palbum_id = ""
            calbum_id = ""

            post_response = bot.make_post()
            while "error" in post_response.keys():
                print(post_response)
                logger.log_error(post_response)
                print("trying again after 10 seconds")
                time.sleep(10)
                post_response = bot.make_post()

            post_id = post_response["post_id"]

            if config.cdir:
                comment_response = bot.make_comment(post_id)
                while "error" in comment_response.keys():
                    print(comment_response)
                    logger.log_error(comment_response)
                    print("trying again after 10 seconds")
                    time.sleep(10)
                    comment_response = bot.make_comment(post_id)

                comment_id = comment_response["id"]

            if config.palbum_id:
                palbum_response = bot.make_album_post(post_id, config.palbum_id, "p")
                while "error" in palbum_response.keys():
                    print(palbum_response)
                    logger.log_error(palbum_response)
                    print("trying again after 10 seconds")
                    time.sleep(10)
                    palbum_response = bot.make_album_post(post_id, config.palbum_id, "p")

                palbum_id = palbum_response["post_id"]

            if config.calbum_id:
                calbum_response = bot.make_album_post(comment_id, config.calbum_id, "c")
                while "error" in calbum_response.keys():
                    print(calbum_response)
                    logger.log_error(calbum_response)
                    print("trying again after 10 seconds")
                    time.sleep(10)
                    calbum_response = bot.make_album_post(comment_id, config.calbum_id, "c")

                calbum_id = calbum_response["post_id"]

            logger.log_posts(curren_frame, post_id, comment_id, palbum_id, calbum_id)
            time.sleep(config.delay)

    except Exception as e:
        print(e)
        print(sys.exc_info())


if __name__ == '__main__':
    main()
