import setuptools
from legal_doc_processing.version import Version


setuptools.setup(name='legal_doc_processing',
                 version=Version('1.0.0').number,
                 description='Theolex document processing',
                 long_description=open('README.md').read().strip(),
                 long_description_content_type='text/x-rst',
                 author='Jawad Alaoui',
                 author_email='jawad@theolex.io',
                 url='http://theolex-document-processing',
                 packages=setuptools.find_packages(),
                #  py_modules=['legal_doc_processing'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='theolex document processing package',
                #  classifiers=['Packages', 'NLP']
                )
