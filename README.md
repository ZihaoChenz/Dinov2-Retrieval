## **1. Introduction**

Dinov2 Image Retrieval: Retrieve the most similar images.

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
git clone https://github.com/ZihaoChenz/Dinov2_Retrieval.git
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
│   ├── surrounding
│   │   ├── surrounding1
│   │   │   ├── check
│   │   │   │   ├── img1.jpg
│   │   │   │   ├── img2.jpg
│   │   │   │   └── img3.jpg
│   │   │   ├── ref
│   │   │   │   ├── img4.jpg
│   │   │   │   ├── img5.jpg
│   │   │   │   └── img6.jpg
│   │   ├── surrounding2
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

## **5. Visualization**

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


