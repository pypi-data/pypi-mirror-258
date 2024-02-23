from setuptools import setup, find_packages

setup(
    name='pointextract',
    version='0.0.50',
    keywords=['transform', 'unwrap', 'topological'],
    description='Unwraps a circular surface through a topological transform',
    url='https://engineering.case.edu/centers/sdle/',
    author='Roger French (ORCID:000000-0002-6162-0532), \
            Thomas Ciardi (ORCID:0009-0006-0942-2666), \
            Liangyi Huang (ORCID:0000-0003-0845-3293)',
    author_email='roger.french@case.edu',
    license='BSD License (BSD-3)',
    packages=find_packages(),
)
