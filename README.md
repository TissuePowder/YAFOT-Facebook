# YAFOT - Facebook
Yet Another Frame-bOT for facebook. As the name suggests, this is a command-line tool to spam video-frames or images in social media. This is the facebook version. Written in python3, uses facebok API to create posts.

Bot is mainly created to post in _Every Frame in Order_ pages, but can be used for similar other posting and spamming. If you don't know about this type of facebook pages, check the links below for example.

- [Every Houseki no Kuni Frame in Order](https://www.facebook.com/hnkframes)
- [Every Ping Pong the Animation Frame in Order](https://www.facebook.com/pingpongframes)


## Requirements
python 3.5 or up. You may need to install some modules separately such as requests.
```
$ pip install requests
```
Or if your pip command invokes pip 2, then try with
```
$ pip3 install requests
```


## How to install
As of now, there is no auto pip install procedure, because I am lazy AF and the script isn't really ready for packaging. Download the release version and run the yafot-facebook.py file.
Or you can clone the repository and run as well.
```
$ git clone https://github.com/TissuePowder/YAFOT-Facebook.git
$ cd Yafot-facebook
$ python yafot-facebook.py
```


## Usage
```
$ python yafot-facebook.py -h

usage: yafot-facebook.py [-h] --page-id PAGE_ID --pdir PDIR [--cdir CDIR] [--palbum-id PALBUM_ID]
[--calbum-id CALBUM_ID] --token TOKEN --start START [--count COUNT]
[--delay DELAY] [--use-timestamp] [-v] [-n]

optional arguments:
-h, --help            show this help message and exit
--page-id PAGE_ID     your facebook page-id
--pdir PDIR           directory of frames for main posts
--cdir CDIR           directory of frames to post as comments under main posts
--palbum-id PALBUM_ID
    album-id to post frames from --pdir
--calbum-id CALBUM_ID
    album-id to post frames from --cdir
--token TOKEN         your facebook page access-token
--start START         starting number of the frame to post
--count COUNT         how many frames to post starting from --start
--delay DELAY         delay between two frame-posts in seconds
--use-timestamp       parse timestamp from filename
-v, --verbose         turns on verbosity
-n, --dry-run         offline testing, no web request made
```


## A bit more detailed explanation of the arguments
**--page-id** - Your facebook page-id. If you want to post only in album, put your album-id after the argument.

**--pdir** - Short for _photo-directory_. Frames from this directory will be used for the main posts. Bot uses _/object-id/photos/_ edge to make these posts.

**--cdir** - Short for _comments-directory_. Frames from this directory will be posted as comments under main posts. Bot uses _/post-id/comments_ edge to make these posts. post-id is returned from previous API request.

**--palbum-id** - Short for _photo-album-id_. Frames from _photo-directory_ are added in this album.

**--calbum-id** - Short for _comments-album-id_. Frames from _comments-directory_ are added in this album.

**--token** - Your facebook page access-token.

**--start** - Starting number of the frame from which bot would start posting.

**--count** - How many frames to post starting from _--start_

**--delay** - Delay or waiting time between two different phases. A single phase carries out all requests for each post, ie, posting, commenting and adding the images to albums.

**--use-timestamp** - If you extract the frames using ffmpeg's __-frame_pts 1__ option, then use this argument to make the bot parse timestamp from the filenames.

**--verbose** - Turns on verbosity.

**--dry-run** - Testing mode. Bot carries out all the works except making any web request. A dummy response is returned for checking. Dry-run mode turns on verbosity automatically.


## Example
```
$ python yafot-facebook.py --page-id 40927481064389 --pdir "Episode_01_subbed" --cdir "Episode_01_raw" --palbum-id 80453984612530 --token your_token --start 101 --count 50 --delay 180
```
The above command makes main posts with frames from **Episode_01_subbed** directory, posts comments with frames from **Episode_01_raw** directory, adds only main photo-frames in an album, starts from frame-number **101**, posts **50** frames and sleeps for **180** seconds between two posts.

Note that if your "python" command invokes python 2, then use "python3" command instead.

Also, the directories in the above example are relative paths. If you are't keeping the python script elsewhere, then use full path-names for directories instead.


## Note: Bot does not extract frames from video, you need to extract frames yourself first
You can find a ton of tutorials in the internet about how to extract frames from a video. You may use whatever way you like, though it is recommended to use FFmpeg.

If you want to include frames' timestamps in your post, bot is capable of doing that, but you need to include the timestamp in milliseconds in the filename. You can achieve this using FFmpeg.

__Filenames must be in FrameNumber_FramePTSinMilliseconds.jpg format to include timestamps. Such as 0023_00163823.jpg, 0256_004872980.jpg etc.__
```
$ ffmpeg -copyts -i "Episode_01.mkv" -r 1000 -vf "mpdecimate=hi=64*12*15:lo=64*5*15:frac=1",subtitles=sub1.ass -frame_pts true -vsync vfr -q:v 5 "Sub_01/%08d.jpg" -r 1000 -vf "mpdecimate=hi=64*12*15:lo=64*5*15:frac=1" -frame_pts true -vsync vfr -q:v 5 "Raw_01/%08d.jpg"
```
__If you want the bot to parse timestamp, then add a serial to the filename.__
You can use the following command inside your frame's directory if you are using linux.
```
$ a=1; for i in *; do mv $i $(printf "%06d" "$a")_$i; let a=$a+1; done
```

**Explanation of the above command:**

**-copyts**: Asks ffmpeg not to sanitize timestamps. Important to keep the subbed and raw frames in sync.

**-i Episode_01.mkv**: Input video file.

**-r 1000**: Framerate to process input. It's necessary to get the timestamps in milliseconds.

**-vf**: Whatever comes after it is used for video-filtering.

**mpdecimate=hi=64\*12\*15:lo=64\*5\*15:frac=1**: Removes duplicate frames. Mpdecimate's default values are hi=64\*12, lo=64\*5 and frac=0.33. Values are multiplied by 15 in the above command to produce less number of frames.

**subtitles=sub1.ass**: Mention your subtitle file here. You need to extract it from the video first.

**-frame_pts true**: Asks ffmpeg to include frame_pts (timestamp) in filenames.

**-vsync vfr**: Outputs in variable frame-rate. By default, ffmpeg will try to achieve 24 or 30 constant fps in output by inserting duplicate frames. This argument prevents ffmpeg to insert duplicate frames.

**-q:v 5**: Image quality of the frames. 1 being the highest and 31 being the lowest.

**Sub_01/%08d.jpg**: Output subtitled frames in Sub_01 directory with 8-digit-wide 0-padded filenames. Directory has the exist.

**Raw_01/%08d.jpg**: Output raw frames in Raw_01 directory with 8-digit-wide 0-padded filenames. Directory has to exist.

Note that you have to add the serial numbers to the frames yourself. For further duplicates removal or other editing you are on your own.


## Features
Go to release section for details as this project is still under development. Open a PR if you want to contribute.
