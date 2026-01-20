# ♟️ Python Chess Game & Web Launcher

Welcome to **Week 1** of my "12 Weeks 12 Projects" challenge! This project is a comprehensive Chess implementation featuring a robust Python-based chess engine, a Playable Desktop GUI, and a modern Web Launcher.

## 🚀 Project Overview

This project is a hybrid Chess Game developed using the Flask framework and Pygame in Python. The application provides a seamless bridge between a web-based control interface and a desktop gameplay environment.

Once the user launches the game via the web dashboard, the backend initializes the chess engine to handle the match logic. The system validates all moves against standard chess rules, ensuring compliance with complex mechanics like castling, en passant, and pawn promotion. The backend also manages game state and communicates it effectively.

The frontend is styled using HTML and CSS to provide a clean, modern, and user-friendly interface for starting game sessions. Error handling and process management are implemented to ensure the desktop game launches smoothly and interacts correctly with the web server.

## ✨ Key Features

- **Advanced Chess Engine**:
  - Full implementation of chess rules and piece logic.
  - Supports special moves: **Pawn Promotion**, **Castling**, and **En Passant**.
  - Check and Checkmate detection.
- **Dual Interface**:
  - **Desktop**: A responsive Pygame window for the actual gameplay.
  - **Web**: A modern HTML/CSS/JS dashboard to launch and manage the game.
- **Architecture**:
  - Modular Object-Oriented Design (Board, Game, Pieces).
  - Flask Rest API for game state management and launching logic.

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **Desktop GUI**: Pygame
- **Backend**: Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## 📂 Project Structure

```text
Chess Game/
├── backend/          # Flask backend handling the launcher and API
│   └── app.py
├── simple_frontend/  # Web interface assets
│   ├── index.html
│   ├── script.js
│   └── style.css
├── pieces/           # Individual piece logic (OOP)
├── images/           # Assets for the GUI
├── main.py           # Entry point for the Desktop Game
├── game.py           # Core game loop and state management
├── board.py          # Board representation
└── chess_engine.py   # Move validation and rule enforcement
```

## 🎮 How to Run

1. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Web Launcher**:

   ```bash
   python backend/app.py
   ```

   Open `http://localhost:5000` in your browser.

3. **Play**:
   Click **"PLAY GAME"** on the web interface to launch the desktop window!

## 🧠 Key Learnings

- **Logical Thinking**: Designing complex algorithms for move validation.
- **System Integration**: Connecting a web backend with a local desktop subprocess.
- **OOP Principles**: efficient class inheritance for Chess pieces.

---

_Created by [Aarav Shah](https://github.com/Aaravshah2806)_
