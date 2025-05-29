# 🏷️ Watermark-Fiiin

A powerful, easy-to-use watermarking service designed for **n8n workflows** and **content creators**. Add your social media handle and custom IDs to images with advanced positioning, transparency control, and automatic font detection.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-supported-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)

## 🎯 What This Does

This service takes any image and adds watermarks to it. Perfect for:
- **Content creators** marking their photos/videos with social handles
- **n8n automation workflows** that process images at scale  
- **Agencies** adding client IDs to deliverables
- **Anyone** who needs to brand their visual content

**Before & After Example:**
```
Original Image → [API Call] → Watermarked Image
                              ├─ @YourHandle (bottom-left, orange, 90% opacity)
                              └─ IMG-001 (top-right, white, 80% opacity)
```

## ✨ Key Features

### 🎯 **Advanced Positioning**
- **Named positions**: `"bottom-right"`, `"center"`, `"top-left"`, etc.
- **Percentage positioning**: `{"left": "10%", "bottom": "5%"}` - positions relative to image size
- **Pixel-perfect**: `{"left": 50, "top": 30}` - exact coordinates
- **Separate positioning**: Put handle and ID in completely different locations

### 👻 **Transparency Control**
- Full opacity control from 0% to 100%
- Different transparency for handle vs ID
- Proper alpha blending that actually works
- Example: Handle at 90% opacity, ID at 60% opacity

### 🔤 **Smart Font Detection**
- **Windows**: Automatically finds Arial, Times New Roman, Calibri, etc.
- **Ubuntu/Linux**: Finds DejaVu, Liberation, Ubuntu fonts
- **macOS**: Detects Helvetica, San Francisco, etc.
- **Fallback**: If specified font not found, uses best available alternative
- **API endpoint**: `GET /fonts` lists all available fonts on your system

### 🎨 **Full Customization**
- Any hex color (`#FF0000`, `#00FF00`, etc.)
- Font sizes from tiny to huge
- Stroke/outline colors and widths  
- Different styles for handle vs ID
- Support for JPEG and PNG output

## 🚀 Quick Start (5 Minutes)

### 1. Get It Running
```bash
# Clone the repository
git clone https://github.com/Mahshadn/watermark-fiiin.git
cd watermark-fiiin

# Start the service (requires Docker)
docker-compose up -d

# Test it's working
curl http://localhost:5001/health
```

### 2. Watermark Your First Image
```bash
# Put any image file in the project folder (jpg, png, etc.)
# Then run the test script
python test_watermark.py
```

Choose option 1, then edit the script to set your image filename and social handle.

### 3. Customize Your Watermark
Open `test_watermark.py` and edit these settings:
```python
# Basic settings
IMAGE_FILE = "your_image.jpg"           # Your image filename
SOCIAL_HANDLE = "@YourHandle"           # Your social media handle
ID_CODE = "IMG-001"                     # Your custom ID

# Advanced positioning (NEW!)
"handle_position": {"left": "5%", "bottom": "5%"},    # Handle position
"id_position": {"right": "5%", "top": "5%"},          # ID position

# Different styles for each
"handle_style": {
    "font_color": "#FF6B35",      # Orange
    "font_size": 32,              # Larger
    "transparency": 0.9           # 90% opacity
},
"id_style": {
    "font_color": "#FFFFFF",      # White
    "font_size": 20,              # Smaller
    "transparency": 0.8           # 80% opacity
}
```

## 📁 Project Structure

```
watermark-fiiin/
├── 🔧 app.py                  # Main Flask service (the brain)
├── 🧪 test_watermark.py       # Test & watermark your images (YOUR MAIN FILE)
├── 📦 requirements.txt        # Python dependencies
├── 🐳 Dockerfile             # Container setup
├── 🐳 docker-compose.yml     # Easy deployment
├── 📖 README.md              # This documentation
└── 🚫 .gitignore            # Git exclusions
```

**For most users**: You only need to edit `test_watermark.py`!

## 📡 API Reference

### Core Endpoint: `POST /watermark`

The main endpoint that does all the watermarking magic.

#### Basic Example
```json
{
  "image": "base64_encoded_image_data",
  "social_handle": "@photographer",
  "id_code": "PHOTO-001",
  "font_size": 24,
  "font_color": "#FFFFFF",
  "position": "bottom-right"
}
```

#### Advanced Example (All Features)
```json
{
  "image": "base64_encoded_image_data",
  "social_handle": "@photographer",
  "id_code": "PHOTO-001",
  
  "handle_position": {"left": "5%", "bottom": "5%"},
  "id_position": {"right": "5%", "top": "5%"},
  
  "handle_style": {
    "font_color": "#FF6B35",
    "font_size": 32,
    "font": "Arial.ttf",
    "stroke_color": "#FFFFFF",
    "stroke_width": 3,
    "transparency": 0.9
  },
  "id_style": {
    "font_color": "#FFFFFF",
    "font_size": 20,
    "font": "DejaVuSans.ttf",
    "stroke_color": "#000000", 
    "stroke_width": 2,
    "transparency": 0.8
  },
  
  "format": "JPEG",
  "quality": 95
}
```

