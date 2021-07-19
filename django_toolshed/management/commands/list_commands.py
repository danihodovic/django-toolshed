import djclick as click
from django.core import management
from iterfzf import iterfzf


def format_cmd(app, command_name):
    return f"{command_name:35s}{app}"


@click.command()
@click.option(
    "--fzf/--no-fzf",
    default=True,
    show_default=True,
)
def command(fzf):
    commands = management.get_commands()
    commands_list = [format_cmd(app, command) for command, app in commands.items()]
    if not fzf:
        click.echo("\n".join(commands_list))
        return
    chosen = iterfzf(iter(commands_list))
    if not chosen:
        return
    chosen = chosen.split()[0]
    click.echo(f"./manage.py {chosen}", nl=False)
