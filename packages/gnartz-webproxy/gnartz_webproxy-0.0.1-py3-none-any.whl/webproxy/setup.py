from setuptools import setup, find_packages

setup(
    name='gnartz-webproxy',
    version='0.0.1',
    author='Jimmy Allen',
    author_email='allenjsomb@gmail.com',
    description='A simple async web proxy.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    python_requires='>=3.10',
    install_requires=['aiohttp==3.9.3', 'click==8.1.7'],
    scripts=['webproxy/webproxy']
)
