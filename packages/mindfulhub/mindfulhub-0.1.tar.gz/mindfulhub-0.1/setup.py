from setuptools import setup, find_packages

setup(
    name='mindfulhub',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here
    ],
    entry_points={
        'console_scripts': [
            # Add any command-line scripts here
        ],
    },
    author='jacryptosis',
    author_email='jacryptosis@gmail.com',
    description='MindfulHub is an open-source platform aimed at promoting mental health and well-being by providing resources, tools, and a supportive community for individuals seeking to improve their emotional and psychological well-being.',
    url='https://github.com/jacryptosis/mindfulhub',
)