#### Response Format
```json
{
  "success": true,
  "image": "base64_encoded_watermarked_image",
  "metadata": {
    "social_handle": "@photographer",
    "id_code": "PHOTO-001",
    "positions": {
      "handle": {"left": "5%", "bottom": "5%"},
      "id": {"right": "5%", "top": "5%"}
    },
    "transparency": 0.9,
    "format": "JPEG",
    "processed_at": "2025-05-29T00:30:15.123456"
  }
}
```

### Utility Endpoints

#### `GET /health`
Check if the service is running.
```json
{"status": "healthy", "service": "watermark-fiiin"}
```

#### `GET /fonts`
List all available fonts on the system.
```json
{
  "total_fonts": 147,
  "fonts": {
    "all": ["Arial.ttf", "DejaVuSans-Bold.ttf", ...],
    "categorized": {
      "serif": ["Times.ttf", "Georgia.ttf"],
      "sans_serif": ["Arial.ttf", "Helvetica.ttc"],
      "monospace": ["Courier.ttf", "Monaco.ttf"]
    }
  },
  "recommended": ["DejaVuSans-Bold.ttf", "Arial.ttf"]
}
```

## 🔗 n8n Integration

Perfect for automating image watermarking in n8n workflows.

### Setup in n8n:

1. **HTTP Request Node**:
   - Method: `POST`
   - URL: `http://watermark-fiiin:5001/watermark` (if using Docker network)
   - URL: `http://localhost:5001/watermark` (if running locally)

2. **Function Node** (prepare the request):
```javascript
// Convert n8n binary data to base64
const imageBuffer = items[0].binary.data.data;
const base64Image = imageBuffer.toString('base64');

// Generate unique ID
const idCode = 'IMG-' + Date.now().toString().slice(-6);

// Return watermark request
return { json: {
  image: base64Image,
  social_handle: '@yourhandle',        // ← Change this
  id_code: idCode,
  
  // Use advanced positioning
  handle_position: {left: "5%", bottom: "5%"},
  id_position: {right: "5%", top: "5%"},
  
  // Custom styling
  handle_style: {
    font_color: '#FF6B35',
    font_size: 28,
    transparency: 0.9
  },
  id_style: {
    font_color: '#FFFFFF',
    font_size: 18,
    transparency: 0.8
  }
}};
```

3. **Process Response** (another Function Node):
```javascript
// Convert base64 back to binary for saving/uploading
const base64Image = items[0].json.image;
const imageBuffer = Buffer.from(base64Image, 'base64');

return {
  json: items[0].json.metadata,
  binary: {
    data: {
      data: imageBuffer,
      mimeType: 'image/jpeg',
      fileName: `watermarked_${items[0].json.metadata.id_code}.jpg`
    }
  }
};
```

## 🎨 Configuration Guide

### Color Reference
Use hex color codes for any color:
```
#FF0000 = Red        #00FF00 = Green      #0000FF = Blue
#FFFF00 = Yellow     #FF6B35 = Orange     #800080 = Purple  
#FFFFFF = White      #000000 = Black      #808080 = Gray
#FFD700 = Gold       #C0C0C0 = Silver     #FFC0CB = Pink
```

### Positioning Options

#### Named Positions (Simple)
```
"position": "top-left"      "position": "top-center"      "position": "top-right"
"position": "center-left"   "position": "center"          "position": "center-right"  
"position": "bottom-left"   "position": "bottom-center"   "position": "bottom-right"
```

#### Percentage Positioning (Flexible)
```json
{"left": "10%", "bottom": "5%"}     // 10% from left, 5% from bottom
{"right": "15%", "top": "8%"}       // 15% from right, 8% from top
{"left": "50%", "top": "50%"}       // Centered using percentages
```

#### Pixel Positioning (Precise)
```json
{"left": 50, "bottom": 30}          // 50px from left, 30px from bottom
{"right": 100, "top": 40}           // 100px from right, 40px from top
```

### Transparency Guide
```
1.0 = Fully opaque (solid)
0.9 = 90% opacity (barely see-through)
0.8 = 80% opacity (recommended for most cases)
0.6 = 60% opacity (noticeably transparent)
0.4 = 40% opacity (quite transparent)
0.2 = 20% opacity (very subtle)
0.0 = Fully transparent (invisible)
```

### Font Recommendations

#### Cross-Platform (work everywhere):
- `DejaVuSans-Bold.ttf` - Bold, clean, always available
- `DejaVuSans.ttf` - Regular weight, very readable

#### Windows:
- `arial.ttf` - Clean, professional
- `times.ttf` - Classic, serif style

