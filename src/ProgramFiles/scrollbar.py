import Tkinter as tk
import copy

class ImageScrollbar(tk.Scrollbar):
	def __init__(self, *args, **kwargs):
		"""
		Initialize a new ImageScrollbar
		"""
		tk.Scrollbar.__init__(self, command=self.scrollbarCallback, *args, **kwargs)
		self.imageList = []
		self.step = 1.0
		self.set(0.0,1.0)

	def setImageList(self, imageList):
		"""
		Set the current image list for the scrollbar, adjust the step size to match, and move to the first image
		<imageList> A list containing 5-tuples with the following format: (imageObj, filePath, byteSize, height, width)
					The first item will be displayed on the canvas, the rest will be displayed in the corresponding labels
					Note that, for field images, the byte size, height, and width should correspond to the field, not the image.
		"""
		self.imageList = imageList
		self.step = 1.0/len(imageList)
		self.scrollbarCallback("moveto", 0.0)

	def disableScrollbar(self):
		"""
		Disable the scrollbar
		"""
		global canvas
		global currentName
		global currentSize
		global currentWidth
		global currentHeight
		self.imageList = []
		self.step = 1.0
		self.set(0.0,1.0)
		canvas.delete("all")
		currentName.set("Name:\n")
		currentSize.set("Size:\n")
		currentWidth.set("Width:\n")
		currentHeight.set("Height:\n")

	def setNoPreview(self, path, byteSize):
		"""
		Sets the scrollbar preview to a random "No Preview" icon
		"""
		self.imageList = [(GetNoPreviewImage(), path, byteSize, "", "")]
		self.step = 1.0
		self.scrollbarCallback("moveto", 0.0)

	def scrollbarCallback(self, *args):
		"""
		Callback function for when the scrollbar is moved
		"""
		# Move the scrollbar to the correct position
		if args[0] == "moveto":
			# Gets the scrollbar's current position as (top, bottom); values range from zero (highest position) to one (lowest position)
			pos = self.get()

			""" 
				First, we check if the args are asking us to move to or past the boundary.
			 	This should only be an issue if there's rounding error, but there WILL be rounding error,
				especially because different parts of Tkinter return floats with different levels of
				approximation. Thanks Tkinter.
			""" 
			if float(args[1]) <= 0:
				# Scrollbar goes to the top
				self.set(0.0,self.step)
			elif float(args[1]) + self.step > 1:
				# Scrollbar goes to the bottom
				self.set(1.0-self.step,1.0)
			else:
				rangeOfValues = numpy.arange(0,1, self.step)
				# Find the closest position and snap to it
				newTopValue = TakeClosest(rangeOfValues,float(args[1]))
				self.set(newTopValue,newTopValue+self.step)
				
		else:
			pos = self.get()
			if args[1] == "-1":
				# Check if we're already at the top, and don't try to go higher!
				if round(pos[0], 5) == 0.0:
					pass
				else:
					self.set(float(pos[0])-self.step, float(pos[1])-self.step)
			else:
				# Ditto, but for the bottom
				if round(pos[1], 5) == 1.0:
					pass
				else:
					self.set(float(pos[0])+self.step, float(pos[1])+self.step)


		# Update GUI displays
		global currentImage
		global currentName
		global currentSize
		global currentWidth
		global currentHeight

		imageIdx = int(
		math.floor(
			round(self.get()[0]*(1/self.step), 2)
			)
		)
		currentImage = self.imageList[imageIdx][0]
		canvas.delete("all")
		imagePreview = canvas.create_image(77,77,image=currentImage)

		# Finally, set the display labels
		if self.imageList[imageIdx][1] != None:
			m = re.search("([^/]+)/?$", self.imageList[imageIdx][1])
			currentName.set("Name:\n" + m.group(0))
		else:
			currentName.set("Name:\n")
		if self.imageList[imageIdx][2] != None:
			currentSize.set("Size:\n" + str(self.imageList[imageIdx][2]) + " bytes")
		else:
			currentSize.set("Size:\n")
		currentHeight.set("Height:\n" + str(self.imageList[imageIdx][3]))
		currentWidth.set("Width:\n" + str(self.imageList[imageIdx][4]))