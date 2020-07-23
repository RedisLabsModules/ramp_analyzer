from setuptools import setup, find_packages
import io

def read_all(f):
    with io.open(f, encoding="utf-8") as I:
        return I.read()
    
requirements = list(map(str.strip, open("requirements.txt").readlines()))
    
setup(
    name='ramp-analyzer',
    version='1.0.0',
    description='Tool to analyze and modify ramp file',
    long_description=read_all("README.md"),
    long_description_content_type='text/markdown',
    url='https://github.com/RedisLabsModules/ramp_analyzer',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Database'
    ],
    keywords='RAMP',
    author='RedisLabs',
    author_email='oss@redislabs.com',
    entry_points='''
        [console_scripts]
        ramp-analyzer=ramp_analyzer.__main__:main
    '''
)