#### macOS:
- `Helvetica.ttc` - Clean, modern
- `Arial.ttf` - Cross-platform reliable

## 🛠️ Testing & Development

### Available Test Options
Run `python test_watermark.py` and choose from:

1. **Watermark my own image** - Main use case (edit the script first)
2. **Test transparency levels** - Creates images showing different opacity levels  
3. **Test percentage positioning** - Demonstrates positioning capabilities
4. **List available fonts** - Shows all fonts detected on your system
5. **Show configuration help** - Quick reference for colors, positions, etc.

### Local Development
```bash
# Run without Docker (for development)
pip install -r requirements.txt
python app.py

# Service will be available at http://localhost:5000
```

### Custom Test Script
You can also create your own test script:
```python
import requests
import base64

# Read your image
with open("my_image.jpg", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()

# Watermark it
response = requests.post("http://localhost:5001/watermark", json={
    "image": image_b64,
    "social_handle": "@myhandle",
    "id_code": "CUSTOM-001",
    "handle_position": {"left": "5%", "bottom": "5%"},
    "id_position": {"right": "5%", "top": "5%"},
    "handle_style": {"font_color": "#FF0000", "transparency": 0.8},
    "id_style": {"font_color": "#0000FF", "transparency": 0.9}
})

# Save result
if response.status_code == 200:
    result = response.json()
    with open("watermarked_output.jpg", "wb") as f:
        f.write(base64.b64decode(result["image"]))
    print("Watermarked image saved!")
```

## 🚀 Production Deployment

### Deploy to Ubuntu VM
```bash
# On your Ubuntu server
git clone https://github.com/Mahshadn/watermark-fiiin.git
cd watermark-fiiin
docker-compose up -d

# Service will be available at http://your-server-ip:5001
```

### Font Considerations
- **Development (Windows)**: Arial, Times, Calibri automatically detected
- **Production (Ubuntu)**: DejaVu, Liberation fonts available by default
- **Add more fonts**: `sudo apt install ttf-mscorefonts-installer fonts-powerline`
- **Check available fonts**: Visit `http://your-server:5001/fonts`

### Performance & Scaling
- **Memory usage**: ~50MB per container
- **Processing speed**: ~1-2 seconds per image (depending on size)
- **Concurrent requests**: Handles multiple requests simultaneously
- **File size limits**: Supports images up to ~50MB (base64 encoded)

### Security Notes
This service is designed for internal/trusted use. For public deployment, consider:
- Adding API authentication (JWT tokens)
- Rate limiting (nginx or API gateway)
- Input validation and file size limits
- HTTPS/TLS termination
- Network isolation (VPC/firewall rules)

## 🔧 Troubleshooting

### Common Issues & Solutions

**Service won't start:**
```bash
docker-compose down
docker-compose up -d
# Check logs: docker-compose logs watermark-fiiin
```

**Port already in use:**
Edit `docker-compose.yml`, change `5001:5000` to `5002:5000`

**Image not found error:**
- Ensure image file is in the same folder as `test_watermark.py`
- Check filename matches exactly (case-sensitive)
- Supported formats: JPG, JPEG, PNG, BMP, TIFF

**Transparency not visible:**
- Use darker background images for testing
- Try extreme values like `0.2` vs `1.0` to see difference
- Ensure you rebuilt container: `docker-compose build --no-cache`

**Font not found:**
- Run `python test_watermark.py` → option 4 to see available fonts
- Use recommended fonts: `DejaVuSans-Bold.ttf` or `DejaVuSans.ttf`
- On Ubuntu: `sudo apt install fonts-dejavu-core`

**n8n can't connect:**
- Ensure both services on same Docker network
- Use service name in URL: `http://watermark-fiiin:5001/watermark`
- Check network: `docker network ls`

## 🤝 Contributing

This project is designed to be simple and focused. If you want to contribute:

1. Fork the repository
2. Create a feature branch
3. Test your changes with `test_watermark.py`
4. Submit a pull request

**Ideas for contributions:**
- Additional image formats support
- Batch processing endpoint
- Image resize before watermarking
- Custom font upload feature
- Background/shadow effects
- Image watermarks (logos)

## 📄 License

MIT License - feel free to use this in your own projects!

## 💡 Use Cases & Examples

### Content Creator Workflow
```
Take photo → Upload to n8n → Auto-watermark with handle → Post to social media
```

### Agency Client Work  
```
Design mockup → Add client ID → Send for approval → Remove watermark when paid
```

### Batch Processing
```
Photo shoot (100 images) → Bulk watermark → Deliver to client
```

### E-commerce
```
Product photos → Add store branding → Upload to marketplace
```

---

**Ready to start watermarking?** 
1. `git clone https://github.com/Mahshadn/watermark-fiiin.git`
2. `cd watermark-fiiin && docker-compose up -d`  
3. `python test_watermark.py`

**Questions?** Check the troubleshooting section or create an issue on GitHub!

🎨 **Happy watermarking!**