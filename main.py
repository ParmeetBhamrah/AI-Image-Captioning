from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QFrame, QTextEdit
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import requests
import sys
import base64

class CaptionGeneratorThread(QThread):
    caption_generated = pyqtSignal(str)

    def __init__(self, image_path, user_description):
        super().__init__()
        self.image_path = image_path
        self.user_description = user_description

    def run(self):
        try:
            url = "http://localhost:11434/api/generate"
            headers = {"Content-Type": "application/json"}

            with open(self.image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")

            prompt = "Generate a catchy, Instagram-friendly caption for the image."
            if self.user_description:
                prompt = f"{prompt} The user describes it as: {self.user_description}."

            data = {
                "model": "llava-phi3:latest",
                "prompt": prompt,
                "stream": False,
                "images": [image_data]
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                caption = response.json().get("response", "No caption generated.")
            else:
                caption = f"Error: {response.text}"

        except Exception as e:
            caption = f"Failed to connect to Ollama: {e}"

        self.caption_generated.emit(caption)

class ImageCaptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.image_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AI Image Captioning")
        self.setGeometry(100, 100, 500, 450)

        self.label = QLabel("Upload an image to generate a caption!", self)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(500, 450)
        self.image_label.setStyleSheet("border: 1px solid gray;")

        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.clicked.connect(self.upload_image)

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Optional: Describe the image (e.g., 'This is my school')")

        self.generate_button = QPushButton("Generate Caption", self)
        self.generate_button.setEnabled(False)
        self.generate_button.clicked.connect(self.start_caption_generation)

        self.caption_frame = QFrame(self)
        self.caption_frame.setFrameShape(QFrame.Shape.Box)
        self.caption_frame.setLineWidth(2)
        self.caption_frame.setStyleSheet("padding: 10px;")

        self.caption_text_edit = QTextEdit(self.caption_frame)
        self.caption_text_edit.setReadOnly(True)
        self.caption_text_edit.setPlainText("Caption will appear here.")
        self.caption_text_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.caption_frame)

        self.caption_frame.setLayout(QVBoxLayout())
        self.caption_frame.layout().addWidget(self.caption_text_edit)

        self.setLayout(layout)

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label.setText("Image uploaded! Add an optional description and click 'Generate Caption'.")
            self.generate_button.setEnabled(True)

    def start_caption_generation(self):
        if not self.image_path:
            self.label.setText("Please upload an image first.")
            return

        self.label.setText("Generating Caption... Please wait.")
        self.generate_button.setEnabled(False)

        user_description = self.description_input.text().strip()
        self.thread = CaptionGeneratorThread(self.image_path, user_description)
        self.thread.caption_generated.connect(self.display_caption)
        self.thread.start()

    def display_caption(self, caption):
        self.caption_text_edit.setPlainText(caption)
        self.label.setText("Caption generated!")
        self.generate_button.setEnabled(True)

app = QApplication(sys.argv)
window = ImageCaptionApp()
window.show()
sys.exit(app.exec())