import click
import os
import shutil
from subprocess import Popen
import tempfile

REQUIREMENTS_FILE = "real-requirements.txt"
DEFAULT_OUTPUT_FILE = "requirements.hippo.txt"


class VirtualenvError(Exception):
    pass

class PipError(Exception):
    pass


class Sandbox(object):

    def __init__(self):
        self.location = tempfile.mkdtemp()
        self._create_virtualenv()
        self.pip = os.path.join(self.location, 'bin', 'pip')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._cleanup()

    def _cleanup(self):
        if os.path.isdir(self.location):
            try:
                shutil.rmtree(self.location)
            except (OSError, IOError):
                pass
        return False

    def _create_virtualenv(self):
        """
        Taken and modified from Armin Ronacher's pipsi
        https://github.com/mitsuhiko/pipsi

        """
        # Install virtualenv
        args = ['virtualenv']
        # if python is not None:
        #     args.append('-p')
        #     args.append(python)
        args.append(self.location)

        if Popen(args).wait() != 0:
            click.echo('Failed to create virtualenv. Aborting.')
            raise VirtualenvError()

    def create(self):
        os.makedirs(self.sandbox_dir)

    def install(self, install_args):
        args = [self.pip, 'install']
        # if editable:
        #     args.append('--editable')

        if Popen(args + install_args).wait() != 0:
            click.echo('Failed to pip install. Aborting.')
            raise PipError()

        return True

    def freeze_to_file(self, output_file):
        with open(output_file, 'wb') as output:
            args = [self.pip, 'freeze']

            if Popen(args, stdout=output).wait() != 0:
                click.echo('Failed to pip freeze. Aborting.')
                return False

        return True


@click.group()
def cli():
    pass

# @cli.command()
# @click.argument('package')
# def install(package):
#     pass

@cli.command()
def generate():
    """
    Generates full requirements

    """
    if not os.path.exists(REQUIREMENTS_FILE):
        click.echo("Failed to find '%s'." % REQUIREMENTS_FILE)
        exit()

    output_file = DEFAULT_OUTPUT_FILE
    if not output_file == os.path.abspath(output_file):
        output_file = os.path.join(os.getcwdu(), output_file)

    if os.path.exists(output_file):
        click.echo("Output file %s already exists. Aborting." % output_file)
        exit()

    click.echo("Setting up sandbox...\n")
    with Sandbox() as sandbox:
        real_packages = []
        with open(REQUIREMENTS_FILE, 'r') as f:
            for package_line in f:
                real_packages.append(package_line.rstrip())

        click.echo("\nGenerating dependencies for %s\n" % ' '.join(real_packages))
        sandbox.install(real_packages)

        click.echo("\nFreezing dependencies to %s" % output_file)
        if sandbox.freeze_to_file(output_file):
            click.echo("\nDone.")
