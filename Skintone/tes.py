import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img

# Load model VGG16 dengan penanganan khusus
try:
    model = load_model('Skintone_Classification.h5', compile=False)
except Exception as e:
    print(f"Error loading model: {e}")
    # Penanganan khusus jika diperlukan
    from keras.layers import InputLayer
    custom_objects = {'InputLayer': InputLayer}
    model = load_model('Skintone_Classification.h5', custom_objects=custom_objects, compile=False)

# Fungsi untuk preprocess gambar
def preprocess_image(image_path):
    img = load_img(image_path, target_size=(64, 64))  # VGG16 expects 224x224 images
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  # Normalization
    return img

# Path gambar untuk pengujian
image_path = "C:\Database\Manajemen Informasi Medika\Skin Tone\image8.jpg"  # Ganti dengan path gambar sebenarnya

# Lakukan prediksi untuk gambar ini
img = preprocess_image(image_path)
prediction = model.predict(img)
predicted_class = np.argmax(prediction, axis=1)
print(f"Image: {image_path}, Predicted Class: {predicted_class}")
