def compress_video(video_file):
    print("Compressing file {}...".format(video_file))
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000
    target_size = 8 * 1000
    t_2 = 8 * 1000 * 1000 * 8
    output_video_file = os.path.join(VIDEO_OUTPUT_DIRECTORY, video_file.split(os.sep)[-1])
    
    probe = ffmpeg.probe(video_file)
    
    # Video duration, in s.
    duration = int(float(probe['format']['duration'])) + 1
    total_bit_rate = t_2/ duration
    # Audio bitrate, in bps.
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_file)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, output_video_file,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run()