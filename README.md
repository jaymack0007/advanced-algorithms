# Advanced Algorithms Course - Week 1 Algorithm Laboratory

## Author
Jaymes McKenzie

## Description
This project sets up a reusable Python algorithm laboratory for implementing,
testing, benchmarking, and analyzing algorithms throughout the course.

## Requirements
- Python 3.9 or later
- pip
- Git

## Setup

### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Check the Environment
```bash
python environment_check.py
```

## Run Tests
```bash
pytest tests/ -v
```

## Run Benchmarks
```bash
python benchmarks/sorting_benchmarks.py
```

Benchmark output is written to the `results/` directory.

## Project Contents
- `src/sorting/basic_sorts.py` - bubble, selection, and insertion sort
- `src/utils/benchmark.py` - reusable benchmarking framework
- `tests/` - pytest test suite
- `benchmarks/sorting_benchmarks.py` - benchmark runner
- `docs/week01_report.md` - performance-analysis report template
- `results/` - generated CSV and PNG benchmark output

## Current Progress
- [x] Environment setup
- [x] Bubble sort
- [x] Selection sort
- [x] Insertion sort
- [x] Benchmark framework
- [x] Automated tests
- [x] Performance report template
