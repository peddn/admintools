import os
import click
import json
from subprocess import run, CalledProcessError, PIPE, STDOUT
from string import Template

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)

    # load the global configuration data and add it to the context
    click.echo('Loading config file.')
    with open('config.json', 'r') as c_file:
        config_json = json.load(c_file)
        ctx.obj['CONFIG'] = config_json
    click.echo('Success.')

    # load all project meta data and add them to the context
    with os.scandir('./projects') as projects_dir:
        for project_file in projects_dir:
            if project_file.is_file():
                if project_file.name.endswith('.json') and not project_file.name.startswith('.'):
                    click.echo('Loading project file ' + project_file.name)
                    with open('./projects/' + project_file.name, 'r') as file:
                        project_json = json.load(file)
                        file_name = os.path.splitext(project_file.name)[0]
                        ctx.obj[file_name] = project_json
                        click.echo(project_json)
                    click.echo('Success.')



@click.command()
@click.option('--password', prompt=True, hide_input=True,
                confirmation_prompt=False, required=True)
@click.pass_context
def dep_install(ctx, password):
    """Installs basic dependencies."""
    dep_install = None
    try:
        click.echo('Installing basic dependencies.')
        dep_install = run(
            [ 'xargs', '-a', './packages/basic.txt',
            'sudo', '-S', 'apt-get', 'install', '-y' ],
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            input=password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
        click.echo(error.stdout)
    if dep_install is not None:
        click.echo(dep_install.stdout)
        click.echo('Success.')


@click.command()
@click.option('--password', prompt=True, hide_input=True,
                confirmation_prompt=False, required=True)
@click.pass_context
def python_init(ctx, password):
    """Upgrade pip and install virtualenv."""
    upgrade_pip = None
    try:
        click.echo('Upgrading pip.')
        upgrade_pip = run(
            [ 'sudo', '-S', 'python3', '-m',
            'pip', 'install', '--upgrade', 'pip' ],
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            input=password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
        click.echo(error.stdout)
    if upgrade_pip is not None:
        click.echo(upgrade_pip.stdout)
        click.echo('Success.')
    
    install_virtualenv = None
    try:
        click.echo('Installing virtualenv')
        install_virtualenv = run(
            ['sudo', '-S', 'pip', 'install', 'virtualenv'],
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            input=password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
        click.echo(error.stdout)
    if install_virtualenv is not None:
        click.echo(install_virtualenv.stdout)
        click.echo('Success.')


@click.command()
@click.option('--password', prompt='account password', hide_input=True,
                confirmation_prompt=False, required=True)
@click.option('--db-password', prompt='database password', hide_input=True,
                confirmation_prompt=True, required=True)
@click.argument('project-name')
@click.pass_context
def db_create(ctx, password, db_password, project_name):
    """Creates a database and a user for this database."""

    db_name = project_name + '-db'
    db_username = project_name + '-user'
    create_db = None

    try:
        click.echo('Creating database ' + db_name + '.')
        create_db = run(
            ['sudo', '-u', 'postgres', '-S', 'createdb', db_name],
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            input=password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
        click.echo(error.stdout)
    if create_db is not None:
        # there is no output by this command
        # click.echo(create_db.stdout)
        click.echo('Success.')

    create_user = None
    try:
        click.echo('Creating user ' + db_username)
        create_user = run(
            ['sudo', '-u', 'postgres', '-S', 'createuser', db_username],
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            input=password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
        click.echo(error.stdout)
    if create_user is not None:
        # there is no output by this command
        # click.echo(create_db.stdout)
        click.echo('Success.')




@click.command()
@click.option('--password', prompt=True, hide_input=True,
                confirmation_prompt=False, required=True)
@click.option('--db-password', prompt=True, hide_input=True,
                confirmation_prompt=True, required=True)
@click.argument('project-name')
@click.pass_context
def db_drop(ctx, password, db_password, project_name):
    """Drops a database and its corresponding user."""
    
    db_name = project_name + '-db'
    db_username = project_name + '-user'
    drop_db = None

    try:
        click.echo('Dropping database ' + db_name + '.')
        drop_db = run(
            ['sudo', '-u', 'postgres', '-S', 'dropdb', db_name],
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            input=password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
        click.echo(error.stdout)
    if drop_db is not None:
        # there is no output by this command
        # click.echo(drop_db.stdout)
        click.echo('Success.')

    drop_user = None
    try:
        click.echo('Dropping user ' + db_username)
        drop_user = run(
            ['sudo', '-u', 'postgres', '-S', 'dropuser', db_username],
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            input=password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
        click.echo(error.stdout)
    if drop_user is not None:
        # there is no output by this command
        # click.echo(create_db.stdout)
        click.echo('Success.')


# TODO validate project-name user input
@click.command()
@click.option('--sudo-password', prompt=True, hide_input=True,
                confirmation_prompt=False, required=True)
@click.argument('project', nargs=1)
@click.pass_context
def gen_systemd(ctx, sudo_password, project):
    """Generates systemd socket and service files."""
    config = ctx.obj['CONFIG']



    with open('./templates/socket_template.socket', 'r') as file:
        template_str = file.read()
        template = Template(template_str)
        template_filled = template.substitute(
            project_name = project,
        )
        click.echo(template_filled)
        # TODO write out to 
    with open('./templates/service_template.service', 'r') as file:
        template_str = file.read()
        template = Template(template_str)
        template_filled = template.substitute(
            project_name = project,
            site_name = site,
            projects_home = config['projectsHome'],
            user = config['user'],
            virtual_environment = config['virtualEnvironment']
        )
        click.echo(template_filled)


cli.add_command(dep_install)
cli.add_command(python_init)
cli.add_command(db_create)
cli.add_command(db_drop)
cli.add_command(gen_systemd)

if __name__ == '__main__':
    cli()
