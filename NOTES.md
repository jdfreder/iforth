# Notes
- Difficult to test on Windows, because I can't find an easy way to install `gforth` on Windows - 
  installing from source is too much work 🤷!
     - Will have to try to run in WSL...

## What files are actually installed?
[How to uninstall after `python setup.py install`](https://stackoverflow.com/a/1550235/12947681)

After `sudo python setup.py install --record files.txt`:
```
> cat files.txt
/usr/local/lib/python3.10/site-packages/forth_kernel.py
/usr/local/lib/python3.10/site-packages/__pycache__/forth_kernel.cpython-310.pyc
/usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info
```

The location of `forth_kernel` Python module is at `/home/sohang/.local/lib/python3.10/site-packages/forth_kernel.py`.

Additionally, the actual Jupyter Kernel is at `/usr/local/share/jupyter/kernels/forth/kernel.json`.

The command below failed due to insufficient permission, but the output is still interesting!
```
> python setup.py install --record files.txt
/home/sohang/external-src/iforth/setup.py:1: DeprecationWarning: The distutils package is deprecated and slated for removal in Python 3.12. Use setuptools or check PEP 632 for potential alternatives
  from distutils.core import setup
/usr/lib64/python3.10/distutils/dist.py:274: UserWarning: Unknown distribution option: 'install_requires'
  warnings.warn(msg)
running install
running build
running build_py
running install_lib
running install_egg_info
removing '/usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info' (and everything under it)
error removing /usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info: [Errno 13] Permission denied: '/usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info/PKG-INFO'
error removing /usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info: [Errno 13] Permission denied: '/usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info/dependency_links.txt'
error removing /usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info: [Errno 13] Permission denied: '/usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info/requires.txt'
error removing /usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info: [Errno 13] Permission denied: '/usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info/top_level.txt'
error removing /usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info: [Errno 13] Permission denied: '/usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info/SOURCES.txt'
error removing /usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info: [Errno 13] Permission denied: '/usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info/installed-files.txt'
error removing /usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info: [Errno 13] Permission denied: '/usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info'
Writing /usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info
error: [Errno 21] Is a directory: '/usr/local/lib/python3.10/site-packages/forth_kernel-0.2-py3.10.egg-info'
```
