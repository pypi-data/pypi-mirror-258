"""Command-line interface."""

import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Libtest76."""


if __name__ == "__main__":
    main(prog_name="ssb-libtest76")  # pragma: no cover
