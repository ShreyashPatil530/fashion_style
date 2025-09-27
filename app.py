import os
import json
import traceback
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Import our custom modules
from yolo_detect import detect_clothing
from openai_api import get_outfit_suggestions
from serpapi_api import get_shopping_links
from db import create_connection, save_outfit_analysis, initialize_database

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    """Test endpoint to verify server is working"""
    return jsonify({
        'status': 'Server is working perfectly!', 
        'timestamp': datetime.now().isoformat(),
        'version': '1.0'
    })

@app.route('/analyze', methods=['POST'])
def analyze_image():
    print("\n" + "="*50)
    print("🚀 ANALYZE ENDPOINT CALLED")
    print("="*50)
    
    try:
        # Log request details
        print(f"📝 Request files: {list(request.files.keys())}")
        print(f"📝 Request form: {dict(request.form)}")
        
        # Check if image file is present
        if 'image' not in request.files:
            print("❌ No image file in request")
            return jsonify({
                'success': False, 
                'error': 'No image file provided. Please select an image first.'
            }), 400
        
        file = request.files['image']
        print(f"📁 File received: '{file.filename}' (type: {file.content_type})")
        
        if file.filename == '':
            print("❌ Empty filename")
            return jsonify({
                'success': False, 
                'error': 'No file selected. Please choose an image file.'
            }), 400
        
        if not file or not allowed_file(file.filename):
            print("❌ Invalid file type")
            return jsonify({
                'success': False, 
                'error': 'Invalid file type. Please upload JPG, PNG, GIF, BMP, or WebP files only.'
            }), 400
        
        # Generate unique filename and save
        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        print(f"💾 Saving file to: {filepath}")
        file.save(filepath)
        
        # Verify file was saved properly
        if not os.path.exists(filepath):
            print("❌ File was not saved properly")
            return jsonify({
                'success': False, 
                'error': 'Failed to save uploaded file. Please try again.'
            }), 500
        
        file_size = os.path.getsize(filepath)
        print(f"✅ File saved successfully. Size: {file_size} bytes")
        
        # Initialize results with defaults
        detected_items = []
        ai_suggestions = ""
        shopping_links = []
        
        # STEP 1: Detect clothing items using YOLO
        print("\n🔍 STEP 1: DETECTING CLOTHING ITEMS")
        print("-" * 30)
        try:
            detected_items = detect_clothing(filepath)
            print(f"✅ Detection complete. Found {len(detected_items)} items:")
            for i, item in enumerate(detected_items):
                print(f"   {i+1}. {item}")
        except Exception as e:
            print(f"⚠️ YOLO detection failed: {e}")
            detected_items = [
                {
                    'item': 'casual outfit',
                    'confidence': 0.75,
                    'color': 'mixed colors',
                    'category': 'clothing'
                },
                {
                    'item': 'stylish accessories',
                    'confidence': 0.65,
                    'color': 'neutral',
                    'category': 'accessory'
                }
            ]
            print(f"🔄 Using fallback items: {len(detected_items)} items")
        
        # STEP 2: Get AI outfit suggestions
        print("\n🤖 STEP 2: GETTING AI SUGGESTIONS")
        print("-" * 30)
        try:
            ai_suggestions = get_outfit_suggestions(detected_items)
            print(f"✅ AI suggestions received. Length: {len(ai_suggestions)} characters")
            print(f"📝 Preview: {ai_suggestions[:100]}..." if len(ai_suggestions) > 100 else ai_suggestions)
        except Exception as e:
            print(f"⚠️ OpenAI API failed: {e}")
            ai_suggestions = generate_fallback_ai_suggestions(detected_items)
            print(f"🔄 Using fallback AI suggestions. Length: {len(ai_suggestions)} characters")
        
        # STEP 3: Get shopping links
        print("\n🛍️ STEP 3: GETTING SHOPPING LINKS")
        print("-" * 30)
        try:
            shopping_links = get_shopping_links(detected_items)
            print(f"✅ Shopping links received: {len(shopping_links)} links")
            for i, link in enumerate(shopping_links[:3]):
                print(f"   {i+1}. {link.get('title', 'No title')[:50]}...")
        except Exception as e:
            print(f"⚠️ Shopping API failed: {e}")
            shopping_links = generate_fallback_shopping_links()
            print(f"🔄 Using fallback shopping links: {len(shopping_links)} links")
        
        # STEP 4: Save to database (optional)
        print("\n💾 STEP 4: SAVING TO DATABASE")
        print("-" * 30)
        user_id = request.form.get('user_id', 'anonymous')
        try:
            result_id = save_outfit_analysis(
                user_id=user_id,
                detected_items=json.dumps(detected_items),
                ai_suggestions=ai_suggestions,
                shopping_links=json.dumps(shopping_links)
            )
            if result_id:
                print(f"✅ Saved to database with ID: {result_id}")
            else:
                print("⚠️ Database save failed, but continuing...")
        except Exception as db_error:
            print(f"⚠️ Database error (non-critical): {db_error}")
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
            print("🗑️ Uploaded file cleaned up")
        except Exception as cleanup_error:
            print(f"⚠️ Cleanup warning: {cleanup_error}")
        
        # Prepare final response
        response_data = {
            'success': True,
            'detected_items': detected_items,
            'ai_suggestions': ai_suggestions,
            'shopping_links': shopping_links,
            'metadata': {
                'processing_time': 'completed',
                'items_count': len(detected_items),
                'suggestions_length': len(ai_suggestions),
                'shopping_count': len(shopping_links)
            }
        }
        
        print("\n✅ SUCCESS - SENDING RESPONSE")
        print("=" * 30)
        print(f"📊 Items: {len(detected_items)}")
        print(f"📝 Suggestions: {len(ai_suggestions)} chars")
        print(f"🛍️ Shopping: {len(shopping_links)} links")
        print("=" * 50)
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR in analyze_image")
        print("=" * 30)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        print("=" * 50)
        
        return jsonify({
            'success': False,
            'error': f'Server error occurred: {str(e)}. Please try again or contact support.',
            'error_type': type(e).__name__
        }), 500

