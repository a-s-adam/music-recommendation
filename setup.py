from setuptools import setup, find_packages

# Function to parse requirements.txt
def parse_requirements(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    # Filter out comments and empty lines
    requirements = [
        line.strip() for line in lines
        if line.strip() and not line.startswith('#')
    ]
    return requirements

setup(
    name='recommendation-system',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_project',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
