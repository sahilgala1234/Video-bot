# Video Search and Upload Bot

This Python-based bot automates the process of searching for `.mp4` videos, uploading them to a server, and handling errors efficiently. It supports directory monitoring and concurrent operations using asyncio.

---

## **Features**
- Monitors a specified directory for `.mp4` files.
- Fetches pre-signed upload URLs from the API.
- Uploads videos to the server using asynchronous PUT requests.
- Handles errors and logs progress for troubleshooting.
- Automatically deletes local video files after successful upload.

---

## **Project Structure**
video-bot/ ├── main.py # Main script ├── requirements.txt # Dependencies ├── README.md # Documentation └── /videos # Directory monitored for .mp4 files

yaml
Copy code

---

## **Setup and Installation**

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd video-bot
2. Install Dependencies
Ensure you have Python 3.8+ installed. Install the required libraries:

bash
Copy code
pip install -r requirements.txt
3. Environment Setup
Create an environment file or set environment variables:

API_BASE_URL: Base URL for API endpoints.
FLIC_TOKEN: Your API access token for authentication.
Example .env file:

makefile
Copy code
API_BASE_URL=https://api.socialverseapp.com
FLIC_TOKEN=your-token-here
4. Directory Structure
Ensure the /videos directory exists:

bash
Copy code
mkdir videos
Usage
1. Run the Bot
To start monitoring the /videos directory:

bash
Copy code
python main.py
2. Upload Workflow
Place .mp4 files in the /videos directory.
The bot will:
Detect new files.
Fetch a pre-signed upload URL.
Upload the video.
Create a post entry in the server.
Delete the video file locally after a successful upload.
API Endpoints
1. Get Upload URL
Endpoint: /posts/generate-upload-url
Method: GET
Headers:
json
Copy code
{
  "Flic-Token": "<YOUR_TOKEN>",
  "Content-Type": "application/json"
}
2. Upload Video
Method: PUT
Use the pre-signed URL returned from the "Get Upload URL" step.
3. Create Post
Endpoint: /posts
Method: POST
Headers:
json
Copy code
{
  "Flic-Token": "<YOUR_TOKEN>",
  "Content-Type": "application/json"
}
Body:
json
Copy code
{
  "title": "<video title>",
  "hash": "<hash from Step 1>",
  "is_available_in_public_feed": false,
  "category_id": <category_id>
}