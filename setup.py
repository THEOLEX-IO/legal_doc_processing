import setuptools
from legal_doc_processing.version import Version

REQUIRED = [
    'pandas','nltk','transformers'
]

setuptools.setup(name='legal_doc_processing',
                 version=Version('1.1.0').number,
                 description='Theolex document processing',
                 long_description=open('README.md').read().strip(),
                 long_description_content_type='text/x-rst',
                 author='Jawad Alaoui',
                 author_email='jawad@theolex.io',
                 url='http://theolex-document-processing',
                 packages=setuptools.find_packages(),
                 install_requires=REQUIRED,
                 license='MIT License',
                 zip_safe=False,
                 keywords='theolex document processing package',
                #  classifiers=['Packages', 'NLP']
                )
