# DEAD AIR

*A cosmic-horror radio investigation game.*

You are an audio archivist contracted by the Blackwater Municipal Emergency Authority to investigate unusual transmissions from radio station **BCR-17**.

The station's operator, Elias Venn, has stopped responding to check-ins. Its broadcasts are still appearing in the monitoring network, but something about the signals is wrong.

Tune into transmissions, record suspicious broadcasts, examine their audio, and uncover what is hiding beneath the static.

> **Development status:** Early prototype. The first signal-discovery puzzle is currently implemented.

---

## Current Features

- **Radio Receiver:** A vintage-inspired receiver interface with adjustable frequency tuning.
- **Signal Detection:** Discover and identify transmissions at specific frequencies.
- **Simulated Broadcasts:** Listen to radio broadcasts, interference, and unidentified signals.
- **Audio Playback:** Play, stop, and monitor transmissions.
- **Recording System:** Capture unlocked transmissions and save them to the archive.
- **Archive and Logbook:** Review recordings and investigation notes.
- **Spectrogram Analysis:** Examine recorded audio for hidden signal patterns.
- **First Investigation Puzzle:** Discover the hidden frequency **3.174 MHz**.

## Technology

- Python 3.12
- PySide6 — graphical interface
- NumPy — numerical processing
- SciPy — signal analysis
- SoundFile — audio file handling
- PyInstaller — Windows executable packaging

## Running from Source

### Requirements

- Windows
- Python 3.12
- Git (optional)

### Installation

Clone the repository:

```powershell
git clone github.com/RDSTREEM/dead-air 
cd dead_air
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the project:

```powershell
python -m pip install --upgrade pip
pip install -e .
```

Launch the game:

```powershell
dead-air
```

Alternatively:

```powershell
python src/dead_air/main.py
```

## Building for Windows

A `build.bat` script is included to package the game using PyInstaller.

Double-click `build.bat` from the project directory.

The resulting application will be located at:

```text
dist/DEAD AIR/DEAD AIR.exe
```

Keep the `_internal` folder alongside the executable when distributing the application.

## Development Roadmap

Planned features include:

- Additional investigation puzzles.
- More hidden transmissions and audio clues.
- Timestamp discrepancy investigation.
- Advanced audio filtering and signal analysis.
- Expanded case files and story progression.
- Final investigation and multiple endings.

These features are not yet implemented in the current prototype.

## About

**DEAD AIR** is an independent game development project exploring radio investigation, audio-based puzzles, atmospheric storytelling, and cosmic horror.

The goal is to make the player feel like they are investigating something that was never meant to be heard.