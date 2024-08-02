import subprocess
import time
import os

from find_link import find_stream_link

# Direct stream URL extracted from network requests
stream_url = "https://s27.ipcamlive.com/streams/1bg2ojrcyftlbnxes/stream.m3u8"
#'https://s27.ipcamlive.com/streams/1br6itsh2bauufzyb/stream.m3u8' 

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
