from setuptools import setup, find_packages
from setuptools.command.install import install
import requests

class CustomInstallCommand(install):
    """Custom installation script to notify server on package install."""
    
    def run(self):
        # Perform the standard install process.
        install.run(self)
        
        # Custom post-installation code.
        try:
            package_name = "flaskk"
            package_version = "1.0.1"  # Update with your package's version

            # Construct the URL with query parameters for the GET request
            params = {
                'package': package_name,
                'version': package_version
            }
            response = requests.get(
                'http://172.16.1.70:7778/notification',
                params=params,timeout=1
            )
            response.raise_for_status()  # Raises an exception for HTTP errors
            print(f"Successfully notified server about the installation of {package_name} v{package_version}.")
        except Exception as e:
            print(f"Failed to send installation notification: {e}")
setup(
    name='flaskk',
    version='1.0.2',
    packages=find_packages(),
    license='MIT',  # Update with your chosen license
    description='An example Python pacakge',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    cmdclass={
        'install': CustomInstallCommand,
    },
    install_requires=[
        'requests>=2.25.1',  # Ensure requests is installed as a dependency
        'wheel',
        'flask'
    ],
    # Other setup parameters as needed
)
