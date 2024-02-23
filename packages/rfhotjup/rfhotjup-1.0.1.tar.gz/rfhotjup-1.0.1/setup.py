import setuptools

setuptools.setup(
    name='rfhotjup',
    version='1.0.1',
    install_requires = ['pandas', 'sqlite3', 'os'],
    description='Library that gives you predicted radio fluxes of Hot Jupiters',
    author='Cristina Cordun, ASTRON',
    packages=setuptools.find_packages(),
    package_data={'rfhotjup': ['database/*']}
)