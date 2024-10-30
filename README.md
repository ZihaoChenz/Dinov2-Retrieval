## **1. Introduction**

Dinov2 location matching converts an image into a one-dimensional feature using Dinov2. By calculating the similarity between features, the location information of the image is determined within an object.

---

## **2. Prepare Open Source Dataset**

1. Download ZuBuD dataset in https://icu.ee.ethz.ch/research/datsets.html
2. ```bash
   python tools/deal_with_ZuBuD.py --src_folder xxx/xxx --dst_folder xxx/xxx
   ```
   --src_folder: The path where the dataset folder is located
   --dst_folder: The path to the processed dataset output, default is data\ZuBuD

---

## **3. Self-Dataset Preparation**

### **Download Code**
```bash
git clone https://github.com/ZihaoChenz/Dinov2_Matching.git
```

### **Install Environment**
```bash
pip install -r requirement.txt
```

### **Prepare Dataset**

1. Place your **check dataset** in the directory: `data/(building)/check`
2. Place your **reference dataset** in the directory: `data/(building)/ref`
3. You can rename the building folder as per your requirement.

The file structure should be like this:

```plaintext
├── data
│   ├── building
│   │   ├── building1
│   │   │   ├── check
│   │   │   │   ├── img1.jpg
│   │   │   │   ├── img2.jpg
│   │   │   │   └── img3.jpg
│   │   │   ├── ref
│   │   │   │   ├── img4.jpg
│   │   │   │   ├── img5.jpg
│   │   │   │   └── img6.jpg
│   │   ├── south-building
│   │   │   ├── check
│   │   │   │   ├── img1.jpg
│   │   │   │   ├── img2.jpg
│   │   │   │   └── img3.jpg
│   │   │   ├── ref
│   │   │   │   ├── img4.jpg
│   │   │   │   ├── img5.jpg
│   │   │   │   └── img6.jpg
│   ├── surrounding
│   │   ├── Cyberport
│   │   │   ├── check
│   │   │   │   ├── img1.jpg
│   │   │   │   ├── img2.jpg
│   │   │   │   └── img3.jpg
│   │   │   ├── ref
│   │   │   │   ├── img4.jpg
│   │   │   │   ├── img5.jpg
│   │   │   │   └── img6.jpg
│   │   ├── HKU
│   │   │   ├── check
│   │   │   │   ├── img1.jpg
│   │   │   │   ├── img2.jpg
│   │   │   │   └── img3.jpg
│   │   │   ├── ref
│   │   │   │   ├── img4.jpg
│   │   │   │   ├── img5.jpg
│   │   │   │   └── img6.jpg
...
```

---

## **4. Inference Data**
If need to inference ZuBuD dataset:
Run a script to inference ZuBuD
```bash
python scripts/inference_ZuBuD.py
```
The output results after inference are saved to output/ZuBuD by default.

Else:
Run the following command to start the inference:
```bash
python inference.py --CheckFolder data/... --OutputFolder xxx/xxx
```
- **CheckFolder**: Path to the folder containing the check images
- **OutputFolder**: Path to save the output

Example:
```bash
python inference.py --CheckFolder data/building --OutputFolder output/building
```

After inference, the file structure will look like this:

```plaintext
├── output
│   ├── building
│   │   ├── building1
│   │   │   ├── check
│   │   │   │   ├── img1.txt
│   │   │   │   ├── img2.txt
│   │   │   │   └── img3.txt
│   │   │   ├── ref
│   │   │   │   ├── img4.txt
│   │   │   │   ├── img5.txt
│   │   │   │   └── img6.txt
│   │   ├── south-building
│   │   │   ├── check
│   │   │   │   ├── img1.txt
│   │   │   │   ├── img2.txt
│   │   │   │   └── img3.txt
│   │   │   ├── ref
│   │   │   │   ├── img4.txt
│   │   │   │   ├── img5.txt
│   │   │   │   └── img6.txt
│   ├── surrounding
│   │   ├── Cyberport
│   │   │   ├── check
│   │   │   │   ├── img1.txt
│   │   │   │   ├── img2.txt
│   │   │   │   └── img3.txt
│   │   │   ├── ref
│   │   │   │   ├── img4.txt
│   │   │   │   ├── img5.txt
│   │   │   │   └── img6.txt
│   │   ├── HKU
│   │   │   ├── check
│   │   │   │   ├── img1.txt
│   │   │   │   ├── img2.txt
│   │   │   │   └── img3.txt
│   │   │   ├── ref
│   │   │   │   ├── img4.txt
│   │   │   │   ├── img5.txt
│   │   │   │   └── img6.txt
```

---

## **5. Visualization (Normal Method)**

To visualize the results, use the following command:
```bash
python visualize.py --ImageType xxx --ResultFolder xxx/xxx --DataFolder xxx/xxx
```
- **ImageType**: Image format (e.g., `jpg`, `png`)
- **ResultFolder**: The folder where the inference results are saved
- **DataFolder**: The folder containing the original dataset images

You can convert the image format using `utils.convert_image_format.py` if needed.

Example:
```bash
python visualize.py --ImageType JPG --ResultFolder output/building/building1 --DataFolder data/building/building1
```

---

## **6. Centroid Method for Matching**

### **Create Embeddings**

To create embeddings, run:
```bash
python create_embedding.py --Embedding_target_folder xxx/xxx --Embedding_save_folder xxx/xxx
```
- **Embedding_target_folder**: Folder containing data to generate embeddings (e.g., `output/building`)
- **Embedding_save_folder**: Folder to save the generated embeddings (e.g., `embedding/building`)

### **Visualize (Centroid Method)**

```bash
python visualize.py --ImageType xxx --GalleryData xxx/xxx --CheckTxtFolder xxx/xxx --OutputBaseFolder xxx/xxx
```
- **GalleryData**: Path to the embedding data folder
- **CheckTxtFolder**: Path to the folder containing check `.txt` files
- **OutputBaseFolder**: Path to the base folder of the check images
- Use `--Normalize` to normalize features if necessary

Example:
```bash
python visualize.py --ImageType jpg --GalleryData embedding/surrounding --CheckTxtFolder output/surrounding/Cyberport/check --OutputBaseFolder output/surrounding
```
