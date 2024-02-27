from setuptools import setup
import os


def find_stubs(package):
    stubs = []
    for root, dirs, files in os.walk(package):
        for file in files:
            path = os.path.join(root, file).replace(package + os.sep, '', 1)
            stubs.append(path)
    return dict(package=stubs)


setup(
    name='_robotic-stubs',
    maintainer="_robotic Developers",
    maintainer_email="example@python.org",
    description="PEP 561 type stubs for _robotic",
    version='1.0',
    packages=['_robotic-stubs'],
    # PEP 561 requires these
    install_requires=['_robotic'],
    package_data=find_stubs('_robotic-stubs'),
)