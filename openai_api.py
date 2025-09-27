import os
from dotenv import load_dotenv

load_dotenv()

# Try to import OpenAI with fallback
try:
    import openai
    OPENAI_AVAILABLE = True
    # Set up OpenAI API
    openai.api_key = os.getenv('OPENAI_API_KEY')
    print("OpenAI imported successfully")
except ImportError as e:
    print(f"OpenAI import failed: {e}")
    OPENAI_AVAILABLE = False

def get_outfit_suggestions(detected_items):
    """
    Generate outfit suggestions based on detected clothing items using OpenAI GPT-4
    """
    print("Getting outfit suggestions...")
    print(f"Detected items: {detected_items}")
    
    try:
        if not OPENAI_AVAILABLE:
            print("OpenAI not available, using fallback suggestions")
            return generate_fallback_suggestions(detected_items)
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key or api_key.strip() == '':
            print("No OpenAI API key found, using fallback")
            return generate_fallback_suggestions(detected_items)
        
        # Format detected items for the prompt
        items_text = []
        for item in detected_items:
            items_text.append(f"- {item['item']} ({item['category']}, {item['color']} color)")
        
        items_string = "\n".join(items_text)
        
        prompt = f"""
You are a professional fashion stylist. Based on the following detected clothing items, provide styling suggestions and outfit recommendations.

Detected Items:
{items_string}

Please provide practical fashion advice in the following format:

## Style Analysis
Brief analysis of the current style and color palette.

## Outfit Suggestions
### Outfit 1: [Style Name]
- Specific recommendations

### Outfit 2: [Style Name] 
- Specific recommendations

### Outfit 3: [Style Name]
- Specific recommendations

## Styling Tips
- Practical advice for improving the look
- Color coordination tips
- Accessory recommendations

## Occasion Recommendations
What occasions these outfits would be suitable for.

Keep the response practical, fashionable, and helpful. Focus on actionable advice.
"""

        try:
            # Try the newer OpenAI API format first
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use GPT-3.5 as fallback, more reliable
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a professional fashion stylist with expertise in color coordination, style trends, and outfit planning. Provide practical, actionable fashion advice."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            suggestions = response.choices[0].message.content.strip()
            print(f"OpenAI suggestions length: {len(suggestions)}")
            return suggestions
            
        except Exception as api_error:
            print(f"OpenAI API call failed: {api_error}")
            # Try with different model or approach
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f"As a fashion stylist, provide outfit suggestions for these items:\n{items_string}\n\nSuggestions:",
                    max_tokens=500,
                    temperature=0.7
                )
                return response.choices[0].text.strip()
            except Exception as backup_error:
                print(f"Backup OpenAI API also failed: {backup_error}")
                return generate_fallback_suggestions(detected_items)
        
    except Exception as e:
        print(f"Error getting OpenAI suggestions: {e}")
        return generate_fallback_suggestions(detected_items)

def generate_fallback_suggestions(detected_items):
    """Generate fallback suggestions when OpenAI API fails"""
    
    print("Generating fallback suggestions...")
    
    # Analyze detected items
    has_top = any(item['category'] == 'top' for item in detected_items)
    has_bottom = any(item['category'] == 'bottom' for item in detected_items)
    has_footwear = any(item['category'] == 'footwear' for item in detected_items)
    
    colors = [item['color'] for item in detected_items]
    main_color = colors[0] if colors else 'neutral'
    
    # Get item names for personalization
    item_names = [item['item'] for item in detected_items]
    top_items = [item['item'] for item in detected_items if item['category'] == 'top']
    bottom_items = [item['item'] for item in detected_items if item['category'] == 'bottom']
    
    suggestions = f"""
## Style Analysis
Your outfit features {main_color} tones with a versatile mix of pieces. The detected items include {', '.join(item_names[:3])}{"..." if len(item_names) > 3 else ""}, which creates a solid foundation for multiple styling options.

## Outfit Suggestions

### Outfit 1: Smart Casual
- Keep your current {top_items[0] if top_items else 'top'} as the centerpiece
- Pair with {bottom_items[0] if bottom_items else 'well-fitted pants'}
- Add a structured blazer or cardigan for polish
- Complete with loafers or clean sneakers
- Accessorize with a classic watch and minimal jewelry

### Outfit 2: Weekend Relaxed
- Layer your {main_color} pieces for comfort
- Add a cozy hoodie or casual jacket
- Choose comfortable denim or joggers
- Finish with your favorite sneakers
- Include a casual cap or beanie for extra style

### Outfit 3: Date Night Ready
- Elevate your look with darker, more fitted pieces
- Pair {main_color} items with black or navy accents
- Add sophisticated accessories like a leather belt
- Choose dress shoes or stylish boots
- Consider a nice watch or subtle jewelry

## Styling Tips
- **Fit is King**: Ensure all pieces fit well - tailoring makes a huge difference
- **Color Harmony**: Your {main_color} base pairs beautifully with neutrals like white, black, gray, and navy
- **Layer Smart**: Use layers to add depth and adjust for different occasions
- **Accessories Matter**: A good belt, watch, or bag can elevate any outfit
- **Balance Proportions**: Mix fitted and relaxed pieces for visual interest

## Color Coordination
- **Primary Palette**: Build around your {main_color} foundation
- **Complementary Colors**: Add white, black, or gray for classic looks
- **Pop of Color**: Introduce one accent color through accessories
- **Seasonal Adjustments**: Lighter shades for spring/summer, deeper tones for fall/winter

## Occasion Recommendations
**Perfect for:**
- Casual coffee dates and weekend brunches
- Shopping trips and casual meetups with friends
- Work-from-home video calls
- Relaxed office environments
- Casual family gatherings

**Level Up for:**
- Date nights (add blazer and dress shoes)
- Business casual events (structured pieces and accessories)
- Social events (layer with interesting textures)

## Quick Styling Hacks
- **Roll up sleeves** on shirts for a more relaxed vibe
- **Tuck in tops** for a more polished look
- **Mix textures** like denim with cotton or leather accessories
- **Use the rule of three** - keep your color palette to 3 colors max
- **Invest in basics** - quality white tees, good jeans, and versatile shoes go with everything
"""
    
    return suggestions

def test_openai_connection():
    """Test OpenAI API connection"""
    try:
        if not OPENAI_AVAILABLE:
            return False, "OpenAI library not installed"
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return False, "No API key found in environment"
        
        # Simple test call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API working' if you can read this."}],
            max_tokens=10
        )
        
        return True, "OpenAI API working"
        
    except Exception as e:
        return False, f"OpenAI API error: {str(e)}"

if __name__ == "__main__":
    # Test the OpenAI connection
    status, message = test_openai_connection()
    print(f"OpenAI Status: {status} - {message}")
    
    # Test with sample items
    sample_items = [
        {'item': 'blue shirt', 'category': 'top', 'color': 'blue'},
        {'item': 'jeans', 'category': 'bottom', 'color': 'blue'}
    ]
    
    suggestions = get_outfit_suggestions(sample_items)
    print(f"\nSample suggestions length: {len(suggestions)}")
    print(suggestions[:200] + "..." if len(suggestions) > 200 else suggestions)