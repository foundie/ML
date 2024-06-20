const fs = require('fs');
const csv = require('csv-parser');
const skmeans = require('skmeans');
const Hapi = require('@hapi/hapi');

// Membaca dataset dari file CSV
const results = [];

fs.createReadStream('FINAL_BENERAN_YA ALLAH_AAMIIN_updated.csv')
  .pipe(csv())
  .on('data', (data) => results.push(data))
  .on('end', async () => {
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

    const cleanResults = results.filter(row => row['Tone'] && row['Season 1 Name'] && row['Shade'] && row['Type']);

    const showProductsDetailsByBrand = (data, selectedIndex, nClusters = 60, topN = 10) => {
      if (selectedIndex < 0 || selectedIndex >= data.length) {
        throw new Error(`Indeks ${selectedIndex} tidak valid.`);
      }

      const referenceProduct = data[selectedIndex];
      const features = data.map(row => [parseFloat(row['Shade']), row['Tone'], row['Season 1 Name'], row['Type']]);

      const kmeansResult = skmeans(features, nClusters);
      const clusters = kmeansResult.idxs;

      data.forEach((row, index) => row['Cluster'] = clusters[index]);

      const clusterLabel = data[selectedIndex]['Cluster'];
      const similarProducts = data.filter(row => row['Cluster'] === clusterLabel);

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

      const topSimilarities = [];
      const brandCounts = {};
      similarities.slice(0, topN).forEach(similarity => {
        if (!brandCounts[similarity.Brand]) {
          brandCounts[similarity.Brand] = 0;
        }
        brandCounts[similarity.Brand]++;
        topSimilarities.push(similarity);
      });

      return { topSimilarities, brandCounts, referenceProduct };
    };

    const init = async () => {
      const server = Hapi.server({
        port: 3000,
        host: 'localhost'
      });

      server.route({
        method: 'GET',
        path: '/compare-product',
        handler: (request, h) => {
          const { index } = request.query;

          if (index === undefined) {
            return h.response({ message: 'Parameter index diperlukan.' }).code(400);
          }

          const selectedIndex = parseInt(index.trim(), 10);

          if (isNaN(selectedIndex)) {
            return h.response({ message: 'Parameter index harus berupa angka.' }).code(400);
          }

          try {
            const result = showProductsDetailsByBrand(cleanResults, selectedIndex);

            if (result && result.topSimilarities && result.topSimilarities.length > 0) {
              const { topSimilarities, brandCounts, referenceProduct } = result;

              return h.response({
                referenceProduct: {
                  "Brand": referenceProduct['Brand'],
                  "Product Title": referenceProduct['Product Title'],
                  "Variant Name": referenceProduct['Variant Name'],
                  "Shade": referenceProduct['Shade'],
                  "Tone": referenceProduct['Tone'],
                  "Color HEX": referenceProduct['Color HEX'],
                  "Season 1 Name": referenceProduct['Season 1 Name'],
                  "Type": referenceProduct['Type']
                },
                similarProducts: topSimilarities,
                brandCounts: brandCounts
              }).code(200);
            } else {
              return h.response({ message: 'No similar products found.' }).code(404);
            }
          } catch (error) {
            console.error(error);
            return h.response({ message: 'Internal Server Error', error: error.message }).code(500);
          }
        }
      });

      await server.start();
      console.log(`Server berjalan di ${server.info.uri}`);
    };

    process.on('unhandledRejection', (err) => {
      console.log(err);
      process.exit(1);
    });

    init();
  });
