import subprocess
import time
import os

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

# Generate the ffmpeg command
ffmpeg_command = [
    'ffmpeg',
    '-i', stream_url,
    '-c', 'copy',  # Copy the codec (no re-encoding)
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
