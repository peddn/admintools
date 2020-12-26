from subprocess import run, CalledProcessError
import click

@click.command()
@click.option('-p', '--password', prompt=True, hide_input=True,
              confirmation_prompt=False, required=True)

def admin(password):
    """Doc String"""

    # INSTALL BASIC DEPENDENCIES
    install_basic = None

    try:
        click.echo('Installing basic dependencies.')
        install_basic = run(['xargs', '-a', './packages/install.txt', 'sudo', '-S', 'apt-get', 'install', '-y'], capture_output=True, text=True, input=password, check=True)
    except CalledProcessError as error:
        click.echo(error)

    if install_basic is not None:
        click.echo(install_basic.stdout)
        click.echo('Success.')

    # UPGRADE PIP AND INSTALL VIRTUALENV
    upgrade_pip = None

    try:
        click.echo('Upgrading pip.')
        upgrade_pip = run(['sudo', '-S', 'python3', '-m', 'pip', 'install', '--upgrade', 'pip'], capture_output=True, text=True, input=password, check=True)
    except CalledProcessError as error:
        click.echo(error)

    if upgrade_pip is not None:
        click.echo(upgrade_pip.stdout)
        click.echo('Success.')

if __name__ == '__main__':
    admin()

