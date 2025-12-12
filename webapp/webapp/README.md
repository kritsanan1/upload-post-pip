# Upload-Post AI WebApp

A modern web application that integrates **Gemini AI** with the **Upload-Post API** to enable intelligent content generation and social media management.

## 🌟 Features

### 🤖 AI-Powered Content Generation
- **Video Descriptions**: Generate engaging, SEO-friendly video descriptions with hashtags
- **Social Media Captions**: Create compelling captions with emojis and relevant hashtags  
- **Content Ideas**: Generate creative content ideas for various topics
- **AI Analysis**: Analyze content and provide suggestions for improvement

### 📱 Multi-Platform Social Media Upload
- **Video Upload**: Upload videos to TikTok, Instagram, LinkedIn, YouTube, Facebook, X (Twitter), Threads, Pinterest
- **Photo Upload**: Upload photos to multiple platforms simultaneously
- **Text Posts**: Create and publish text-based content
- **Batch Operations**: Upload to multiple platforms at once

### 🎨 Modern Web Interface
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Drag & Drop**: Intuitive file upload with drag-and-drop support
- **Real-time Preview**: Preview files before uploading
- **Progress Indicators**: Visual feedback for all operations
- **Error Handling**: Comprehensive error messages and recovery

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Upload-Post API key
- Gemini AI API key (optional but recommended)

### Installation

1. **Clone and navigate to the webapp directory:**
   ```bash
   cd webapp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

5. **Access the webapp:**
   Open your browser to `http://localhost:5000`

## 🛠️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Gemini AI Configuration (Optional)
GEMINI_API_KEY=your-gemini-api-key-here

# Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB in bytes
UPLOAD_FOLDER=uploads

# Upload-Post API Configuration (Required)
UPLOAD_POST_API_KEY=your-upload-post-api-key-here
```

### API Keys

#### Upload-Post API Key
Get your API key from [Upload-Post.com](https://upload-post.com). This is required for social media uploads.

#### Gemini AI API Key (Optional)
Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey). This enables AI content generation features.

## 📖 Usage

### 1. Content Upload

#### Video Upload
1. Navigate to the **Upload** page
2. Select **Video** tab
3. Choose your video file (MP4, AVI, MOV, WMV, FLV, MKV)
4. Enter title and select target platforms
5. Click **Upload**

#### Photo Upload
1. Navigate to the **Upload** page
2. Select **Photos** tab
3. Choose multiple photos (JPG, JPEG, PNG, GIF, BMP, WebP)
4. Enter album title, caption, and select platforms
5. Click **Upload**

#### Text Posts
1. Navigate to the **Upload** page
2. Select **Text** tab
3. Enter post title and select platforms
4. Click **Post**

### 2. AI Content Generation

#### Generate Video Descriptions
1. Navigate to the **AI Generate** page
2. Select **Video Description** type
3. Enter your video topic
4. Click **Generate**
5. Copy the AI-generated description

#### Generate Social Media Captions
1. Navigate to the **AI Generate** page
2. Select **Post Caption** type
3. Enter your content theme
4. Click **Generate**
5. Copy the AI-generated caption

#### Generate Content Ideas
1. Navigate to the **AI Generate** page
2. Select **Content Ideas** type
3. Enter your niche/topic
4. Click **Generate**
5. Explore the AI-suggested content ideas

## 🔧 API Endpoints

The webapp provides a REST API for programmatic access:

### Upload Endpoints

#### Upload Video
```http
POST /api/upload
Content-Type: multipart/form-data

form data:
- type: video
- file: [video file]
- title: Video title
- user: User identifier
- platforms[]: List of platforms
```

#### Upload Photos
```http
POST /api/upload
Content-Type: multipart/form-data

form data:
- type: photos
- files[]: [photo files]
- title: Album title
- caption: Photo caption
- user: User identifier
- platforms[]: List of platforms
```

#### Upload Text
```http
POST /api/upload
Content-Type: multipart/form-data

form data:
- type: text
- title: Post title
- user: User identifier
- platforms[]: List of platforms
```

### AI Generation Endpoints

#### Generate Content
```http
POST /api/generate
Content-Type: application/json

{
  "type": "video_description|post_caption|content_ideas",
  "prompt": "Your content theme or topic"
}
```

#### Get Available Platforms
```http
GET /api/platforms
```

## 🎯 Supported Platforms

### Video Platforms
- TikTok
- Instagram (Reels)
- LinkedIn
- YouTube
- Facebook
- X (Twitter)
- Threads
- Pinterest

### Photo Platforms
- TikTok
- Instagram
- LinkedIn
- Facebook
- X (Twitter)
- Threads
- Pinterest

### Text Platforms
- LinkedIn
- X (Twitter)
- Facebook
- Threads

## 🧪 Testing

Run the test script to verify the installation:

```bash
python3 test_api.py
```

This will test:
- ✅ Webapp health check
- ✅ API endpoints
- ✅ AI generation (if configured)

## 🐛 Troubleshooting

### Webapp Won't Start
- Check Python 3.7+ is installed: `python3 --version`
- Install dependencies: `pip install -r requirements.txt`
- Check port 5000 is available

### Upload-Post API Issues
- Verify your API key in `.env` file
- Check the API key format and expiration
- Review Upload-Post API documentation

### Gemini AI Not Working
- Add your Gemini API key to `.env`
- Check if Gemini API is enabled for your account
- Verify API key has proper permissions

### File Upload Errors
- Check file size limits (16MB default)
- Verify file format is supported
- Ensure upload directory has write permissions

### Platform Authentication Issues
- Verify platform-specific credentials in Upload-Post dashboard
- Check if platforms require additional authentication steps
- Review platform API rate limits

## 🔒 Security Features

- **File Type Validation**: Only allowed file types can be uploaded
- **File Size Limits**: Configurable maximum file size (default 16MB)
- **Secure Filenames**: All uploaded files are sanitized
- **Error Handling**: Comprehensive error handling without information leakage
- **CSRF Protection**: Built-in CSRF protection for forms

## 📁 File Structure

```
webapp/
├── app.py                    # Main Flask application
├── requirements.txt         # Python dependencies
├── run.sh                    # Startup script
├── test_api.py               # API testing script
├── .env.example              # Environment variables template
├── .env                      # Environment variables (create from .env.example)
├── uploads/                  # Uploaded files directory
├── static/                   # Static assets
│   ├── css/style.css        # Custom styles
│   ├── js/app.js            # JavaScript functionality
│   └── images/              # Image assets
└── templates/               # HTML templates
    ├── base.html            # Base template
    ├── index.html           # Home page
    ├── upload.html          # Upload interface
    └── generate.html        # AI generation interface
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the upload-post-pip package. See the main repository for license information.

## 🆘 Support

For issues and questions:
- Check the [Upload-Post API Documentation](https://upload-post.com/docs)
- Review the [Google Gemini AI Documentation](https://ai.google.dev/gemini-api/docs)
- Create an issue in the GitHub repository

---

**Made with ❤️ using Flask, Gemini AI, and Bootstrap**