#!/usr/bin/env python3
"""
Quick Video Audit - Extract Preview Frames
Extracts first/middle/last frame from each video segment for coverage assessment
"""

import subprocess
import os
import json
from pathlib import Path

# Paths
VIDEO_DIR = Path(r"C:\Users\stusa\Documents\GitHub\glitchLFS1121origin\v6-nextgen\assets\video\ERA_2020\segments")
OUTPUT_DIR = Path(r"C:\Users\stusa\Documents\GitHub\glitchLFS1121origin\v6-nextgen\assets\processed\video_audit")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_video_duration(video_path):
    """Get video duration in seconds using ffprobe"""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(video_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def extract_frame_at_time(video_path, timestamp, output_path):
    """Extract a single frame at specific timestamp"""
    cmd = [
        'ffmpeg',
        '-ss', str(timestamp),
        '-i', str(video_path),
        '-vframes', '1',
        '-q:v', '2',
        '-y',
        str(output_path)
    ]
    subprocess.run(cmd, capture_output=True, check=True)

def process_segment(video_path):
    """Extract first, middle, last frames from a video segment"""
    segment_name = video_path.stem
    duration = get_video_duration(video_path)
    
    # Calculate timestamps
    first = 0.1  # Slightly after start to avoid black frames
    middle = duration / 2
    last = max(duration - 0.5, 0.1)  # Slightly before end
    
    frames = []
    
    for position, timestamp in [('first', first), ('middle', middle), ('last', last)]:
        output_filename = f"{segment_name}_{position}.jpg"
        output_path = OUTPUT_DIR / output_filename
        
        try:
            extract_frame_at_time(video_path, timestamp, output_path)
            frames.append({
                'position': position,
                'timestamp': round(timestamp, 2),
                'filename': output_filename,
                'path': str(output_path)
            })
            print(f"  [OK] Extracted {position} frame @ {timestamp:.2f}s")
        except Exception as e:
            print(f"  [FAIL] Failed to extract {position} frame: {e}")
    
    return {
        'segment': segment_name,
        'duration': round(duration, 2),
        'frames': frames
    }

def main():
    """Process all video segments"""
    print("=" * 60)
    print("QUICK VIDEO AUDIT - PREVIEW FRAME EXTRACTION")
    print("=" * 60)
    print()
    
    # Find all MP4 files
    video_files = sorted(VIDEO_DIR.glob("*.mp4"))
    
    if not video_files:
        print(f"No video files found in {VIDEO_DIR}")
        return
    
    print(f"Found {len(video_files)} video segments")
    print(f"Output directory: {OUTPUT_DIR}")
    print()
    
    # Process each segment
    manifest = {
        'total_segments': len(video_files),
        'total_frames_extracted': 0,
        'segments': []
    }
    
    for video_path in video_files:
        print(f"Processing: {video_path.name}")
        segment_data = process_segment(video_path)
        manifest['segments'].append(segment_data)
        manifest['total_frames_extracted'] += len(segment_data['frames'])
        print()
    
    # Save manifest
    manifest_path = OUTPUT_DIR / 'video_audit_manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print("=" * 60)
    print(f"EXTRACTION COMPLETE")
    print(f"Total frames extracted: {manifest['total_frames_extracted']}")
    print(f"Manifest saved: {manifest_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
