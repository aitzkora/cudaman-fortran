CUDAMAN-FORTRAN: CUDA API Fortran Reference to Man Pages
========================================

I stole the idea (and `template.man`) to the github project [https://github.com/sangmank/cudaman]. Trying to make it work, 
I decide to use another framework and to build man pages for FORTRAN instead of the C API.

Prerequisite
============

- python 3.8
- pandoc
- beautifulSoup for python
- requests

Generating man pages
====================
Simply type:
```bash
python extract_manpages.py
```
By default, this creates man pages in `./man8` directory. You can
change the directory by giving OUT_DIR option:

