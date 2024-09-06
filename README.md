# rpi5-opencv-face-recognition

一个用 OpenCV 和`face_recognition`库在树莓派5上进行人脸识别的小项目，包含一个 WebUI。

## 项目结构

- `hardwareBackend.py`：该脚本处理面部识别的后台操作，包括加载已知人脸、编码新的人脸以及从摄像头捕捉照片。
- `app.py`：一个Flask Web应用程序，提供与面部识别系统交互的Web界面。
- `templates/index.html`：Web界面的HTML模板。
- `static/style.css`：用于Web界面样式的CSS文件。
- `static/script.js`：处理客户端交互的JavaScript文件。

## 安装与设置

1. **克隆仓库：**
   ```bash
   git clone https://github.com/yourusername/rpi5-opencv-face-recognition.git
   cd rpi5-opencv-face-recognition
   ```

2. **安装所需依赖：**

   ```bash
   sudo apt install build-essential cmake libgtk-3-dev libboost-all-dev
   sudo apt install python3-opencv python3-flask
   pip install numpy==1.26.0 face_recognition --break-system-packages   # 注意 numpy 需安装 1.x 版本，以及安装时需要加 --break-system-packages
   ```

3. **运行Flask应用程序：**
   ```bash
   python app.py
   ```

4. **访问Web界面：**
   打开浏览器，访问`http://<your-raspberry-pi-ip>:5000`。

## 使用说明

### Web界面

1. **视频流：**
   - 主页面显示来自树莓派摄像头的实时视频流。

2. **上传新的人脸：**
   - 输入人的名字并点击“Upload new face”以上传新的人脸图像。

3. **拍照：**
   - 输入人的名字并点击“Take a photo”以使用树莓派摄像头捕捉照片。

4. **重新加载现有的人脸：**
   - 点击“Reload exsiting faces”以重新加载本地目录中的所有已知人脸。

### API端点

- `/video_feed`：提供实时视频流。
- `/upload_faces` (POST)：上传新人脸图像。
- `/reload_faces` (POST)：重新加载所有已知人脸。
- `/take_photo` (POST)：使用树莓派摄像头捕捉新照片。

## 注意事项

- 确保摄像头已正确连接并配置。
- 人脸默认存储在 `/home/powerfullz/face/faces` 目录中，这显然对大多数人不适用，当然，你可以修改程序的行为。

## 许可证

该项目采用MIT许可证。有关更多详情，请参见[LICENSE](LICENSE)文件。