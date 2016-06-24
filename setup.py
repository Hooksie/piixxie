from setuptools import setup

setup(
    name='piixxie',
    version='0.1.0',
    packages=['piixxie'],
    url='https://github.com/Hooksie/piixxie',
    license='MIT',
    author='Matt Hooks',
    author_email='me@matthooks.com',
    description='A pixel art resizing tool.',
    entry_points={
        'console_scripts': [
            'piixxie = piixxie.pix:main'
        ]
    },
)
