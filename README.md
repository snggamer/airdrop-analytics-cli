# Airdrop Analytics CLI

Compute simple holder distribution metrics (top-N share, deciles, Gini) and export results for research.
## Features
- Reads CSV or JSON with columns: address, balance.
- Outputs Rich table + JSON block.
- Metrics: top-N share, total holders/balance, deciles, Gini.
## Installation
Requires Python 3.10+.
Option A — pipx (recommended):
pipx install .
Option B — pip (editable dev install):
pip install -e .
## Usage
Summarize a CSV file:
airdrop-cli summarize holders.csv --format csv --top 10
Summarize a JSON file:
airdrop-cli summarize holders.json --format json --top 20
Input CSV example (two columns):
address,balance
0x111...,123.45
0x222...,0.5
## Roadmap
- Filters: min balance, include/exclude addresses.
- Extra outputs: CSV/JSON export file path.
- Charts (separate repo).
## Contributing
Issues and PRs are welcome. Good first issues:
- Add export CSV/JSON flags.
- Add filters and address lists.
- Add tests + CI.
## License
MIT

