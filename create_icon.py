from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a new image with a white background
    size = (256, 256)
    image = Image.new('RGB', size, 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a blue envelope
    envelope_points = [
        (30, 80),    # top-left
        (226, 80),   # top-right
        (226, 176),  # bottom-right
        (30, 176),   # bottom-left
    ]
    draw.polygon(envelope_points, fill='#007bff')
    
    # Draw envelope flap
    flap_points = [
        (30, 80),     # bottom-left
        (128, 128),   # middle point
        (226, 80),    # bottom-right
    ]
    draw.polygon(flap_points, fill='#0056b3')
    
    # Save the image as ICO
    image.save('app_icon.ico', format='ICO', sizes=[(256, 256)])

if __name__ == '__main__':
    try:
        from PIL import Image
    except ImportError:
        os.system('pip install pillow')
    create_icon()
