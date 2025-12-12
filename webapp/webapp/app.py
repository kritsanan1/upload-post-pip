import os
import json
import logging
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import google.generativeai as genai
from dotenv import load_dotenv

# Import the upload-post client
import sys
sys.path.append('..')
from upload_post import UploadPostClient, UploadPostError

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure upload directory exists
os.makedirs(os.path.join('webapp', UPLOAD_FOLDER), exist_ok=True)

# Configure Gemini AI
gemini_api_key = os.environ.get('GEMINI_API_KEY')
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    gemini_model = genai.GenerativeModel('gemini-pro')
else:
    gemini_model = None
    logger.warning("Gemini AI not configured. Content generation features will be disabled.")

# Load Upload-Post API key
UPLOAD_POST_API_KEY = None
try:
    # Try to load from the uploaded file
    api_key_file = Path(__file__).parent.parent / 'upload_post' / 'upload_files' / 'uploaded_file_0'
    if api_key_file.exists():
        with open(api_key_file, 'r') as f:
            UPLOAD_POST_API_KEY = f.read().strip().replace('UPLOAD_POST_API_KEY=', '')
        logger.info("Upload-Post API key loaded successfully")
    else:
        # Fallback to environment variable
        UPLOAD_POST_API_KEY = os.environ.get('UPLOAD_POST_API_KEY')
        if UPLOAD_POST_API_KEY:
            logger.info("Upload-Post API key loaded from environment")
except Exception as e:
    logger.error(f"Failed to load Upload-Post API key: {e}")

# Initialize Upload-Post client
upload_client = None
if UPLOAD_POST_API_KEY:
    try:
        upload_client = UploadPostClient(api_key=UPLOAD_POST_API_KEY)
        logger.info("Upload-Post client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Upload-Post client: {e}")
else:
    logger.warning("Upload-Post client not initialized. Upload features will be disabled.")

def allowed_file(filename, allowed_extensions):
    """Check if file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_content_with_ai(content_type, prompt, **kwargs):
    """Generate content using Gemini AI"""
    if not gemini_model:
        return None
    
    try:
        if content_type == "video_description":
            full_prompt = f"Generate an engaging video description for: {prompt}. Make it SEO-friendly and include relevant hashtags."
        elif content_type == "post_caption":
            full_prompt = f"Generate an engaging social media caption for: {prompt}. Include relevant emojis and hashtags."
        elif content_type == "content_ideas":
            full_prompt = f"Generate creative content ideas for: {prompt}. Provide 5-10 unique and engaging ideas."
        else:
            full_prompt = prompt
        
        response = gemini_model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini AI generation failed: {e}")
        return None

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', 
                         gemini_available=gemini_model is not None,
                         upload_available=upload_client is not None)

@app.route('/upload')
def upload_page():
    """Upload page"""
    return render_template('upload.html',
                           gemini_available=gemini_model is not None,
                           upload_available=upload_client is not None)

@app.route('/generate')
def generate_page():
    """AI content generation page"""
    return render_template('generate.html', gemini_available=gemini_model is not None)

@app.route('/api/upload', methods=['POST'])
def api_upload():
    """Handle file uploads"""
    if not upload_client:
        return jsonify({"error": "Upload service not available"}), 503
    
    try:
        upload_type = request.form.get('type', 'video')
        user = request.form.get('user', 'default_user')
        platforms = request.form.getlist('platforms[]')
        title = request.form.get('title', '')
        
        if not platforms:
            return jsonify({"error": "No platforms specified"}), 400
        
        if upload_type == 'video':
            return handle_video_upload(user, platforms, title)
        elif upload_type == 'photos':
            return handle_photos_upload(user, platforms, title)
        elif upload_type == 'text':
            return handle_text_upload(user, platforms, title)
        else:
            return jsonify({"error": "Invalid upload type"}), 400
            
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return jsonify({"error": str(e)}), 500

def handle_video_upload(user, platforms, title):
    """Handle video file upload"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
        return jsonify({"error": "Invalid file type. Allowed: " + ", ".join(ALLOWED_VIDEO_EXTENSIONS)}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join('webapp', UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Upload to platforms
        response = upload_client.upload_video(
            video_path=filepath,
            title=title,
            user=user,
            platforms=platforms
        )
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({"success": True, "response": response})
        
    except UploadPostError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Video upload failed: {e}")
        return jsonify({"error": "Upload failed"}), 500

def handle_photos_upload(user, platforms, title):
    """Handle photos upload"""
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return jsonify({"error": "No files provided"}), 400
    
    photo_paths = []
    try:
        for file in files:
            if allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
                filename = secure_filename(file.filename)
                filepath = os.path.join('webapp', UPLOAD_FOLDER, filename)
                file.save(filepath)
                photo_paths.append(filepath)
        
        if not photo_paths:
            return jsonify({"error": "No valid image files"}), 400
        
        caption = request.form.get('caption', '')
        response = upload_client.upload_photos(
            photos=photo_paths,
            user=user,
            platforms=platforms,
            title=title,
            caption=caption
        )
        
        # Clean up files
        for path in photo_paths:
            if os.path.exists(path):
                os.remove(path)
        
        return jsonify({"success": True, "response": response})
        
    except UploadPostError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Photos upload failed: {e}")
        return jsonify({"error": "Upload failed"}), 500

def handle_text_upload(user, platforms, title):
    """Handle text post upload"""
    try:
        response = upload_client.upload_text(
            user=user,
            platforms=platforms,
            title=title
        )
        return jsonify({"success": True, "response": response})
    except UploadPostError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Text upload failed: {e}")
        return jsonify({"error": "Upload failed"}), 500

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """Generate content using Gemini AI"""
    if not gemini_model:
        return jsonify({"error": "AI service not available"}), 503
    
    try:
        data = request.get_json()
        content_type = data.get('type', 'post_caption')
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400
        
        generated_content = generate_content_with_ai(content_type, prompt)
        
        if generated_content:
            return jsonify({"success": True, "content": generated_content})
        else:
            return jsonify({"error": "Failed to generate content"}), 500
            
    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        return jsonify({"error": "Generation failed"}), 500

@app.route('/api/platforms')
def api_platforms():
    """Get available platforms for different content types"""
    return jsonify({
        "video": ["tiktok", "instagram", "linkedin", "youtube", "facebook", "x", "threads", "pinterest"],
        "photos": ["tiktok", "instagram", "linkedin", "facebook", "x", "threads", "pinterest"],
        "text": ["linkedin", "x", "facebook", "threads"]
    })

@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large. Maximum size is 16MB."}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)