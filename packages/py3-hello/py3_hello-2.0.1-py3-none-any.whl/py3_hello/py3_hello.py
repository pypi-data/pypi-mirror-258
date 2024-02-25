# -*- coding: utf-8 -*-
"""Hello World example.

An example CLI application to display Hello World!

"""
import click


@click.command()
@click.version_option("2.0.1", prog_name="hello")
@click.option(
    "-n",
    "--name",
    "name",
    type=click.STRING,
    default="World",
    required=False,
    help="The person to greet. Default World",
)
def hello(name: str) -> None:
    """Display Hello!

    Args:
        name (str): name or World by default
    """
    click.echo(f"Hello, {name}!")


if __name__ == "__main__":
    hello()  # pragma: no cover
