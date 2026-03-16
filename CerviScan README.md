# CerviScan — Cervical Cancer CT Scan Analyser

A desktop application that uses a U-Net deep learning model to automatically detect and highlight potential cancerous regions in cervical CT scan images.

> ⚠️ **Medical Disclaimer:** This tool is a proof-of-concept built for academic purposes. It is **not** a certified medical device and should **not** be used for clinical diagnosis. Always consult a qualified medical professional.

---

## Overview

CerviScan takes a folder of CT scan images (`.jpg` / `.jpeg`), runs them through a trained U-Net segmentation model, and outputs copies of the images with potential tumour regions circled in blue. The entire pipeline runs locally — no data is sent to any server.

The project was developed as part of academic coursework at Babeș-Bolyai University.

---

## Features

- 🔍 **Automated tumour detection** — U-Net model segments potential cancerous regions from grayscale CT scans
- 🔵 **Visual highlighting** — detected regions are outlined with bounding circles on the original image
- 🖥️ **Desktop GUI** — clean CustomTkinter interface, no command line required
- 📁 **Batch processing** — scan an entire folder of images in one run with a live progress bar
- 💾 **Export results** — processed images saved directly to a chosen output folder
- 📬 **Contact page** — built-in help/contact screen for support queries

---

## How It Works

### Model Architecture — U-Net
The core of CerviScan is a U-Net convolutional neural network, a widely used architecture for biomedical image segmentation.

```
Input (256x256 grayscale)
    │
    ├── Encoder
    │     Conv2D(64) → Conv2D(64) → MaxPool
    │     Conv2D(128) → Conv2D(128) → MaxPool
    │
    ├── Bottleneck
    │     Conv2D(256) → Conv2D(256)
    │
    └── Decoder
          Conv2DTranspose(128) + skip connection → Conv2D(128)
          Conv2DTranspose(64)  + skip connection → Conv2D(64)
          Conv2D(1, sigmoid) → Output mask
```

### Prediction Pipeline
1. Image is loaded and resized to **256×256**
2. Converted to grayscale and normalised to `[0, 1]`
3. U-Net predicts a binary segmentation mask (threshold: `0.5`)
4. Contours are extracted from the mask using OpenCV
5. A minimum enclosing circle is drawn around each contour with area > 100px²

### Training
The model was trained on annotated cervical CT scan data. Annotations were stored in CSV format with circle coordinates (`cx`, `cy`, `r`, `rx`, `ry`) per image. The `MaskCreator` module parses these annotations and generates binary training masks. Training used:
- **Optimiser:** Adam (`lr=0.001`)
- **Loss:** Binary cross-entropy
- **Epochs:** 50
- **Train/val split:** 80/20

---

## Tech Stack

| Layer | Technology |
|---|---|
| GUI | Python, CustomTkinter |
| ML Model | TensorFlow / Keras |
| Image Processing | OpenCV, NumPy, Pillow |
| Data Handling | Pandas, CSV |
| Model Format | `.keras` |

---

## Project Structure

```
CervicalCancerScanner/
├── frontend/
│   ├── main_frontend.py          # App entry point
│   ├── assets/                   # Images and icons
│   ├── pages/
│   │   ├── WelcomePage.py        # Landing screen
│   │   ├── ScanMenuPage.py       # Main scan interface
│   │   └── ContactPage.py        # Help / contact screen
│   └── model/
│       ├── UNETModel.py          # Model loading & prediction logic
│       ├── trainModel.py         # U-Net architecture & training script
│       ├── MaskCreator.py        # Annotation CSV → binary mask converter
│       └── unet_cervical.keras   # Pre-trained model weights
└── requirements.txt
```

---

## Installation & Usage

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/CervicalCancerScanner.git
cd CervicalCancerScanner

# Install dependencies
pip install -r requirements.txt

# Additional dependencies for model inference (not in requirements.txt)
pip install tensorflow opencv-python numpy
```

### Running the App

```bash
cd frontend
python main_frontend.py
```

### Using the App
1. Click **Continue** on the welcome screen
2. **Browse** to select the folder containing your CT scan images (`.jpg`/`.jpeg`)
3. **Browse** to select an output folder for processed results
4. Click **Start Scan** — a progress bar will track the job
5. Click **See Result** when done to open the output folder

---

## Retraining the Model

To retrain on your own annotated data:

1. Prepare a CSV annotation file with columns including shape details (`cx`, `cy`, `r`/`rx`/`ry`)
2. Update the `IMAGE_DIR` and `MASK_DIR` paths in `trainModel.py`
3. Run:

```bash
cd frontend/model
python trainModel.py
```

The trained model will be saved as `unet_cervical.keras`.

---

## Known Limitations

- Currently processes `.jpg` and `.jpeg` only (no DICOM support)
- Absolute file paths hardcoded in `UNETModel.py` and `trainModel.py` — update before running
- Model accuracy is dependent on training data volume and quality
- No zoom/pan in result viewer — results must be opened in an external viewer

## License

This project is for academic and educational purposes only.
