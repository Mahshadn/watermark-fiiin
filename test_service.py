import requests
import base64
import json
from PIL import Image
import io

def create_test_image():
    """Create a simple test image"""
    # Create a simple 400x300 test image
    img = Image.new('RGB', (400, 300), color='lightblue')
    
    # Save to base64
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

def test_watermark_service():
    """Test the watermark service"""
    # Service URL - Updated for port 5001
    url = "http://localhost:5001/watermark"
    
    # Create test image
    test_image_b64 = create_test_image()
    
    # Test data
    test_data = {
        "image": test_image_b64,
        "social_handle": "@testuser",
        "id_code": "TEST-001",
        "font_size": 28,
        "font_color": "#FF6B35",
        "position": "bottom-right",
        "margin": 20
    }
    
    try:
        # Make request
        response = requests.post(url, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Watermark service is working!")
            print(f"Social Handle: {result['metadata']['social_handle']}")
            print(f"ID Code: {result['metadata']['id_code']}")
            print(f"Position: {result['metadata']['position']}")
            print(f"Font Size: {result['metadata']['font_size']}")
            
            # Save the watermarked image
            watermarked_image_data = base64.b64decode(result['image'])
            with open('test_watermarked_output.jpg', 'wb') as f:
                f.write(watermarked_image_data)
            print("💾 Watermarked image saved as 'test_watermarked_output.jpg'")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to service. Make sure it's running on localhost:5001")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:5001/health")
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(response.json())
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Watermark Service...")
    print("="*50)
    
    # Test health endpoint first
    print("1. Testing health endpoint...")
    test_health_endpoint()
    
    print("\n2. Testing watermark functionality...")
    test_watermark_service()
    
    print("\n🎉 Test completed!")
    print("🚀 Service ready for n8n at: http://localhost:5001/watermark")
