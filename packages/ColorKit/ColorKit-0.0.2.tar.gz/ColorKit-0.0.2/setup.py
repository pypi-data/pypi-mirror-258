from setuptools import setup, find_packages

VERSION = '0.0.2'

DESCRIPTION = 'Python advanced color package'

# Setting up
setup(
    name="ColorKit",
    version=VERSION,
    url='https://github.com/bzm10/ColorKit',
    project_urls={
        'Source Code': 'https://github.com/bzm10/ColorKit',
    },  # Added comma here
    author="Benjamin Markovits",
    author_email="bzmarkovits@yahoo.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=["color conversion", "RGB", "HEX", "CMYK", "HSL", "LAB", "LUV", "XYZ", "YIQ", "HSV", "YUV", "YCbCr", "LCH", "LMS", "color toolkit", "color space", "Python color", "color manipulation", "color analysis", "color utility","python","color"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)