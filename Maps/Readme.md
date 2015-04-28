The Sphere of the Earth.

Author: Daniel Ramos

This file explains how to configure and generate the maps. Maps are used in the Program, and you can also get pdf files to print them in poster size. You don't need to generate new maps if you want to use the default ones.

Configuration
=============
Using the configuration file param.ini, you can configure the source image, the size of the maps, and the center of some projections.


* Configuring the source image

By default it is used a NASA topographic map available at 
http://visibleearth.nasa.gov/view.php?id=57752
You can download it from the site or just running the script get_source.
You can also use another map (add country borders, change colors...). Use the src_img parameter to specify the source image.


* Configuring the maps size

The size of the maps is determined by two parameters: the radius of the globe and the resolution. The parameter radius_of_the_globe is the radius of your model of the Earth (in mm). The parameter resolution is in dots per inch (dpi).

If you print the images generated at this resolution, you will have a map at nominal scale 1:1 of your globe. This means that, for instance, if your globe has radius R, the equator of your Mercator map will measure 2*pi*R and your Gall-Peters map (which is equal-area) will have an area of 4*pi*R^2. This implies that the size of the maps will be very different from one to another (e.g. the Gnomonic map will be about 65 times bigger than the Gall-Peters map, and will also take 65 times the processing time). When running the scripts, you can find the sizes of the posters to be printed.

* Configuring the center of some projections

Certain maps (azimuthal equidistant, gnomonic) use a center location. Add the local coordinates (latitude and longitude) of your city to the file param.ini. The default maps provided with the program are centered in Barcelona.



Generating the maps
===================
Maps are composed of two layers: topography and graticule

* Check the requirements:

	$ sudo apt-get install python python-pyproj octave epstool

* To create the topographic images, enter the folder 'topography' and run

	$ ./get_source

	$ ./create_topo

	You will see the sizes of each map in mm and in pixels. Don't run get_source if you configured another source image.

* To greate the graticules, enter the folder 'graticules' and run

	$ ./create_graticules

	Both sets of files will apear on the folder 'images'. 

* Merge each topographic map with its graticule using Inkscape:
	- Open the svg file.
	- Add the image map in the background (linked, not embedded).	
	- Change the canvas size and adapt to the map (size of bitmap image).
	- Change the color and width of the lines as desired (e.g. grey L 120, 4 px)
	- Save the svg file.

* If you want to print the maps, you may want to export the svg images as pdf. Check the dimensions with the values given by the create_topo script.

* If you want to generate the images for the program, run the script 'to_final' to convert all the svg images to png images. Use the resolution as the parameter.

	$ ./to_final 30

	Then copy the images from the folder 'final' to the folder 'Program'.


