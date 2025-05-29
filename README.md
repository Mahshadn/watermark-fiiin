# Watermark-Fiiin

Advanced watermarking service for n8n workflows. Adds social media handle and ID to images with extensive customization options including percentage positioning, transparency control, and automatic system font detection.

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Mahshadn/watermark-fiiin.git
cd watermark-fiiin
```

### 2. Run with Docker
```bash
docker-compose up -d
```

### 3. Test the Service
```bash
curl http://localhost:5000/health
```

## 🎯 New Advanced Features

### ✨ Percentage Positioning
Position watermarks using percentages relative to image size:
```json
{
  "handle_position": {"left": "10%", "bottom": "5%"},
  "id_position": {"right": "10%", "top": "5%"}
}
```

### 👻 Transparency Control
Control watermark opacity independently:
```json
{
  "transparency": 0.8,  // 80% opacity
  "handle_style": {"transparency": 0.9},
  "id_style": {"transparency": 0.7}
}
```

### 🔤 Automatic Font Detection
Service automatically detects all system fonts:
- **Windows**: C:/Windows/Fonts/
- **Ubuntu/Linux**: /usr/share/fonts/
- **macOS**: /System/Library/Fonts/

## 📡 API Endpoints

### `POST /watermark` - Main Watermarking

**Required Parameters:**
- `image` (string): Base64 encoded image
- `social_handle` (string): Your social media handle (e.g., "@username")
- `id_code` (string): ID code for the image (e.g., "IMG-001")

**Basic Parameters:**
- `font_size` (int): Font size (default: 24)
- `font` (string): Font filename (default: "DejaVuSans-Bold.ttf")
- `font_color` (string): Hex color (default: "#FFFFFF")
- `stroke_color` (string): Stroke color (default: "#000000")
- `stroke_width` (int): Stroke width (default: 2)
- `transparency` (float): Overall transparency 0.0-1.0 (default: 1.0)
- `margin` (int): Margin from edges (default: 20)
- `format` (string): Output format "JPEG" or "PNG" (default: "JPEG")
- `quality` (int): JPEG quality 1-100 (default: 95)

**Positioning Options:**

*Named Positions:*
- `position`: `"top-left"`, `"top-center"`, `"top-right"`, `"center-left"`, `"center"`, `"center-right"`, `"bottom-left"`, `"bottom-center"`, `"bottom-right"`

*Percentage Positioning:*
```json
{
  "handle_position": {"left": "5%", "bottom": "10%"},
  "id_position": {"right": "5%", "top": "10%"}
}
```

*Pixel Positioning:*
```json
{
  "handle_position": {"left": 50, "bottom": 30},
  "id_position": {"right": 50, "top": 30}
}
```

**Separate Styling:**
```json
{
  "handle_style": {
    "font_color": "#FF6B35",
    "font_size": 32,
    "font": "Arial.ttf",
    "transparency": 0.9
  },
  "id_style": {
    "font_color": "#0066CC",
    "font_size": 20,
    "font": "DejaVuSans.ttf",
    "transparency": 0.8
  }
}
```

### `GET /fonts` - List Available Fonts

Returns all system fonts categorized by type:
```json
{
  "total_fonts": 147,
  "fonts": {
    "all": ["Arial.ttf", "DejaVuSans-Bold.ttf", ...],
    "categorized": {
      "serif": ["Times.ttf", "Georgia.ttf", ...],
      "sans_serif": ["Arial.ttf", "Helvetica.ttc", ...],
      "monospace": ["Courier.ttf", "Monaco.ttf", ...]
    }
  },
  "recommended": ["DejaVuSans-Bold.ttf", "Arial.ttf", ...]
}
```

### `GET /health` - Health Check

Returns service status.

## 📋 Usage Examples

### Basic Watermark
```json
{
  "image": "base64_encoded_image_here",
  "social_handle": "@myhandle",
  "id_code": "IMG-2025-001",
  "font_size": 28,
  "font_color": "#FF6B35",
  "position": "bottom-right"
}
```

### Advanced Separate Positioning
```json
{
  "image": "base64_encoded_image_here",
  "social_handle": "@photographer",
  "id_code": "PHOTO-001",
  
  "handle_position": {"left": "5%", "bottom": "5%"},
  "id_position": {"right": "5%", "top": "5%"},
  
  "handle_style": {
    "font_color": "#FFFFFF",
    "font_size": 32,
    "font": "Arial.ttf",
    "stroke_color": "#000000",
    "stroke_width": 3,
    "transparency": 0.9
  },
  "id_style": {
    "font_color": "#FFD700",
    "font_size": 20,
    "font": "DejaVuSans.ttf",
    "transparency": 0.8
  }
}
```

## 🧪 Testing

### Test New Features
```bash
git pull
docker-compose down && docker-compose build --no-cache && docker-compose up -d
python test_new_features.py
```

### Test Your Own Images
```bash
python my_watermark_test.py
```

### Basic Functionality Test
```bash
python test_service.py
```

## 🔗 n8n Integration

### Sample n8n Function Node:
```javascript
// Convert binary image to base64
const imageBuffer = items[0].binary.data.data;
const base64Image = imageBuffer.toString('base64');

