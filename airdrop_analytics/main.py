import sys
import json
import math
import click
import pandas as pd
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
def cli():
    """Airdrop Analytics CLI"""
    pass

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("--format", type=click.Choice(["csv","json"]), default="csv", help="Input format")
@click.option("--top", type=int, default=10, help="Top-N holders to show")
def summarize(input_file, format, top):
    """Summarize holder balances: top-N, totals, deciles, Gini"""
    if format == "csv":
        df = pd.read_csv(input_file)
    else:
        df = pd.DataFrame(json.load(open(input_file)))

    # Expect columns: address, balance
    if not {"address","balance"}.issubset(df.columns):
        console.print("[red]Input must contain 'address' and 'balance' columns[/red]")
        sys.exit(1)

    df = df.copy()
    df["balance"] = pd.to_numeric(df["balance"], errors="coerce").fillna(0)
    df = df.sort_values("balance", ascending=False).reset_index(drop=True)

    total = df["balance"].sum()
    top_df = df.head(top)
    top_sum = top_df["balance"].sum()
    top_share = (top_sum / total) if total > 0 else 0

    # Deciles
    deciles = []
    n = len(df)
    for d in range(1, 11):
        idx = math.ceil(n * d / 10) - 1
        idx = max(0, min(idx, n - 1))
        deciles.append(float(df.iloc[idx]["balance"]))

    # Gini (simple discrete formula)
    x = df["balance"].to_numpy()
    if x.sum() == 0:
        gini = 0.0
    else:
        sorted_x = sorted(x)
        n = len(sorted_x)
        cum = 0
        for i, val in enumerate(sorted_x, start=1):
            cum += i * val
        gini = (2 * cum) / (n * x.sum()) - (n + 1) / n

    # Output table
    table = Table(title="Airdrop Analytics")
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("holders", str(len(df)))
    table.add_row("total_balance", f"{total}")
    table.add_row(f"top_{top}_share", f"{top_share:.4f}")
    table.add_row("gini", f"{gini:.4f}")
    console.print(table)

    # JSON output
    out = {
        "holders": int(len(df)),
        "total_balance": float(total),
        "top_share": float(top_share),
        "gini": float(gini),
        "deciles_balance": deciles
    }
    console.print_json(data=out)

if __name__ == "__main__":
    cli()
