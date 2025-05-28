from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os
from datetime import datetime

app = Flask(__name__)

# Simple configuration
DEFAULT_CONFIG = {
    'font_size': 24,
    'font_color': (255, 255, 255, 200),  # White with transparency
    'stroke_color': (0, 0, 0, 255),      # Black stroke
    'stroke_width': 2,
    'margin': 20
}

def load_font(font_name, size):
    """Load font with fallback options"""
    font_paths = [
        f"/usr/share/fonts/truetype/dejavu/{font_name}",
        f"/usr/share/fonts/truetype/liberation/{font_name}",
        f"/System/Library/Fonts/{font_name}",
        f"C:/Windows/Fonts/{font_name}"
    ]
    
    # Try to load custom font
    for path in font_paths:
        try:
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
        except:
            continue
    
    # Fallback to default font
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()

def hex_to_rgba(hex_color, alpha=255):
    """Convert hex color to RGBA tuple"""
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    if len(hex_color) == 6:
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (r, g, b, alpha)
    return (255, 255, 255, alpha)  # Default white

def add_single_watermark_text(draw, text, position, img_size, config):
    """Add a single watermark text at specified position"""
    # Get configuration
    font_size = config.get('font_size', DEFAULT_CONFIG['font_size'])
    font_name = config.get('font', 'DejaVuSans-Bold.ttf')
    margin = config.get('margin', DEFAULT_CONFIG['margin'])
    
    # Handle colors
    font_color = config.get('font_color', '#FFFFFF')
    if isinstance(font_color, str):
        font_color = hex_to_rgba(font_color, config.get('opacity', 200))
    
    stroke_color = config.get('stroke_color', '#000000')
    if isinstance(stroke_color, str):
        stroke_color = hex_to_rgba(stroke_color, 255)
    
    stroke_width = config.get('stroke_width', DEFAULT_CONFIG['stroke_width'])
    
    # Load font
    font = load_font(font_name, font_size)
    
    # Get text dimensions
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate position
    img_width, img_height = img_size
    
    positions = {
        'top-left': (margin, margin),
        'top-center': ((img_width - text_width) // 2, margin),
        'top-right': (img_width - text_width - margin, margin),
        'center-left': (margin, (img_height - text_height) // 2),
        'center': ((img_width - text_width) // 2, (img_height - text_height) // 2),
        'center-right': (img_width - text_width - margin, (img_height - text_height) // 2),
        'bottom-left': (margin, img_height - text_height - margin),
        'bottom-center': ((img_width - text_width) // 2, img_height - text_height - margin),
        'bottom-right': (img_width - text_width - margin, img_height - text_height - margin)
    }
    
    x, y = positions.get(position, positions['bottom-right'])
    
    # Draw watermark
    draw.text(
        (x, y), 
        text, 
        font=font, 
        fill=font_color,
        stroke_fill=stroke_color,
        stroke_width=stroke_width,
        align='left'
    )

def add_watermark(image, social_handle, id_code, config):
    """Add watermark to image - supports single or separate positioning"""
    img = image.copy()
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Check if separate positioning is requested
    handle_position = config.get('handle_position')
    id_position = config.get('id_position')
    
    if handle_position and id_position:
        # Add social handle and ID separately
        handle_config = config.copy()
        handle_config.update(config.get('handle_style', {}))
        
        id_config = config.copy()
        id_config.update(config.get('id_style', {}))
        
        add_single_watermark_text(draw, social_handle, handle_position, img.size, handle_config)
        add_single_watermark_text(draw, id_code, id_position, img.size, id_config)
    else:
        # Original combined watermark
        watermark_text = f"{social_handle}\n{id_code}"
        position = config.get('position', 'bottom-right')
        add_single_watermark_text(draw, watermark_text, position, img.size, config)
    
    return img

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'watermark-fiiin'})

@app.route('/watermark', methods=['POST'])
def watermark_image():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        if 'social_handle' not in data:
            return jsonify({'error': 'Social handle is required'}), 400
        
        if 'id_code' not in data:
            return jsonify({'error': 'ID code is required'}), 400
        
        # Decode base64 image
        try:
            image_data = base64.b64decode(data['image'])
            image = Image.open(io.BytesIO(image_data))
        except Exception as e:
            return jsonify({'error': f'Invalid image data: {str(e)}'}), 400
        
        # Get watermark parameters
        social_handle = data['social_handle']
        id_code = data['id_code']
        
        # Configuration from request
        config = {
            'font_size': data.get('font_size', 24),
            'font': data.get('font', 'DejaVuSans-Bold.ttf'),
            'font_color': data.get('font_color', '#FFFFFF'),
            'stroke_color': data.get('stroke_color', '#000000'),
            'stroke_width': data.get('stroke_width', 2),
            'position': data.get('position', 'bottom-right'),
            'margin': data.get('margin', 20),
            'opacity': data.get('opacity', 200),
            # New separate positioning options
            'handle_position': data.get('handle_position'),
            'id_position': data.get('id_position'),
            'handle_style': data.get('handle_style', {}),
            'id_style': data.get('id_style', {})
        }
        
        # Add watermark
        watermarked_image = add_watermark(image, social_handle, id_code, config)
        
        # Convert to output format
        output_format = data.get('format', 'JPEG').upper()
        
        # Handle RGBA to RGB conversion for JPEG
        if watermarked_image.mode in ('RGBA', 'P') and output_format == 'JPEG':
            rgb_image = Image.new('RGB', watermarked_image.size, (255, 255, 255))
            if watermarked_image.mode == 'P':
                watermarked_image = watermarked_image.convert('RGBA')
            rgb_image.paste(watermarked_image, mask=watermarked_image.split()[-1] if watermarked_image.mode == 'RGBA' else None)
            watermarked_image = rgb_image
        
        # Save to bytes
        img_byte_arr = io.BytesIO()
        quality = data.get('quality', 95)
        watermarked_image.save(img_byte_arr, format=output_format, quality=quality)
        img_byte_arr.seek(0)
        
        # Return base64 encoded image
        encoded_img = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image': encoded_img,
            'metadata': {
                'social_handle': social_handle,
                'id_code': id_code,
                'positions': {
                    'handle': config.get('handle_position', config.get('position')),
                    'id': config.get('id_position', config.get('position'))
                },
                'font_size': config['font_size'],
                'format': output_format,
                'processed_at': datetime.utcnow().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
