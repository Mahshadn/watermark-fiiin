import requests
import base64
import os

def watermark_my_image():
    """Watermark your own image file"""
    
    # Configuration - Edit these values
    IMAGE_FILE = "your_image.jpg"  # Change this to your image file name
    SOCIAL_HANDLE = "@yourhandle"  # Change this to your social media handle
    ID_CODE = "MY-001"             # Change this to your desired ID
    
    # Watermark settings - Customize as needed
    FONT_SIZE = 30
    FONT_COLOR = "#FFFFFF"         # White text
    STROKE_COLOR = "#000000"       # Black stroke
    POSITION = "bottom-right"      # Options: top-left, top-center, top-right, center-left, center, center-right, bottom-left, bottom-center, bottom-right
    MARGIN = 25
    
    # Check if image file exists
    if not os.path.exists(IMAGE_FILE):
        print(f"❌ Image file '{IMAGE_FILE}' not found!")
        print("📁 Put your image file in the same folder as this script")
        print("🔧 Or change the IMAGE_FILE variable above to match your file name")
        return
    
    print(f"📸 Reading image: {IMAGE_FILE}")
    
    # Read and encode image
    try:
        with open(IMAGE_FILE, "rb") as f:
            image_data = f.read()
        image_b64 = base64.b64encode(image_data).decode()
        print("✅ Image loaded successfully")
    except Exception as e:
        print(f"❌ Error reading image: {e}")
        return
    
    # Prepare watermark request
    watermark_data = {
        "image": image_b64,
        "social_handle": SOCIAL_HANDLE,
        "id_code": ID_CODE,
        "font_size": FONT_SIZE,
        "font_color": FONT_COLOR,
        "stroke_color": STROKE_COLOR,
        "position": POSITION,
        "margin": MARGIN
    }
    
    print(f"🎨 Adding watermark: {SOCIAL_HANDLE} | {ID_CODE}")
    
    try:
        # Send request to watermark service
        response = requests.post("http://localhost:5001/watermark", json=watermark_data)
        
        if response.status_code == 200:
            result = response.json()
            
            # Save watermarked image
            output_filename = f"watermarked_{IMAGE_FILE}"
            watermarked_data = base64.b64decode(result["image"])
            
            with open(output_filename, "wb") as f:
                f.write(watermarked_data)
            
            print("🎉 Success!")
            print(f"💾 Watermarked image saved as: {output_filename}")
            print(f"📋 Details:")
            print(f"   - Social Handle: {result['metadata']['social_handle']}")
            print(f"   - ID Code: {result['metadata']['id_code']}")
            print(f"   - Position: {result['metadata']['position']}")
            print(f"   - Font Size: {result['metadata']['font_size']}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to watermark service!")
        print("🔧 Make sure the service is running: docker-compose up -d")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_different_positions():
    """Test watermark in different positions using a test image"""
    print("🧪 Testing different watermark positions...")
    
    # Create a simple test image
    from PIL import Image
    import io
    
    # Create test image
    img = Image.new('RGB', (600, 400), color='lightblue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    test_image_b64 = base64.b64encode(img_byte_arr.getvalue()).decode()
    
    positions = ['top-left', 'top-center', 'top-right', 
                'center-left', 'center', 'center-right',
                'bottom-left', 'bottom-center', 'bottom-right']
    
    for position in positions:
        try:
            response = requests.post("http://localhost:5001/watermark", json={
                "image": test_image_b64,
                "social_handle": "@test",
                "id_code": "POS-TEST",
                "position": position,
                "font_size": 20
            })
            
            if response.status_code == 200:
                result = response.json()
                filename = f"test_{position.replace('-', '_')}.jpg"
                with open(filename, "wb") as f:
                    f.write(base64.b64decode(result["image"]))
                print(f"✅ {position}: {filename}")
            else:
                print(f"❌ {position}: Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ {position}: {e}")

if __name__ == "__main__":
    print("🏷️  Personal Image Watermarker")
    print("=" * 50)
    
    choice = input("\nChoose an option:\n1. Watermark my own image\n2. Test different positions\nEnter 1 or 2: ")
    
    if choice == "1":
        watermark_my_image()
    elif choice == "2":
        test_different_positions()
    else:
        print("Invalid choice. Running default watermark test...")
        watermark_my_image()
    
    print("\n🎯 Ready for n8n: http://localhost:5001/watermark")
