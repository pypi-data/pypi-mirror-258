from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name="mcMqttComms",
    version="0.1.2",
    description="Module for handling mission control messages to be sent to a Drone via MQTT.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages= find_packages(where="src"),
    package_dir={
    '': 'src',
    },
    author="Jonathan Thai",
    author_email="thaijonathan53@gmail.com",      
    install_requires = ["boto3", "paho-mqtt"]
      
      
      )


