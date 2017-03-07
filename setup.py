from distutils.core import setup

with open('README.md') as readme:
    long_description = readme.read()

try:
    import pypandoc
    long_description = pypandoc.convert(long_description, 'rst', 'markdown')
except(IOError, ImportError):
    long_description = long_description

VERSION = '1.0.1'

setup(
    name='asyncio-contextmanager',
    py_modules=['aiocontext'],
    version=VERSION,
    url='https://github.com/sashgorokhov/asyncio-contextmanager',
    download_url='https://github.com/sashgorokhov/asyncio-contextmanager/archive/v%s.zip' % VERSION,
    keywords=['python', 'asyncio'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development'
    ],
    long_description=long_description,
    license='MIT License',
    author='sashgorokhov',
    author_email='sashgorokhov@gmail.com',
    description='Decorator that turns async generator functions into async context managers.',
)