import time


def log_error(message):
    with open("yafot_error.log", "a+") as file:
        newline = "\n"
        file.write(f"{time.ctime()}{newline}{message}\n\n")
        file.close()


def log_posts(curren_frame, post_id, comment_id, palbum_id, calbum_id):
    with open("yafot_posts.log", "a+") as file:
        if not comment_id:
            comment_id = "null"
        if not palbum_id:
            palbum_id = "null"
        if not calbum_id:
            calbum_id = "null"
        file.write(f"{curren_frame},{post_id},{comment_id},{palbum_id},{calbum_id}\n")
        file.close()
