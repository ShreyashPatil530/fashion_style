#!/usr/bin/env python3
"""
AI Fashion Stylist - Test Script
Run this to test if everything is working properly
"""

import requests
import json
import os
from datetime import datetime

def test_server_connection():
    """Test if the Flask server is running"""
    try:
        print("🔌 Testing server connection...")
        response = requests.get('http://localhost:5000/test', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server is running: {data.get('status')}")
            return True
        else:
            print(f"❌ Server returned error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Flask app is running on port 5000.")
        return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def test_components():
    """Test individual components"""
    print("\n🧪 Testing components...")
    print("-" * 40)
    
    # Test YOLO
    try:
        from yolo_detect import detect_clothing, generate_fallback_items
        print("✅ YOLO module imported successfully")
        
        # Test fallback
        items = generate_fallback_items()
        print(f"✅ YOLO fallback working: {len(items)} items")
        
    except Exception as e:
        print(f"❌ YOLO test failed: {e}")
    
    # Test OpenAI
    try:
        from openai_api import get_outfit_suggestions
        print("✅ OpenAI module imported successfully")
        
        # Test with sample data
        sample_items = [{'item': 'test shirt', 'color': 'blue', 'category': 'top'}]
        suggestions = get_outfit_suggestions(sample_items)
        print(f"✅ OpenAI working: {len(suggestions)} characters")
        
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
    
    # Test SerpAPI
    try:
        from serpapi_api import get_shopping_links
        print("✅ SerpAPI module imported successfully")
        
        # Test with sample data
        sample_items = [{'item': 'test shirt', 'color': 'blue', 'category': 'top'}]
        links = get_shopping_links(sample_items)
        print(f"✅ SerpAPI working: {len(links)} links")
        
    except Exception as e:
        print(f"❌ SerpAPI test failed: {e}")
    
    # Test Database
    try:
        from db import create_connection
        conn = create_connection()
        if conn:
            print("✅ Database connection successful")
            conn.close()
        else:
            print("⚠️ Database connection failed (will use fallback)")
    except Exception as e:
        print(f"⚠️ Database test failed: {e}")

def create_test_image():
    """Create a simple test image"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple test image
        img = Image.new('RGB', (400, 400), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Draw some shapes to simulate clothing
        draw.rectangle([100, 100, 300, 200], fill='darkblue', outline='navy')
        draw.rectangle([120, 220, 280, 320], fill='brown', outline='darkbrown')
        
        # Save test image
        test_image_path = 'test_outfit.jpg'
        img.save(test_image_path)
        print(f"✅ Test image created: {test_image_path}")
        return test_image_path
        
    except Exception as e:
        print(f"❌ Failed to create test image: {e}")
        return None

def test_full_analysis():
    """Test the complete analysis pipeline"""
    print("\n🎯 Testing full analysis pipeline...")
    print("-" * 40)
    
    # Create test image
    test_image_path = create_test_image()
    
    if not test_image_path or not os.path.exists(test_image_path):
        print("❌ No test image available")
        return False
    
    try:
        # Prepare test data
        files = {'image': open(test_image_path, 'rb')}
        data = {'user_id': 'test_user'}
        
        print("📡 Sending test request to /analyze...")
        
        # Send request
        response = requests.post(
            'http://localhost:5000/analyze',
            files=files,
            data=data,
            timeout=60
        )
        
        files['image'].close()
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                print("✅ Analysis completed successfully!")
                print(f"📊 Detected items: {len(result.get('detected_items', []))}")
                print(f"📝 AI suggestions: {len(result.get('ai_suggestions', ''))} characters")
                print(f"🛍️ Shopping links: {len(result.get('shopping_links', []))}")
                
                # Show sample results
                items = result.get('detected_items', [])
                if items:
                    print(f"   Sample item: {items[0]}")
                
                suggestions = result.get('ai_suggestions', '')
                if suggestions:
                    print(f"   Suggestions preview: {suggestions[:100]}...")
                
                return True
            else:
                print(f"❌ Analysis failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data.get('error', 'Unknown error')}")
            except:
                print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Full analysis test failed: {e}")
        return False
    finally:
        # Clean up test image
        if test_image_path and os.path.exists(test_image_path):
            os.remove(test_image_path)
            print("🗑️ Test image cleaned up")

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 AI FASHION STYLIST - TESTING SUITE")
    print("="*60)
    print(f"📅 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Server Connection
    server_ok = test_server_connection()
    
    if not server_ok:
        print("\n❌ Server is not running. Please start the Flask app first:")
        print("   python app.py")
        return
    
    # Test 2: Components
    test_components()
    
    # Test 3: Full Analysis
    analysis_ok = test_full_analysis()
    
    # Summary
    print("\n" + "="*60)
    print("📋 TEST SUMMARY")
    print("="*60)
    print(f"🔌 Server Connection: {'✅ PASS' if server_ok else '❌ FAIL'}")
    print(f"🎯 Full Analysis: {'✅ PASS' if analysis_ok else '❌ FAIL'}")
    
    if server_ok and analysis_ok:
        print("\n🎉 ALL TESTS PASSED! Your AI Fashion Stylist is working perfectly!")
        print("🌐 You can now use the web interface at: http://localhost:5000")
    else:
        print("\n⚠️ Some tests failed. Check the error messages above.")
    
    print("="*60)

if __name__ == "__main__":
    main()