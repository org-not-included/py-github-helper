from setuptools import setup, find_packages


VERSION = '0.0.4'
DESCRIPTION = 'Python Script for interacting with Github API'

setup(
    name="py-github-helper",
    version=VERSION,
    author="mtsadler (Mike Sadler)",
    author_email="<michaeltsadler1@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'pendulum'],
    keywords=['python', 'github', 'api', 'comment', 'action', 'Pull Request'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
