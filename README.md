# schedprobe

Expose scheduler stats (as delta) in a csv format

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements
```

## Usage

```bash
source venv/bin/activate
python3 schedprobe.py --name={hostname} --delay={delay_in_ms} --output={output}
```

A notebook is present for example purposes

## Background usage

```bash
./backgroundprobe.sh hostname delay output
sleep {duration}
systemctl --user stop schedprobe
```