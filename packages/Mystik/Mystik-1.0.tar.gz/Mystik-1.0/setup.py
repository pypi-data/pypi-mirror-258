from setuptools import setup, find_packages

setup(
    name='Mystik',
    version='1.0',
    author='Mystik Creatures Inc.',
    description='Custom-built AI for creating creatures in Mystik Creatures TCG',
    packages=find_packages(),  # Automatically discover and include all packages
    install_requires=[
        # List any external dependencies here, if applicable
    ],
    entry_points={
        'console_scripts': [
            # If your package includes any command-line scripts, you can define them here
        ],
    },
)
