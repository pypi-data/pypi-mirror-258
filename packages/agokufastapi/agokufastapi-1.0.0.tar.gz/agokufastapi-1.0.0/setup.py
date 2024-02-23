from setuptools import setup, find_packages

setup(
    name='agokufastapi',
    version='1.0.0',
    author='zyx',
    author_email='308711822@qq.com',
    description='基于Fatapi框架的封装扩展库',
    long_description='个人封装的库',
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    install_requires=[
        'aiohttp==3.9.3',
        'aiojobs==1.2.1',
        'fastapi==0.109.2',
        'pydantic==2.6.1',
        'pyee==11.1.0',
        'setuptools==65.5.0',
        'starlette==0.26.1',
        'typing_extensions==4.9.0',
        'uvicorn==0.27.1',
    ],
)
