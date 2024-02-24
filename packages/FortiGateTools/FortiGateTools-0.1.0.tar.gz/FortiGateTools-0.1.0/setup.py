from setuptools import setup, find_packages

setup(
    name='FortiGateTools',  # Replace with your package name
    version='0.1.0',
    author='Jeremiah Eastwood',  # Replace with your name
    author_email='cisconomadic@gmail.com',  # Replace with your email
    description='Tools for FortiGate configuration comparison and MOP operations',
    long_description=open('README.md').read(),  # If you have a README.md file
    long_description_content_type='text/markdown',
    url='https://github.com/yourgithub/FortiGateTools',  # Replace with the URL to your project
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',  # Assuming you are using pandas as seen in the filenames
        'urllib3',
        'csv',
        'json',
        'os',
        'urllib3', 
        # Add any other dependencies required by your scripts
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Or whichever license you choose
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',  # Adjust based on your compatibility requirements
)


