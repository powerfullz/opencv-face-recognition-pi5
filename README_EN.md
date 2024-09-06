# rpi5-opencv-face-recognition

A small face recognition project using OpenCV and the `face_recognition` library on a Raspberry Pi 5.

## Project Structure

- `hardwareBackend.py`: This script handles the backend operations of face recognition, including loading known faces, encoding new faces, and capturing photos from the camera.
- `app.py`: A Flask web application that provides a web interface to interact with the face recognition system.
- `templates/index.html`: HTML template for the web interface.
- `static/style.css`: CSS file for styling the web interface.
- `static/script.js`: JavaScript file for handling client-side interactions.

## Installation and Setup

1. **Clone the repository:**
   
   ```bash
   git clone https://github.com/yourusername/rpi5-opencv-face-recognition.git
   cd rpi5-opencv-face-recognition
   ```

2. **Install the required dependencies:**
   
   Temporarily increase swap size:

   ```bash
   sudo nano /etc/dphys-swapfile

   < change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=1024 and save / exit nano >

   sudo /etc/init.d/dphys-swapfile restart
   ```

   Install dlib build dependencies:

   ```bash
   sudo apt install build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-pip \
    zip
   ```

   Finally, install dependencies for this project:
   
   ```bash
   sudo apt install python3-opencv python3-flask
   pip install numpy==1.26.0 face_recognition --break-system-packages   # Note: numpy needs to be installed in version 1.x, and the installation requires the --break-system-packages flag
   ```

3. **Run the Flask application:**
   
   ```bash
   python app.py
   ```

4. **Access the web interface:**
   
   Open a browser and visit `http://<your-raspberry-pi-ip>:5000`.

## Usage Instructions

### Web Interface

1. **Video Stream:**
   - The main page displays a real-time video stream from the Raspberry Pi camera.

2. **Upload a New Face:**
   - Enter the person's name and click "Upload new face" to upload a new face image.

3. **Take a Photo:**
   - Enter the person's name and click "Take a photo" to capture a photo using the Raspberry Pi camera.

4. **Reload Existing Faces:**
   - Click "Reload existing faces" to reload all known faces from the local directory.

### API Endpoints

- `/video_feed`: Provides the real-time video stream.
- `/upload_faces` (POST): Uploads new face images.
- `/reload_faces` (POST): Reloads all known faces.
- `/take_photo` (POST): Captures a new photo using the Raspberry Pi camera.

## Notes

- Ensure the camera is properly connected and configured.
- Faces are stored by default in the `/home/powerfullz/face/faces` directory, which may not be suitable for most users. You can modify the program's behavior to change this.

## License

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.