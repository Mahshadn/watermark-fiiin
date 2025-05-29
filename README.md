# Watermark-Fiiin

Simple watermarking service for n8n workflows with advanced features including percentage positioning, transparency control, and automatic font detection.

## 📁 Project Structure

```
watermark-fiiin/
├── app.py                  # Main Flask service
├── test_watermark.py       # Test & watermark your images  
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container setup
├── docker-compose.yml     # Easy deployment
├── README.md              # This file
└── .gitignore            # Git exclusions
```

## 🚀 Quick Start

### 1. Clone & Start Service
```bash
git clone https://github.com/Mahshadn/watermark-fiiin.git
cd watermark-fiiin
docker-compose up -d
```

### 2. Watermark Your Image
```bash
python test_watermark.py
```
Choose option 1, then edit the script to set your image filename and social handle.

## 🎯 How to Watermark Your Images

### Step 1: Put your image in the project folder
- Copy any JPG/PNG image to the `watermark-fiiin` folder
- Name it something simple like `my_photo.jpg`

### Step 2: Edit the test script
Open `test_watermark.py` and change these lines:
```python
IMAGE_FILE = "my_photo.jpg"           # Your image filename
SOCIAL_HANDLE = "@YourHandle"         # Your social media handle
ID_CODE = "IMG-001"                   # Your custom ID
```

### Step 3: Customize positioning and colors
```python
# Position using percentages (NEW!)
"handle_position": {"left": "5%", "bottom": "5%"},    # Handle position
"id_position": {"right": "5%", "top": "5%"},          # ID position

# Different styles for handle vs ID
"handle_style": {
    "font_color": "#FF6B35",      # Orange handle
    "font_size": 32,              # Larger font
    "transparency": 0.9           # 90% opacity (NEW!)
},
"id_style": {
    "font_color": "#FFFFFF",      # White ID
    "font_size": 20,              # Smaller font  
    "transparency": 0.8           # 80% opacity (NEW!)
}
```

### Step 4: Run it
```bash
python test_watermark.py
```
Choose option 1, and it creates `watermarked_my_photo.jpg`

## ✨ Features

### 🎯 **Positioning Options**
- **Named**: `"bottom-right"`, `"top-left"`, `"center"`, etc.
- **Percentage**: `{"left": "10%", "bottom": "5%"}` (NEW!)
- **Pixel**: `{"left": 50, "top": 30}`

### 👻 **Transparency Control** (NEW!)
- `"transparency": 1.0` - Fully opaque
- `"transparency": 0.8` - 80% opacity (recommended)
- `"transparency": 0.5` - 50% opacity (subtle)

### 🔤 **Font Support**
- **Windows**: Arial, Times New Roman, Calibri, etc.
- **Ubuntu**: DejaVu, Liberation fonts
- **Auto-detection**: Service finds all available fonts
- **Endpoint**: `GET /fonts` to list available fonts

### 🎨 **Color Options**
Use hex codes: `#FF0000` (red), `#00FF00` (green), `#0000FF` (blue), `#FFFFFF` (white), `#000000` (black), `#FF6B35` (orange)

## 📡 API Usage

### Main Endpoint: `POST /watermark`

**Basic Usage:**
```json
{
  "image": "base64_encoded_image",
  "social_handle": "@myhandle",
  "id_code": "IMG-001",
  "font_size": 24,
  "font_color": "#FFFFFF",
  "position": "bottom-right"
}
```

**Advanced Usage with New Features:**
```json
{
  "image": "base64_encoded_image",
  "social_handle": "@photographer",
  "id_code": "PHOTO-001",
  
  "handle_position": {"left": "5%", "bottom": "5%"},
  "id_position": {"right": "5%", "top": "5%"},
  
  "handle_style": {
    "font_color": "#FF6B35",
    "font_size": 32,
    "transparency": 0.9
  },
  "id_style": {
    "font_color": "#FFFFFF",
    "font_size": 20, 
    "transparency": 0.8
  }
}
```

### Other Endpoints:
- `GET /health` - Service status
- `GET /fonts` - List available fonts

## 🔗 n8n Integration

1. **HTTP Request Node**:
   - Method: POST
   - URL: `http://watermark-fiiin:5001/watermark` (Docker network)
   - Body: JSON with image (base64) + settings

2. **Function Node** (to prepare request):
```javascript
const imageBuffer = items[0].binary.data.data;
const base64Image = imageBuffer.toString('base64');

return { json: {
  image: base64Image,
  social_handle: '@yourhandle',
  id_code: 'IMG-' + Date.now().toString().slice(-6),
  handle_position: {left: "5%", bottom: "5%"},
  id_position: {right: "5%", top: "5%"},
  handle_style: {font_color: '#FF6B35', transparency: 0.9},
  id_style: {font_color: '#FFFFFF', transparency: 0.8}
}};
```

## 🛠️ Testing Options

Run `python test_watermark.py` and choose:

1. **Watermark my own image** - Main use (edit script first)
2. **Test transparency levels** - See different opacity examples  
3. **Test percentage positioning** - See positioning in action
4. **List available fonts** - See all fonts on your system
5. **Show configuration help** - Color codes and options

## 🔧 Troubleshooting

- **Service not starting**: `docker-compose down && docker-compose up -d`
- **Port conflicts**: Change `5001:5000` to `5002:5000` in docker-compose.yml
- **Image not found**: Put image file in same folder as scripts
- **Transparency not visible**: Use darker background images for testing

## 🚀 Production Deployment

### Deploy to Ubuntu VM:
```bash
git clone https://github.com/Mahshadn/watermark-fiiin.git
cd watermark-fiiin
docker-compose up -d
```

### Font Compatibility:
- **Development (Windows)**: Arial, Times, Calibri available
- **Production (Ubuntu)**: DejaVu, Liberation fonts available  
- **Recommended**: Use DejaVu fonts for cross-platform compatibility
- **Additional fonts**: `sudo apt install ttf-mscorefonts-installer`

---

**Ready to watermark?** Put your image in the folder, edit `test_watermark.py`, and run it! 🎨