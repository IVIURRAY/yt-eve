from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt', 'r') as req:
        content = req.read()
        requirements = content.split('\n')

    return requirements


setup(
    name='eve',
    version='0.2.0',
    packages=find_packages(),
    include_package_date=True,
    install_requires=read_requirements(),
    package_data = {"eve": ["meta/start/*.json", "meta/start/licenses/*.txt", "meta/start/templates/*.json"]},
    entry_points="""
        [console_scripts]
        eve=eve.cli:cli
    """,
)
