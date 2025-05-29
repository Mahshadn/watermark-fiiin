from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import os
import glob
from datetime import datetime

app = Flask(__name__)

# Simple configuration
DEFAULT_CONFIG = {
    'font_size': 24,
    'font_color': (255, 255, 255, 200),  # White with transparency
    'stroke_color': (0, 0, 0, 255),      # Black stroke
    'stroke_width': 2,
    'margin': 20,
    'transparency': 1.0  # Full opacity
}

def get_system_fonts():
    """Get all available system fonts"""
    font_paths = []
    font_dirs = [
        "/usr/share/fonts/",           # Linux/Ubuntu
        "/System/Library/Fonts/",      # macOS
        "C:/Windows/Fonts/",           # Windows
        "/usr/share/fonts/truetype/",  # Ubuntu truetype
        "/usr/share/fonts/opentype/",  # Ubuntu opentype
    ]
    
    fonts = {}
    for font_dir in font_dirs:
        if os.path.exists(font_dir):
            for root, dirs, files in os.walk(font_dir):
                for file in files:
                    if file.lower().endswith(('.ttf', '.otf', '.ttc')):
                        full_path = os.path.join(root, file)
                        fonts[file] = full_path
    
    return fonts

def load_font(font_name, size):
    """Load font with automatic system font detection"""
    available_fonts = get_system_fonts()
    
    # Try exact match first
    if font_name in available_fonts:
        try:
            return ImageFont.truetype(available_fonts[font_name], size)
        except:
            pass
    
    # Try partial match (case insensitive)
    for font_file, font_path in available_fonts.items():
        if font_name.lower() in font_file.lower():
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    
    # Fallback fonts in order of preference
    fallback_fonts = [
        "DejaVuSans-Bold.ttf", "DejaVuSans.ttf",
        "arial.ttf", "Arial.ttf", "ARIAL.TTF",
        "helvetica.ttc", "Helvetica.ttc",
        "LiberationSans-Bold.ttf", "LiberationSans.ttf"
    ]
    
    for fallback in fallback_fonts:
        if fallback in available_fonts:
            try:
                return ImageFont.truetype(available_fonts[fallback], size)
            except:
                continue
    
    # Ultimate fallback
    return ImageFont.load_default()

def hex_to_rgba(hex_color, alpha=255):
    """Convert hex color to RGBA tuple"""
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    if len(hex_color) == 6:
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (r, g, b, alpha)
    return (255, 255, 255, alpha)  # Default white

def parse_position(position_config, img_size, text_size, margin=20):
    """Parse position - supports both named positions and percentage positioning"""
    img_width, img_height = img_size
    text_width, text_height = text_size
    
    # Handle percentage positioning
    if isinstance(position_config, dict):
        x = margin
        y = margin
        
        # Parse left/right positioning
        if 'left' in position_config:
            if isinstance(position_config['left'], str) and position_config['left'].endswith('%'):
                x = int((float(position_config['left'][:-1]) / 100) * img_width)
            else:
                x = int(position_config['left'])
        elif 'right' in position_config:
            if isinstance(position_config['right'], str) and position_config['right'].endswith('%'):
                x = img_width - int((float(position_config['right'][:-1]) / 100) * img_width) - text_width
            else:
                x = img_width - int(position_config['right']) - text_width
        
        # Parse top/bottom positioning
        if 'top' in position_config:
            if isinstance(position_config['top'], str) and position_config['top'].endswith('%'):
                y = int((float(position_config['top'][:-1]) / 100) * img_height)
            else:
                y = int(position_config['top'])
        elif 'bottom' in position_config:
            if isinstance(position_config['bottom'], str) and position_config['bottom'].endswith('%'):
                y = img_height - int((float(position_config['bottom'][:-1]) / 100) * img_height) - text_height
            else:
                y = img_height - int(position_config['bottom']) - text_height
        
        return (x, y)
    
    # Handle named positions (existing functionality)
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
    
    return positions.get(position_config, positions['bottom-right'])

