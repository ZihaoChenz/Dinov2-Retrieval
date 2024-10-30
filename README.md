## **1. Introduction**

Dinov2 Image Retrieval: Retrieve the most similar images.
Including UI visualize and evaluation

---


## **2. Self-Dataset Preparation**

### **Download Code**
```bash
git clone https://github.com/ZihaoChenz/Dinov2_Retrieval.git
```

### **Install Environment**
```bash
pip install -r requirement.txt
```

### **Prepare Dataset**

1. Place your **check dataset** in the directory: `data/(surrounding)/check`
2. Place your **reference dataset** in the directory: `data/(surrounding)/ref`
3. You can rename the surrounding folder as per your requirement.

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

## **3. Inference Data**
Run the following command to start the inference:
```bash
python inference.py --CheckFolder data/... --OutputFolder xxx/xxx
```
- **CheckFolder**: Path to the folder containing the check images
- **OutputFolder**: Path to save the output

Example:
```bash
python inference.py --CheckFolder data/surrounding/surrounding1 --OutputFolder output/surrounding/surrounding2
```

After inference, the file structure will look like this:

```plaintext
├── output
│   ├── surrounding
│   │   ├── surrounding1
│   │   │   ├── check
│   │   │   │   ├── img1.txt
│   │   │   │   ├── img2.txt
│   │   │   │   └── img3.txt
│   │   │   ├── ref
│   │   │   │   ├── img4.txt
│   │   │   │   ├── img5.txt
│   │   │   │   └── img6.txt
│   │   ├── surrounding2
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

## **4. Visualization**

To visualize the results, use the following command:
```bash
python visualize.py --ImageType xxx --ResultFolder xxx/xxx --DataFolder xxx/xxx
```
- **ImageType**: Image format (e.g., `jpg`, `png`)
- **ResultFolder**: The folder where the inference results are saved
- **DataFolder**: The folder containing the original dataset images
- **GenerateTxtFolder**: The path that save all generated compare files similarity
- **Eval**: choose whether evaluate the dataset accuracy

You can convert the image format using `utils.convert_image_format.py` if needed.

Example:
```bash
python visualize.py --ImageType JPG --ResultFolder output/surrounding/surrounding1 --DataFolder data/surrounding/surrounding1 --GenerateTxtFolder txt_folder --Eval
```


## **5. Evaluation**
To evaluate accuracy, use the following command:
```bash
python evaluation.py --EvaluatedFolder xxx
```
- **EvaluatedFolder**: result similarity txt folder path

Example:
```bash
python evaluation.py --EvaluatedFolder result_similarity
```
