import djclick as click
from pathlib import Path
from iterfzf import iterfzf
from django.apps import apps

@click.command()
def command():
    d = local_apps()
    selected_app_label = iterfzf(iter(d.keys()))
    selected_app = d[selected_app_label]
    command_name = click.prompt('Command name')
    if not command_name.endswith(".py"):
        command_name += ".py"

    path = Path(selected_app.path) / "management" / "commands" / command_name
    with open(path, "w") as f:
        f.write("""
import djclick as click

@click.command()
def command():
    click.secho("Hello", fg="green")
""")


def local_apps():
    d = {}
    for app in apps.get_app_configs():
        if ".venv" in app.path or ".virtualenv" in app.path:
            continue
        d[app.label] = app
    return d
