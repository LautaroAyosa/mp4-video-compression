import os
import subprocess
import sys
import re
import time
import shutil

from tqdm import tqdm  # Progress bar

# Folder paths
input_folder = "./videos"
output_folder = "./compressed_videos"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# FFmpeg settings
crf = 28  # Lower = better quality, larger file (recommended: 17-28)
preset = "slow"  # Options: ultrafast, fast, medium, slow (better compression = slower)

# Get list of all MP4 files
mp4_files = [f for f in os.listdir(input_folder) if f.endswith(".mp4")]
total_files = len(mp4_files)
total_start_time = time.time()

if total_files == 0:
    print("No MP4 files found in the input folder.")
    sys.exit(1)

print(f"Found {total_files} MP4 files. Starting compression...\n")

# Function to extract duration from video metadata
def get_video_duration(filepath):
    cmd = ["ffprobe", "-i", filepath, "-show_entries", "format=duration", "-v", "quiet", "-of", "csv=p=0"]
    try:
        duration = float(subprocess.check_output(cmd).decode().strip())
        return duration
    except:
        return None

# Process each MP4 file
for index, filename in enumerate(mp4_files, start=1):
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, f"compressed_{filename}")

    # Get video duration
    video_duration = get_video_duration(input_path)
    if video_duration is None:
        print(f"Skipping {filename} (unable to read duration)")
        continue

    print(f"\n[{index}/{total_files}] Compressing: {filename} (Duration: {video_duration:.2f} sec)")

    # Start compression and capture output
    command = [
        "ffmpeg", "-i", input_path,
        "-c:v", "libx265", "-crf", str(crf), "-preset", preset,
        "-c:a", "aac", "-b:a", "128k",
        "-y", output_path
    ]
    
    # Run FFmpeg and capture stderr for progress
    process = subprocess.Popen(command, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1)

    # Progress bar setup
    with tqdm(total=video_duration, unit="s", unit_scale=True, dynamic_ncols=True) as pbar:
        start_time = time.time()

        for line in process.stderr:
            match = re.search(r"time=(\d+:\d+:\d+\.\d+)", line)
            if match:
                # Convert HH:MM:SS to seconds
                h, m, s = map(float, match.group(1).split(":"))
                current_time = h * 3600 + m * 60 + s
                pbar.update(current_time - pbar.n)  # Update progress bar

                elapsed_time = time.time() - start_time
                estimated_total = (elapsed_time / (current_time + 1e-6)) * video_duration
                estimated_remaining = max(0, estimated_total - elapsed_time)
                pbar.set_postfix(elapsed=f"{elapsed_time:.1f}s", remaining=f"{estimated_remaining:.1f}s")

        process.wait()  # Wait for FFmpeg to finish

    # Calculate size reduction
    original_size = os.path.getsize(input_path) / (1024 * 1024)
    compressed_size = os.path.getsize(output_path) / (1024 * 1024)
    reduction = (1 - (compressed_size / original_size)) * 100

    print(f"✅ Done: {filename} | Size Reduced: {original_size:.2f}MB → {compressed_size:.2f}MB ({reduction:.1f}% smaller)")

total_time = time.time() - total_start_time
print(f"\n🎉 Compression Completed! Total Time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
