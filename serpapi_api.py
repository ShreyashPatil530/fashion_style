import requests
import os
from dotenv import load_dotenv
import random

load_dotenv()

SERPAPI_KEY = os.getenv('SERPAPI_KEY')

def get_shopping_links(detected_items):
    """
    Fetch shopping links for detected clothing items using SerpAPI
    """
    print(f"Getting shopping links for {len(detected_items)} items...")
    
    shopping_results = []
    
    for item in detected_items:
        try:
            # Limit to avoid too many API calls
            if len(shopping_results) >= 6:  # Max 6 shopping items
                break
                
            # Search for the clothing item
            search_query = f"{item['item']} buy online"
            print(f"Searching for: {search_query}")
            
            links = search_product(search_query, item)
            
            if links:
                shopping_results.extend(links[:2])  # Max 2 per item
                print(f"Added {len(links)} links for {item['item']}")
            else:
                # Add fallback links if API fails
                print(f"API failed for {item['item']}, using fallback")
                fallback_links = generate_fallback_shopping_links(item)
                shopping_results.extend(fallback_links[:2])
                
        except Exception as e:
            print(f"Error fetching shopping links for {item['item']}: {e}")
            # Add fallback links
            fallback_links = generate_fallback_shopping_links(item)
            shopping_results.extend(fallback_links[:1])  # Just 1 fallback per failed item
    
    # If no results at all, generate some basic ones
    if not shopping_results:
        shopping_results = generate_basic_shopping_links()
    
    print(f"Total shopping links: {len(shopping_results)}")
    return shopping_results

def search_product(query, item_info):
    """Search for product using SerpAPI Google Shopping"""
    try:
        if not SERPAPI_KEY or SERPAPI_KEY.strip() == '':
            print("No SerpAPI key found, skipping API call")
            return []
        
        url = "https://serpapi.com/search"
        params = {
            "engine": "google_shopping",
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": 3,  # Limit to 3 results per item
            "hl": "en",
            "gl": "us"
        }
        
        print(f"Making SerpAPI request for: {query}")
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            shopping_results = data.get('shopping_results', [])
            
            if not shopping_results:
                print("No shopping results found in API response")
                return []
            
            links = []
            for result in shopping_results[:2]:  # Take top 2 results
                try:
                    link_info = {
                        'item': item_info['item'],
                        'title': result.get('title', 'Fashion Item')[:80],  # Truncate long titles
                        'price': result.get('price', 'Check price'),
                        'source': result.get('source', 'Online Store'),
                        'link': result.get('link', '#'),
                        'image': result.get('thumbnail', ''),
                        'rating': result.get('rating', 'No rating')
                    }
                    
                    # Validate the link
                    if link_info['link'] and link_info['link'] != '#':
                        links.append(link_info)
                        print(f"Added product: {link_info['title'][:50]}...")
                    
                except Exception as parse_error:
                    print(f"Error parsing result: {parse_error}")
                    continue
            
            return links
            
        else:
            print(f"SerpAPI request failed: {response.status_code}")
            return []
            
    except requests.exceptions.Timeout:
        print("SerpAPI request timed out")
        return []
    except requests.exceptions.RequestException as e:
        print(f"SerpAPI request error: {e}")
        return []
    except Exception as e:
        print(f"Error in SerpAPI search: {e}")
        return []

def generate_fallback_shopping_links(item_info):
    """Generate fallback shopping links when SerpAPI fails"""
    
    item_name = item_info['item']
    color = item_info['color']
    category = item_info['category']
    
    # Popular fashion retailers with proper search URLs
    stores = [
        {
            'name': 'Amazon',
            'base_url': 'https://www.amazon.com/s?k=',
            'price_range': '$15-$50'
        },
        {
            'name': 'Zara',
            'base_url': 'https://www.zara.com/us/en/search?searchTerm=',
            'price_range': '$25-$80'
        },
        {
            'name': 'H&M',
            'base_url': 'https://www2.hm.com/en_us/search-results.html?q=',
            'price_range': '$10-$40'
        },
        {
            'name': 'ASOS',
            'base_url': 'https://www.asos.com/us/search/?q=',
            'price_range': '$20-$100'
        },
        {
            'name': 'Target',
            'base_url': 'https://www.target.com/s?searchTerm=',
            'price_range': '$8-$35'
        }
    ]
    
    fallback_links = []
    
    # Select 2-3 random stores
    selected_stores = random.sample(stores, min(3, len(stores)))
    
    for store in selected_stores:
        # Create search term
        search_term = item_name.replace(' ', '+')
        
        link_info = {
            'item': item_name,
            'title': f"{color.title()} {category.title()} - {store['name']}",
            'price': store['price_range'],
            'source': store['name'],
            'link': store['base_url'] + search_term,
            'image': get_placeholder_image(category),
            'rating': f"{random.uniform(3.5, 4.8):.1f}/5"
        }
        fallback_links.append(link_info)
    
    return fallback_links

