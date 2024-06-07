from logger import setup_logger
from model import BiSeNet

import torch

import os
import os.path as osp
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
import cv2

'''
def vis_parsing_maps(im, parsing_anno, stride, save_im=False, save_path='vis_results/parsing_map_on_im.jpg'):
    # Colors for all 20 parts
    part_colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0],
                   [255, 0, 85], [255, 0, 170],
                   [0, 255, 0], [85, 255, 0], [170, 255, 0],
                   [0, 255, 85], [0, 255, 170],
                   [0, 0, 255], [85, 0, 255], [170, 0, 255],
                   [0, 85, 255], [0, 170, 255],
                   [255, 255, 0], [255, 255, 85], [255, 255, 170],
                   [255, 0, 255], [255, 85, 255], [255, 170, 255],
                   [0, 255, 255], [85, 255, 255], [170, 255, 255]]

    im = np.array(im)
    vis_im = im.copy().astype(np.uint8)
    vis_parsing_anno = parsing_anno.copy().astype(np.uint8)
    vis_parsing_anno = cv2.resize(vis_parsing_anno, None, fx=stride, fy=stride, interpolation=cv2.INTER_NEAREST)
    vis_parsing_anno_color = np.zeros((vis_parsing_anno.shape[0], vis_parsing_anno.shape[1], 3)) + 255

    num_of_class = np.max(vis_parsing_anno)

    for pi in range(1, num_of_class + 1):
        index = np.where(vis_parsing_anno == pi)
        vis_parsing_anno_color[index[0], index[1], :] = part_colors[pi]

    vis_parsing_anno_color = vis_parsing_anno_color.astype(np.uint8)
    # print(vis_parsing_anno_color.shape, vis_im.shape)
    vis_im = cv2.addWeighted(cv2.cvtColor(vis_im, cv2.COLOR_RGB2BGR), 0.4, vis_parsing_anno_color, 0.6, 0)

    # Save result or not
    if save_im:
        cv2.imwrite(save_path[:-4] +'.png', vis_parsing_anno)
        cv2.imwrite(save_path, vis_im, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    # return vis_im

import numpy as np
import cv2

def vis_parsing_maps(im, parsing_anno, stride, save_im=False, save_path='vis_results/parsing_map_on_im.jpg'):
    # Colors for specific parts: eyes, nose, mouth
    part_colors = {    # Mata kanan
        1: [0, 255, 0],   
        3: [0, 0, 255],
        4: [255, 0, 0],    
        5: [155, 0, 0],
        10: [255,255,0],
        12: [255,0,0],
        13: [255,0,0]
    }

    im = np.array(im)
    vis_im = im.copy().astype(np.uint8)
    vis_parsing_anno = parsing_anno.copy().astype(np.uint8)
    vis_parsing_anno = cv2.resize(vis_parsing_anno, None, fx=stride, fy=stride, interpolation=cv2.INTER_NEAREST)
    
    # Create a mask to keep only the desired parts
    mask = np.zeros((vis_parsing_anno.shape[0], vis_parsing_anno.shape[1]), dtype=np.uint8)
    for pi in part_colors.keys():
        mask[vis_parsing_anno == pi] = 1
    
    # Apply mask to the image
    vis_im = cv2.bitwise_and(vis_im, vis_im, mask=mask)

    # Set the background (non-desired parts) to white
    white_background = np.full_like(vis_im, 255)
    vis_im = np.where(mask[:, :, None] == 1, vis_im, white_background)
    
    # Save result or not
    if save_im:
        cv2.imwrite(save_path, vis_im, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
# Contoh penggunaan fungsi dengan gambar dan parsing_anno sebagai input
# im = ... # Gambar input
# parsing_anno = ... # Parsing annotation untuk gambar
# vis_parsing_maps(im, parsing_anno, stride=1, save_im=True)

'''

import numpy as np
import cv2

