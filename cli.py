#!/usr/bin/env python3

import typer
from typing_extensions import Annotated

app = typer.Typer(name="spacex", help="🚀 SpaceX Launch Tracker & Analyzer")


@app.command()
def launches(
    start: Annotated[str, typer.Option(help="Start date (YYYY-MM-DD)")] = "",
    end: Annotated[str, typer.Option(help="End date (YYYY-MM-DD)")] = "",
    rocket: Annotated[str, typer.Option(help="Rocket name or ID")] = "",
    success: Annotated[bool, typer.Option(help="Show only successful launches")] = False,
    failed: Annotated[bool, typer.Option(help="Show only failed launches")] = False,
    site: Annotated[str, typer.Option(help="Launch site name")] = "",
):
    pass


@app.command()
def launch(id: str = typer.Argument(..., help="Launch ID")):
    pass


@app.command()
def rockets():
    pass


@app.command()
def launchpads():
    pass


if __name__ == "__main__":
    app()
