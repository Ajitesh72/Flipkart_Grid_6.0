


# Smart Vision Technology Quality Control(Flipkart Grid 6.0) 🚀

**Team Name:** dubeyajitesh07  
**Track Name:** Robotics Challenge  
**College/University:** Dwarkadas J. Sanghvi College of Engineering (DJSCE), Mumbai  
**Date:** 6th December 2024  

**Inventory Scanner:** https://inventory-scanning.dbbwrgx5bbx9c.amplifyapp.com/

(Credentials):

Email:athsankhe@gmail.com, Password:ath123

**Inventory Dashboard:** https://inventory-dashboard.d3eoyvmyg9b5y3.amplifyapp.com/


**Inventory Scanner Demo**

![WhatsApp Image 2024-12-07 at 14 41 35_be7530e1](https://github.com/user-attachments/assets/07a203cc-6495-47c1-8328-3e580d5cc0c6)


**Inventory Dashboard Demo**

![image](https://github.com/user-attachments/assets/21d1333a-5890-4277-b011-117f8a4bd939)

---

## 📋 Executive Summary

Ensuring high standards of product quality is crucial for brand reputation, customer satisfaction, and regulatory compliance. Traditional quality control methods often involve manual inspection, which is time-consuming, prone to human error, and difficult to scale.

**Key Benefits of Our Solution:**
- Reduced Cost
- Better Efficiency
- Increased Accuracy
- Enhanced Customer Satisfaction

---

## 🛠️ Proposed Solution

### Key Features:
1. **OCR Integration**: Accurately detects and extracts text from product labels.
2. **Object Detection and Classification**: Counts products and identifies key quality attributes.
3. **ML-based Freshness Classification**: Ensures product freshness.

---

## 🖥️ Technical Approach

### Application Overview:
1. **Scanner Application**: AI and CV algorithms automate quality inspection, identifying products and their attributes in real-time.
2. **Admin (Inventory) Dashboard**: Provides real-time analytics to enhance decision-making and inventory management.

### Base Model:
- **Model**: Qwen2VL-7B-Instruct  
- **Fine-Tuning Method**: QLoRA-8 bit  
- **Compute**: 2 x A100 4GB GPUs  

### Hyperparameters:
| Parameter       | Stage 1 | Stage 2 |
|-----------------|----------|---------|
| Epochs          | 15       | 20      |
| Batch Size      | 8        | 4       |
| Gradient Accum. | 8        | 4       |
| LR Scheduler    | Cosine   | ReduceLROnPlateau |

---

## 💾 Dataset and Codebase

- **Product Details** (Extracted from Flipkart Mart): [Dataset Link](https://drive.google.com/drive/u/0/folders/1SqKRgCrPiJo3BuzA9sP5YeTHPCoNNxWB)
- **Flipkart Product Details**: [Kaggle Link](https://www.kaggle.com/datasets/PromptCloudHQ/flipkart-products)
- **Fruits and Vegetables Freshness**: [Kaggle Link](https://www.kaggle.com/datasets/muhriddinmuxiddinov/fruits-and-vegetables-dataset)
- **Codebase**: [GitHub Repository](https://github.com/Ajitesh72/Flipkart_Grid_6.0)

---

## 🔗 Live Links

- **Scanner Web Link**: [Scanner Link](https://inventory-scanning.dbbwrgx5bbx9c.amplifyapp.com/)  
- **Admin Dashboard**: [Dashboard Link](https://inventory-dashboard.d3eoyvmyg9b5y3.amplifyapp.com/)  

---

## ⚙️ Tech Stack and System Requirements

### Tech Stack:
- **Frontend**: React, Tailwind CSS, Material-UI
- **Backend**: Node.js, Flask
- **Cloud**: AWS (Amplify, DynamoDB, S3, EC2)
- **Models**: Qwen2 7B, YOLO, GoogleNet, SVM

### System Requirements:
- **Hardware**: 1 x A100 4GB GPU (Recommended: 2 x A100 4GB)
- **Software**: Python 3.8+, Node.js 16+, PyTorch 1.12+, TensorFlow 2.8+

---

## 📊 Application Demo

Check out the [demo video](https://docs.google.com/file/d/1STmaKN67HQ5qhONIzjDxvkorOPxc9-Up/preview) showcasing the system in action!

---

## 👥 Team Members
- **Ajitesh Dubey** - Web Developer  
- **Siddharth Adak** - ML Developer  
- **Atharva Sankhe** - ML Developer

---


