# pyScan

[![CI (Lint & Test)](https://img.shields.io/github/actions/workflow/status/snowlock-dev/pyscan/test.yml?style=for-the-badge&label=Build&labelColor=2a2a2a&logo=github)](https://github.com/snowlock-dev/pyScan/actions/workflows/test.yml)

A fast, lightweight and simple asynchronous TCP port scanner written in Python (using `asyncio`)

Blogposts: 
* [Implementing Concurrency](https://snowlock.bearblog.dev/pyscan-devblog-1/)
* [Setting up unit tests & Github Action](https://snowlock.bearblog.dev/pyscan-devblog-2/)

## Getting Started

Make sure you have python >= 3.10 installed.

1. Clone the repo & navigate to the directory:

```bash
   git clone https://github.com/snowlock-dev/pyScan.git

   cd pyScan
```

2. Setup (& activate) the virtual env:

```bash
   python -m venv venv

   source venv/bin/activate
```

3. Install the dependencies (`pip install -r requirements.txt`)

4. Launch the interactive script: `python pyscan.py`

You will be prompted to enter:

* Host IP / Name (Default: 127.0.0.1)
* Start Port (Default: 1)
* End Port (Default: 1024)

## Testing

Unit test is located in the `tests/` directory and use `pytest` alongside `pytest-asyncio` and `unittest.mock` to simulate asynchronous network connections without requiring real network traffic. 

The test suite verifies:
* Single open port detection & closed port handling (using mocked `asyncio.open_connection`)
* Timeout and network error handling (`asyncio.TimeoutError`, `OSError`)
* Asynchronous range scanning with boundary clamping and task concurrency control
* Edge cases and invalid port ranges

To run the tests locally:

```bashs
   python -m pytest
```

## Future Roadmap:

- [x] ~~Add Github CI/CD tests~~
- [x] ~~Benchmarking Python's single-threaded `asyncio` event loop against `ThreadPoolExecutor` to see which handles high concurrency better~~
- [ ] Swapping full TCP connections for raw SYN (half-open) packet crafting using Scapy
- [ ] Probing open ports to read service headers and automatically identify running software
- [ ] Adding `argparse` support for custom port ranges and outputting scan results directly to JSON
- [ ] Add rate-limiting / concurrency control using asyncio.Semaphore to prevent socket exhaustion
- [ ] Pretty Terminal UI (Rich CLI)
- [ ] Top Ports / Common Port Presets (like `nmap`)
