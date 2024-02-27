from setuptools import setup, find_packages

setup(
    name="auto_fill_don",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        # Add dependencies here,
        # e.g. 'numpy>=1.11.1'
    ],
    entry_points={
        "console_scripts": [
            "auto_fill_don = auto_fill_don:autofill",
            "don = auto_fill_don:don"
        ]
    }
)
