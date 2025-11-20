#!/usr/bin/env python3

import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from api import v4

app = typer.Typer(name="spacex", help="🚀 SpaceX Launch Tracker & Analyzer")
console = Console()
error_console = Console(stderr=True)


@app.command()
def launches(
    start: Annotated[str, typer.Option(help="Start date (YYYY-MM-DD)")] = "",
    end: Annotated[str, typer.Option(help="End date (YYYY-MM-DD)")] = "",
    rocket: Annotated[str, typer.Option(help="Rocket name or ID")] = "",
    launchpad: Annotated[str, typer.Option(help="Launch site name")] = "",
    limit: Annotated[int, typer.Option(help="Launch site name")] = 10,
):
    try:
        table = Table("ID", "Date", "Rocket", "Launchpad", "Details")
        for launch in v4.filter_launches(
            start=start, end=end, rocket=rocket, site=launchpad, limit=limit
        ):
            table.add_row(
                launch.id,
                str(launch.date),
                launch.rocket.name,
                launch.launchpad.name,
                launch.details,
            )
        console.print(table)
    except Exception as exc:
        error_console.print(exc, style="red")
        raise typer.Exit(code=1)


@app.command()
def launch(id: str = typer.Argument(..., help="Launch ID")):
    try:
        launch_data = v4.get_launch(id=id)
        if launch_data:
            console.print(f"ID:\t\t{launch_data.id}")
            console.print(f"Date:\t\t{launch_data.date}")
            console.print(f"Rocket:\t\t{launch_data.rocket.name}")
            console.print(f"Launchpad:\t{launch_data.launchpad.name}")
            console.print(f"Details:\t{launch_data.details}")
    except Exception as exc:
        error_console.print(exc, style="red")
        raise typer.Exit(code=1)


@app.command()
def rockets():
    try:
        table = Table("ID", "Name", "Type", "Description", "Status")
        for rocket in v4.get_all_rockets():
            table.add_row(
                rocket.id,
                rocket.name,
                rocket.type,
                rocket.description,
                "Active" if rocket.active == True else "Inactive",
            )
        console.print(table)
    except Exception as exc:
        error_console.print(exc, style="red")
        raise typer.Exit(code=1)


@app.command()
def launchpads():
    try:
        table = Table(
            "ID", "Name", "Region", "Timezone", "Longitude", "Latitude", "Status"
        )
        for launchpad in v4.get_all_launchpads():
            table.add_row(
                launchpad.id,
                launchpad.name,
                launchpad.region,
                launchpad.timezone,
                str(launchpad.longitude),
                str(launchpad.latitude),
                launchpad.status,
            )
        console.print(table)
    except Exception as exc:
        error_console.print(exc, style="red")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