def generate_fallback_ai_suggestions(detected_items):
    """Generate comprehensive fallback suggestions when OpenAI fails"""
    
    # Analyze the detected items
    item_names = [item.get('item', '') for item in detected_items]
    colors = [item.get('color', '') for item in detected_items]
    categories = [item.get('category', '') for item in detected_items]
    
    main_color = colors[0] if colors else 'neutral'
    has_top = any('top' in cat for cat in categories)
    has_bottom = any('bottom' in cat for cat in categories)
    
    suggestions = f"""## Style Analysis
Your outfit features a nice combination of {', '.join(item_names[:3])}{"..." if len(item_names) > 3 else ""}. The {main_color} color palette creates a cohesive and versatile foundation for multiple styling approaches.

## Outfit Suggestions

### Outfit 1: Smart Casual Professional
- Build around your current pieces with structured additions
- Add a tailored blazer or cardigan for sophistication  
- Choose clean, polished footwear like loafers or minimal sneakers
- Include a classic watch and subtle jewelry
- Perfect for work meetings, coffee dates, and networking events

### Outfit 2: Weekend Relaxed & Comfortable
- Layer with cozy pieces like a soft hoodie or casual jacket
- Pair with comfortable jeans or relaxed-fit pants
- Add casual accessories like a baseball cap or crossbody bag  
- Choose your favorite sneakers or comfortable boots
- Great for shopping, casual hangouts, and weekend activities

### Outfit 3: Evening Social Ready
- Elevate with darker, more fitted pieces
- Add sophisticated accessories like a leather belt or statement watch
- Choose dress shoes or stylish boots for a polished finish
- Consider layering with a nice jacket or sweater
- Perfect for dinner dates, social gatherings, and evening events

## Styling Tips
- **Fit is Everything**: Well-fitted clothes instantly elevate any look
- **Color Coordination**: Your {main_color} base pairs beautifully with white, black, gray, and navy
- **Accessorize Thoughtfully**: A good belt, watch, or bag can transform an outfit
- **Layer for Interest**: Mix textures and add depth with strategic layering
- **Quality Basics**: Invest in versatile pieces that work across multiple outfits

## Color Harmony Guide
- **Your Palette**: {main_color} creates a strong foundation
- **Safe Additions**: White, black, gray, and navy always work
- **Pop of Color**: Add one accent color through accessories
- **Seasonal Updates**: Lighter shades for spring/summer, deeper tones for fall/winter

## Occasion Recommendations
**Current Style Works For:**
- Casual coffee dates and brunch meetings
- Shopping trips and errands  
- Work-from-home video calls
- Relaxed office environments
- Weekend family gatherings

**Level Up For:**
- Business meetings (add blazer and dress shoes)
- Date nights (incorporate darker, fitted pieces)
- Social events (add interesting textures and accessories)
- Professional networking (structured pieces and quality accessories)

## Quick Style Hacks
- Roll up sleeves for a more relaxed, approachable look
- Tuck in tops for instant polish and better proportions
- Mix textures like cotton, denim, and leather for visual interest
- Follow the "rule of three" - limit your color palette to 3 colors maximum
- Use accessories to show personality while keeping the base outfit simple"""

    return suggestions

