from setuptools import setup, find_packages

setup(
    name="git-commit-suggest",
    version="1.0",
    packages = find_packages(),
    install_requires = [
        'requests>=2.25.1',
    ],
    package_data={
        'git_commit_message': ['shell/*'],
    },
    entry_points={
            'console_scripts': [
                'git-commit-suggest=git_commit_suggest.suggest:main'
            ]
        },
    author="Biraj Dahal",
    author_email="dahalbiraj10@gmail.com",
    description="AI-powered git commit messasge suggestions",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/biraj-dahal/git_commit_suggest",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)