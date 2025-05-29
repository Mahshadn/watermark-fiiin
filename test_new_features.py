import requests
import base64
import os
from PIL import Image
import io

def test_percentage_positioning():
    """Test new percentage positioning feature"""
    
    # Create a test image
    img = Image.new('RGB', (800, 600), color='lightblue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    test_image_b64 = base64.b64encode(img_byte_arr.getvalue()).decode()
    
    print("🎯 Testing percentage positioning...")
    
    # Test 1: Percentage positioning
    response = requests.post("http://localhost:5001/watermark", json={
        "image": test_image_b64,
        "social_handle": "@photographer",
        "id_code": "PERCENT-001",
        
        # Percentage positioning - 10% from left, 5% from bottom
        "handle_position": {"left": "10%", "bottom": "5%"},
        "id_position": {"right": "10%", "top": "5%"},
        
        "handle_style": {
            "font_color": "#FF6B35",
            "font_size": 28,
            "transparency": 0.8  # 80% opacity
        },
        "id_style": {
            "font_color": "#0066CC", 
            "font_size": 20,
            "transparency": 0.9  # 90% opacity
        }
    })
    
    if response.status_code == 200:
        with open("test_percentage.jpg", "wb") as f:
            f.write(base64.b64decode(response.json()["image"]))
        print("✅ Percentage positioning: test_percentage.jpg")
    else:
        print(f"❌ Error: {response.text}")

def test_transparency_levels():
    """Test different transparency levels"""
    
    img = Image.new('RGB', (600, 400), color='darkblue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    test_image_b64 = base64.b64encode(img_byte_arr.getvalue()).decode()
    
    print("👻 Testing transparency levels...")
    
    transparencies = [1.0, 0.8, 0.6, 0.4, 0.2]
    
    for i, transparency in enumerate(transparencies):
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

def list_available_fonts():
    """List all available fonts on the system"""
    
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
                    for font in fonts[:5]:  # Show first 5 of each category
                        print(f"    • {font}")
                    if len(fonts) > 5:
                        print(f"    ... and {len(fonts)-5} more")
            
            return fonts_data['fonts']['all']
        else:
            print(f"❌ Error getting fonts: {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def test_different_fonts():
    """Test different font combinations"""
    
    fonts = list_available_fonts()
    if not fonts:
        print("❌ No fonts available for testing")
        return
    
    # Create test image
    img = Image.new('RGB', (700, 500), color='lightgray')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    test_image_b64 = base64.b64encode(img_byte_arr.getvalue()).decode()
    
    print("\n🎨 Testing different fonts...")
    
    # Test a few different fonts
    test_fonts = []
    for font in fonts:
        if any(name in font.lower() for name in ['arial', 'dejavu', 'liberation', 'times']):
            test_fonts.append(font)
        if len(test_fonts) >= 3:
            break
    
    if not test_fonts:
        test_fonts = fonts[:3]  # Just take first 3 if no preferred fonts found
    
    for i, font in enumerate(test_fonts):
        response = requests.post("http://localhost:5001/watermark", json={
            "image": test_image_b64,
            "social_handle": "@fonttest",
            "id_code": f"FONT-{i+1}",
            "position": "center",
            "font": font,
            "font_size": 24,
            "font_color": "#000000"
        })
        
        if response.status_code == 200:
            filename = f"font_test_{font.replace('.', '_')}.jpg"
            with open(filename, "wb") as f:
                f.write(base64.b64decode(response.json()["image"]))
            print(f"✅ Font {font}: {filename}")

def advanced_watermark_demo():
    """Demo of all advanced features combined"""
    
    # Check if user has an image
    IMAGE_FILE = "demo_image.jpg"
    
    if not os.path.exists(IMAGE_FILE):
        # Create a demo image
        print("📸 Creating demo image...")
        img = Image.new('RGB', (900, 600), color='#2E86AB')
        # Add some simple graphics to make it more interesting
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.rectangle([100, 100, 800, 500], fill='#A23B72')
        draw.ellipse([200, 150, 700, 450], fill='#F18F01')
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        test_image_b64 = base64.b64encode(img_byte_arr.getvalue()).decode()
    else:
        with open(IMAGE_FILE, "rb") as f:
            test_image_b64 = base64.b64encode(f.read()).decode()
    
    print("🚀 Creating advanced watermark demo...")
    
    response = requests.post("http://localhost:5001/watermark", json={
        "image": test_image_b64,
        "social_handle": "@MyAwesomeHandle",
        "id_code": "DEMO-2025-001",
        
        # Advanced positioning: Handle top-left with percentage, ID bottom-right with percentage
        "handle_position": {"left": "5%", "top": "5%"},
        "id_position": {"right": "5%", "bottom": "5%"},
        
        # Different styles for each
        "handle_style": {
            "font_color": "#FFFFFF",
            "font_size": 36,
            "font": "DejaVuSans-Bold.ttf",
            "stroke_color": "#000000",
            "stroke_width": 3,
            "transparency": 0.9
        },
        "id_style": {
            "font_color": "#FFD700",  # Gold color
            "font_size": 24,
            "font": "DejaVuSans.ttf",
            "stroke_color": "#8B0000",  # Dark red
            "stroke_width": 2,
            "transparency": 0.85
        }
    })
    
    if response.status_code == 200:
        with open("advanced_demo.jpg", "wb") as f:
            f.write(base64.b64decode(response.json()["image"]))
        print("✅ Advanced demo created: advanced_demo.jpg")
        print("📋 Features used:")
        print("  • Percentage positioning (5% from edges)")
        print("  • Different fonts for handle vs ID")
        print("  • Different colors and transparency levels")
        print("  • Custom stroke colors and widths")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    print("🎨 Advanced Watermark Features Test")
    print("=" * 50)
    
    print("\nChoose an option:")
    print("1. Test percentage positioning")
    print("2. Test transparency levels")
    print("3. List available fonts")
    print("4. Test different fonts")
    print("5. Advanced demo (all features)")
    print("6. Run all tests")
    
    choice = input("\nEnter 1-6: ").strip()
    
    if choice == "1":
        test_percentage_positioning()
    elif choice == "2":
        test_transparency_levels()
    elif choice == "3":
        list_available_fonts()
    elif choice == "4":
        test_different_fonts()
    elif choice == "5":
        advanced_watermark_demo()
    elif choice == "6":
        print("🔄 Running all tests...")
        test_percentage_positioning()
        print()
        test_transparency_levels()
        print()
        list_available_fonts()
        print()
        test_different_fonts()
        print()
        advanced_watermark_demo()
    else:
        print("Invalid choice. Running advanced demo...")
        advanced_watermark_demo()
    
    print("\n🎯 New Features Available:")
    print("✅ Percentage positioning: {'left': '10%', 'bottom': '5%'}")
    print("✅ Transparency control: 'transparency': 0.8 (80% opacity)")
    print("✅ All system fonts detected automatically")
    print("✅ Font endpoint: GET /fonts to list available fonts")
    print("\n🚀 Service ready at: http://localhost:5001/watermark")
