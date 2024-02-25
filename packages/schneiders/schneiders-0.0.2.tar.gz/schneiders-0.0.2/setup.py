from setuptools import setup 

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='schneiders',
    version='0.0.2',
    license='MIT License',
    author='Júlio Rolim Schneiders',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='julioschneiders@ieee.org',
    keywords='schneiders mosquito',
    description=u'biblioteca para auxílio da simulação de um braço robótico de 3 DOF',
    packages=['schneiders_V0'],
    install_requires=['numpy', 'matplotlib'],)