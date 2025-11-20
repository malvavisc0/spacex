# 🚀 SpaceX Launch Tracker CLI

A simple command-line tool to track and analyze SpaceX launches, rockets, and launchpads.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### View Recent Launches
```bash
python cli.py launches
```

### Filter Launches
```bash
# By date range
python cli.py launches --start 2024-01-01 --end 2024-12-31

# By rocket
python cli.py launches --rocket "5e9d0d95eda69955f709d1eb"

# By launchpad
python cli.py launches --launchpad "5e9e4502f5090927f8566f85"

# Limit results
python cli.py launches --limit 5
```

### Get Launch Details
```bash
python cli.py launch <launch-id>
```

### List All Rockets
```bash
python cli.py rockets
```

### List All Launchpads
```bash
python cli.py launchpads
```
