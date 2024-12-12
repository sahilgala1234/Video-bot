# main.py

import os
import asyncio
import aiohttp
import requests
import hashlib
import shutil
from pathlib import Path
from tqdm import tqdm

# Constants
FLIC_TOKEN = "<YOUR_TOKEN>"  # Replace with your Flic-Token
API_BASE_URL = "https://api.socialverseapp.com"
VIDEOS_DIR = "./videos"

# Headers for API requests
HEADERS = {
    "Flic-Token": FLIC_TOKEN,
    "Content-Type": "application/json",
}

async def get_upload_url():
    """Fetches a pre-signed upload URL from the API."""
    url = f"{API_BASE_URL}/posts/generate-upload-url"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to get upload URL: {response.status}")

async def upload_video(upload_url, file_path):
    """Uploads a video file using the pre-signed URL."""
    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as file:
            async with session.put(upload_url, data=file) as response:
                if response.status == 200:
                    print(f"Uploaded {file_path}")
                else:
                    raise Exception(f"Failed to upload video: {response.status}")

async def create_post(title, video_hash, category_id=25):
    """Creates a new post after uploading the video."""
    url = f"{API_BASE_URL}/posts"
    payload = {
        "title": title,
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": category_id,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=HEADERS, json=payload) as response:
            if response.status == 201:
                print(f"Post created for {title}")
            else:
                raise Exception(f"Failed to create post: {response.status}")

async def process_video(file_path):
    """Processes a single video: uploads and creates a post."""
    # Calculate file hash
    with open(file_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    # Step 1: Get upload URL
    upload_data = await get_upload_url()
    upload_url = upload_data["url"]
    video_hash = upload_data["hash"]

    # Step 2: Upload video
    await upload_video(upload_url, file_path)

    # Step 3: Create post
    title = Path(file_path).stem
    await create_post(title, video_hash)

    # Step 4: Delete local file
    os.remove(file_path)
    print(f"Deleted local file: {file_path}")

async def monitor_directory():
    """Monitors the directory for new .mp4 files and processes them."""
    print(f"Monitoring directory: {VIDEOS_DIR}")
    processed_files = set()
    while True:
        video_files = [f for f in Path(VIDEOS_DIR).glob("*.mp4") if f not in processed_files]
        for file_path in video_files:
            try:
                await process_video(file_path)
                processed_files.add(file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        await asyncio.sleep(5)

if __name__ == "__main__":
    # Ensure videos directory exists
    os.makedirs(VIDEOS_DIR, exist_ok=True)

    # Run the directory monitoring loop
    try:
        asyncio.run(monitor_directory())
    except KeyboardInterrupt:
        print("Exiting...")
