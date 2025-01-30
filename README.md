# MP4 Video Compressor

This script compresses **MP4 video files** using **FFmpeg** without significant quality loss. It reduces file size by using the H.265 (HEVC) codec while displaying **real-time progress**, **estimated completion time**, and **file size reduction stats**. The processing time varies based on your computer's hardware capabilities; more powerful systems will complete compression faster than slower ones. For example, on a system with an **8th Gen Intel i7 CPU** and **16GB RAM**, using a `fast` preset with `crf=28`, a **3.5GB MP4 file** took approximately **1 hour 25 minutes** to compress, reducing its size down to **201mb**.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
  - [Install FFmpeg](#install-ffmpeg)
  - [Install Python Dependencies](#install-python-dependencies)
- [Usage](#usage)
- [Customization](#customization)
- [Example Output](#example-output)
- [License](#license)

## Features

✅ **Lossless-like compression** using H.265 (HEVC).\
✅ **Real-time progress bar** with estimated remaining time.\
✅ **Batch processing** for all MP4 files in a folder.\
✅ **Error handling** (skips unreadable files).

## Requirements:

Ensure the following software is installed on your machine:

1. **Python** – Download from [python.org](https://www.python.org/downloads/). Python 3.x is recommended.
2. **FFmpeg** – Required for video processing (see installation steps below).
3. **Python dependencies** – Install using `pip install tqdm`.

### Install FFmpeg

- **Windows**: Download from [FFmpeg official site](https://ffmpeg.org/download.html)
- **Mac (Homebrew)**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg` (Debian/Ubuntu) or `sudo dnf install ffmpeg` (Fedora)

### Install Python Dependencies

```
pip install tqdm
```

## Usage

### 1. Place MP4 files in the `videos/` folder

Create a folder named `videos` and put all MP4 files inside.

### 2. Run the script

```
python compress.py
```

### 3. Compressed files will be saved in `compressed_videos/`

The script will process all `.mp4` files and save optimized versions.

## Customization

You can modify these settings inside `compress_videos.py`:

- **Set input folder**
  - The code initially has the input folder set to ./videos. Modify this at will to point to the folder that contains your videos
  (You should also be able to use an absolute path like `"C:\Users\<YourUserName>\Videos\"`)
- **Change quality:**
  - Lower CRF = **better quality, larger file** (Recommended: `17-28`)
  - Change `crf = 28` → `crf = 23` for better quality
- **Faster compression:**
  - Change `preset = "slow"` → `preset = "fast"`
- **Reduce file size more:**
  - Increase `crf = 30` (more compression)

## Example Output

```
Found 3 MP4 files. Starting compression...

[1/3] Compressing: video1.mp4 (Duration: 120.5 sec)
  80% |███████████████████▏   |  96.5/120.5s [elapsed: 30s, remaining: 7.5s]

```

## License

This project is **MIT Licensed**. Feel free to use and modify it!
