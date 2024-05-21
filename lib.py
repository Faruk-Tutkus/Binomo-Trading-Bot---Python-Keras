import subprocess

libraries = [
    "selenium",
    "pytesseract",
    "joblib",
    "opencv-python",
    "pillow",
    "numpy",
    "tensorflow",
    "keras",
    "scikit-learn",
    "pandas"
]

pip_commands = [f"pip install {library}" for library in libraries]

# Kütüphaneleri yükle
for command in pip_commands:
    subprocess.run(command, shell=True)
