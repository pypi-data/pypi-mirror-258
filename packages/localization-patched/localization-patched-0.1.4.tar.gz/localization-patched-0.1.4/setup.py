from distutils.core import setup

setup(
    name='localization-patched',
    version='0.1.4',
    author='Kamal Shadi',
    author_email='kamal.shadi85@gmail.com',
    packages=['localization', 'localization.test'],
    scripts=['bin/sample.py'],
    install_requires=['scipy', 'shapely', 'descartes'],
    url='https://github.com/kamalshadi/Localization',
    license='LICENSE.txt',
    description='Multilateration and triangulation.',
    long_description=open('README.txt').read(),
)
