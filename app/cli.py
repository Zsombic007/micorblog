from app import app
import os
import sys
import click

def _pybabel(*args):
    return os.system("{} -m babel.messages.frontend {}".format(
        sys.executable, " ".join(args)))

@app.cli.group()
def translate():
    """Translation and localization commands."""
    pass

@translate.command()
def update():
    """Update all languages."""
    if _pybabel("extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if _pybabel("update -i messages.pot -d app/translations"):
        raise RuntimeError("update command failed")
    os.remove("messages.pot")

@translate.command()
def compile():
    """Compile all languages."""
    if _pybabel("compile -d app/translations"):
        raise RuntimeError("compile command failed")

@translate.command()
@click.argument("lang")
def init(lang):
    """Initialize a new language."""
    if _pybabel("extract -F babel.cfg -k _l -o messages.pot ."):
        raise RuntimeError("extract command failed")
    if _pybabel("init -i messages.pot -d app/translations -l" + lang):
        raise RuntimeError("init command failed")
    os.remove("messages.pot")