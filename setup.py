import io
from subprocess import Popen, PIPE

from setuptools import setup


def get_version():
    p = Popen(['git', 'describe', '--tags'], stdout=PIPE, stderr=PIPE)
    p.stderr.close()
    line = p.stdout.readlines()[0]
    return line.strip().decode('utf-8')


setup(
    name='virga',
    version=get_version(),
    description='Analysing your Cloud infrastructure before the rain falls to the ground',
    long_description=io.open('README.rst', encoding='utf-8').read(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
    ],
    url='http://github.com/gurdulu/virga',
    author='Gurdulù',
    author_email='macgurd@gmail.com',
    license='MIT',
    packages=[
        'virga',
        'virga.providers',
        'virga.providers.aws',
    ],
    install_requires=io.open('requirements.txt', encoding='utf-8').readlines(),
    keywords='qa testing cloud aws',
    zip_safe=False,
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=[
        'bin/virga-asserts',
        'bin/virga-samples',
    ],
    include_package_data=True,
)
