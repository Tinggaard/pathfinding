from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

setup(
    name='pathfinding',
    version='0.0.1',

    # metadata
    author='Jens Tinggaard',
    author_email='tinggaard@yahoo.com',
    description='Using pathfinding algorithms to solve mazes.',
    keywords='pathfinding maze labyrith astar dijkstra breadthfirst depthfirst solving daedalus',
    url='https://github.com/Tinggaard/pathfinding',

    license=LICENSE,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    python_requires='>=3.6', #tested with

    zip_safe=False,

    py_modules=['src/main'],
    install_requires=[
       'numpy',
       'pillow',
       'pydaedalus',
       'matplotlib',
        ],
    entry_points={
        'console_scripts': ['pathfinding=src.main:main']
    },

)
