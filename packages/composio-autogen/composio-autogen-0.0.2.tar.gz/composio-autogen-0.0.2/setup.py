from setuptools import setup, find_packages

setup(
    name = 'composio-autogen',
    version = '0.0.2',
    author = 'Utkarsh',
    author_email = 'utkarsh@composio.dev',
    description = 'Provides integrations skill with 50+ services in autogen',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/SamparkAI/autogen-composio-skills',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    python_requires = '>=3.7',
    include_package_data = True,
    scripts = ['composio-autogen'],
)
