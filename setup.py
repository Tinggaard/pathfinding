from setuptools import setup

setup(
    name='pathfinding',
    version='0.0.1',

    # metadata
    author='Jens Tinggaard',
    author_email='tinggaard@yahoo.com',
    description='Using pathfinding algorithms to solve mazes.',
    keywords='pathfinding maze labyrith astar dijkstra breadthfirst depthfirst solving daedalus',
    url='https://github.com/Tinggaard/pathfinding',

    license=open('LICENSE').read(),
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.6', #tested with

    zip_safe=False,

    py_modules=[
    'pathfinding/main',
    'pathfinding/solve',
    'pathfinding/scheme',
    'pathfinding/generate',
    # 'pathfinding/algs'
    ],
    install_requires=[
       'numpy',
       'pillow',
       'pydaedalus',
       'matplotlib',
        ],
    entry_points={
        'console_scripts': ['pathfinding=pathfinding.main:main']
    },

)
