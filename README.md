# -IAS-CS121-Steganography-Tool
A Python-based steganography tool for hiding and extracting messages in image and text files. Created as a student project for the Information Assurance and Security course. Features LSB image encoding and whitespace text encoding. Includes a menu-driven interface for ease of use.

# Steganography Tool

A Python-based steganography tool for hiding and extracting messages in image and text files. This was developed as a student project for the subject **Information Assurance and Security**.

# Features
- Image Steganography using LSB (Least Significant Bit) method.
- Text Steganography using whitespace encoding (space = 0, tab = 1).
- Command-line interface with a looping menu.
- File path support for inputs/outputs.

# Requirements
- Python 3.x
- Pillow (`pip install pillow`)

# How to Use
1. Run the script.
2. Choose between image or text steganography.
3. Choose to encode or decode a message.
4. Enter file paths and the message (if encoding).
5. Repeat or exit when done.

# Notes
- Image steganography works best with uncompressed formats (e.g., PNG).

# License
This project is for educational purposes.
