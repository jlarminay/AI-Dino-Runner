# AI Dino Runner

This is a small program I built to play the famous Google Chrome Dino game using AI. A cross browser version can be found at https://trex-runner.com/.

Currently the program doesn't use actual AI, it only scans if an object is in front of the dino to jump.

---
## Getting Started

Requirements:
* `pip 22.3.1`
* `python 3.10.0`

You can start by installing all required dependancies using pip:
```bash
pip install -r requirements.txt
```

To run the program:
```bash
python main.py
```

The program will create a folder named `processing` to create screenshots and log files needed to run. The folder will be created on startup if none exists.