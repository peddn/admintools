from subprocess import run, CalledProcessError
import click

@click.command()
@click.option('-p', '--password', prompt=True, hide_input=True,
              confirmation_prompt=False, required=True)

def admin(password):
    """Doc String"""

    apt_get_update = None

    try:
        apt_get_update = run(['sudo', '-S', 'apt-get', 'update'], capture_output=True, text=True, input=password, check=True)
    except CalledProcessError as error:
        click.echo(error)

    if apt_get_update is not None:
        click.echo(apt_get_update.stdout)


if __name__ == '__main__':
    admin()