def vis_parsing_maps(im, parsing_anno, stride, save_im=False, save_path='vis_results/parsing_map_on_im.jpg', use_grayscale=False, crop_face=True):
    # Bagian yang ingin disimpan: mata, hidung, bibir
    desired_parts = {    
        1, 3, 4, 5, 10, 12, 13
    }

    # Load Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    im = np.array(im)
    vis_im = im.copy().astype(np.uint8)
    vis_parsing_anno = parsing_anno.copy().astype(np.uint8)
    vis_parsing_anno = cv2.resize(vis_parsing_anno, None, fx=stride, fy=stride, interpolation=cv2.INTER_NEAREST)
    
    # Create a mask to keep only the desired parts
    mask = np.zeros((vis_parsing_anno.shape[0], vis_parsing_anno.shape[1]), dtype=np.uint8)
    for pi in desired_parts:
        mask[vis_parsing_anno == pi] = 1
    
    # Apply mask to the image to keep only the desired parts
    vis_im = cv2.bitwise_and(vis_im, vis_im, mask=mask)

    # Set the background (non-desired parts) to white
    white_background = np.full_like(vis_im, 255)
    vis_im = np.where(mask[:, :, None] == 1, vis_im, white_background)
    
    if crop_face:
        # Convert image to grayscale for face detection
        gray_im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray_im, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        
        if len(faces) > 0:
            # Assume the first face is the one we want
            (x, y, w, h) = faces[0]
            vis_im = vis_im[y:y+h, x:x+w]

    # Convert to grayscale if required
    if use_grayscale:
        vis_im = cv2.cvtColor(vis_im, cv2.COLOR_RGB2GRAY)
        #vis_im = cv2.cvtColor(vis_im, cv2.COLOR_GRAY2BGR)  # Convert back to 3 channels for compatibility with CNN expecting 3 channel input
    
    # Save result or not
    if save_im:
        cv2.imwrite(save_path, vis_im, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

# Assuming you have BiSeNet and vis_parsing_maps defined somewhere in your code

def evaluate(image_path, respth='./res/test_res', dspth='./', cp='79999_iter.pth'):
    if not os.path.exists(respth):
        os.makedirs(respth)

    n_classes = 19
    net = BiSeNet(n_classes=n_classes)
    # Move the model to CPU
    net.cpu()
    
    # Load the model from the current directory
    save_pth = cp
    net.load_state_dict(torch.load(save_pth, map_location=torch.device('cpu')))
    net.eval()

    to_tensor = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])

    # Load the specific image 'oblong (6).jpg' for evaluation
    #image_path = 'oblong (6).jpg'
    img = Image.open(image_path)
    image = img.resize((512, 512), Image.BILINEAR)
    img = to_tensor(image)
    img = torch.unsqueeze(img, 0)
    # Move the input data to CPU
    img = img.cpu()
    with torch.no_grad():
        out = net(img)[0]
        parsing = out.squeeze(0).cpu().numpy().argmax(0)
        print(np.unique(parsing))

        vis_parsing_maps(image, parsing, stride=1, save_im=True, save_path=os.path.join(respth, image_path))


# Definisi fungsi execute_on_jpg_files
def execute_on_jpg_files(folder_path):
    # Mendapatkan daftar semua file dalam folder
    files = os.listdir(folder_path)
    # Filter hanya file dengan ekstensi .jpg
    jpg_files = [file for file in files if file.endswith('.jpg')]
    # Mendapatkan path lengkap untuk setiap file .jpg
    jpg_paths = [os.path.join(folder_path, file) for file in jpg_files]

    # Iterasi melalui setiap file .jpg dan melakukan evaluasi
    for index, jpg_path in enumerate(jpg_paths, start=1):
        print(f"Sedang mengeksekusi file ke-{index}: {jpg_path}")
        try:
            evaluate(image_path=jpg_path)
        except Exception as e:
            print(f"Error saat memproses gambar: {e}. Melanjutkan ke gambar berikutnya...")
            continue
    print("Semua file telah dieksekusi.")


# Bagian utama program
if __name__ == "__main__":
    folder_path = "C:\\Database\\Manajemen Informasi Medika\\Shape Analysis\\FaceShape_Dataset\\training_set\\3"
    execute_on_jpg_files(folder_path)


if __name__ == "__main__":
    evaluate(cp='79999_iter.pth')
