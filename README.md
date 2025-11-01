# Typing Trainer (Pygame)

A Pygame-based typing trainer that helps users practice left-, right-, or both-hand coordination through customizable modes. Includes adjustable fonts, colors, and sounds. Built to explore interactive design and efficient code structure.
---

## ⚙️ Requirements

- Python 3.8+ (recommended 3.10+)
- Pygame 2.3+

Install dependencies:
python -m pip install --upgrade pip
pip install pygame

Files
Make sure these files are in the same folder:
project.py
correct.mp3
incorrect.mp3
README.md

How to Run
From a terminal in the project folder:
python project.py

How to Play
Menu
Play – start a session
Options – adjust volume, text/background color, and font
Quit – exit the program

Play Setup
Choose Left hand / Right hand / Both hands
Choose Letters / Words
Click Go! to begin

Gameplay
Letters mode: Type the single letter shown (case-insensitive).
Correct - score +1, “correct” sound
Incorrect - brief red lockout + “incorrect” sound
Words mode: Type the full word and press Enter when done.
Backspace deletes characters
Correct word - score +1 and new word

HUD

Center text → current prompt
Top text → Score, Mode, and chosen hand
Back returns to the main menu

Options Menu
Volume: Drag slider to set volume (affects both sounds).
Text/Background color: Click the box, type a color (e.g. black, navy, lightgray), press Enter.
Font: Type a valid font from pygame.font.get_fonts() (e.g. arial, calibri, comicsansms), press Enter.
Invalid entries briefly display an error message (“Color not found” or “Font not found”).

Notes
The game window is resizable (pygame.RESIZABLE | pygame.SCALED), adapting to any display size.
Fonts and colors come from Pygame’s built-in libraries.
Sound effects are royalty-free from Pixabay.
The app runs at 60 FPS and maintains smooth input handling for typing practice.

Troubleshooting
Issue	Fix
ModuleNotFoundError: No module named 'pygame'	Run pip install pygame (or python3 -m pip install pygame).
No sound or mp3 errors	Ensure correct.mp3 and incorrect.mp3 are in the same folder as project.py.
“Color/Font not found”	Use valid names from pygame.color.THECOLORS or pygame.font.get_fonts().
Window too large	Resize freely — scaling is enabled.
