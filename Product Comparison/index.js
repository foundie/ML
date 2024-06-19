const fs = require('fs');
const csv = require('csv-parser');
const skmeans = require('skmeans');

// Membaca dataset dari file CSV
const results = [];

fs.createReadStream('FINAL_BENERAN_YA ALLAH_AAMIIN_updated.csv')
  .pipe(csv())
  .on('data', (data) => results.push(data))
  .on('end', () => {
    // Mengonversi kolom 'Tone' dan 'Season 1 Name' menjadi fitur numerik
    const toneMapping = {'dark_deep': 3, 'medium_tan': 2, 'fair_light': 1};
    const seasonMapping = {
      'autumn warm': 1, 'autumn soft': 2, 'autumn deep': 3,
      'summer soft': 4, 'summer cool': 5, 'summer light': 6,
      'spring warm': 7, 'spring light': 8, 'spring clear': 9,
      'winter deep': 10, 'winter clear': 11, 'winter cool': 12
    };
    const typeMapping = {'lip': 1, 'face': 2, 'foundation & cussion': 3, 'cheek': 4, 'powder': 5, 'eye': 6};

    results.forEach(row => {
      row['Tone'] = toneMapping[row['Tone']];
      row['Season 1 Name'] = seasonMapping[row['Season 1 Name']];
      row['Type'] = typeMapping[row['Type']];
    });

    // Menghapus baris yang mengandung nilai NaN
    const cleanResults = results.filter(row => row['Tone'] && row['Season 1 Name'] && row['Shade'] && row['Type']);

    // Fungsi untuk menampilkan produk berdasarkan brand dan atribut lainnya
    const showProductsDetailsByBrand = (data, selectedIndex, nClusters = 60, topN = 10) => {
      if (selectedIndex < 0 || selectedIndex >= data.length) {
        console.log(`Indeks ${selectedIndex} tidak valid.`);
        return;
      }

      const referenceProduct = data[selectedIndex];
      const features = data.map(row => [parseFloat(row['Shade']), row['Tone'], row['Season 1 Name'], row['Type']]);

      // K-Means Clustering
      const kmeansResult = skmeans(features, nClusters);
      const clusters = kmeansResult.idxs;

      data.forEach((row, index) => row['Cluster'] = clusters[index]);

      // Filter produk lain dalam cluster yang sama
      const clusterLabel = data[selectedIndex]['Cluster'];
      const similarProducts = data.filter(row => row['Cluster'] === clusterLabel);

      // Menghitung similarity dengan jarak Euclidean
      const referenceFeatures = features[selectedIndex];
      const similarities = similarProducts.map(product => {
        const productFeatures = features[data.indexOf(product)];
        const distance = Math.sqrt(referenceFeatures.reduce((sum, val, i) => sum + Math.pow(val - productFeatures[i], 2), 0));
        const similarity = 1 / (1 + distance);

        return {
          "Brand": product['Brand'],
          "Product Title": product['Product Title'],
          "Type": product['Type'],
          "Variant Name": product['Variant Name'],
          "Shade": product['Shade'],
          "Tone": product['Tone'],
          "Color HEX": product['Color HEX'],
          "Season 1 Name": product['Season 1 Name'],
          "Similarity": similarity
        };
      });

      similarities.sort((a, b) => b['Similarity'] - a['Similarity']);

      // Mengumpulkan nilai similarity 10 teratas untuk setiap brand
      const topSimilarities = [];
      const brandCounts = {};
      similarities.slice(0, topN).forEach(similarity => {
        if (!brandCounts[similarity.Brand]) {
          brandCounts[similarity.Brand] = 0;
        }
        brandCounts[similarity.Brand]++;
        topSimilarities.push(similarity);
      });

      return { topSimilarities, brandCounts };
    };

    // Main program
    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });

    readline.question("Masukkan nomor indeks dari produk yang dipilih: ", index => {
      const selectedIndex = parseInt(index.trim(), 10);
      const { topSimilarities, brandCounts } = showProductsDetailsByBrand(cleanResults, selectedIndex);

      if (topSimilarities && topSimilarities.length > 0) {
        const referenceProduct = cleanResults[selectedIndex];
        console.log("\nDetail produk referensi yang dipilih:");
        console.log(`Brand: ${referenceProduct['Brand']}`);
        console.log(`Product Title: ${referenceProduct['Product Title']}`);
        console.log(`Variant Name: ${referenceProduct['Variant Name']}`);
        console.log(`Shade: ${referenceProduct['Shade']}`);
        console.log(`Tone: ${referenceProduct['Tone']}`);
        console.log(`Color HEX: ${referenceProduct['Color HEX']}`);
        console.log(`Season 1 Name: ${referenceProduct['Season 1 Name']}`);
        console.log(`Type: ${referenceProduct['Type']}`);
        console.log("\nDetail produk berdasarkan brand:");
        console.table(topSimilarities);
        console.log("\nJumlah produk per brand:");
        console.table(brandCounts);
      }

      readline.close();
    });
  });
