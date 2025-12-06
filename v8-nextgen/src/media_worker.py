#!/usr/bin/env python3
"""
media_worker.py - Set-and-forget batch processor for photos & videos

Designed for the V6 mall reconstruction repo:

v6-nextgen/
  assets/
    photos/                  # source images
    video/                   # source video (e.g. ERA_2020/segments/)
    processed/               # this script will create/populate

What it does:
- Recursively scans assets/photos and assets/video
- For each image:
    - creates a normalized JPEG (max side 2048px)
    - creates a thumbnail JPEG (max side 512px)
- For each video:
    - copies to processed/videos (if moviepy is available)
    - extracts frames every N seconds into processed/frames
- Skips files that are already up-to-date
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Tuple

import hashlib
from PIL import Image

try:
    from moviepy.editor import VideoFileClip  # optional, for video frame extraction
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

# ----------------- PATH CONFIG --------------------

# This file lives in v6-nextgen/src/media_worker.py
REPO_ROOT = Path(__file__).resolve().parents[1]          # v6-nextgen/
ASSETS_ROOT = REPO_ROOT / "assets"

PHOTOS_SRC = ASSETS_ROOT / "photos"                      # source photos
VIDEO_SRC = ASSETS_ROOT / "video"                        # source videos (recurses)

PROCESSED_ROOT = ASSETS_ROOT / "processed"
PHOTOS_OUT = PROCESSED_ROOT / "photos"
THUMBS_OUT = PROCESSED_ROOT / "thumbnails"
VIDEOS_OUT = PROCESSED_ROOT / "videos"
FRAMES_OUT = PROCESSED_ROOT / "frames"
LOGS_OUT = PROCESSED_ROOT / "logs"

# Image processing config
MAX_IMAGE_SIZE = 2048          # longest side for normalized images
THUMB_SIZE = 512               # longest side for thumbnails

# Video processing config
FRAME_EVERY_N_SECONDS = 2      # extract one frame every N seconds

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

# --------------------------------------------------


def ensure_dirs() -> None:
    for d in [PHOTOS_OUT, THUMBS_OUT, VIDEOS_OUT, FRAMES_OUT, LOGS_OUT]:
        d.mkdir(parents=True, exist_ok=True)


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTS


def is_video(path: Path) -> bool:
    return path.suffix.lower() in VIDEO_EXTS


def discover_media_files(root: Path) -> Tuple[List[Path], List[Path]]:
    images: List[Path] = []
    videos: List[Path] = []
    if not root.exists():
        return images, videos

    for dirpath, _, filenames in os.walk(root):
        dp = Path(dirpath)
        for name in filenames:
            p = dp / name
            if is_image(p):
                images.append(p)
            elif is_video(p):
                videos.append(p)
    return images, videos


def normalized_rel(base_root: Path, src: Path) -> Path:
    """
    Return src path relative to a base root, but if src is not under base_root,
    just use the filename.
    """
    try:
        rel = src.relative_to(base_root)
    except ValueError:
        rel = Path(src.name)
    return rel


def process_image(src: Path) -> None:
    rel = normalized_rel(PHOTOS_SRC, src)
    out_img = PHOTOS_OUT / rel
    out_thumb = THUMBS_OUT / rel

    out_img.parent.mkdir(parents=True, exist_ok=True)
    out_thumb.parent.mkdir(parents=True, exist_ok=True)

    # Skip if already exists and newer or equal mtime
    if out_img.exists() and out_thumb.exists():
        if out_img.stat().st_mtime >= src.stat().st_mtime:
            print(f"[IMG] SKIP (up-to-date): {src}")
            return

    try:
        with Image.open(src) as im:
            im = im.convert("RGB")

            # Normalized main image
            normalized = im.copy()
            normalized.thumbnail((MAX_IMAGE_SIZE, MAX_IMAGE_SIZE), Image.LANCZOS)
            normalized.save(out_img, format="JPEG", quality=90)
            print(f"[IMG] NORMALIZED: {src} -> {out_img}")

            # Thumbnail
            thumb = im.copy()
            thumb.thumbnail((THUMB_SIZE, THUMB_SIZE), Image.LANCZOS)
            thumb.save(out_thumb, format="JPEG", quality=85)
            print(f"[IMG] THUMB: {src} -> {out_thumb}")

    except Exception as e:
        print(f"[IMG] ERROR processing {src}: {e}")


def process_video(src: Path) -> None:
    rel = normalized_rel(VIDEO_SRC, src)
    out_copy = VIDEOS_OUT / rel
    frames_dir = FRAMES_OUT / rel.with_suffix("")  # folder for frames

    out_copy.parent.mkdir(parents=True, exist_ok=True)
    frames_dir.mkdir(parents=True, exist_ok=True)

    # Simple copy if needed
    need_copy = True
    if out_copy.exists():
        if out_copy.stat().st_mtime >= src.stat().st_mtime:
            need_copy = False

    if need_copy:
        with open(src, "rb") as f_in, open(out_copy, "wb") as f_out:
            while True:
                chunk = f_in.read(8192)
                if not chunk:
                    break
                f_out.write(chunk)
        print(f"[VID] COPIED: {src} -> {out_copy}")
    else:
        print(f"[VID] SKIP COPY (up-to-date): {src}")

    if not MOVIEPY_AVAILABLE:
        print(f"[VID] SKIP FRAMES (moviepy not installed): {src}")
        return

    # Frame extraction
    try:
        clip = VideoFileClip(str(src))
        duration = clip.duration or 0
        if duration <= 0:
            print(f"[VID] WARN: {src} has zero duration?")
            clip.close()
            return

        t = 0.0
        while t < duration:
            frame_name = f"frame_{t:06.2f}.jpg"
            frame_path = frames_dir / frame_name
            if frame_path.exists():
                t += FRAME_EVERY_N_SECONDS
                continue

            frame = clip.get_frame(t)
            img = Image.fromarray(frame)
            img.save(frame_path, format="JPEG", quality=85)
            print(f"[VID] FRAME {t:.2f}s -> {frame_path}")
            t += FRAME_EVERY_N_SECONDS

        clip.close()

    except Exception as e:
        print(f"[VID] ERROR processing {src}: {e}")


def main() -> None:
    print("=== MEDIA WORKER START ===")
    print(f"Repo root:       {REPO_ROOT}")
    print(f"Assets root:     {ASSETS_ROOT}")
    print(f"Photos source:   {PHOTOS_SRC}")
    print(f"Video source:    {VIDEO_SRC}")
    print(f"Processed out:   {PROCESSED_ROOT}")

    ensure_dirs()

    # Discover media
    img_files, _ = discover_media_files(PHOTOS_SRC)
    vid_files, _ = discover_media_files(VIDEO_SRC)

    print(f"Discovered {len(img_files)} images under {PHOTOS_SRC}")
    print(f"Discovered {len(vid_files)} videos under {VIDEO_SRC}")

    start = time.time()

    # Process images
    for i, img in enumerate(img_files, 1):
        print(f"\n[{i}/{len(img_files)}] Processing IMAGE: {img}")
        process_image(img)

    # Process videos
    for i, vid in enumerate(vid_files, 1):
        print(f"\n[{i}/{len(vid_files)}] Processing VIDEO: {vid}")
        process_video(vid)

    elapsed = time.time() - start
    print(f"\n=== MEDIA WORKER COMPLETE in {elapsed:.1f}s ===")


if __name__ == "__main__":
    main()
