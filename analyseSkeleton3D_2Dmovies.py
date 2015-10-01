#!/usr/bin/env python

# This is a Python script that can be run from Fiji (is just imageJ - batteries incuded),
# using the builtin Jython interpreter
#(Jython is a java implementation of Python which runs natively on the Java Virtual machine.
# You can use all java classes and imagej classes from it, which is nice.)

# Purpose of this script:
# There is a limitation in the Analyze Skeleton 2D/3D plugin
# where it can not handle a 2D time series stack as such.
# It just treats it as a z series, meaning that the results are not as expected
# since it treats the data as a single 3D dataset instead of as many 2D time points.

# Solution
# To get around this limiatation,
# we can run the "Analyze Skeleton (2D/3D)" command
# on each individual frame of the time series, 
# since the plygin a"Analyze Skeleton (2D/3D)" works as expected on single frames!
# We need to output the results for each frame, in a sensible readable manner (save as .xls)
# and make a tagged results image "movie" by converting all the single frame
# taqgged result images into a stack.


# how to use this script

#1) Install the script by putting it in the Fiji plugins directory,
# then run menu command Plugins - Scripting - Refresh Jythion Scripts.
# The script name will then appear in the plugins menu (at the bottom)

#2) open a movie dataset in Fiji - check image metadata (Bat Cochlea Volume sample image works)
# check that it is a 2D movie not a 3D z stack:
# select the mobie image window, then do menu item Image - Properties
# You might need to change it from a z stack to a time series by changing the numbers there.
# You can also set the pixel size here if it is wrong in the first instance,
# so your results are calibrated in micrometers etc. instead of pixels (i hope thats true)

#3) Segment objects from the background, for instance using one of the auto threshold methods,
# such that you have an 8 bit binary image comtaining zeros for background and 255 for objects.

#4) Skeletonize each frame of the movie using the menu command Process - Bnary - Skeletonize
# Click yes when it asks you if you want to do all the frames/slices in the movie.

#5) Run the script:
#with the skeletonized movie selected run the script by choosing it from the plugins menu.
# NOTE!!! You MUST change the line in the script:
# IJ.saveAs("Measurements", ("/Users/dan/Desktop/Results" + str(i) + ".xls") )
# so that the path to where you want the results .xls files to be written!!!
# On windows it might need to be something like:
# IJ.saveAs("Measurements", ("C:\\Some Folder\\Whatever name want" + str(i) + ".xls") )

#6) Save the result tagged image movie: TaggedMovie (as a a tiff for example) and the
# results summary which is in the Log window. 
# The results for each frame were already saved in the last step!




# from java.util.concurrent import Executors  # lets hold off on multithreading for now.
from ij import IJ, ImagePlus
#from ij.plugin import Concatenator

# the current image
imp = IJ.getImage()
stack = imp.getStack()


#class Task(Runnable):
#  def __init__(self, slice):
#    self.slice = slice
#  def run(self):
#    IJ.run(self.slice, "Analyze Skeleton (2D/3D)", "")

#futures = []  # list of tasks submitted to the threads Executor pool

# A pool of threads to process the slices
#exe = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors())

# for all the frames in the movie, run  "Analyze Skeleton (2D/3D)" (maybe later in multiple threads)
for i in range(1, imp.getNFrames() + 1):  # remember a python range (1, 10) is the numbers 1 to 9 !
#getNFrames not getNSlices since input data is a 2D time series stack NOT a 3D stack.
  slice = ImagePlus(str(i), stack.getProcessor(i))
  # Execute plugin exactly on this slice i
  IJ.run(slice, "Analyze Skeleton (2D/3D)", "")
  #fu = exe.submit(Task(slice))
  #futures.append(fu)
  IJ.saveAs("Measurements", ("/Users/dan/Desktop/Results" + str(i) + ".xls") )

 
# Wait until all finish
#for fu in futures:
#  fu.get()

# Quit threads
#exe.shutdownNow()


# concatenate the new tagged image onto the end of the tagged image stack we want in the end, but not if its then 1st one!
   
  if i == 1:
    IJ.run("Rename...", "TaggedImageMovie")
  else:
    IJ.run("Concatenate...", "stack1=[TaggedImageMovie] stack2=[Tagged skeleton] title=TaggedImageMovie")


IJ.log("Done!")