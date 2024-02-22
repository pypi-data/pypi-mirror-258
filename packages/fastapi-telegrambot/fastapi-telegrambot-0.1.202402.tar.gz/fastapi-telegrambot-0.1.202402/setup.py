from setuptools import setup, find_packages
import app

with open( 'README.md', 'r', encoding = 'utf-8' ) as f:
    long_description = f.read()

setup(
    name = 'fastapi-telegrambot',
    version = app.__version__,
    author = 'knowidea-k',
    author_email = 'knowidea.k@gmail.com',
    description = 'TelegramBot wrapped by FastAPI',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/knowidea-k/fastapi-telegrambot',
    project_urls = {
        'Bug Tracker': 'https://github.com/knowidea-k/fastapi-telegrambot/issues',
    },
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir = { '': 'app' },
    packages = find_packages( where = 'app' ),
    python_requires = '>=3.6',
    install_requires = [ 'uvicorn', 'fastapi', 'asyncio', 'python-telegram-bot', 'setuptools', 'pydantic' ],
)