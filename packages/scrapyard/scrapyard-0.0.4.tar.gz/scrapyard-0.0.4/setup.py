from setuptools import setup, find_packages

setup(
    name='scrapyard',
    version='0.0.4',
    packages=find_packages(),
    author='Samoxiaki',
    author_email='samoxiaki@yahoo.com',
    description='Scrapyard Framework',
	install_requires = [
		"junkpy>=0.4.2",
		"toposort"
	]
)
