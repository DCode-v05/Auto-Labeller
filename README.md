# Auto-Labeller

**A desktop tool that pre-labels object-detection images with a YOLOv8 model, lets you fix the boxes by hand, and ships the result to a YOLO/COCO dataset or straight to Roboflow.**

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![Tkinter](https://img.shields.io/badge/Tkinter-3776AB?style=flat&logo=python&logoColor=white) ![Ultralytics YOLOv8](https://img.shields.io/badge/YOLOv8-00FFFF?style=flat&logo=ultralytics&logoColor=black) ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white) ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white) ![Roboflow](https://img.shields.io/badge/Roboflow-6706CE?style=flat&logo=roboflow&logoColor=white) ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white) ![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat)

## Overview

Hand-labelling images for object detection is slow and repetitive. Every box has to be drawn, every class assigned, and the dataset has to end up in the exact directory layout a trainer expects. Auto-Labeller cuts most of that out: you point it at an existing YOLOv8 model, drop in a folder of images, and it runs inference to draw the first pass of bounding boxes for you. You then review and correct, name the result, and save it as a proper YOLOv8 dataset — or push it to Roboflow without leaving the app.

I built this at **iQube** as the data-preparation half of the WelVision roller-inspection project. WelVision's runtime station runs YOLO defect models on a factory line; this tool closes the loop behind it — raw inspection images get auto-labelled here, exported as a versioned dataset, and used to (re)train the models that go back into the inspection station. It's a Tkinter desktop app with a MySQL backend that keeps a registry of which models and datasets exist.

## Key Features

- **Auto-labelling with YOLOv8** — load any Ultralytics `.pt` model and let it generate the first set of bounding boxes for every image, so you start from suggestions instead of a blank canvas.
- **Three working tabs** — Image Labeling (load model + images, run inference, edit), Dataset Preview (browse saved datasets and verify annotations), and a Roboflow Projects view (hidden by default, switched on in code).
- **Model management** — register YOLO model files in MySQL with name/path/description; the app only lists models whose weight files actually still exist on disk.
- **Dataset management** — create a brand-new dataset or add labelled images to an existing one, with live name-availability checking so you don't clobber a dataset that's already there.
- **Manual refinement** — draw, move, and adjust boxes on an interactive canvas with zoom (mouse-wheel) and per-box class labels.
- **Split / comparison views** — flip between Split View, Raw Only, and Labeled Only, plus a side-by-side image comparison to sanity-check what the model drew against the original.
- **Standards-correct export** — writes YOLOv8 layout (`images/`, `labels/`, `data.yaml`, `classes.json`) with normalised coordinates, and converts YOLO annotations to COCO `annotations.json` on demand.
- **Roboflow sync** — upload a finished dataset two ways: image-by-image (with YOLO→Roboflow annotation conversion and a live progress callback) or as a single COCO workspace upload; also list, create, and download projects.
- **Device auto-detection** — picks CUDA, then Apple Silicon MPS, then CPU; runs a real CUDA test tensor before trusting the GPU and auto-retries on CPU if it hits a GPU out-of-memory error mid-run.
- **Threaded batch inference** — labelling runs on a background thread so the UI stays responsive while a folder of images is processed.
- **One-click launcher** — `run_labeler.bat` checks Python, installs missing packages, warns if the DB password isn't set, and starts the app.

## How It Works

The app is one Tkinter window (`YOLOLabelerApp`, a `tk.Tk` subclass) with a `ttk.Notebook` holding the tabs. The heavy GUI logic lives in `yolo_labeler_app.py` (~330 KB, ~116 methods), and the supporting concerns are split into focused manager modules so the inference, dataset, database, and Roboflow code each stand on their own.

### 1. Model loading and device selection

`YOLOModelManager` wraps Ultralytics `YOLO`. On startup it detects the best device: it checks `torch.cuda.is_available()`, allocates a throwaway `640×640` tensor to confirm CUDA actually works, and reports GPU name/memory/count. If there's no working NVIDIA GPU it falls back to Apple MPS, and finally to CPU (reporting core count and RAM via `psutil`). When you load a model the weights are moved to that device.

### 2. Auto-labelling pass

`safe_yolo_inference()` runs the model over each image with the configured confidence threshold (default `0.25`), IoU threshold (`0.45`), and max detections (`1000`). The wrapper catches `torch.cuda.OutOfMemoryError`, clears the CUDA cache, moves the model to CPU, and re-runs the same image — so a single oversized image can't kill a whole batch. The batch loop runs on a `threading.Thread` and stores its detections in a temporary in-memory structure until you decide to save.

### 3. Review and correct

Detected boxes render on an `ImageCanvas` with class labels and colours. You can add or adjust boxes; helper math in `AnnotationUtils` converts between YOLO normalised coords, absolute pixel boxes, and COCO `[x, y, w, h]`, and includes IoU calculation plus an overlap filter (NMS-style) to drop duplicate boxes. The comparison views let you eyeball the labelled result against the raw image before committing.

### 4. Dataset export

`DatasetManager` builds the standard YOLOv8 folder (`images/` + `labels/`), writes a `data.yaml` (`path`, `train`, `val`, `nc`, `names`) and a `classes.json`, copies images in, and writes one `.txt` label file per image with normalised coordinates. `convert_yolo_to_coco()` reads `data.yaml` and every label file, pulls real image dimensions with Pillow, and emits a COCO `annotations.json` (images, annotations, categories) — which is what the Roboflow workspace upload path consumes. A `validate_dataset_structure()` check confirms the required files and folders are present before anything downstream trusts the dataset.

### 5. Persistence

`DatabaseManager` (mysql-connector-python) talks to a `welvision_db` MySQL database with two tables, `ai_models` and `datasets`. On first run `check_and_create_database()` creates the database and tables automatically if they're missing. Models and datasets are soft-deleted via an `is_active` flag rather than hard-deleted, and `get_models()` filters out any model whose file path no longer exists so the UI never offers a model you can't load.

### 6. Roboflow upload

`RoboflowManager` initialises the Roboflow SDK from an API key and exposes the workspace. `upload_dataset_individual()` walks the images, finds each matching `.txt` label, converts it to Roboflow's format, and uploads with a per-image progress callback; `upload_dataset_workspace()` does a single COCO upload with a timestamped batch name. It can also list/create projects and download a dataset back in `yolov8` format.

## Tech Stack

- **Language:** Python 3.8+
- **GUI:** Tkinter / ttk (Notebook, Canvas), custom reusable widgets in `gui_components.py`
- **ML / CV:** Ultralytics YOLOv8, PyTorch (CUDA / MPS / CPU), OpenCV, Pillow
- **Dataset / formats:** YOLOv8 layout, COCO JSON, PyYAML (`data.yaml`), Roboflow SDK
- **Data:** MySQL (`mysql-connector-python`) — model & dataset registry
- **Tooling:** `run_labeler.bat` launcher, `psutil` for device/system info

## Getting Started

### Prerequisites
- Python 3.8+
- A running MySQL server (local is fine)
- An NVIDIA GPU is optional — it falls back to CPU
- A Roboflow API key, only if you want to use the upload features

### Installation
```bash
git clone https://github.com/DCode-v05/Auto-Labeller.git
cd Auto-Labeller
pip install ultralytics roboflow mysql-connector-python opencv-python pillow pyyaml torch
```

Set your MySQL password in `config.py` (the `DATABASE_CONFIG['password']` field). The database and tables are created automatically on first launch, or you can run `create_database.sql` yourself.

### Running
```bash
python main.py
```
On Windows you can use the launcher instead, which checks dependencies and DB config first:
```bash
run_labeler.bat
```

## Usage

1. **Register a model** — in the Image Labeling tab, browse to a YOLOv8 `.pt` file and load it. The console prints the device it landed on.
2. **Add images** — upload individual images or a whole folder.
3. **Start Labeling** — the model runs over the images on a background thread and draws suggested boxes.
4. **Review** — use Split View / Raw Only / Labeled Only and the comparison view to check the boxes; adjust or add any that are wrong.
5. **Save** — create a new dataset (name is checked for availability) or add to an existing one. The YOLOv8 folder, `data.yaml`, and `classes.json` are written for you.
6. **Preview** — the Dataset Preview tab lists saved datasets with image/label counts so you can re-verify annotations later.
7. **Upload (optional)** — enable the Roboflow tab, enter your API key, pick or create a project, and push the dataset (per-image or COCO workspace).

YOLO confidence/IoU/max-detection thresholds and the default datasets path are configurable in `config.py`.

## Project Structure

```
Auto-Labeller/
├── main.py                 # Entry point — launches the Tkinter app
├── yolo_labeler_app.py     # Main GUI: tabs, canvas, labelling/preview/upload flows (~116 methods)
├── yolo_model_manager.py   # YOLOv8 load + device detection + safe inference w/ CPU fallback
├── dataset_manager.py      # YOLOv8 dataset creation, YOLO->COCO conversion, validation
├── database_manager.py     # MySQL CRUD for ai_models / datasets, auto DB+table creation
├── roboflow_manager.py     # Roboflow SDK: list/create/upload (per-image + COCO)/download
├── gui_components.py       # Reusable widgets: StatusBar, ImageCanvas, selection frames
├── image_utils.py          # Image processing + annotation math (YOLO/COCO/IoU/NMS)
├── config.py               # DB, app, file, and YOLO settings
├── create_database.sql     # SQL schema (reference)
├── create_db_train.py      # DB setup helper
├── run_labeler.bat         # Windows launcher (checks Python/deps/DB)
├── test.py                 # Scratch/test script
├── LICENSE                 # MIT
└── README.md
```

---

## Contact

**Portfolio:** [Denistan](https://www.denistan.me)<br>
**LinkedIn:** [Denistan](https://www.linkedin.com/in/denistanb)<br>
**GitHub:** [DCode-v05](https://github.com/DCode-v05)<br>
**LeetCode:** [Denistan_B](https://leetcode.com/u/Denistan_B)<br>
**Email:** [denistanb05@gmail.com](mailto:denistanb05@gmail.com)

Made with ❤️ by **Denistan B**
