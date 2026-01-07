# 🛰️ **Satellite Imagery–Based Property Valuation**
*A multimodal machine learning system that enhances house price prediction by selectively integrating satellite imagery with structured housing data.*

---

## 📌 **Project Overview**

This project develops a **multimodal regression pipeline** that combines:
- 📊 **Tabular housing data**
- 🖼️ **Satellite imagery**

To ensure robustness and prevent overfitting, satellite imagery is incorporated using a **residual learning strategy**, where images are used **only to correct high-error predictions** produced by a strong tabular baseline model.

---

## 🎯 **Objectives**

- Predict residential property prices using tabular housing data  
- Fetch satellite images programmatically using latitude–longitude coordinates  
- Extract visual features using convolutional neural networks (CNNs)  
- Improve generalization through residual-based multimodal learning  
- Interpret image influence on predictions using Grad-CAM  
- Compare performance between:
  - Tabular-only model  
  - Tabular + satellite imagery model  

---

## 🗂️ **Dataset Description**

### 📊 **Tabular Data**
- **Source:** Provided dataset (`train.xlsx` and `test.xlsx`)
- **Files:**
  - `train.xlsx` — includes target variable (`price`)
  - `test.xlsx` — used for final prediction generation

**Key Features:**
- `bedrooms`, `bathrooms`, `sqft_living`, `sqft_lot`
- `floors`, `waterfront`, `view`, `condition`, `grade`
- `sqft_above`, `sqft_basement`
- `yr_built`, `yr_renovated`
- `lat`, `long`
- Neighborhood context: `sqft_living15`, `sqft_lot15`

**Target Variable:**
- `price` (modeled as `log1p(price)` during training)

---

### 🖼️ **Visual Data**
- **Source:** Mapbox Static Images API  
- **Documentation:** https://docs.mapbox.com/api/maps/static-images/

**Image Specifications:**
- Resolution: `224 × 224`
- Zoom level optimized for neighborhood context
- Images fetched **only for high-residual training samples**

---

## 🧠 **Modeling Strategy**

### 1️⃣ **Baseline Tabular Model**
- Algorithm: **Gradient Boosting Regressor**
- Target transformation: `log1p(price)`
- Feature scaling using **StandardScaler**
- Provides a strong predictive baseline

---

### 2️⃣ **Residual Learning (Key Innovation)**
- Identify top **33–35% high-residual samples**
- Satellite imagery used **only for difficult cases**
- Prevents unnecessary noise injection and overfitting

---

### 3️⃣ **Image Feature Extraction**
- CNN Backbone: **ResNet-18 (Pretrained)**
- Feature embedding size: `512`
- Dimensionality reduction using **PCA (75 components)**

---

### 4️⃣ **Multimodal Fusion**
Final prediction is computed as:

Final Price = Baseline Prediction + Image-Based Residual Correction

This late-fusion approach ensures stability and interpretability.

---

### 5️⃣ **Model Explainability**
- **Grad-CAM** applied to the last convolutional layer
- Visual explanations highlight:
  - Green cover
  - Road density
  - Urban layout
  - Proximity to water bodies

---

## 📈 **Results Summary**

| Model Type                         | Outcome |
|----------------------------------|---------|
| Tabular Only (Baseline)           | Strong predictive performance |
| Tabular + Satellite (Residual)    | Improved generalization on hard cases |

📌 Satellite imagery contributes **incremental value** when applied selectively through residual learning.

---

## 🗂️ Repository Structure

satellite-property-valuation/


├── Data/

├── train.xlsx

└── test.xlsx

├── satellite_images/

└── residual_train/

├── notebooks/

├── preprocessing.ipynb

├── baseline_model.ipynb

├── multimodal_residual.ipynb

└── gradcam_visualization.ipynb

├── data_fetcher_residuals.py

├── baseline_model.pkl

├── scaler.pkl

├── final_predictions.csv

├── README.md

└── report.pdf

---

## ⚙️ **Tech Stack**

- **Data Handling:** Pandas, NumPy  
- **Machine Learning:** Scikit-learn  
- **Deep Learning:** PyTorch, Torchvision  
- **Image Processing:** PIL  
- **Visualization:** Matplotlib  
- **Explainability:** Grad-CAM  
- **API Services:** Mapbox Static Images API  

---

## 🚀 **How to Run the Project**

Execute the following notebooks sequentially to complete the full pipeline:
- `preprocessing.ipynb`
- `baseline_model.ipynb`
- `multimodal_residual.ipynb`
- `gradcam_visualization.ipynb`

## **By: Chesta Tiwari**
