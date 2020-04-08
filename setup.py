import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = __import__('gopher_render').__version__

setuptools.setup(
    name="goper-render",
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
)
