import cv2
import numpy as np

# Load segmented image
segmented_image = cv2.imread('result_masking.jpg')

# Convert segmented image to grayscale
gray_segmented = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)

# Threshold the grayscale image to get a binary mask
_, mask = cv2.threshold(gray_segmented, 1, 255, cv2.THRESH_BINARY)

# Create a new mask to keep only specific facial components (e.g., eyes, nose, mouth)
specific_mask = np.zeros_like(mask)
specific_mask[(mask == 1) & ((segmented_image[:,:,2] == 255) | (segmented_image[:,:,1] == 255))] = 255

# Apply the specific mask to the original image
result = cv2.bitwise_and(segmented_image, segmented_image, mask=specific_mask)

# Save the result
cv2.imwrite('specific_components_only.jpg', result)
