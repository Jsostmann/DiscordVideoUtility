import ffmpeg
import os
import time
from multiprocessing.pool import ThreadPool
import threading
import discord_util

MAX_THREADS = os.cpu_count() - 1
FFMPEG_PATH = os.path.join(os.getcwd(), "ffmpeg", "bin")

os.environ['PATH'] += os.pathsep + FFMPEG_PATH
GAMES_LIST = ["Fortnite"]

def compress_video(video_file):
    
    print("({}) Compressing file {}...".format(get_current_thread(), video_file))
    
    # target_size in bits
    target_size = 8 * 1000 * 1000 * 8
    output_video_file = os.path.join(OUTPUT_DIRECTORY, *video_file.split(os.sep)[-2::])
    
    probe = ffmpeg.probe(video_file)
    
    # Video duration rounded up in s.
    duration = int(float(probe['format']['duration'])) + 1
    total_bit_rate = target_size / duration

    # Audio bitrate, in bps.
    audio_bitrate = 128 * 1000
    video_bitrate = total_bit_rate - audio_bitrate

    i = ffmpeg.input(video_file)

    start_time = int(time.time())
    ffmpeg.output(i, output_video_file, **{'c:v': 'libx264', 'b:v': video_bitrate, 'c:a': 'aac', 'b:a': audio_bitrate}).overwrite_output().run(quiet=True)
    elapsed_time = int(time.time()) - start_time

    if DELETE_FLAG:
        os.remove(video_file)

    print("Uploading Video {} to Discord...".format(output_video_file))

    discord_util.send_webhook(WEBHOOK_URL, output_video_file, get_file_size(output_video_file), duration, elapsed_time)
    
def get_video_files():
    video_files = []
    for root, _, files in os.walk(INPUT_DIRECTORY):
        for file in files:
            if len(video_files) > 3:
                return video_files

            if root.split(os.sep)[-1].strip() not in GAMES_LIST:
                continue     

            if file.endswith(".mp4"):
                video_file = os.path.join(root, file)
                video_files.append(video_file)

    return video_files

def get_file_size(filepath):
    '''
        Returns filesize in Mb
    '''
    size_in_bytes = os.stat(filepath).st_size
    return size_in_bytes // 1048576

def get_current_thread():
    return threading.current_thread().name.replace(" (worker)","")

def get_clip_duration(filepath):
    '''
        Returns duration of video in seconds
    '''
    probe = ffmpeg.probe(filepath)
    return int(float(probe['format']['duration'])) + 1

def check_directories_exist():
    '''
        Checks if input / output directories are present and creates if needeed.
    '''
    if not os.path.exists(INPUT_DIRECTORY):
        print("Couldn't find input directory {} exiting...".format(INPUT_DIRECTORY))
        exit(1)

    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
        print("Created output directory {}".format(OUTPUT_DIRECTORY))

    for game in GAMES_LIST:
        game_dir = os.path.join(OUTPUT_DIRECTORY, game)
        if not os.path.exists(game_dir):
            os.makedirs(game_dir)
            print("Created output game directory for {}".format(game))

def start(env_vars):
    global WEBHOOK_URL, INTERVAL, INPUT_DIRECTORY, OUTPUT_DIRECTORY, DELETE_FLAG

    WEBHOOK_URL = env_vars["WEBHOOK_URL"]
    INTERVAL = ["INTERVAL"]
    INPUT_DIRECTORY = env_vars["INPUT_DIRECTORY"]
    OUTPUT_DIRECTORY = env_vars["OUTPUT_DIRECTORY"]
    DELETE_FLAG = env_vars["DELETE_FLAG"]

    check_directories_exist()

    pool = ThreadPool(processes=MAX_THREADS)
    print("Creating thread pool with size= {}".format(MAX_THREADS))

    video_files = get_video_files()
    pool.map(compress_video, video_files)
    