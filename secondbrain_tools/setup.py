from setuptools import setup, find_packages

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    # The name of your project. This should be a short, lowercase name with no spaces or special characters.
    name='secondbrain-tools',

    # The version number for the project. This should follow the semantic versioning rules.
    version='0.1.0',

    # A brief description of the project. This will be displayed on the project's PyPI page.
    description='Tool components for the SecondBrain project',

    # The package directories to include. In this case, all package directories will be included.
    packages=find_packages(),

    # The dependencies that this project requires. These will be installed by pip when your project is installed.
    install_requires=[
        'requests',
        'langchain',
        'openai',
        # Add more dependencies as needed
    ],

    # This section is for optional features that users can choose to install.
    extras_require={},

    # This section can be used to specify additional metadata, such as the project's home page, author details, license, etc.
    author='Latrobe Consulting Group',
    author_email='jack@latrobe.group',
    url='https://github.com/jacklatrobe/secondbrain-ai',
)
