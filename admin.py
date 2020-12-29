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
                        filename_without_extension = os.path.splitext(project_file.name)[0]
                        ctx.obj[filename_without_extension] = project_json
                    click.echo('Success.')

# GLOBAL commands

@click.command()
@click.option('--password', prompt=True, hide_input=True,
                confirmation_prompt=False, required=True)
@click.pass_context
def aptget_firsttime(ctx, password):
    """Installs basic dependencies."""
    aptget_install = None
    try:
        click.echo('Installing basic dependencies.')
        aptget_install = run(
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
    if aptget_install is not None:
        click.echo(aptget_install.stdout)
        click.echo('Success.')


@click.command()
@click.option('--password', prompt=True, hide_input=True,
                confirmation_prompt=False, required=True)
@click.pass_context
def python_firsttime(ctx, password):
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

# PROJECT specific commands

# validation callbacks
def validate_project(ctx, param, project):
    ctx.ensure_object(dict)
    if project not in ctx.obj:
        raise click.BadParameter('Project "' + project + '" not loaded. Probably there is no json file present.')
    else:
        return project

@click.command()
@click.option('--sudo-password', prompt=True, hide_input=True,
                confirmation_prompt=False, required=True)
@click.option('--db-password', prompt=True, hide_input=True,
                confirmation_prompt=True, required=True)
@click.argument('project', nargs=1, callback=validate_project, required=True)
@click.pass_context
def db_create(ctx, sudo_password, db_password, project):
    """Creates a database and a user for this database."""

    create_db = None
    try:
        click.echo('Creating database ' + project + '.')
        create_db = run(
            ['sudo', '-u', 'postgres', '-S', 'createdb', project],
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            input=sudo_password,
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
        click.echo('Creating user ' + project)
        create_user = run(
            ['sudo', '-u', 'postgres', '-S', 'createuser', project],
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            input=sudo_password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
        click.echo(error.stdout)
    if create_user is not None:
        # there is no output by this command
        # click.echo(create_db.stdout)
        click.echo('Success.')
    
    if create_db is not None and create_user is not None:

        alter_role_encoding = None
        try:
            click.echo('ALTER ROLE on user: ' + project)
            utf8 = "'utf8'"
            psql = ['sudo', '-u', 'postgres', '-S', 'psql', '-tA', '--command="ALTER ROLE ' + project + ' SET client_encoding TO \'utf8\';"', 'postgres']
            alter_role_encoding = run(
                psql,
                stdout=PIPE,
                stderr=STDOUT,
                text=True,
                input=sudo_password,
                check=True
            )
        except CalledProcessError as error:
            click.echo(error)
            click.echo(error.stdout)
        if alter_role_encoding is not None:
            # there is no output by this command
            # click.echo(create_db.stdout)
            click.echo('Success.')



@click.command()
@click.option('--sudo-password', prompt=True, hide_input=True,
                confirmation_prompt=False, required=True)
@click.argument('project', nargs=1, callback=validate_project, required=True)
@click.pass_context
def db_drop(ctx, sudo_password, project):
    """Drops a database and its corresponding user."""

    drop_db = None
    try:
        click.echo('Dropping database ' + project + '.')
        drop_db = run(
            ['sudo', '-u', 'postgres', '-S', 'dropdb', project],
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            input=sudo_password,
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
        click.echo('Dropping user ' + project)
        drop_user = run(
            ['sudo', '-u', 'postgres', '-S', 'dropuser', project],
            stdout=PIPE,
            stderr=STDOUT,
            text=True,
            input=sudo_password,
            check=True
        )
    except CalledProcessError as error:
        click.echo(error)
        click.echo(error.stdout)
    if drop_user is not None:
        # there is no output by this command
        # click.echo(create_db.stdout)
        click.echo('Success.')




@click.command()
@click.option('--sudo-password', prompt=True, hide_input=True,
                confirmation_prompt=False, required=True)
@click.argument('project', nargs=1, callback=validate_project, required=True)
@click.pass_context
def systemd_create(ctx, sudo_password, project):
    """Generates systemd socket and service files for the given project."""

    # get the configuration
    global_config = ctx.obj['CONFIG']
    project_config = ctx.obj[project]

    with open('./templates/socket_template.socket', 'r') as file:
        template_str = file.read()
        template = Template(template_str)
        template_filled = template.substitute(
            project_wagtail = project_config['wagtailProject'],
        )
        click.echo(template_filled)
        # TODO write out to /etc/systemd/system

    with open('./templates/service_template.service', 'r') as file:
        template_str = file.read()
        template = Template(template_str)
        template_filled = template.substitute(
            user = global_config['user'],
            virtual_environment = global_config['virtualEnvironment'],
            projects_root = global_config['projectsRoot'],
            project_meta = project,
            project_wagtail = project_config['wagtailProject'],
        )
        click.echo(template_filled)
        # TODO write out to /etc/systemd/system

@click.command()
@click.option('--sudo-password', prompt=True, hide_input=True,
                confirmation_prompt=False, required=True)
@click.argument('project', nargs=1, callback=validate_project, required=True)
@click.pass_context
def systemd_delete(ctx, sudo_password, project):
    """Deletes systemd socket and service files for the given project."""
    pass


cli.add_command(aptget_firsttime)
cli.add_command(python_firsttime)
cli.add_command(db_create)
cli.add_command(db_drop)
cli.add_command(systemd_create)
cli.add_command(systemd_delete)

if __name__ == '__main__':
    cli()
