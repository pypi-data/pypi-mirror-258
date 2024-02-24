from setuptools import find_packages, setup

setup(
    name="pbj_tools",
    version="0.1.2",
    description="Python package used to interact with phage.db",
    url="https://github.com/JoshuaIszatt",
    author="Joshua Iszatt",
    author_email="joshiszatt@gmail.com",
    install_requires=["biopython==1.83"],
    python_requires=">3",
    packages=find_packages(),
    data_files=[("", ["README.md"])],
    entry_points={
    'console_scripts': [
        'pbj_tools = pbj_tools.main:main',
    ],
}
)