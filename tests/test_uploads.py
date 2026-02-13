import sys
import os
import io
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
from main import app

import pytest
from fastapi.testclient import TestClient
from pathlib import Path

client = TestClient(app)

# Clean up uploads directory after tests
@pytest.fixture(autouse=True)
def cleanup_uploads():
    yield
    upload_dir = Path("uploads")
    if upload_dir.exists():
        for file in upload_dir.iterdir():
            if file.is_file():
                file.unlink()


def test_upload_video_success():
    """Test successful video upload."""
    # Create a fake video file
    video_content = b"fake video content for testing"
    video_file = ("test_video.mp4", io.BytesIO(video_content), "video/mp4")
    
    response = client.post(
        "/api/upload/video",
        files={"file": video_file}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["filename"] == "test_video.mp4"
    assert data["message"] == "Video uploaded successfully"
    assert data["size"] == len(video_content)


def test_upload_video_invalid_format():
    """Test video upload with invalid format."""
    # Create a file with invalid extension
    file_content = b"not a video"
    file = ("test_file.txt", io.BytesIO(file_content), "text/plain")
    
    response = client.post(
        "/api/upload/video",
        files={"file": file}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["status"] == "error"
    assert data["detail"]["error"]["code"] == "INVALID_FORMAT"
    assert "Invalid video format" in data["detail"]["error"]["message"]


def test_upload_video_no_file():
    """Test video upload without file."""
    response = client.post("/api/upload/video")
    
    assert response.status_code == 422  # FastAPI validation error


def test_upload_video_too_large():
    """Test video upload with file exceeding size limit."""
    # Create a file larger than MAX_FILE_SIZE (100 MB)
    # We'll create a 101 MB file
    large_content = b"x" * (101 * 1024 * 1024)
    video_file = ("large_video.mp4", io.BytesIO(large_content), "video/mp4")
    
    response = client.post(
        "/api/upload/video",
        files={"file": video_file}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["status"] == "error"
    assert data["detail"]["error"]["code"] == "INVALID_FORMAT"
    assert "File size exceeds maximum allowed" in data["detail"]["error"]["message"]


def test_upload_file_success():
    """Test successful file upload."""
    # Create a fake file
    file_content = b"fake file content for testing"
    file = ("test_document.pdf", io.BytesIO(file_content), "application/pdf")
    
    response = client.post(
        "/api/upload/file",
        files={"file": file}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["filename"] == "test_document.pdf"
    assert data["message"] == "File uploaded successfully"
    assert data["size"] == len(file_content)


def test_upload_file_with_session_id():
    """Test file upload with session ID."""
    file_content = b"file with session"
    file = ("session_file.jpg", io.BytesIO(file_content), "image/jpeg")
    
    response = client.post(
        "/api/upload/file",
        files={"file": file},
        data={"session_id": "session-123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"


def test_upload_file_invalid_format():
    """Test file upload with invalid format."""
    # Create a file with invalid extension
    file_content = b"executable content"
    file = ("malicious.exe", io.BytesIO(file_content), "application/x-executable")
    
    response = client.post(
        "/api/upload/file",
        files={"file": file}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["status"] == "error"
    assert data["detail"]["error"]["code"] == "INVALID_FORMAT"
    assert "Invalid file format" in data["detail"]["error"]["message"]


def test_upload_different_video_formats():
    """Test uploading different video formats."""
    video_formats = ["test.mp4", "test.avi", "test.mov", "test.mkv", "test.webm"]
    
    for filename in video_formats:
        video_content = b"video content"
        video_file = (filename, io.BytesIO(video_content), "video/mp4")
        
        response = client.post(
            "/api/upload/video",
            files={"file": video_file}
        )
        
        assert response.status_code == 200, f"Failed for {filename}"
        data = response.json()
        assert data["filename"] == filename
