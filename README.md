# License-Plate-Recognition with YOLOv11 and OCR

This project is a **FastAPI-based web application** that detects license plates from images using the **YOLOv11** object detection model. The application reads and extracts the license plate text using Optical Character Recognition (OCR) and stores the results as text in an **SQL database** (SQLite/PostgreSQL). The app is designed to be scalable and containerized using **Docker Compose**.

---

## Features

- **License Plate Detection**: The YOLOv11 model (exported as an ONNX format) is used to detect license plates from input images.
- **OCR for Text Extraction**: The extracted license plate regions are processed using the `fast_plate_ocr` library to read and convert it to text.
- **Database Integration**: Stores extracted license plate text in an SQL database (SQLite/PostgreSQL).
- **Authentication & Authorization**: Secure endpoints with user authentication and role-based access control (RBAC).
- **Scalability with Docker Compose**: Easily deploy the entire application stack (FastAPI backend, database) using Docker Compose.
- **Model Training**: Training of the YOLOv11 model is performed using the **Ultralytics** library.

---

## Tech Stack
- **YOLOv11**: Object detection model in ONNX format for detecting license plates.
- **OCR**: fast_plate_ocr library.
- **FastAPI**: Python framework for building the API endpoints.
- **Database**: SQLite/PostgreSQL
- **Docker**: Containerization for deployment.
- **Python**: Backend language (Python 3.10).
- **ONNX Runtime**: Runtime for deploying ONNX models efficiently.

---


## Installation & Setup

### 1. Clone the Repository

```bash
   git clone https://github.com/jaykrshn/License-Plate-Recognition.git
   cd License-Plate-Recognition
   ```

### 2. Create a Python Environment

Create a new Python environment (recommended using `venv` or `conda`) and install the required dependencies. 
*Note: python 3.10 recommended*

```bash
# Create a new virtual environment
python3 -m venv .venv

# Activate the virtual environment

# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate

# Install required libraries
pip install -r requirements.txt
```

---
### 3. Train YOLO model for License plate detection

#### 1. Prepare your dataset in YOLO format (images and labels).

You can refer: [Roboflow dataset](https://universe.roboflow.com/new-workspace-ertfx/yolo-plate/dataset/4)

Keep your dataset of yolo format in  folder named 'dataset' in the root 

#### 2. Train model.
```bash
python train.py
```
This will creates a runs folder in the root with training results. You can find the trained model in runs/weights directory.

---

### 4. Test the App

First move the trained YOLO onnx model to app/trained_model dir

To test the FastAPI app, run the following command:

```bash
python uvicorn app.main:app --reload
```

The FastAPI application could be accessible from
   ```
   http://localhost:8000/docs
   ```
   Use the Swagger UI to test the endpoints. 

---

### 5. Dockerize the Application

You can containerize the app using Docker with following steps.

#### a) Build the Docker Image

Navigate to the root directory of the project and build the Docker image using the following command:

```bash
docker build -t license-plate-reading .
```

#### b) Run the Docker Container

Once the image is built, run the Docker container:

```bash
docker run -p 8000:8000 license-plate-reading 
```

This will start the FastAPI app inside a container and expose it on `http://127.0.0.1:8000/`.

---

### 6. Run App with PostgreSQL and Docker Compose


#### 1. Configuration

1. **Create a `.env` file**  
   In the root directory, create a file named `.env`. Refer to the `.env.example` file for guidance:  
   ```
   cp .env.example .env
   ```  
   Update the values in the `.env` file according to your configuration. Example keys include:  
   - `APP_PORT`  
   - `DB_USER`  
   - `DB_PASSWORD`  
   - `DB_DATABASE`  
   - `DB_HOST`  
   - `DB_PORT`  

---

#### 2. Modify Database Configuration

- Open the file **`app/database.py`**.
- Make the following changes:  
   - **Comment out lines 16 and 17**: These lines refer to the SQLite configuration.  
   - **Uncomment lines 13 and 14**: Update the PostgreSQL database URL and engine creation lines as follows:  

   ```python
   SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
   engine = create_engine(SQLALCHEMY_DATABASE_URL)
   ```  
---

#### 3. Run the Application

To build and start the containers, run the following command in the root directory:

```bash
docker-compose up
```

This will:

- Start a PostgreSQL container named **`license-plate-reading-db`** using the `postgres:17-alpine` image.  
- Start another container named **`license-plate-reading-app`** to run the application code.  
---
#### 4. Verify the Containers

You can check the running containers with:

```bash
docker ps
```
---
### 5. Access the Application:
   The FastAPI application by default will be available at: (change the port according to that given in .env file)
   ```
   http://localhost:8040/docs
   ```
   Use the Swagger UI to test the endpoints. 

---

#### Application Details

- **Database**: PostgreSQL 17 (Alpine)  
- **Backend**: Python with SQLAlchemy ORM  

---
#### Notes

- Stop the containers using `Ctrl+C` or:

   ```bash
   docker-compose down
   ```
- Ensure your `.env` file contains correct values to avoid connection issues.
---

That's it! The application should now be running successfully using Docker and PostgreSQL. 🚀
---
## Folder Structure

```
├── app/                           # Application source code
│   ├── trained_model/             # Directory to store machine learning models
│       ├── best.onnx              # ONNX file containing the trained YOLO model
│   ├── temp/                      # Directory to store temporary files (adjusted folder name for clarity)
│   ├── routers/                   # Directory containing API route definitions for various functionalities
│       ├── admin.py               # Routes for admin-related operations (e.g., managing system settings)
│       ├── auth.py                # Routes for authentication and authorization (e.g., login, JWT token)
│       ├── predict.py             # Routes for License Plate Recognition (LPR) predictions
│       ├── users.py               # Routes for user management (e.g., CRUD operations on users)
│   ├── main.py                    # Entry point for the FastAPI application
│   ├── database.py                # Database connection setup and ORM engine configuration
│   ├── models.py                  # SQLAlchemy models for database tables
│   ├── inference.py               # Script to perform inference on input images
│   ├── yolo_inference.py          # Script to perform object detection using the YOLO model
│
├── dataset/                       # Directory containing datasets used for model training and validation
│   ├── train                      # Training dataset
│       ├── images                 # Training images
│       ├── labels                 # Corresponding labels for training images
│   ├── valid                      # Validation dataset
│       ├── images                 # Validation images
│       ├── labels                 # Corresponding labels for validation images
│   ├── test                       # Test dataset
│       ├── images                 # Test images
│       ├── labels                 # Corresponding labels for test images
│   ├── data.yml                   # YOLO-specific configuration file specifying dataset paths
│
├── Dockerfile                     # Docker instructions to build the container for the FastAPI application
├── docker-compose.yml             # Docker Compose configuration for managing multi-container setups
├── .dockerignore                  # Specifies files and directories to exclude during Docker image build
├── .env                           # Environment variables for application configuration
│
├── requirements.txt               # List of required Python packages for production environment
├── requirements.dev.txt           # List of required Python packages for development and testing
│
└── README.md                      # Project documentation, setup instructions, and usage guide

```

---

**Happy Coding!** 💡
