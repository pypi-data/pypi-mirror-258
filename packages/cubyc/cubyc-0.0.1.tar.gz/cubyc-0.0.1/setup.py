from setuptools import setup

setup(
    name='cubyc',
    version='0.0.1',
    packages=['cubyc'],
    url='https://cubyc.com',
    license='License :: GNU Lesser General Public License v3 (LGPLv3)',
    author='Cubyc, Inc.',
    author_email='legal@cubyc.com',
    description='The framework for algorithmic decision-makers.',
    requires_python='>=3.11.0',
    install_requires=[
        'APScheduler',
        'matplotlib',
        'numpy',
        'pandas',
        'pyarrow',
        'pydantic',
        'pydantic-core',
        'python-decouple',
        'requests',
        'rich',
        'sqlalchemy',
        'requests',
        'time-machine'
    ]
)
