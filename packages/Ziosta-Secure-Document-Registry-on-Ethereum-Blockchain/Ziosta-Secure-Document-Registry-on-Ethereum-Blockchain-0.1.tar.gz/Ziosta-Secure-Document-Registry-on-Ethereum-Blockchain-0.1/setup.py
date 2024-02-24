from setuptools import setup, find_packages

setup(
    name='Ziosta-Secure-Document-Registry-on-Ethereum-Blockchain',
    version='0.1',
    url='https://github.com/ziosta/Ziosta-Secure-Document-Registry-on-Ethereum-Blockchain',
    author='Ziosta',
    author_email='ziosta.eth@gmail.com',
    packages=find_packages(),
    install_requires=[
        'web3==5.24.0'
        # Eğer projenizde başka bağımlılıklar varsa buraya ekleyin
    ],
)
