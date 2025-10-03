# Nimbus File Sharing

Nimbus is a web application designed for quick and easy file sharing. It allows both anonymous and authenticated users to upload files and generate shareable links. The project is built with Django and utilizes MinIO for S3-compatible object storage.

---

## ✨ Key Features

* **Anonymous Uploads**: Quickly upload a file without an account.Files uploaded by anonymous users are automatically set to expire in 7 days.
* **User Authentication**: A complete user registration and login/logout system.
* **Authenticated Dashboard**: Logged-in users have a personal dashboard to view and manage their uploaded files.
* **Customizable Uploads**: Authenticated users can set a custom title and expiry date for their files.
* **Secure File Storage**: Integrates with MinIO for robust, S3-compatible file storage.
* **Direct Download Links**: Each uploaded file gets a unique, shareable link for easy downloading and sharing.
* **Responsive Frontend**: A clean and modern user interface built with HTML, JavaScript, and Bootstrap.

---

## 🎬 Features in Action

### 🚀 Instant & Anonymous Uploads

Quickly upload a file without needing an account. Get a shareable link in seconds. Files are automatically set to expire in 7 days.

![nimbus_1](https://github.com/user-attachments/assets/0e101874-103f-4f65-b1bd-f485842d7fce)

### 👤 Role-Based Views

The application provides a streamlined experience for both guests and registered users. Logged-in users get access to a personal dashboard to manage their files, while guests see a direct upload form.

![nimbus_2](https://github.com/user-attachments/assets/2a4f1914-dc43-4d38-98d5-b82fcc35af0b)

### ⚙️ Customizable Uploads for Users

Registered users can add a custom title and set a specific expiry date for their files, giving them more control over their shared content.

![nimbus_3](https://github.com/user-attachments/assets/9af89491-533b-4c8e-9b0d-b1fd0b18e398)

---

## 🛠️ Tech Stack

* **Backend**: Django
* **Database**: PostgreSQL
* **File Storage**: MinIO (S3 Compatible) 
* **Frontend**: HTML, Bootstrap, JavaScript and Django Template Language
* **Key Python Libraries**:
    * `django-storages` & `boto3` for MinIO integration.
    * `psycopg2-binary` for PostgreSQL connection.

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.x
* Docker and Docker Compose

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/thebigby10/Nimbus.git
    cd thebigby01-nimbus
    ```

2.  **Create a virtual environment and activate it**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Start the external services (PostgreSQL & MinIO) using Docker:**

    * **Start PostgreSQL:**
        ```bash
        docker run --name nimbus-postgres-db -d \
                    -p 5432:5432 \
                    -e POSTGRES_USER=admin \
                    -e POSTGRES_PASSWORD=12345678 \
                    -e POSTGRES_DB=nimbus_db \
                    -v postgres_data:/var/lib/postgresql/data \
                    postgres:14-alpine
        ```
    * **Start MinIO:**
        ```bash
        docker run -d \
           -p 9000:9000 \
           -p 9001:9001 \
           --name minio-server \
           -v ./minio-data:/data \
           -e "MINIO_ROOT_USER=admin" \
           -e "MINIO_ROOT_PASSWORD=12345678" \
           minio/minio server /data --console-address ":9001"
        ```

5.  **Configure MinIO Bucket:**
    * Navigate to the MinIO console at `http://localhost:9001`.
    * Log in with the credentials `admin` and `12345678`.
    * Create a new bucket named `nimbus-upload-bucket`.

6.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000`.

---

## 📂 Project Structure

The project follows a standard Django structure:
```
└── thebigby10-nimbus/
    ├── Nimubus/          # Main Django project configuration (settings.py, urls.py)
    ├── file_shareapp/    # App for core file sharing logic (models, views, forms)
    ├── user_auth/        # App for user registration and authentication
    ├── templates/        # Contains all HTML templates for the project
    ├── requirements.txt  # Project dependencies
    ├── manage.py         # Django's command-line utility
    └── docker_commands   # Commands to start services
```
