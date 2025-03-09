# AI Image Captioning Tool

## Overview

The **AI Image Captioning Tool** is a desktop application built with PyQt6 that allows users to upload images and generate AI-powered captions. The tool leverages a locally hosted **LLaVA-Phi3** model via Ollama to generate creative and Instagram-friendly captions.

## Features

- 📷 **Upload Images**: Supports common image formats like PNG, JPG, JPEG, BMP, and GIF.
- 📝 **User Input**: Optionally describe the image to influence the generated caption.
- 🤖 **AI-Powered Captions**: Uses a local LLaVA-Phi3 model to generate catchy captions.
- 🎨 **Responsive UI**: Built with PyQt6 for a clean and user-friendly interface.
- 🚀 **Offline Capability**: Runs completely on your local machine without external API dependencies.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.9+
- Ollama (for running LLaVA-Phi3 locally)
- Required Python libraries:

```sh
pip install PyQt6 requests
```

### Running the Application

1. Start the Ollama server with LLaVA-Phi3:
   ```sh
   ollama run llava-phi3
   ```
2. Run the application:
   ```sh
   python main.py
   ```

## Usage

1. Click **Upload Image** and select an image.
2. (Optional) Enter a description to refine the caption.
3. Click **Generate Caption** and wait for the AI to generate a caption.
4. Copy or share your caption!

## Project Structure

```
📂 AI-Image-Captioning
 ├── main.py         # Main application script
 ├── README.md       # Project documentation
```

## Future Enhancements

- ✅ Add support for more AI models.
- ✅ Implement real-time image preview.
- ✅ Allow saving captions for later use.

## License

This project is licensed under the MIT License.

