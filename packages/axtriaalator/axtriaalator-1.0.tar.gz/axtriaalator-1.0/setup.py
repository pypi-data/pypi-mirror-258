from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='axtriaalator',
    version='1.0',
    url='https://github.com/Rehaaaan/tensorfloe/tree/master',
    packages=find_packages(),
    author='Your Name',
    author_email='your@email.com',
    description='Description of your package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'spam = tensorfloe.spam:main',
            'sentiment = tensorfloe.sentiment:main',
            'gender = tensorfloe.gender:main',
            'pos = tensorfloe.pos:main',
            'word2vec = tensorfloe.word2vec:main',
            'skipgram = tensorfloe.skipgram:main',
            'chatbot = tensorfloe.chatbot:main',
            'summary = tensorfloe.summary:main',
            'transformer = tensorfloe.transformer:main',
            'latent = tensorfloe.latent:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

