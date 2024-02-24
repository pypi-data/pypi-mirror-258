from setuptools import setup

setup(
    name='Watermarkerer',
    url='https://github.com/NoneNameDeveloper/WaterMarkerer.git',
    author='John Doe',
    author_email='anon@user.com',
    packages=["watermarkerer"],
    install_requires=['pillow==9.5.0', 'moviepy==1.0.3'],
    version='0.1',
    license='MIT',
    description='Python package to put watermarks to videos or images',
)