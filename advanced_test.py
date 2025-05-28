import requests
import base64
import os
from PIL import Image
import io

def test_separate_positioning():
    """Test putting handle and ID in different positions with different styles"""
    
    # Create a test image
    img = Image.new('RGB', (600, 400), color='lightblue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    test_image_b64 = base64.b64encode(img_byte_arr.getvalue()).decode()
    
    # Example 1: Handle top-left, ID bottom-right, different colors
    print("🎨 Test 1: Handle top-left (red), ID bottom-right (blue)")
    response = requests.post("http://localhost:5001/watermark", json={
        "image": test_image_b64,
        "social_handle": "@myhandle",
        "id_code": "IMG-2025-001",
        
        # Separate positions
        "handle_position": "top-left",
        "id_position": "bottom-right",
        
        # Different styles for each
        "handle_style": {
            "font_color": "#FF0000",      # Red
            "font_size": 24,
            "font": "DejaVuSans-Bold.ttf"
        },
        "id_style": {
            "font_color": "#0000FF",      # Blue  
            "font_size": 18,
            "font": "DejaVuSans.ttf"
        }
    })
    
    if response.status_code == 200:
        with open("test_separate_1.jpg", "wb") as f:
            f.write(base64.b64decode(response.json()["image"]))
        print("✅ Saved as test_separate_1.jpg")
    
    # Example 2: Handle bottom-left, ID top-right, different fonts
    print("🎨 Test 2: Handle bottom-left (white), ID top-right (yellow)")
    response = requests.post("http://localhost:5001/watermark", json={
        "image": test_image_b64,
        "social_handle": "@photographer",
        "id_code": "PHOTO-001",
        
        "handle_position": "bottom-left",
        "id_position": "top-right",
        
        "handle_style": {
            "font_color": "#FFFFFF",      # White
            "font_size": 28,
            "stroke_color": "#000000",    # Black stroke
            "stroke_width": 3
        },
        "id_style": {
            "font_color": "#FFFF00",      # Yellow
            "font_size": 16,
            "stroke_color": "#800080",    # Purple stroke
            "stroke_width": 2
        }
    })
    
    if response.status_code == 200:
        with open("test_separate_2.jpg", "wb") as f:
            f.write(base64.b64decode(response.json()["image"]))
        print("✅ Saved as test_separate_2.jpg")

def watermark_my_image_advanced():
    """Advanced watermarking with separate positioning"""
    
    IMAGE_FILE = "your_image.jpg"  # Change this
    
    if not os.path.exists(IMAGE_FILE):
        print(f"❌ Put your image file '{IMAGE_FILE}' in this folder first!")
        return
    
    # Read image
    with open(IMAGE_FILE, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()
    
    print("🎨 Creating advanced watermark...")
    
    # Advanced configuration
    watermark_data = {
        "image": image_b64,
        "social_handle": "@yourhandle",           # Change this
        "id_code": "CUSTOM-001",                  # Change this
        
        # Separate positions
        "handle_position": "bottom-left",         # Handle position
        "id_position": "bottom-right",            # ID position
        
        # Handle styling (your social media handle)
        "handle_style": {
            "font_color": "#FF6B35",              # Orange
            "font_size": 32,                      # Larger font
            "stroke_color": "#FFFFFF",            # White stroke
            "stroke_width": 3,
            "font": "DejaVuSans-Bold.ttf"        # Bold font
        },
        
        # ID styling (image identifier)
        "id_style": {
            "font_color": "#FFFFFF",              # White
            "font_size": 20,                      # Smaller font
            "stroke_color": "#000000",            # Black stroke
            "stroke_width": 2,
            "font": "DejaVuSans.ttf"             # Regular font
        }
    }
    
    try:
        response = requests.post("http://localhost:5001/watermark", json=watermark_data)
        
        if response.status_code == 200:
            result = response.json()
            output_file = f"advanced_watermarked_{IMAGE_FILE}"
            
            with open(output_file, "wb") as f:
                f.write(base64.b64decode(result["image"]))
            
            print("🎉 Success!")
            print(f"💾 Saved as: {output_file}")
            print(f"📋 Handle position: {result['metadata']['positions']['handle']}")
            print(f"📋 ID position: {result['metadata']['positions']['id']}")
            
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def show_color_examples():
    """Show different color options"""
    print("🎨 Available color options:")
    print("Colors (use hex codes):")
    print("  #FF0000 = Red")
    print("  #00FF00 = Green") 
    print("  #0000FF = Blue")
    print("  #FFFF00 = Yellow")
    print("  #FF6B35 = Orange")
    print("  #800080 = Purple")
    print("  #FFFFFF = White")
    print("  #000000 = Black")
    print("  #808080 = Gray")
    print()
    print("Fonts available:")
    print("  DejaVuSans-Bold.ttf (default, bold)")
    print("  DejaVuSans.ttf (regular)")
    print("  LiberationSans-Bold.ttf (if available)")
    print()
    print("Positions:")
    print("  top-left, top-center, top-right")
    print("  center-left, center, center-right") 
    print("  bottom-left, bottom-center, bottom-right")

if __name__ == "__main__":
    print("🎯 Advanced Watermark Testing")
    print("=" * 50)
    
    print("\nChoose an option:")
    print("1. Test separate positioning (creates demo images)")
    print("2. Watermark my own image with advanced settings")
    print("3. Show color and font options")
    
    choice = input("\nEnter 1, 2, or 3: ").strip()
    
    if choice == "1":
        test_separate_positioning()
    elif choice == "2":
        watermark_my_image_advanced()
    elif choice == "3":
        show_color_examples()
    else:
        print("Invalid choice. Running demo...")
        test_separate_positioning()
    
    print("\n🚀 Service ready at: http://localhost:5001/watermark")
