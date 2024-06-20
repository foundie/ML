import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

# Membaca dataset dari file CSV
df = pd.read_csv('FINAL_BENERAN_YA ALLAH_AAMIIN_updated.csv')

# Mengonversi kolom 'Tone' dan 'Season 1 Name' menjadi fitur numerik
tone_mapping = {'dark_deep': 3, 'medium_tan': 2, 'fair_light': 1}
season_mapping = {
    'autumn warm': 1, 'autumn soft': 2, 'autumn deep': 3, 
    'summer soft': 4, 'summer cool': 5, 'summer light': 6, 
    'spring warm': 7, 'spring light': 8, 'spring clear': 9, 
    'winter deep': 10, 'winter clear': 11, 'winter cool': 12
}
type_mapping = {
    'lip':1, 'face':2, 'foundation & cussion':3, 'cheek':4, 'powder':5, 'eye':6
}

df['Tone'] = df['Tone'].map(tone_mapping)
df['Season 1 Name'] = df['Season 1 Name'].map(season_mapping)
df['Type'] = df['Type'].map(type_mapping)

# Menghapus baris yang mengandung nilai NaN
df.dropna(subset=['Tone', 'Season 1 Name', 'Shade', 'Type'], inplace=True)

# Fungsi untuk menampilkan produk berdasarkan brand dan atribut lainnya
def show_products_details_by_brand(df, selected_index, n_clusters=60, top_n=10):
    # Memastikan indeks valid
    if selected_index not in df.index:
        print(f"Indeks {selected_index} tidak valid.")
        return None, None

    # Mengambil produk referensi berdasarkan indeks yang dipilih
    reference_product = df.loc[selected_index]

    # Ekstraksi fitur yang diperlukan
    features = df[['Shade', 'Tone', 'Season 1 Name', 'Type']]

    # Standarisasi fitur
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)

    # K-Means Clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    df['Cluster'] = kmeans.fit_predict(features_scaled)

    # Filter produk lain dalam cluster yang sama
    cluster_label = df.loc[selected_index, 'Cluster']
    similar_products = df[df['Cluster'] == cluster_label]

    # Menghitung similarity dengan jarak Euclidean
    reference_features = features_scaled[df.index.get_loc(selected_index)]
    similarities = []
    for index, product in similar_products.iterrows():
        product_features = features_scaled[df.index.get_loc(index)]
        distance = np.linalg.norm(reference_features - product_features)  # Euclidean distance
        similarity = 1 / (1 + distance)
        similarities.append({
            "Brand": product['Brand'],
            "Product Title": product['Product Title'],
            "Type": product['Type'],
            "Variant Name": product['Variant Name'],
            "Shade": product['Shade'],
            "Tone": product['Tone'],
            "Color HEX": product['Color HEX'],
            "Season 1 Name": product['Season 1 Name'],
            "Similarity": similarity
        })

    similarities_df = pd.DataFrame(similarities)

    # Mengumpulkan nilai similarity 10 teratas untuk setiap brand
    top_similarities = pd.DataFrame()
    brands = similarities_df['Brand'].unique()
    for brand in brands:
        brand_df = similarities_df[similarities_df['Brand'] == brand]
        brand_df = brand_df.sort_values(by='Similarity', ascending=False).head(top_n)
        top_similarities = pd.concat([top_similarities, brand_df], ignore_index=True)

    # Menghitung jumlah produk per brand
    brand_counts = top_similarities['Brand'].value_counts()

    return top_similarities, brand_counts

# Main program
if __name__ == "__main__":
    # Input dari pengguna
    selected_index = int(input("\nMasukkan nomor indeks dari produk yang dipilih: ").strip())

    # Memanggil fungsi untuk menampilkan detail produk per brand sesuai input pengguna
    similarities_df, brand_counts = show_products_details_by_brand(df, selected_index)

    # Memeriksa apakah similarities_df tidak kosong
    if similarities_df is not None:
        # Menampilkan detail produk referensi yang dipilih oleh pengguna
        print("\nDetail produk referensi yang dipilih:")
        reference_product = df.loc[selected_index]
        print(f"Brand: {reference_product['Brand']}")
        print(f"Product Title: {reference_product['Product Title']}")
        print(f"Variant Name: {reference_product['Variant Name']}")
        print(f"Shade: {reference_product['Shade']}")
        print(f"Tone: {reference_product['Tone']}")
        print(f"Color HEX: {reference_product['Color HEX']}")
        print(f"Season 1 Name: {reference_product['Season 1 Name']}")
        print(f"Type: {reference_product['Type']}")
        print("\n")

        # Menampilkan hasil similarities_df dalam bentuk DataFrame
        print("Detail produk berdasarkan brand:")
        print(similarities_df)

        # Menampilkan jumlah produk per brand
        print("\nJumlah produk per brand:")
        print(brand_counts)
