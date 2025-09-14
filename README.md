# 🧩 Rubik's Cube Solver

## 📌 Overview
This project is a **Rubik’s Cube Solver** that helps users solve any scrambled cube using computer vision and algorithms.  
It uses a **camera to capture the cube faces**, extracts the colors, and then applies the **Kociemba algorithm** to generate the optimal solution in the shortest number of moves.  
Additionally, the project provides a **3D cube visualization** to guide the user while scanning and solving.

---

## 🚀 Features
- 🎥 **Camera-based color detection** for all 6 faces of the cube.  
- 🖌️ **Manual color input option** (in case of poor lighting or camera issues).  
- 🧮 **Kociemba algorithm** implementation for optimal solution.  
- 📊 **3D Cube visualization** to display scanned state and solution steps.  
- 🖥️ **User-friendly interface** to guide the solving process.

---

## 🛠️ Tech Stack
- **Programming Language:** Python 🐍  
- **Libraries & Tools:**
  - OpenCV → for image processing & color detection  
  - Kociemba → for solving the cube  
  - Matplotlib / PyOpenGL / Three.js → for 3D cube visualization  
  - Tkinter / PyQt → for GUI (optional depending on your implementation)

---

## 📂 Project Structure

## 📂 Project Structure
RubikCubeSolver/
│── main.py # Main entry point
│── cube_scanner.py # Handles camera capture & color detection
│── solver.py # Applies Kociemba algorithm
│── cube_visualizer.py # 3D cube visualization
│── gui.py # User interface (optional)
│── requirements.txt # Dependencies
│── README.md # Documentation

yaml
نسخ الكود

---

## ⚙️ Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/RubikCubeSolver.git
   cd RubikCubeSolver
Install dependencies:

bash
نسخ الكود
pip install -r requirements.txt
Run the project:

bash
نسخ الكود
python main.py
🎮 How to Use
1-Hold your Rubik’s Cube in front of the camera.

2- Scan all 6 faces (guided by the app).

3-Preview the scanned cube in 3D visualization.

4- Press Solve → get the move sequence (e.g., R U R' U').

5- Follow the steps and enjoy solving your cube 🎉.


**Developed by ENG:Bashar Alkhawlani ✨**
