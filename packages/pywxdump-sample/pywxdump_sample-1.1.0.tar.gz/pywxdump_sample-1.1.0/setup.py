from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "1.1.0"

install_requires = [
    "pymem",
    "psutil"
]

setup(
    name="pywxdump_sample",
    author="",
    version=version,
    author_email="",
    description="微信信息获取工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zezezez/pywxdump_sample/",
    license='MIT',

    packages=['pywxdump_mini'],
    package_dir={'pywxdump_mini': 'pywxdump_mini'},

    package_data={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6, <4',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'wxinfo = pywxdump_mini.simplify_wx_info:read_info',
        ],
    },
    setup_requires=['wheel']
)
