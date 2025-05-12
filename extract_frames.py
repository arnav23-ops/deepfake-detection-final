import cv2
import os
import argparse
from tqdm import tqdm

def extract_frames(video_path, output_dir, frame_rate=1):
    """
    Extract frames from a video file
    frame_rate: extract 1 frame every N frames
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return
    
    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Extract frames
    frame_count = 0
    saved_count = 0
    
    with tqdm(total=total_frames, desc=f"Processing {os.path.basename(video_path)}") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % frame_rate == 0:
                # Save frame
                frame_path = os.path.join(output_dir, f"frame_{saved_count:06d}.jpg")
                cv2.imwrite(frame_path, frame)
                saved_count += 1
                
            frame_count += 1
            pbar.update(1)
    
    cap.release()
    print(f"Extracted {saved_count} frames from {video_path}")

def process_directory(input_dir, output_dir, frame_rate=1):
    """Process all videos in a directory"""
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all video files
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv')
    video_files = [f for f in os.listdir(input_dir) if f.lower().endswith(video_extensions)]
    
    print(f"Found {len(video_files)} videos in {input_dir}")
    
    # Process each video
    for video_file in video_files:
        video_path = os.path.join(input_dir, video_file)
        video_output_dir = os.path.join(output_dir, os.path.splitext(video_file)[0])
        extract_frames(video_path, video_output_dir, frame_rate)

def main():
    parser = argparse.ArgumentParser(description='Extract frames from videos')
    parser.add_argument('input_dir', help='Directory containing videos')
    parser.add_argument('output_dir', help='Directory to save extracted frames')
    parser.add_argument('--frame-rate', type=int, default=1, help='Extract 1 frame every N frames')
    
    args = parser.parse_args()
    
    process_directory(args.input_dir, args.output_dir, args.frame_rate)

if __name__ == '__main__':
    main() 