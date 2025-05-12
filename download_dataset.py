import os
import requests
import zipfile
import shutil
from tqdm import tqdm
import gdown
import tarfile

def download_file(url, output_path):
    """Download a file with progress bar"""
    print(f"Downloading {output_path}...")
    try:
        gdown.download(url, output_path, quiet=False)
    except Exception as e:
        print(f"Error downloading with gdown: {str(e)}")
        print("Trying alternative download method...")
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as file, tqdm(
            desc=os.path.basename(output_path),
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                pbar.update(size)

def extract_zip(zip_path, extract_to):
    """Extract zip file with progress bar"""
    print(f"Extracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def setup_dataset():
    # Create directories
    os.makedirs('dataset', exist_ok=True)
    os.makedirs('dataset/raw', exist_ok=True)
    os.makedirs('dataset/processed', exist_ok=True)
    
    # DeepFake-TIMIT dataset URLs
    real_url = "https://www.idiap.ch/dataset/deepfaketimit/download/real.zip"
    fake_url = "https://www.idiap.ch/dataset/deepfaketimit/download/fake.zip"
    
    # Alternative URLs (if the above don't work)
    backup_real_url = "https://drive.google.com/uc?id=1-5X9QzqQzqQzqQzqQzqQzqQzqQzqQzqQ"
    backup_fake_url = "https://drive.google.com/uc?id=1-6X9QzqQzqQzqQzqQzqQzqQzqQzqQzqQ"
    
    # Download real images
    real_zip = "dataset/raw/real_images.zip"
    try:
        download_file(real_url, real_zip)
    except:
        print("Trying backup URL for real images...")
        download_file(backup_real_url, real_zip)
    
    # Download fake images
    fake_zip = "dataset/raw/fake_images.zip"
    try:
        download_file(fake_url, fake_zip)
    except:
        print("Trying backup URL for fake images...")
        download_file(backup_fake_url, fake_zip)
    
    # Extract images
    print("Extracting images...")
    extract_zip(real_zip, "dataset/processed/real")
    extract_zip(fake_zip, "dataset/processed/fake")
    
    # Clean up zip files
    os.remove(real_zip)
    os.remove(fake_zip)
    
    print("Dataset download and extraction completed!")
    print("\nNext step:")
    print("Train the model:")
    print("python deepfake_detector.py --train dataset/processed/real dataset/processed/fake")

def extract_tar(tar_path, extract_to):
    """Extract tar file with progress bar"""
    print(f"Extracting {tar_path}...")
    with tarfile.open(tar_path, 'r:gz') as tar:
        tar.extractall(path=extract_to)

if __name__ == "__main__":
    setup_dataset()

    # Extract tar file
    tar_path = 'path/to/your/deepfaketimit.tar.gz'  # Update this path
    extract_path = 'dataset/raw'  # Or wherever you want to extract

    os.makedirs(extract_path, exist_ok=True)

    extract_tar(tar_path, extract_path)

    print("Extraction complete!")