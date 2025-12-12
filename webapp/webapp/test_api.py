#!/usr/bin/env python3
"""Test script for Upload-Post AI WebApp API endpoints"""

import requests
import json

# Base URL for the webapp
BASE_URL = "https://5000-irihg3nfu2lrpv41m330r-2e77fc33.sandbox.novita.ai"

def test_health_check():
    """Test if the webapp is running"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Health check: {response.status_code} - {response.url}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🧪 Testing API endpoints...")
    
    # Test platforms endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/platforms")
        if response.status_code == 200:
            platforms = response.json()
            print(f"✅ Platforms API: {list(platforms.keys())}")
        else:
            print(f"❌ Platforms API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Platforms API error: {e}")

def test_ai_generation():
    """Test AI content generation"""
    print("\n🤖 Testing AI generation...")
    
    try:
        payload = {
            "type": "post_caption",
            "prompt": "A beautiful sunset over the ocean"
        }
        response = requests.post(
            f"{BASE_URL}/api/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ AI Generated content: {result.get('content', 'No content')[:100]}...")
        elif response.status_code == 503:
            print("⚠️  AI service not available - Gemini API key not configured")
        else:
            print(f"❌ AI generation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ AI generation error: {e}")

def main():
    """Main test function"""
    print("🚀 Testing Upload-Post AI WebApp...")
    
    # Test health check
    if not test_health_check():
        print("❌ WebApp is not responding properly")
        return
    
    # Test API endpoints
    test_api_endpoints()
    
    # Test AI generation
    test_ai_generation()
    
    print("\n✅ Testing completed!")
    print(f"🌐 WebApp is running at: {BASE_URL}")

if __name__ == "__main__":
    main()