def create_text_overlay(text, position_config, img_size, config):
    """Create a transparent text overlay that can be blended with main image"""
    img_width, img_height = img_size
    
    # Get configuration
    font_size = config.get('font_size', DEFAULT_CONFIG['font_size'])
    font_name = config.get('font', 'DejaVuSans-Bold.ttf')
    margin = config.get('margin', DEFAULT_CONFIG['margin'])
    transparency = config.get('transparency', DEFAULT_CONFIG['transparency'])
    
    # Handle colors - full opacity for the overlay, transparency applied later
    font_color = config.get('font_color', '#FFFFFF')
    if isinstance(font_color, str):
        font_color = hex_to_rgba(font_color, 255)  # Full opacity initially
    
    stroke_color = config.get('stroke_color', '#000000')
    if isinstance(stroke_color, str):
        stroke_color = hex_to_rgba(stroke_color, 255)  # Full opacity initially
    
    stroke_width = config.get('stroke_width', DEFAULT_CONFIG['stroke_width'])
    
    # Load font
    font = load_font(font_name, font_size)
    
    # Create a transparent overlay the same size as the main image
    overlay = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Get text dimensions
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Parse position
    x, y = parse_position(position_config, img_size, (text_width, text_height), margin)
    
    # Ensure text stays within image bounds
    x = max(0, min(x, img_width - text_width))
    y = max(0, min(y, img_height - text_height))
    
    # Draw text on overlay with full opacity
    draw.text(
        (x, y), 
        text, 
        font=font, 
        fill=font_color,
        stroke_fill=stroke_color,
        stroke_width=stroke_width,
        align='left'
    )
    
    # Apply transparency to the entire overlay
    if transparency < 1.0:
        # Create alpha mask
        alpha = overlay.split()[-1]  # Get alpha channel
        alpha = alpha.point(lambda p: int(p * transparency))  # Apply transparency
        overlay.putalpha(alpha)
    
    return overlay

def add_single_watermark_text(img, text, position_config, config):
    """Add a single watermark text using proper transparency blending"""
    # Create text overlay
    overlay = create_text_overlay(text, position_config, img.size, config)
    
    # Blend overlay with main image
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Composite the overlay onto the main image
    img = Image.alpha_composite(img, overlay)
    
    return img

def add_watermark(image, social_handle, id_code, config):
    """Add watermark to image - supports single or separate positioning with proper transparency"""
    img = image.copy()
    
    # Ensure image is in RGBA mode for transparency support
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Check if separate positioning is requested
    handle_position = config.get('handle_position')
    id_position = config.get('id_position')
    
    if handle_position and id_position:
        # Add social handle and ID separately
        handle_config = config.copy()
        handle_config.update(config.get('handle_style', {}))
        
        id_config = config.copy()
        id_config.update(config.get('id_style', {}))
        
        img = add_single_watermark_text(img, social_handle, handle_position, handle_config)
        img = add_single_watermark_text(img, id_code, id_position, id_config)
    else:
        # Original combined watermark
        watermark_text = f"{social_handle}\n{id_code}"
        position = config.get('position', 'bottom-right')
        img = add_single_watermark_text(img, watermark_text, position, config)
    
    return img

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'watermark-fiiin'})

@app.route('/fonts', methods=['GET'])
def list_fonts():
    """List all available system fonts"""
    fonts = get_system_fonts()
    font_list = list(fonts.keys())
    
    # Categorize fonts
    categorized = {
        'serif': [],
        'sans_serif': [],
        'monospace': [],
        'other': []
    }
    
    for font in font_list:
        font_lower = font.lower()
        if any(serif in font_lower for serif in ['times', 'serif', 'georgia', 'palatino']):
            categorized['serif'].append(font)
        elif any(mono in font_lower for mono in ['mono', 'courier', 'consolas', 'inconsolata']):
            categorized['monospace'].append(font)
        elif any(sans in font_lower for sans in ['arial', 'helvetica', 'dejavu', 'liberation', 'ubuntu', 'roboto']):
            categorized['sans_serif'].append(font)
        else:
            categorized['other'].append(font)
    
    return jsonify({
        'total_fonts': len(font_list),
        'fonts': {
            'all': sorted(font_list),
            'categorized': {k: sorted(v) for k, v in categorized.items()}
        },
        'recommended': [
            'DejaVuSans-Bold.ttf',
            'DejaVuSans.ttf', 
            'Arial.ttf',
            'arial.ttf'
        ]
    })

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
            'transparency': data.get('transparency', 1.0),  # Transparency control
            # Separate positioning options
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
                'transparency': config['transparency'],
                'format': output_format,
                'processed_at': datetime.utcnow().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
