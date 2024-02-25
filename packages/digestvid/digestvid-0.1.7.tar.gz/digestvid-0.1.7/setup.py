from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='digestvid',
    version='0.1.7',
    author='AI Sherpa',
    author_email='contact@ai-sherpa.com',
    packages=find_packages(),
    install_requires=[
        'moviepy>=1.0.0',
        'openai-whisper>=2023117',
        'openai>=1.0.0',
        'yt_dlp>=2021.12.1',
        'pyyaml>=6.0.0',
    ],
    description='A tool to transcribe and summarize video content.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/AI-Sherpa/digestvid',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'digestvid=digestvid.main:main',
        ],
    }
)