def generate_basic_shopping_links():
    """Generate basic shopping links when everything else fails"""
    basic_links = [
        {
            'item': 'clothing',
            'title': 'Trendy Casual Shirt - Amazon',
            'price': '$19.99 - $39.99',
            'source': 'Amazon',
            'link': 'https://www.amazon.com/s?k=casual+shirt',
            'image': get_placeholder_image('top'),
            'rating': '4.2/5'
        },
        {
            'item': 'pants',
            'title': 'Comfortable Jeans - Target',
            'price': '$24.99 - $49.99',
            'source': 'Target',
            'link': 'https://www.target.com/s?searchTerm=jeans',
            'image': get_placeholder_image('bottom'),
            'rating': '4.0/5'
        },
        {
            'item': 'shoes',
            'title': 'Stylish Sneakers - Nike',
            'price': '$79.99 - $129.99',
            'source': 'Nike',
            'link': 'https://www.nike.com/w/shoes',
            'image': get_placeholder_image('footwear'),
            'rating': '4.5/5'
        }
    ]
    
    return basic_links

def get_placeholder_image(category):
    """Get placeholder image URL based on category"""
    placeholder_images = {
        'top': 'https://via.placeholder.com/200x200/4285f4/ffffff?text=TOP',
        'bottom': 'https://via.placeholder.com/200x200/34a853/ffffff?text=BOTTOM',
        'footwear': 'https://via.placeholder.com/200x200/ea4335/ffffff?text=SHOES',
        'accessory': 'https://via.placeholder.com/200x200/fbbc04/000000?text=ACCESSORY',
        'clothing': 'https://via.placeholder.com/200x200/9aa0a6/ffffff?text=FASHION',
        'other': 'https://via.placeholder.com/200x200/9aa0a6/ffffff?text=FASHION'
    }
    
    return placeholder_images.get(category, placeholder_images['other'])

def format_shopping_results(shopping_results):
    """Format shopping results for frontend display"""
    formatted_results = []
    
    for result in shopping_results:
        # Clean and validate data
        formatted_result = {
            'title': str(result.get('title', 'Fashion Item'))[:100],  # Limit title length
            'price': str(result.get('price', 'Check price')),
            'store': str(result.get('source', 'Online Store')),
            'url': str(result.get('link', '#')),
            'image': str(result.get('image', get_placeholder_image('other'))),
            'rating': str(result.get('rating', 'No rating'))
        }
        
        # Ensure we have valid data
        if formatted_result['title'] and formatted_result['url'] != '#':
            formatted_results.append(formatted_result)
    
    return formatted_results

def test_serpapi_connection():
    """Test SerpAPI connection"""
    try:
        if not SERPAPI_KEY or SERPAPI_KEY.strip() == '':
            return False, "No SerpAPI key found in environment"
        
        # Simple test call
        url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": "test",
            "api_key": SERPAPI_KEY,
            "num": 1
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            return True, "SerpAPI working"
        else:
            return False, f"SerpAPI returned status {response.status_code}"
            
    except Exception as e:
        return False, f"SerpAPI error: {str(e)}"

if __name__ == "__main__":
    # Test the SerpAPI connection
    status, message = test_serpapi_connection()
    print(f"SerpAPI Status: {status} - {message}")
    
    # Test with sample items
    sample_items = [
        {'item': 'blue shirt', 'category': 'top', 'color': 'blue'},
        {'item': 'jeans', 'category': 'bottom', 'color': 'blue'}
    ]
    
    links = get_shopping_links(sample_items)
    print(f"\nSample shopping links: {len(links)}")
    for link in links[:2]:
        print(f"- {link['title']} at {link['source']}")