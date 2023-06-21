from setuptools import setup, find_packages

pkgs = find_packages('src')

setup_kwds = dict(
    name='centerline',
    version="0.1",
    author="Michele Tirico",
    author_mail="tirico.michele@outlook.com",
    python_required="3.10",
    zip_safe=False,
    packages=pkgs,
    package_dir={'': 'src'},
    entry_points={},
    )

setup(**setup_kwds)

