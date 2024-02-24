from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='libproton',
    version='3.3',
    url='https://github.com/PeterJCLaw/libproton',
    project_urls={
        'Issue tracker': 'https://github.com/PeterJCLaw/libproton/issues',
    },

    packages=find_packages(),

    description="Proton-compliant match scorer library.",
    long_description=long_description,
    long_description_content_type='text/markdown',

    author="Peter Law",
    author_email="PeterJCLaw@gmail.com",

    python_requires='>=3.7',
    install_requires=[
        'PyYAML >=3.11, <7',
    ],
    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],

    zip_safe=True,
)
