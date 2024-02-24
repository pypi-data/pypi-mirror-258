from setuptools import setup

setup(
    name='pythlete',
    version='0.1.1',
    description='Python package for instantaneous decision making in sports',
    url='https://github.com/AbdullahKhurram30/Pythlete',
    author='Muhammad Abdullah Khan',
    author_email='abdullah.khurram@uni.minerva.edu',
    packages=['pythlete'],
    install_requires=['fastf1==3.1.3', 'ipython', 'matplotlib==3.5.3',
                      'numpy==1.22.4', 'pandas==1.4.4', 'scipy==1.7.3',
                      'seaborn==0.11.1']
)