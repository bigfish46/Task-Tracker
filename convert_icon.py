from PIL import Image
import os

def convert_to_ico(png_path, ico_path):
    # Open the PNG file
    img = Image.open(png_path)
    
    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Create a list to store different size versions
    icon_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    img_list = []
    
    # Resize the image for each size
    for size in icon_sizes:
        resized_img = img.resize(size, Image.Resampling.LANCZOS)
        img_list.append(resized_img)
    
    # Save as ICO
    img_list[0].save(ico_path, format='ICO', sizes=[(img.size[0], img.size[1]) for img in img_list], append_images=img_list[1:])

if __name__ == '__main__':
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define input and output paths relative to script directory
    png_path = os.path.join(script_dir, 'app.png')
    ico_path = os.path.join(script_dir, 'app.ico')
    
    if not os.path.exists(png_path):
        print(f"Error: Could not find {png_path}")
        print("Please place your PNG file named 'app.png' in the same directory as this script.")
        exit(1)
    
    try:
        convert_to_ico(png_path, ico_path)
        print(f"Successfully converted {png_path} to {ico_path}")
    except Exception as e:
        print(f"Error converting icon: {e}") 