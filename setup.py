from setuptools import find_packages, setup


def read_requirements(filename):
    with open(filename, 'r') as file:
        for line in file:
            s = line.strip()
            if s and not s.startswith('-'):
                yield s


setup(
    name="shortener",
    version="0.0.1",
    author="Sam Heybey",
    author_email="sam@heybey.org",
    description="Link shortener",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    entry_points="[console_scripts]",
    python_requires=">=3.5",
    install_requires=list(read_requirements('requirements.txt')),
    extras_require={
        'admin': list(read_requirements('requirements-admin.txt'))
    }
)
