import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = "0.1.0"

setuptools.setup(
    name="gopher-render",
    version=version,
    author="Kevin Houlihan",
    author_email="kevin@hyperlinkyourheart.com",
    description="Render HTML and Markdown to plain text or gophermap files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khoulihan/gopher-render",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'gopher-render = gopher_render.__main__:main',
        ]
    },
)
