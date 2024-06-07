import cv2
import numpy as np

# Baca gambar asli
original_image = cv2.imread('oblong (6).jpg')

# Baca gambar hasil segmentasi
segmented_image = cv2.imread('black.jpg')

# Pastikan ukuran gambar hasil segmentasi sama dengan gambar asli
segmented_image = cv2.resize(segmented_image, (original_image.shape[1], original_image.shape[0]))

# Konversi gambar hasil segmentasi menjadi grayscale
segmented_gray = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)

# Lakukan deteksi tepi pada gambar hasil segmentasi
edges = cv2.Canny(segmented_gray, 30, 150)

# Invers hasil deteksi tepi
edges = cv2.bitwise_not(edges)

# Terapkan operasi pengurangan tepi pada gambar asli
clean_image = cv2.subtract(original_image, np.zeros_like(original_image), mask=edges)

# Simpan gambar hasil
cv2.imwrite('clean_image.jpg', clean_image)