// Advanced watermark request
const requestData = {
  image: base64Image,
  social_handle: '@yourhandle',
  id_code: 'IMG-' + Date.now().toString().slice(-6),
  
  // Use percentage positioning
  handle_position: {left: "5%", bottom: "5%"},
  id_position: {right: "5%", top: "5%"},
  
  // Different styles
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
};

return { json: requestData };
```

**n8n HTTP Request Node:**
- **Method:** POST
- **URL:** `http://watermark-fiiin:5001/watermark` (Docker network) or `http://localhost:5001/watermark`
- **Body:** Use the output from Function Node above

## 🖥️ Font Compatibility

### Windows → Ubuntu VM Deployment

**On Windows (Development):**
- Fonts: Arial, Times New Roman, Calibri, etc.
- Test with: `python test_new_features.py` → option 3

**On Ubuntu VM (Production):**
- Default fonts: DejaVu family, Liberation family
- Additional fonts: Install with `apt install fonts-*`
- Recommended: Install Microsoft fonts: `apt install ttf-mscorefonts-installer`

**Best Practice:**
- Use DejaVu fonts for cross-platform compatibility
- Test font availability with `GET /fonts` endpoint
- Fallback to default font if specified font not found

## 🛠️ Development

### Local Development (without Docker)
```bash
pip install -r requirements.txt
python app.py
```

### Available System Fonts
The service automatically detects fonts from:
- `/usr/share/fonts/` (Linux)
- `C:/Windows/Fonts/` (Windows)
- `/System/Library/Fonts/` (macOS)

## 🔧 Troubleshooting

### Common Issues:
- **Port conflicts**: Change port in docker-compose.yml from 5001:5000
- **Font not found**: Use `GET /fonts` to see available fonts
- **Large images**: Service handles most sizes, larger images take more time
- **Docker network**: Ensure n8n and watermark service use same network

### Performance Tips:
- Use JPEG for smaller files, PNG for transparency
- Reduce image size before watermarking for faster processing
- Lower quality setting (80-90) for faster processing

## 🚀 Production Deployment

### VM Deployment:
```bash
git clone https://github.com/Mahshadn/watermark-fiiin.git
cd watermark-fiiin
docker-compose up -d
```

### Scaling Considerations:
- Add nginx reverse proxy for multiple instances
- Use Docker Swarm or Kubernetes for high availability
- Consider Redis caching for repeated watermarks
- Monitor memory usage with large images

## 📝 Security Note

This service is designed for internal/personal use. For production with external access, consider adding:
- API authentication (JWT tokens)
- Rate limiting 
- Input validation and sanitization
- HTTPS/TLS termination
- Request size limits

---

## 🎨 Color Reference

**Popular Colors:**
- `#FF0000` - Red
- `#00FF00` - Green  
- `#0000FF` - Blue
- `#FFFF00` - Yellow
- `#FF6B35` - Orange
- `#800080` - Purple
- `#FFFFFF` - White
- `#000000` - Black
- `#FFD700` - Gold

**Transparency Values:**
- `1.0` - Fully opaque
- `0.8` - 80% opacity (recommended)
- `0.5` - 50% opacity (subtle)
- `0.2` - 20% opacity (very subtle)
