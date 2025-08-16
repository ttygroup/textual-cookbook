# stndlib
from __future__ import annotations
import click


@click.command()
@click.argument("recipe", type=str, default=None, required=False)
@click.option(
    "--run", "-r", is_flag=True, default=False, help="Run recipe immediately"
)
def cli(
    recipe: str | None,
    run: bool = False,
) -> None:
    """
    Textual-Cookbook
    """
    from textual_cookbook.main import CookBookApp

    CookBookApp(starting_recipe=recipe, run=run).run()



def run() -> None:
    """Entry point for the application."""
    cli()


if __name__ == "__main__":
    cli()
