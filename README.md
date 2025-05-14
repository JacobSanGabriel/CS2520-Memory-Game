# CS2520 - Memory Game 

A Simon Says–style memory game where users input the correct color sequence to progress. Difficulty affects how quickly the colors flash and as the level increases, so does sequence length. Created using Python and Tkinter for the GUI

## Team Members
Adrian Caballero, Caitlyn Hue, Jacob San Gabriel, Luis Felix Reyes

## How to Play

> **Note:** Make sure all dependencies are installed before running the game (see [Dependencies](#dependencies)).

1. Run `MemoryGame.py`.
2. Select a difficulty: Easy, Medium, or Hard.
3. Click **Start**.
4. Watch the color tiles flash white—this is the pattern to memorize.
5. Repeat the pattern by clicking the color tiles in the same order.
6. If you're correct, a new color is added to the sequence.
7. If you're wrong, the game ends and your session is logged.
8. After a game ends, you can retry, quit, or change difficulty.

## Output Logging 

Each game session is saved in `output.txt` and includes:
- Timestamp when game happened
- Difficulty level
- Time spent on each level
- The correct sequence shown
- The player's input for that level

> `output.txt` is cleared each time the program is restarted.

## Dependencies

Install dependencies using:

```bash terminal
pip install -r requirements.txt


