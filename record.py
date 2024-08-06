import subprocess
import time
import os
from datetime import datetime, timedelta
from find_link import find_stream_link



# find Direct stream URL extracted from Javascript
try:
    url = "https://laine.surf/"
    iframe_xpath = "//*[@id='laine']/div/div[2]/div/div/div/iframe"
    stream_url = find_stream_link(url, iframe_xpath)
    if stream_url:
        print(stream_url)
    else:
        raise Exception("Stream link not found")
        
except Exception as e:
    print(f"{e}, link was not found")


# Duration of each chunk in seconds (10 minutes)
chunk_duration = 20 * 60

#this is not working currently
tallinn_offset = 6 * 3600  # Seconds offset from UTC (adjust for DST if necessary)


# Generate the ffmpeg command
ffmpeg_command = [
    'ffmpeg',
    '-i', stream_url,
    '-vf', (
        "settb=AVTB, "
        "setpts='trunc(PTS/1K)*1K+st(1,trunc(RTCTIME/1K+{}))-1K*trunc(ld(1)/1K)',"
        "drawtext=text='%{{localtime}}.%{{eif\\:1M*t-1K*trunc(t*1K)\\:d}}':"
        "fontcolor=white:fontsize=48:x=w-tw-10:y=h-th-10"
    ).format(tallinn_offset),
    '-an',  # Disable audio
    '-c:v', 'libx264',  # Re-encode the video with libx264 codec
    '-preset', 'fast',  # Use a fast preset for encoding
    '-crf', '23',  # Constant Rate Factor (quality setting, lower is better, 23 is a good compromise)
    '-b:v', '1M',  # Set bitrate to 1Mbps
    '-f', 'segment',  # Split into segments
    '-segment_time', str(chunk_duration),  # Duration of each segment
    '-reset_timestamps', '1',  # Reset timestamps at the beginning of each segment
    'output/output_chunk_%03d.mp4'  # Output file pattern
]

# Run the ffmpeg command
try:
    subprocess.run(ffmpeg_command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")

print("Streaming and recording finished.")
