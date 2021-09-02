import setuptools
from legal_doc_processing.version import Version
import setuptools.command.build_py
from subprocess import call
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call

REQUIRED = [
    "pandas",
    "nltk",
    "transformers",
    "spacy",
    "tensorflow",
    "clean-text",
    "word2vec",
    "dateparser",
    "scikit-learn",
    "google-cloud-storage",
]

setuptools.setup(
    name="legal_doc_processing",
    version=Version("2.2.6").number,
    description="Theolex document processing",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/x-rst",
    author="Jawad Alaoui",
    author_email="jawad@theolex.io",
    url="http://theolex-document-processing",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=REQUIRED,
    license="MIT License",
    zip_safe=False,
    keywords="theolex document processing package",
    #  classifiers=['Packages', 'NLP']
)
