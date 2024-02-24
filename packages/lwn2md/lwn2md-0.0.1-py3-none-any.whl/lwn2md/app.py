import httpx
from rich.console import Console
import typer

from typing import Optional, Annotated
from lwn2md.util import html2md

app = typer.Typer()
console = Console()


@app.command()
def main(url: str, output: Annotated[Optional[str], typer.Argument()] = ""):
    """Convert LWN articles to markdown."""

    # check if the url is valid
    if not url.startswith("https://lwn.net"):
        console.log("Invalid URL", style="bold red")
        return

    with httpx.Client(
        cookies={
            "sub_nag": '"Support LWN.net"',
        },
        timeout=600,
    ) as client:
        response = client.get(url)

    text = response.text
    if len(text) < 100:
        console.log("Failed to get the page, check url?", style="bold red")
        if not url.endswith("/"):
            console.log("Try to append a '/' to the url.", style="yellow")
        return

    title, author, _ = html2md(text, output)

    console.log(f"Transfered {title} of {author}", style="bold green")
