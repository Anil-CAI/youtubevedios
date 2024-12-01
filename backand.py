from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import yt_dlp
from datetime import datetime
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cur_dir = os.getcwd()

@app.post("/download")
async def download_video(link: str = Form(...)):
    try:
        # Validate URL (basic check, extend as needed)
        if not link.startswith("http"):
            raise HTTPException(status_code=400, detail="Invalid URL")

        # Dynamic filename based on timestamp
        filename = f"video_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
        filepath = os.path.join(cur_dir, filename)

        youtube_dl_options = {
            "format": "best",
            "outtmpl": filepath,
            "quiet": True,  # Suppress console logs for cleaner output
        }

        # Download video using yt_dlp
        with yt_dlp.YoutubeDL(youtube_dl_options) as ydl:
            ydl.download([link])

        return JSONResponse(
            content={"status": "Download completed", "file": filename}, 
            status_code=200
        )

    except yt_dlp.utils.DownloadError as e:
        logging.error(f"Download failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to download video")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
