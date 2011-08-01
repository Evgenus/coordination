params = dict(
    name='coordination',
    version='0.3.0',
    description="System for linking GUI components based on mediators. ",
    long_description="""
    System of classes and code management method at same time.
    Makes presenter of MVP more clear and understandable but more verbose.
    Rise code reuse and extendability.
    """,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
        ],
    keywords='msvs',
    author='Eugene Chernyshov',
    author_email='Chernyshov.Eugene@gmail.com',
    url='http://evgenus.github.com/coordination/',
    license='LGPL',
    packages=['coordination'],
    )

if __name__ == "__main__":
    from setuptools import setup
    setup(**params)