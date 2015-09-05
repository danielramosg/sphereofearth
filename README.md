The Sphere of the Earth
=======================


Educational and museographic project for science museums and exhibitions, about cartography, maps and the geometry of the sphere.

The purpose is to develop an open source exhibit to be displayed in a science museum or science fair. In this repository one can find posters and programs that can be used in addition to some physical materials in order to create an exhibit.

First part of materials consist on a collection of posters with several map projections, obtained by manipulating a satellite image from NASA. Its intended use is to be printed and exhibited together with an Earth globe and some tools (rulers, protractors...)

Second part is a program that shows the Tissot's indicatrix for the same map projections. Tissot's indicatrix is a mathematical graphical tool that helps to understand the inherent distortion of a map.

The project was originally developed by Daniel Ramos, at Museu de Matemàtiques de Catalunya (MMACA), and was awarded the first prize on the international competition "Mathematics for Planet Earth 2013".

Written in Python/Qt and documented in LaTeX.

Program licensed under the General Public License v3.
Texts and documentation licensed under the Creative Commons Attribution license 4.0.


Install
-------

All the program is a bunch of python scripts. The only requirement is a working python installation together with appropriate libraries.

- Install on Linux (Ubuntu): Type the following commands in a terminal
    - $ sudo apt-get install python python-numpy python-pyproj python-qt4
    - $ python soe.py

- To run in fullscreen mode (exhibitions) use
    - $ python soe.py --fullscreen

- Install on Windows (preferred method).
    - Use the installer SoE_installer.exe

- Install on Windows (manual method). Download and install the interpreter and the libraries from their respective websites:

    - http://python.org/ftp/python/2.7.3/python-2.7.3.msi
    - http://sourceforge.net/projects/numpy/files/NumPy/1.7.0b2/numpy-1.7.0b2-win32-superpack-python2.7.exe/download
    - http://pyproj.googlecode.com/files/pyproj-1.9.2.win32-py2.7.exe
    - http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.9.5/PyQt-Py2.7-x86-gpl-4.9.5-1.exe
    - Double click on the file soe.py , select “Open with...” and select the program python.exe just installed.


















