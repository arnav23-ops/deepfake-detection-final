import os
import shutil
import glob

# === USER: Set your target speaker here ===
TARGET_SPEAKER = 'fadg0'  # Change this to any speaker you want

# === Paths ===
BASE_DIR = 'DeepfakeTIMIT/lower_quality'
REAL_OUT = 'dataset/raw/real'
FAKE_OUT = 'dataset/raw/fake'

os.makedirs(REAL_OUT, exist_ok=True)
os.makedirs(FAKE_OUT, exist_ok=True)

# 1. Copy real videos for the target speaker
real_speaker_dir = os.path.join(BASE_DIR, TARGET_SPEAKER)
real_videos = glob.glob(os.path.join(real_speaker_dir, '*.avi'))
print(f'Found {len(real_videos)} real videos for {TARGET_SPEAKER}')
for vid in real_videos:
    shutil.copy(vid, os.path.join(REAL_OUT, os.path.basename(vid)))

# 2. Copy fake videos generated to look like the target speaker
for speaker in os.listdir(BASE_DIR):
    speaker_dir = os.path.join(BASE_DIR, speaker)
    if not os.path.isdir(speaker_dir) or speaker == TARGET_SPEAKER:
        continue
    # Find all videos in this folder that are deepfakes of the target speaker
    pattern = f'*video-{TARGET_SPEAKER}.avi'
    fake_videos = glob.glob(os.path.join(speaker_dir, pattern))
    for vid in fake_videos:
        shutil.copy(vid, os.path.join(FAKE_OUT, os.path.basename(vid)))
print(f'Organized fake videos for {TARGET_SPEAKER}')

print('\nDone!')
print(f'Real videos: {REAL_OUT}')
print(f'Fake videos: {FAKE_OUT}')
print('You can now extract frames and train your model.') 