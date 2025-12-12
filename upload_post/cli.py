import argparse
import logging
from pathlib import Path
from typing import List, Optional
from . import UploadPostClient, UploadPostError

logger = logging.getLogger(__name__)

def upload_video_command(client: UploadPostClient, args):
    """Handle video upload command"""
    try:
        response = client.upload_video(
            video_path=args.video,
            title=args.title,
            user=args.user,
            platforms=args.platforms
        )
        logger.info(f"Video upload successful! Response: {response}")
        return response
    except UploadPostError as e:
        logger.error(f"Video upload failed: {str(e)}")
        raise SystemExit(1) from e

def upload_photos_command(client: UploadPostClient, args):
    """Handle photos upload command"""
    try:
        response = client.upload_photos(
            photos=args.photos,
            user=args.user,
            platforms=args.platforms,
            title=args.title,
            caption=args.caption
        )
        logger.info(f"Photos upload successful! Response: {response}")
        return response
    except UploadPostError as e:
        logger.error(f"Photos upload failed: {str(e)}")
        raise SystemExit(1) from e

def upload_text_command(client: UploadPostClient, args):
    """Handle text upload command"""
    try:
        response = client.upload_text(
            user=args.user,
            platforms=args.platforms,
            title=args.title
        )
        logger.info(f"Text post successful! Response: {response}")
        return response
    except UploadPostError as e:
        logger.error(f"Text post failed: {str(e)}")
        raise SystemExit(1) from e

def main():
    parser = argparse.ArgumentParser(
        description="Upload content to multiple social platforms via Upload-Post.com API"
    )
    parser.add_argument("--api-key", required=True, help="API authentication key")
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    # Create subparsers for different upload types
    subparsers = parser.add_subparsers(dest='command', help='Upload type', required=True)
    
    # Video upload parser
    video_parser = subparsers.add_parser('video', help='Upload video content')
    video_parser.add_argument("--video", required=True, type=Path, help="Path to video file or URL")
    video_parser.add_argument("--title", required=True, help="Video title")
    video_parser.add_argument("--user", required=True, help="User identifier")
    video_parser.add_argument(
        "--platforms", 
        nargs="+",
        required=True,
        choices=["tiktok", "instagram", "linkedin", "youtube", "facebook", "x", "threads", "pinterest"],
        help="Platforms to upload to"
    )
    video_parser.set_defaults(func=upload_video_command)
    
    # Photos upload parser
    photos_parser = subparsers.add_parser('photos', help='Upload photo content')
    photos_parser.add_argument("--photos", nargs="+", required=True, help="Paths to photo files or URLs")
    photos_parser.add_argument("--title", required=True, help="Photo album title")
    photos_parser.add_argument("--user", required=True, help="User identifier")
    photos_parser.add_argument("--caption", help="Optional caption for photos")
    photos_parser.add_argument(
        "--platforms", 
        nargs="+",
        required=True,
        choices=["tiktok", "instagram", "linkedin", "facebook", "x", "threads", "pinterest"],
        help="Platforms to upload to"
    )
    photos_parser.set_defaults(func=upload_photos_command)
    
    # Text upload parser
    text_parser = subparsers.add_parser('text', help='Upload text content')
    text_parser.add_argument("--title", required=True, help="Text content for the post")
    text_parser.add_argument("--user", required=True, help="User identifier")
    text_parser.add_argument(
        "--platforms", 
        nargs="+",
        required=True,
        choices=["linkedin", "x", "facebook", "threads"],
        help="Platforms to upload to"
    )
    text_parser.set_defaults(func=upload_text_command)

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    client = UploadPostClient(api_key=args.api_key)
    
    # Execute the appropriate command function
    args.func(client, args)

if __name__ == "__main__":
    main()
