import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
import numpy as np

# Fungsi untuk mengubah warna HEX ke RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Membaca data dari CSV
#df = pd.read_csv("final_product_classifier.csv")
df = pd.read_excel('powder_foundation_cussion_tone_classifier.xlsx')
df['Color RGB'] = df['Color HEX'].apply(hex_to_rgb)

# One-Hot Encoding untuk fitur kategori
encoder = OneHotEncoder(sparse_output=False)
encoded_features = encoder.fit_transform(df[['Type', 'Season 1 Name', 'Season 2 Name', 'Tone']])
features = np.hstack((np.array(df['Color RGB'].tolist()), encoded_features))

# Normalisasi fitur
scaler = StandardScaler()
normalized_features = scaler.fit_transform(features)

# Clustering dengan K-Means
kmeans = KMeans(n_clusters=100, random_state=42)
df['Cluster'] = kmeans.fit_predict(normalized_features)

# Fungsi untuk mencari produk berdasarkan nama yang diinput oleh user
def search_products(product_title, df):
    return df[df['Product Title'].str.contains(product_title, case=False, na=False)]

# Fungsi untuk merekomendasikan produk
def recommend_products(input_product, df, normalized_features, kmeans, encoder, scaler, top_n=5):
    input_rgb = hex_to_rgb(input_product['Color HEX'])
    input_df = pd.DataFrame([input_product])
    input_encoded = encoder.transform(input_df[['Type', 'Season 1 Name', 'Season 2 Name', 'Tone']])
    input_features = np.hstack((input_rgb, input_encoded[0]))
    input_features = scaler.transform([input_features])
    input_cluster = kmeans.predict(input_features)[0]
    
    cluster_products = df[df['Cluster'] == input_cluster]
    distances = pairwise_distances(input_features, normalized_features[cluster_products.index])
    closest_indices = np.argsort(distances)[0][:top_n]
    
    recommendations = cluster_products.iloc[closest_indices].copy()
    recommendations['Similarity'] = 100 - (distances[0][closest_indices] / distances[0][closest_indices].max() * 100)
    recommendations = recommendations[recommendations['Product Title'] != input_product['Product Title']]
    
    return recommendations

# User memasukkan nama produk yang ingin dicari
product_title_input = input("Masukkan nama produk yang ingin dicari: ")

# Cari produk berdasarkan nama
search_results = search_products(product_title_input, df)

if not search_results.empty:
    print("Produk ditemukan:")
    print(search_results[['Product Title', 'Brand', 'Type', 'Season 1 Name', 'Tone', 'Color HEX']])
    
    
    # User memilih produk dari hasil pencarian
    selected_index = int(input("Pilih indeks produk yang ingin dibandingkan: "))
    
    if selected_index in search_results.index:
        selected_product = search_results.loc[selected_index]
        
        # Membuat dictionary produk input untuk rekomendasi
        input_product = {
            'Product Title': selected_product['Product Title'],
            'Brand': selected_product['Brand'],
            'Type': selected_product['Type'],
            'Color HEX': selected_product['Color HEX'],
            'Season 1 Name': selected_product['Season 1 Name'],
            'Season 2 Name': selected_product['Season 2 Name'],
            'Tone': selected_product['Tone']
        }
        
        # Tentukan jumlah rekomendasi yang diinginkan
        top_n = 10
        
        # Cari rekomendasi
        recommended_products = recommend_products(input_product, df, normalized_features, kmeans, encoder, scaler, top_n)
        print("Rekomendasi Produk:")
        print(input_product['Product Title'], input_product['Type'], input_product['Brand'], input_product['Season 1 Name'], input_product['Color HEX'], input_product['Tone'])
        print(recommended_products[['Product Title', 'Type', 'Brand','Season 1 Name', 'Color HEX', 'Tone','Similarity']])
    else:
        print("Indeks produk tidak valid.")
else:
    print("Produk tidak ditemukan.")