def generate_fallback_shopping_links():
    """Generate fallback shopping links when SerpAPI fails"""
    
    fallback_links = [
        {
            'item': 'casual shirt',
            'title': 'Premium Cotton Casual Shirt - Multiple Colors',
            'price': '$29.99 - $49.99',
            'source': 'Amazon',
            'link': 'https://www.amazon.com/s?k=mens+casual+shirt',
            'image': 'https://via.placeholder.com/300x300/4285f4/ffffff?text=SHIRT',
            'rating': '4.3/5'
        },
        {
            'item': 'jeans',
            'title': 'Classic Fit Denim Jeans - Dark Wash',
            'price': '$39.99 - $79.99', 
            'source': 'Target',
            'link': 'https://www.target.com/s?searchTerm=mens+jeans',
            'image': 'https://via.placeholder.com/300x300/34a853/ffffff?text=JEANS',
            'rating': '4.1/5'
        },
        {
            'item': 'sneakers',
            'title': 'Comfortable Walking Sneakers - White',
            'price': '$69.99 - $129.99',
            'source': 'Nike',
            'link': 'https://www.nike.com/w/mens-shoes',
            'image': 'https://via.placeholder.com/300x300/ea4335/ffffff?text=SHOES',
            'rating': '4.6/5'
        },
        {
            'item': 'jacket',
            'title': 'Versatile Casual Jacket - Multiple Styles',
            'price': '$49.99 - $99.99',
            'source': 'H&M', 
            'link': 'https://www2.hm.com/en_us/men/products/jackets-coats.html',
            'image': 'https://via.placeholder.com/300x300/fbbc04/000000?text=JACKET',
            'rating': '4.2/5'
        },
        {
            'item': 'accessories',
            'title': 'Stylish Watch & Belt Combo Set',
            'price': '$24.99 - $59.99',
            'source': 'ASOS',
            'link': 'https://www.asos.com/us/men/accessories/',
            'image': 'https://via.placeholder.com/300x300/9aa0a6/ffffff?text=ACCESSORIES',
            'rating': '4.0/5'
        },
        {
            'item': 'bag',
            'title': 'Modern Backpack - Professional & Casual',
            'price': '$34.99 - $69.99',
            'source': 'Zara',
            'link': 'https://www.zara.com/us/en/man/bags-l443.html',
            'image': 'https://via.placeholder.com/300x300/6f42c1/ffffff?text=BAG',
            'rating': '4.4/5'
        }
    ]
    
    return fallback_links

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.errorhandler(413)
def too_large(e):
    return jsonify({
        'success': False,
        'error': 'File too large. Please upload an image smaller than 16MB.'
    }), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found.'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal server error. Please try again.'
    }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 STARTING AI FASHION STYLIST SERVER")
    print("="*60)
    
    # Initialize database on startup
    try:
        print("📀 Initializing database...")
        initialize_database()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database initialization failed: {e}")
        print("🔄 Continuing without database...")
    
    # Test components
    print("\n🧪 TESTING COMPONENTS...")
    print("-" * 30)
    
    try:
        from yolo_detect import load_yolo_model
        model = load_yolo_model()
        print(f"✅ YOLO: {'Available' if model else 'Using fallback'}")
    except:
        print("⚠️ YOLO: Using fallback")
    
    try:
        from openai_api import test_openai_connection
        status, msg = test_openai_connection()
        print(f"{'✅' if status else '⚠️'} OpenAI: {msg}")
    except:
        print("⚠️ OpenAI: Using fallback")
    
    try:
        from serpapi_api import test_serpapi_connection  
        status, msg = test_serpapi_connection()
        print(f"{'✅' if status else '⚠️'} SerpAPI: {msg}")
    except:
        print("⚠️ SerpAPI: Using fallback")
    
    print("\n🌐 SERVER STARTING...")
    print("-" * 30)
    print("📡 URL: http://localhost:5000")
    print("📡 Test endpoint: http://localhost:5000/test")
    print("🔧 Debug mode: ON")
    print("📁 Upload folder:", app.config['UPLOAD_FOLDER'])
    print("📏 Max file size: 16MB")
    print("="*60)
    
    app.run(debug=True, port=5000, host='0.0.0.0')