# pyScan

A fast, lightweight and simple TCP port scanner written in Python

## Getting Started

Make sure you have python >= 3.10 installed.

1. Clone the repo & navigate to the directory:

```bash
   git clone https://github.com/snowlock-dev/pyScan.git
   cd pyScan
```

2. Install the dependencies (req.txt; `pip install -r req.txt`)

3. Launch the interactive script: `python pyscan.py`

You will be prompted to enter:

* Host IP / Name (Default: 127.0.0.1)
* Start Port (Default: 1)
* End Port (Default: 1024)

## Testing

Unit tests are located in the `tests/` directory and use `pytest` with `unittest.mock` to simulate network connections without requiring real network traffic. 

The test suite verifies:
* Single open port detection
* Closed port handling
* Concurrent range scanning across multiple ports

To run the tests locally:

```bash
python -m pytest
```
