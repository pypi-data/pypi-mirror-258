import sys
import click
from clisync import CliSync
from .configure import configure_group

def main():
    group = CliSync(module="autopress", classes=["Autopress"])
    cli = click.CommandCollection(
        sources=[
            configure_group,
            group
        ]
    )
    # Standalone mode is False so that the errors can be caught by the runs
    cli(standalone_mode=False)
    sys.exit()

if __name__ == "__main__":
    main()
