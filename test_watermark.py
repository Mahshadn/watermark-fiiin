import requests
import base64
import os
from PIL import Image
import io

def watermark_my_image():
    """Watermark your own image with all new features"""
    
    # Configuration - EDIT THESE VALUES
    IMAGE_FILE = "your_image.jpg"          # ← Change this to your image filename
    SOCIAL_HANDLE = "@YourHandle"          # ← Change this to your social media handle  
    ID_CODE = "IMG-001"                    # ← Change this to your desired ID
    
    # Check if image exists
    if not os.path.exists(IMAGE_FILE):
        print(f"❌ Image file '{IMAGE_FILE}' not found!")
        print(f"📁 Put your image in this folder and update IMAGE_FILE variable")
        return
    
    print(f"📸 Processing: {IMAGE_FILE}")
    
    # Read and encode image
    with open(IMAGE_FILE, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()
    
    # Watermark configuration with new features
    watermark_data = {
        "image": image_b64,
        "social_handle": SOCIAL_HANDLE,
        "id_code": ID_CODE,
        
        # NEW: Separate positioning with percentages
        "handle_position": {"left": "5%", "bottom": "5%"},    # Handle bottom-left
        "id_position": {"right": "5%", "top": "5%"},          # ID top-right
        
        # NEW: Different styles for each
        "handle_style": {
            "font_color": "#FF6B35",      # Orange
            "font_size": 32,              # Larger
            "font": "DejaVuSans-Bold.ttf",
            "stroke_color": "#FFFFFF",    # White stroke
            "stroke_width": 3,
            "transparency": 0.9           # NEW: 90% opacity
        },
        "id_style": {
            "font_color": "#FFFFFF",      # White  
            "font_size": 20,              # Smaller
            "font": "DejaVuSans.ttf",
            "stroke_color": "#000000",    # Black stroke
            "stroke_width": 2,
            "transparency": 0.8           # NEW: 80% opacity
        }
    }
    
    try:
        response = requests.post("http://localhost:5001/watermark", json=watermark_data)
        
        if response.status_code == 200:
            result = response.json()
            output_file = f"watermarked_{IMAGE_FILE}"
            
            with open(output_file, "wb") as f:
                f.write(base64.b64decode(result["image"]))
            
            print("🎉 Success!")
            print(f"💾 Saved as: {output_file}")
            print(f"📋 Handle: {result['metadata']['social_handle']} at {result['metadata']['positions']['handle']}")
            print(f"📋 ID: {result['metadata']['id_code']} at {result['metadata']['positions']['id']}")
            
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_transparency_levels():
    """Test different transparency levels"""
    img = Image.new('RGB', (600, 400), color='darkblue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    test_image_b64 = base64.b64encode(img_byte_arr.getvalue()).decode()
    
    print("👻 Testing transparency levels...")
    
    transparencies = [1.0, 0.8, 0.6, 0.4, 0.2]
    
    for transparency in transparencies:
        response = requests.post("http://localhost:5001/watermark", json={
            "image": test_image_b64,
            "social_handle": "@test",
            "id_code": f"T-{int(transparency*100)}",
            "position": "center",
            "font_size": 32,
            "font_color": "#FFFFFF",
            "transparency": transparency
        })
        
        if response.status_code == 200:
            filename = f"transparency_{int(transparency*100)}.jpg"
            with open(filename, "wb") as f:
                f.write(base64.b64decode(response.json()["image"]))
            print(f"✅ {int(transparency*100)}% opacity: {filename}")

def test_percentage_positioning():
    """Test percentage positioning"""
    img = Image.new('RGB', (800, 600), color='lightblue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    test_image_b64 = base64.b64encode(img_byte_arr.getvalue()).decode()
    
    print("🎯 Testing percentage positioning...")
    
    response = requests.post("http://localhost:5001/watermark", json={
        "image": test_image_b64,
        "social_handle": "@photographer",
        "id_code": "PERCENT-001",
        
        # Percentage positioning
        "handle_position": {"left": "10%", "bottom": "5%"},
        "id_position": {"right": "10%", "top": "5%"},
        
        "handle_style": {
            "font_color": "#FF6B35",
            "font_size": 28,
            "transparency": 0.8
        },
        "id_style": {
            "font_color": "#0066CC", 
            "font_size": 20,
            "transparency": 0.9
        }
    })
    
    if response.status_code == 200:
        with open("test_percentage.jpg", "wb") as f:
            f.write(base64.b64decode(response.json()["image"]))
        print("✅ Percentage positioning: test_percentage.jpg")

def list_available_fonts():
    """List all available fonts"""
    print("🔤 Available fonts on this system:")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:5001/fonts")
        if response.status_code == 200:
            fonts_data = response.json()
            
            print(f"📊 Total fonts found: {fonts_data['total_fonts']}")
            print("\n🎯 Recommended fonts:")
            for font in fonts_data['recommended']:
                print(f"  • {font}")
            
            print("\n📂 Fonts by category:")
            for category, fonts in fonts_data['fonts']['categorized'].items():
                if fonts:
                    print(f"\n  {category.upper()}:")
                    for font in fonts[:5]:  # Show first 5
                        print(f"    • {font}")
                    if len(fonts) > 5:
                        print(f"    ... and {len(fonts)-5} more")
            
            return fonts_data['fonts']['all']
        else:
            print(f"❌ Error: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def show_help():
    """Show help with configuration options"""
    print("🎨 Configuration Help")
    print("=" * 50)
    print("\n📍 POSITIONING OPTIONS:")
    print("  Percentage: {'left': '10%', 'bottom': '5%'}")
    print("  Pixel: {'left': 50, 'bottom': 30}")
    print("  Named: 'top-left', 'center', 'bottom-right', etc.")
    
    print("\n🎨 COLOR OPTIONS (hex codes):")
    print("  #FF0000 = Red      #00FF00 = Green")
    print("  #0000FF = Blue     #FFFF00 = Yellow") 
    print("  #FF6B35 = Orange   #800080 = Purple")
    print("  #FFFFFF = White    #000000 = Black")
    
    print("\n👻 TRANSPARENCY:")
    print("  1.0 = Fully opaque (solid)")
    print("  0.8 = 80% opacity (recommended)")
    print("  0.5 = 50% opacity (subtle)")
    print("  0.2 = 20% opacity (very faint)")
    
    print("\n🔤 FONTS:")
    print("  Run option 4 to see all available fonts")
    print("  Recommended: DejaVuSans-Bold.ttf, Arial.ttf")

if __name__ == "__main__":
    print("🎯 Watermark Service - All Features")
    print("=" * 50)
    
    print("\nWhat do you want to do?")
    print("1. Watermark my own image (MAIN USE)")
    print("2. Test transparency levels") 
    print("3. Test percentage positioning")
    print("4. List available fonts")
    print("5. Show configuration help")
    
    choice = input("\nEnter 1-5: ").strip()
    
    if choice == "1":
        print("\n🖼️  WATERMARK YOUR IMAGE")
        print("=" * 30)
        print("Edit the script to change:")
        print("- IMAGE_FILE = 'your_image.jpg'")
        print("- SOCIAL_HANDLE = '@YourHandle'") 
        print("- ID_CODE = 'IMG-001'")
        print("- Colors, positions, transparency")
        print()
        watermark_my_image()
    elif choice == "2":
        test_transparency_levels()
    elif choice == "3":
        test_percentage_positioning()
    elif choice == "4":
        list_available_fonts()
    elif choice == "5":
        show_help()
    else:
        print("Invalid choice. Running main watermark function...")
        watermark_my_image()
    
    print(f"\n🚀 Service URL: http://localhost:5001/watermark")
    print("📖 Edit this script to customize your watermark settings!")
