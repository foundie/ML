# Machine Learning Repository

This repository contains the creation of mathematical logic, machine learning models, and computational data processing with the following list of features:

    1. Visual Weight Classifier 
    2. Skin Tone Classifier 
    3. Color Analysis 
    4. Product Comparison

## 1. Visual Weight Classifier 
The model can classify faces into two categories low visual weight and high visual weight. 

![App Screenshot](https://i.ytimg.com/vi/gWCAVT0lH4g/maxresdefault.jpg)

The dataset of this feature can be accessed at the link  [Google Drive](https://drive.google.com/file/d/1GhXA0SBQaRaoAbGLlv4Nk7KfxD0NY1tT/view?usp=sharing). The dataset has been preprocessed using OpenCV haarcascade_frontalface_default.xml and segmented using the face parsing model by removing unnecessary noise so that only the part of the face without hair remains. 

The model used uses CNN architecture with the following architectural details 

    0: low visual weight 
    1: high visual weight

| Layer (type)              | Output Shape          | Param #   |
| :------------------------ | :-------------------- | --------: |
| Conv2D                    | (None, 62, 62, 32)    | 896       |
| MaxPooling2D              | (None, 31, 31, 32)    | 0         |
| Dropout                   | (None, 31, 31, 32)    | 0         |
| Conv2D                    | (None, 29, 29, 64)    | 18,496    |
| MaxPooling2D              | (None, 14, 14, 64)    | 0         |
| Dropout                   | (None, 14, 14, 64)    | 0         |
| Conv2D                    | (None, 12, 12, 128)   | 73,856    |
| MaxPooling2D              | (None, 6, 6, 128)     | 0         |
| Dropout                   | (None, 6, 6, 128)     | 0         |
| Flatten                   | (None, 4608)          | 0         |
| Dense                     | (None, 128)           | 589,952   |
| Dropout                   | (None, 128)           | 0         |
| Dense                     | (None, 1)             | 129       |

The resulting accuracy reached 89%. When testing the model, the images that enter the model must be preprocessed first so that the images that enter the model are more accurate and clean from noise. 

The deployment process for this feature uses Flask or directly uses the Python backend without converting to Javascript.

## 2. Skin Tone Classifier 
The Skin Tone dataset can be accessed publicly at [Kaggle](https://www.kaggle.com/datasets/ducnguyen168/dataset-skin-tone) with cleaning and adjustment before entering the model. 

The architecture of the model uses CNN with increasing regularization. There are three classes that are classified 

    0: dark deep,
    1: fair light, 
    2: medium tan,

| Layer (type)              | Output Shape          | Param #   |
| :------------------------ | :-------------------- | --------: |
| Conv2D                    | (None, 62, 62, 32)    | 896       |
| MaxPooling2D              | (None, 31, 31, 32)    | 0         |
| Dropout                   | (None, 31, 31, 32)    | 0         |
| Conv2D                    | (None, 29, 29, 64)    | 18,496    |
| MaxPooling2D              | (None, 14, 14, 64)    | 0         |
| Dropout                   | (None, 14, 14, 64)    | 0         |
| Conv2D                    | (None, 12, 12, 128)   | 73,856    |
| MaxPooling2D              | (None, 6, 6, 128)     | 0         |
| Dropout                   | (None, 6, 6, 128)     | 0         |
| Flatten                   | (None, 4608)          | 0         |
| Dense                     | (None, 256)           | 1,179,904 |
| Dropout                   | (None, 256)           | 0         |
| Dense                     | (None, 3)             | 771       |

The resulting accuracy results reached 95%. Then deployment is done using Tensorflow.js by changing the .h5 format to .json and .bin so that it can be executed on the server side. 

## 3. Color Analysis
In color analysis using rules or rules that are reinforced using a recommender system. Details of color analysis can be accessed through

    Color Analysis/colorfixpol.ipynb

## 4. Product Comparison 
![pict2](https://github.com/foundie/ML/blob/main/Product_classifier/classify_tone_product/Shade%20Pict/compare.png?raw=True)
The process of the product comparison feature starts from several steps resulting in a final dataset that includes several variables and annotations. 

| Column Name         | Description                                                                                  | Unique Values                                                                                   |
|---------------------|----------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| Product Title       | Product name obtained from scraping                                                          |                                                                                                 |
| Brand               | Product brand obtained from scraping                                                         | wardah, hanasui, pixy, somethinc, emina, meybelline                                             |
| Type                | Product type categories                                                                      | lip, foundation & cushion, powder, face, eye, cheek                                             |
| Variant Name        | Information about the product variant obtained from scraping                                 |                                                                                                 |
| Color HEX           | Hexadecimal color code of the product obtained from scraping                                 |                                                                                                 |
| Color RGB           | RGB color values of the product obtained from scraping                                       |                                                                                                 |
| Season 1 Name       | Season 1 product classification using k-means from ground truth color reference              | autumn warm, autumn soft, autumn deep, summer soft, summer cool, summer light, spring warm, spring light, spring clear, winter deep, winter clear, winter cool |
| Season 1 Percent    | Percentage of similarity to season 1 calculated using Euclidean distance from centroid 1     |                                                                                                 |
| S1 Closest Color    | Closest color to season 1 centroid                                                           |                                                                                                 |
| Season 2 Name       | Season 2 product classification                                                              | autumn warm, autumn soft, autumn deep, summer soft, summer cool, summer light, spring warm, spring light, spring clear, winter deep, winter clear, winter cool |
| Season 2 Percent    | Percentage of similarity to season 2 calculated using Euclidean distance from centroid 2     |                                                                                                 |
| S2 Closest Color    | Closest color to season 2 centroid                                                           |                                                                                                 |
| Tone                | Product tone classification using k-means                                                    | medium_tan, dark_deep, fair_light                                                               |
| Shade               | Product shade per type classification using k-means                                          | 12 shades, 1 being the lightest                                                                 |
| Image URL           | Link to the product image                                                                    |                                                                                                 |
| Product URL         | Link to the product page                                                                     |                                                                                                 |

The process carried out to obtain the dataset in order

    1. Scraping website product beauty catalog 
    2. Classify Season Name 
    3. Clasify Tone Products 
    4. Classify Shade Products 

### Scraping Website Products 
The scraping process begins by collecting resource links for each product page from several beuty product brands in Indonesia and one beuty product brand from outside Indonesia. The brands scraped include [wardah], [hanasui], [emina], [somethinc], [pixy], and [maybelline]. 
Then scraping is carried out using Python BeautifulSoup which can be seen at 

    Product_classifier/get_data 

### Classify Season Name
Based on the data obtained from scraping, further analysis is carried out by classifying products based on the two closest seasons and the distance becomes the percentage of the euclidian distance of the product. The ground truth used is taken from a color reference that has been classified into 12 seasons which become the centroid of the product color distribution. 


Sebaran Warna Setiap Season 
![Autumn Deep](https://github.com/foundie/ML/blob/main/Product_classifier/clasify_season/pict/Autumn%20Deep.png?raw=True)  
![Autumn Deep](https://github.com/foundie/ML/blob/main/Product_classifier/clasify_season/pict/Autumn%20Soft.png?raw=True)  
![Autumn Deep](https://github.com/foundie/ML/blob/main/Product_classifier/clasify_season/pict/Autumn%20Warm.png?raw=True)  
![Autumn Deep](https://github.com/foundie/ML/blob/main/Product_classifier/clasify_season/pict/Spring%20Clear.png?raw=True)  
![Autumn Deep](https://github.com/foundie/ML/blob/main/Product_classifier/clasify_season/pict/Spring%20Light.png?raw=True)  
![Autumn Deep](https://github.com/foundie/ML/blob/main/Product_classifier/clasify_season/pict/Spring%20Warm.png?raw=True)  
![Autumn Deep](https://github.com/foundie/ML/blob/main/Product_classifier/clasify_season/pict/Summer%20Cool.png?raw=True)  
![Autumn Deep](https://github.com/foundie/ML/blob/main/Product_classifier/clasify_season/pict/Summer%20Soft.png?raw=True)  
![Autumn Deep](https://github.com/foundie/ML/blob/main/Product_classifier/clasify_season/pict/Summer%20Light.png?raw=True)  
![Autumn Deep](https://github.com/foundie/ML/blob/main/Product_classifier/clasify_season/pict/Winter%20Deep.png?raw=True)  
![Autumn Deep](https://github.com/foundie/ML/blob/main/Product_classifier/clasify_season/pict/Winter%20Clear.png?raw=True)  
![Autumn Deep](https://github.com/foundie/ML/blob/main/Product_classifier/clasify_season/pict/Winter%20Cool.png?raw=True)  

### Classify Tone Product 
Overall, the products that have been obtained are classified using K-Means that dark tone is at a relatively high RGB amount, fair_light is at a low RGB value and medium_tan is at a value between fair_light and dark_deep. 

### Classify Shade Product 
Each type of product such as lipstick foundation or blush has a shade that can be classified into degrees of darkness in a color. The darker the color, the higher the shade. This is done based on the type of product because generally foundation has a color-based facial skin color and lipstick generally has a color-based, lip color so that if classification is carried out simultaneously it will cause collisions and reduce the accuracy of product similarity. Therefore, classification is done based on different types. Examples of classifications on powder, foundation, and cusshion types are visualized as follows using Sklearn's K-Means algorithm. 
![pict1](https://github.com/foundie/ML/blob/main/Product_classifier/classify_tone_product/Shade%20Pict/product.png?raw=True)![pict2](https://github.com/foundie/ML/blob/main/Product_classifier/classify_tone_product/Shade%20Pict/centroid.png?raw=True)

The centroid distribution of the color of each cluster product is as follows 
### Foundation, Cusshion, Powder
![pict1](https://github.com/foundie/ML/blob/main/Product_classifier/classify_tone_product/Shade%20Pict/powder.png?raw=True)

### Lip Product
![pict2](https://github.com/foundie/ML/blob/main/Product_classifier/classify_tone_product/Shade%20Pict/lip.png?raw=True)

### Eye Product
![pict2](https://github.com/foundie/ML/blob/main/Product_classifier/classify_tone_product/Shade%20Pict/eye.png?raw=True)

### Face Product
![pict2](https://github.com/foundie/ML/blob/main/Product_classifier/classify_tone_product/Shade%20Pict/face.png?raw=True)


