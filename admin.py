from subprocess import run, CalledProcessError, PIPE, STDOUT
import click

@click.group()
def cli():
    pass


@click.command()
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=False, required=True)
def dep_install(password):
    """Installs basic dependencies."""
    dep_install = None
    try:
        click.echo('Installing basic dependencies.')
        dep_install = run(
            [ 'xargs', '-a', './packages/basic.txt',
            'sudo', '-S', 'apt-get', 'install', '-y' ],
            capture_output=True,
            text=True,
            input=password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
    if dep_install is not None:
        click.echo(dep_install.stdout)
        click.echo('Success.')


@click.command()
@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=False, required=True)
def python_init(password):
    """Upgrade pip and install virtualenv."""
    upgrade_pip = None
    try:
        click.echo('Upgrading pip.')
        upgrade_pip = run(
            [ 'sudo', '-S', 'python3', '-m',
            'pip', 'install', '--upgrade', 'pip' ],
            capture_output=True,
            text=True,
            input=password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
    if upgrade_pip is not None:
        click.echo(upgrade_pip.stdout)
        click.echo('Success.')
    
    install_virtualenv = None
    try:
        click.echo('Installing virtualenv')
        install_virtualenv = run(
            ['sudo', '-S', 'pip', 'install', 'virtualenv'],
            capture_output=True,
            text=True,
            input=password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
    if install_virtualenv is not None:
        click.echo(install_virtualenv.stdout)
        click.echo('Success.')


@click.command()
@click.option('--password', prompt=True, hide_input=True,
            confirmation_prompt=False, required=True)
@click.argument('project-name')
def db_create(password, project_name):
    """Creates a database and a user for this database."""
    create_db = None
    try:
        click.echo('Creating database ' + project_name + '.')
        create_db = run(
            ['sudo', '-u', 'postgres', '-S', 'createdb', project_name],
            capture_output=True,
            text=True,
            input=password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
    if create_db is not None:
        click.echo(create_db.stdout)
        click.echo('Success.')



@click.command()
@click.option('--password', prompt=True, hide_input=True,
            confirmation_prompt=False, required=True)
@click.argument('project-name')
def db_drop(password, project_name):
    """Drops a database and its corresponding user."""
    drop_db = None
    try:
        click.echo('Dropping database ' + project_name + '.')
        drop_db = run(
            ['sudo', '-u', 'postgres', '-S', 'dropdb', project_name],
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            input=password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
        click.echo(error.output)
        click.echo(error.stdout)
    if drop_db is not None:
        click.echo(drop_db.stdout)
        click.echo('Success.')

cli.add_command(dep_install)
cli.add_command(python_init)
cli.add_command(db_create)
cli.add_command(db_drop)

if __name__ == '__main__':
    cli()
