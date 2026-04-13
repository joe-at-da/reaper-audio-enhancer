from setuptools import setup, find_packages

setup(
    name="reaper-audio-enhancement",
    version="0.1.0",
    description="REAPER plugin for audio noise reduction and contextual audio enhancement",
    author="Audio Enhancement Team",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "librosa>=0.10.0",
        "numpy>=1.24.3",
        "scipy>=1.11.1",
        "opencv-python>=4.8.0",
        "PyQt5>=5.15.9",
        "python-osc>=1.8.3",
        "soundfile>=0.12.1",
        "matplotlib>=3.7.2",
        "Pillow>=10.0.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "reaper-audio-enhancement=src.main:main",
        ],
    },
)
