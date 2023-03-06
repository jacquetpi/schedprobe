# schedprobe

Expose scheduler stats (as delta) in a csv format

## Installation

```bash
git clone https://github.com/jacquetpi/schedprobe
cd schedprobe
```

## Usage

```bash
python3 schedprobe.py --name={hostname} --delay={delay_in_ms} --output={output}
```

A notebook is present for example purposes

## Background usage

```bash
./backgroundprobe.sh hostname delay output
sleep {duration}
systemctl --user stop schedprobe
```