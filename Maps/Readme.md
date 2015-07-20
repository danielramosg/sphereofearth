The Sphere of the Earth.

Author: Daniel Ramos

This file explains how to configure and generate the maps. Maps are used in the Program, and you can also get pdf files to print them in poster size. You don't need to generate new maps if you want to use the default ones.
It is recommended to use a Linux system.

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

If you print the images generated at this resolution, you will have a map at nominal scale 1:1 of your globe. This means that, for instance, if your globe has radius R, the equator of your Mercator map will measure 2*pi*R and your Gall-Peters map (which is equal-area) will have an area of 4*pi*R^2. This implies that the size of the maps will be very different from one to another (e.g. the Gnomonic map will be about 60 times bigger than the Gall-Peters map, and will also take 60 times the processing time). When running the scripts, you can find the sizes of the posters to be printed.

* Configuring the center of some projections

Certain maps (azimuthal equidistant, gnomonic) use a center location. Add the local coordinates (latitude and longitude) of your city to the file param.ini. The default maps provided with the program are centered in Barcelona.



Generating the maps (for the Program)
=====================================

* Check that you have the required packages:

	$ sudo apt-get install python python-pyproj python-scitools python-pil

* Download the NASA satellite image with the topographic data:
	$ ./get_source

* Open the file param.ini and configure it with your local coordinates. You can leave a radius of 50 and a resolution of 200.

* Run the script make_maps:
	$ ./make_maps

The new images will be automatically placed in the Program folder. In order to run the program you only need the file param.ini and the folder Program. Once you are done, you can safely delete the NASA original file.


Generating the maps (for Printing)
==================================
If you want to print the maps at "nominal scale 1:1" of your globe, do the following:

* Download the NASA image and configure the parameters as above. Make sure that you measure the radius (not the diameter) of your globe in milimeters (e.g. 100 mm for a 20 cm diameter globe). Use a printing resolution of at least 300 dpi.

* Open the file mapping_routines.py and uncomment the last line, while commenting the penultimate line. This is to generate pdf files.
	#plt.savefig(name + '.png',dpi=resol, bbox_inches='tight', pad_inches=0)
	plt.savefig(name + '.pdf',dpi=resol, bbox_inches='tight', pad_inches=0)

* Run the script make_maps:
	$ ./make_maps
Beware that this can take a long time (40 min or more in a recent computer).

* You will get six pdf files. Pdf files contain information of physical document size and resolution. You can bring the files to a reprographic service and get the posters. Tell them NOT TO RESCALE the documents. You can write down the size of the posters that you will obtain in the console while running the scripts.






	
