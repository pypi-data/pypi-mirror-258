import asyncio
import sys
import typer
import httpx
import toml
from pathlib import Path
from loguru import logger
from botifyme.cli.common import (
    init_cli,
    configure_logging,
    load_tools_from_directory,
)
from botifyme.registry import tool_registry, get_function_details

app = typer.Typer(name="BotifyMe", help="Command line interface for botifyMe.dev.")


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose mode."),
    src_dir: str = typer.Option(
        Path.cwd(), "--src", "-d", help="Source directory for tools."
    ),
):
    init_cli()
    configure_logging(verbose)
    load_tools_from_directory(src_dir)

@app.command(help="List all tools.")
def tools():
    """List all tools and their functions."""

    load_tools_from_directory(Path.cwd())

    for tool_name, details in tool_registry.items():
        print(f"Tool: {tool_name}")
        for func_name, func in details["functions"].items():

            function_details = get_function_details(func)
            print(f"\t > Function: {func_name}", function_details["description"])
