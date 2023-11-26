# AI Dino Runner

This is a small program I built to play the famous Google Chrome Dino game using AI. A cross browser version can be found at <https://trex-runner.com/>.

Currently the program doesn't use actual AI, it only scans if an object is in front of the dino to jump. My goal is to eventaully add TensorFlow, but right now that's a bit above my head.

---

## Getting Started

Requirements:

* `pip ~23.3.1`
* `python ~3.12.0`
* `microsoft edge ~108.0.1462.54`

You can start by installing all required dependencies using pip and venv:

```bash
# create env
python -m venv .venv

# turn on env
.venv/scripts/activate

# install packages
python -m pip install -r requirements.txt

# save packages to requirement.txt file
python -m pip freeze > requirements.txt

# turn off env
deactivate
```

To run the program:

```bash
python main.py
```

The program will create a folder named `processing` to create screenshots and log files needed to run. The folder will be created on startup if none exists.
