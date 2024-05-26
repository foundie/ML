import cv2
import numpy as np

def apply_lipstick(image, lip_color):
    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define lower and upper bounds for lip color in HSV
    lower_lip_color = np.array([120, 50, 50])
    upper_lip_color = np.array([180, 255, 255])
    
    # Create a mask for the lip color in HSV
    lip_mask = cv2.inRange(hsv_image, lower_lip_color, upper_lip_color)
    
    # Apply the lipstick color to the lip region
    image_with_lipstick = np.copy(image)
    image_with_lipstick[lip_mask != 0] = lip_color
    
    return image_with_lipstick

def main():
    # Load the image
    image = cv2.imread('test_image.jpg')
    
    # Resize image (optional)
    # image = cv2.resize(image, (new_width, new_height))
    
    # Input lipstick color in hex format
    hex_color = input("Masukkan kode hex warna lipstick (contoh: #FF0000 untuk warna merah): ")
    
    # Convert hex color to BGR format
    bgr_color = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    # Apply lipstick
    image_with_lipstick = apply_lipstick(image, bgr_color)
    
    # Display the result
    cv2.imshow('Lipstick Segmentation', image_with_lipstick)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
