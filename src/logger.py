import time


def log_error(message):
    with open("yafot_error.log", "a+") as file:
        newline = "\n"
        # First write the current local time, then write the error message
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
        # Post-id's will be logged in a file in csv format, without heading
        # current_frame,main_post_id,comment_id,photo_album_id,comment_album_id
        # If a value doesn't exist, "null" would be written in its place
        file.write(f"{curren_frame},{post_id},{comment_id},{palbum_id},{calbum_id}\n")
        file.close()
