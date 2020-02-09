from distutils.core import setup
import setuptools

def readme():
    """Import the README.md Markdown file and try to convert it to RST format."""
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError):
        with open('README.md') as readme_file:
            return readme_file.read()
        
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]

setup(
    name='{{cookiecutter.package_name}}',
    version='{{cookiecutter.package_version}}',
    description='{{cookiecutter.package_short_description}}',
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    url='{{cookiecutter.project_url}}',
    author='{{cookiecutter.author_name}}',
    author_email='{{cookiecutter.author_email}}',
    license='{{cookiecutter.package_license}}',
    packages=['{{cookiecutter.package_name}}'],
    install_requires=requirements,
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
