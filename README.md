# WelVision YOLO Data Labeller

## Project Description
The **WelVision YOLO Data Labeller** is a robust desktop application designed to streamline the process of labeling images for computer vision object detection tasks. Leveraging the power of **YOLOv8** for smart auto-labeling and offering seamless integration with **Roboflow**, this tool provides a comprehensive solution for managing datasets, annotating images, and preparing data for model training. The application features a user-friendly GUI built with Tkinter and uses a MySQL backend for efficient data management.

---

## Project Details

### Problem Statement
Creating high-quality datasets for object detection is often a labor-intensive and manual process. Developers and researchers face challenges in managing local datasets, ensuring consistent annotations, and syncing data with cloud platforms. This project addresses these issues by providing a unified interface for labeling, previewing, and uploading datasets.

### key Features
- **Smart Auto-Labeling:** utilization of YOLOv8 models to automatically detect and annotate objects, significantly reducing manual effort.
- **Dataset Preview:** Visual inspection of datasets with support for COCO and YOLO formats, allowing users to verify annotations overlayed on images.
- **Database Management:** A local MySQL database tracks AI models, datasets, and image counts, ensuring organized data persistence.
- **Roboflow Integration:** Built-in module to upload local datasets directly to Roboflow projects, supporting both individual image uploads and workspace uploads.
- **GUI Interface:** A comprehensive Tkinter-based desktop interface with tabs for Labeling, Previewing, and Uploading.

### Labeling Workflow
1.  **Load Images:** Import images from local directories.
2.  **Auto-Label:** Apply a selected YOLOv8 model to generate initial bounding boxes.
3.  **Refine:** Manually adjust or add annotations using the visual editor.
4.  **Save:** Persist annotations in standard formats (YOLO/COCO).

### Integration
The application bridges the gap between local development and cloud operations by integrating the **Roboflow SDK**. This allows users to:
- List and create Roboflow projects.
- Upload datasets with automatic format conversion.
- Sync versions for training.

---

## Tech Stack
- **Language:** Python 3.x
- **GUI Framework:** Tkinter
- **Database:** MySQL
- **AI/ML:** YOLOv8 (Ultralytics), Roboflow SDK
- **Image Processing:** Pillow (PIL)
- **Utilities:** PyYAML, mysql-connector-python

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/DCode-v05/Welvision-Auto-Labeller.git
cd Welvision-Auto-Labeller
```

### 2. Database Setup
Ensure you have a MySQL server running locally.
1.  Open `config.py`.
2.  Update the `DATABASE_CONFIG` dictionary with your MySQL credentials, specifically the `password`.
    ```python
    DATABASE_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'YOUR_PASSWORD',  # Update this
        'database': 'welvision_db',
        'port': 3306
    }
    ```

### 3. Install dependencies
Install the required Python packages:
```bash
pip install ultralytics roboflow mysql-connector-python pillow pyyaml
```

### 4. Run the Application
Launch the main application entry point:
```bash
python main.py
```
*Note: On the first run, the application will attempt to create the necessary database and tables automatically.*

---

## Usage
- **Labeling Tab:** Select a model and dataset to start labeling images. Use the "Auto Label" feature to let YOLOv8 suggest annotations.
- **Dataset Preview:** Browse through existing datasets to verify the quality of annotations.
- **Roboflow Upload:** Switch to the Upload tab, authenticate with your Roboflow API key, and push your prepared datasets to the cloud.
- **Settings:** Configure default paths and display preferences in `config.py`.

---

## Project Structure
```
Welvision-Auto-Labeller/
│
├── main.py                    # Application entry point
├── yolo_labeler_app.py        # Core GUI application logic
├── config.py                  # Configuration settings (DB, paths, YOLO)
├── database_manager.py        # MySQL database interactions
├── roboflow_manager.py        # Roboflow API wrapper and upload logic
├── dataset_manager.py         # Local dataset directory management
├── gui_components.py          # Reusable Tkinter GUI widgets
├── image_utils.py             # Image processing helper functions
├── create_database.sql        # SQL schema script (reference)
└── README.md                  # Project documentation
```

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request describing your changes.

---

## Contact
- **GitHub:** [DCode-v05](https://github.com/DCode-v05)
- **Email:** denistanb05@gmail.com
