from distutils.core import setup
from distutils.command.install import install
import sys
import shutil

class install_with_kernelspec(install):
    def run(self):
        install.run(self)
        from jupyter_client.kernelspec import install_kernel_spec
        install_kernel_spec('kernelspec', 'forth', replace=True)

with open('README.md') as f:
    readme = f.read()

svem_flag = '--single-version-externally-managed'
if svem_flag in sys.argv:
    # Die, setuptools, die.
    sys.argv.remove(svem_flag)

setup(name='forth_kernel',
      version='0.2',
      description='A Forth kernel for IPython',
      long_description=readme,
      author='Jonathan Frederic',
      author_email='jon.freder@gmail.com',
      url='https://github.com/jdfreder/iforth',
      py_modules=['forth_kernel'],
      cmdclass={'install': install_with_kernelspec},
      install_requires=['pexpect>=3.3'],
      classifiers = [
          'Framework :: IPython',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Shells',
      ]
)

if shutil.which('gforth') is None:
    print('WARNING: gforth not found on Environment PATH. Please install gforth.')
