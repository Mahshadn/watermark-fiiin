# Watermark-Fiiin

Simple watermarking service for n8n workflows. Adds social media handle and ID to images with customizable font, color, and position.

## Quick Start

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

## API Usage

### Endpoint: `POST /watermark`

**Required Parameters:**
- `image` (string): Base64 encoded image
- `social_handle` (string): Your social media handle (e.g., "@username")
- `id_code` (string): ID code for the image (e.g., "IMG-001")

**Optional Parameters:**
- `font_size` (int): Font size (default: 24)
- `font` (string): Font name (default: "DejaVuSans-Bold.ttf")
- `font_color` (string): Hex color (default: "#FFFFFF")
- `stroke_color` (string): Stroke color (default: "#000000")
- `stroke_width` (int): Stroke width (default: 2)
- `position` (string): Position on image (default: "bottom-right")
- `margin` (int): Margin from edges (default: 20)
- `opacity` (int): Text opacity 0-255 (default: 200)
- `format` (string): Output format "JPEG" or "PNG" (default: "JPEG")
- `quality` (int): JPEG quality 1-100 (default: 95)

**Position Options:**
- `top-left`, `top-center`, `top-right`
- `center-left`, `center`, `center-right`
- `bottom-left`, `bottom-center`, `bottom-right`

### Example Request
```json
{
  "image": "base64_encoded_image_here",
  "social_handle": "@myhandle",
  "id_code": "IMG-2025-001",
  "font_size": 28,
  "font_color": "#FF6B35",
  "position": "bottom-right",
  "margin": 25
}
```

### Example Response
```json
{
  "success": true,
  "image": "base64_encoded_watermarked_image",
  "metadata": {
    "social_handle": "@myhandle",
    "id_code": "IMG-2025-001",
    "position": "bottom-right",
    "font_size": 28,
    "format": "JPEG",
    "processed_at": "2025-05-28T00:45:21.123456"
  }
}
```

## n8n Integration

1. Use **HTTP Request** node
2. Set method to **POST**
3. Set URL to `http://watermark-fiiin:5000/watermark` (if using Docker network)
4. Or use `http://localhost:5000/watermark` (if running locally)
5. In the body, include your image as base64 and watermark parameters

### Sample n8n Function Node (to prepare request):
```javascript
// Convert binary image to base64
const imageBuffer = items[0].binary.data.data;
const base64Image = imageBuffer.toString('base64');

// Prepare watermark request
const requestData = {
  image: base64Image,
  social_handle: '@yourhandle',
  id_code: 'IMG-' + Date.now().toString().slice(-6),
  position: 'bottom-right',
  font_size: 24,
  font_color: '#FFFFFF'
};

return { json: requestData };
```

## Development

### Local Development (without Docker)
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

### Available Fonts
The service includes common system fonts:
- DejaVuSans-Bold.ttf (default)
- DejaVuSans.ttf
- LiberationSans-Bold.ttf
- Arial.ttf (Windows)
- Helvetica.ttc (macOS)

## Troubleshooting

- **Service not responding**: Check `docker-compose logs watermark-fiiin`
- **Font not found**: Use default fonts or check font availability
- **Large images**: Service handles most common image sizes
- **n8n connection**: Ensure both services are on same Docker network

## Security Note

This is a simple service for personal/internal use. For production use with external access, consider adding:
- API authentication
- Rate limiting
- Input validation
- HTTPS/TLS