import struct

class DDSLoader:
	"""A very basic DDS loader. Only works with uncompressed DDSes, whereas Pyglet and Pillow (among others) only work with DDSes using compression."""

	def __init__(self,data,height=0,width=0):
		if isinstance(data, list):
			self.data = data
			self.height = height
			self.width = width
			#self.hasAlpha =
			#self.bitDepth = 
			self.channelOrder = "RGBA"
		elif isinstance(data, str) or isinstance(data, unicode):
			# Load data from Path
			path = data
			self.data = [[]]
			with open(path, "rb") as texture:
				word = texture.read(4) # Magic numbers
				if word.encode("hex") != "44445320":
					raise ValueError("File provided is not a .dds file")
				texture.read(4) # Header size; should always be 0x7C = 124
				word = texture.read(4) # Header flags, denotes which values are written
				word = struct.unpack("I",word)[0]
				if not (word & 0x1): # All of these flags are nominally required, so print a warning if they're not there.
					print "Warning! Caps flag not set in DDS file."
				if not (word & 0x2):
					print "Warning! Height flag not set in DDS file."
				if not (word & 0x4):
					print "Warning! Width flag not set in DDS file."
				if not (word & 0x1000):
					print "Warning! Pixelformat flag not set in DDS file."
				self.height = struct.unpack("I",texture.read(4))[0] # Image Height
				self.width = struct.unpack("I",texture.read(4))[0] # Image Width
				texture.read(4) # PitchOrLinearSize
				texture.read(4) # Depth
				texture.read(4) # MipMapCount
				for i in xrange(11):
					texture.read(4) # Unused (11 element DWORD array)
				# Pixel Format information begins here
				texture.read(4) # Pixel Format size; should always be 0x20 = 32
				word = texture.read(4) # Pixel format flags
				word = struct.unpack("I",word)[0]
				if (word & 0x1):
					self.hasAlpha = True
				else:
					self.hasAlpha = False
				if (word & 0x4):
					# Data is compressed
					# This DDS loader is meant to work with uncompressed DDSes; raise an exception to let the developer know they should be using Pillow or Pyglet!
					raise ValueError("DDS file provided has compression")
				if (word & 0x200):
					# Data is in YUV format
					# This DDS loader is not meant to work with YUV files (like any DDS loader you're likely to come across!); raise an exception to let the developer know.
					raise ValueError("DDS file is in the YUV format and cannot be read")
				if (word & 0x20000):
					# Data is in monochrome format
					# This DDS loader is not meant to work with single-channel files; raise an exception to let the developer know.
					raise ValueError("DDS file is in the single-channel format and cannot be read")
				if not (word & 0x40):
					# This flag *should* be set if the previous three flags are not. The only way for this flag and the previous flags to all be unset would be a poorly-created DDS
					# Print a warning and attempt to read the data anyway (which, if the DDS does not contain that data, will crash)
					print "Warning! DDPF_FOURCC and DDPF_RGB flags are both unset! DDS file may be damaged or incorrectly saved!"
				texture.read(4) # Compression format
				self.bitDepth = struct.unpack("I",texture.read(4))[0] # Number of bits per pixel
				# Next, we determine the order of the color channels
				self.channelOrder = ""
				flags = (("R",struct.unpack("I",texture.read(4))[0]),("G",struct.unpack("I",texture.read(4))[0]),("B",struct.unpack("I",texture.read(4))[0]),("A",struct.unpack("I",texture.read(4))[0]))
				for i in flags:
					if i[1] == 255:
						self.channelOrder += i[0]
				for i in flags:
					if i[1] == 65280:
						self.channelOrder += i[0]
				for i in flags:
					if i[1] == 16711680:
						self.channelOrder += i[0]
				for i in flags:
					if i[1] == 4278190080:
						self.channelOrder += i[0]
				# Pixel format ends here
				texture.read(4) # Complexity data for DDS files with multiple surfaces
				texture.read(4) # ^
				texture.read(12) # Unused

				# Now, we load in the image data:
				word = texture.read(4)
				rowLength = 0
				col = 0
				while word:
					pixel = (struct.unpack("B",word[0]),struct.unpack("B",word[1]),struct.unpack("B",word[2]),struct.unpack("B",word[3]))
					pixelOrder = list(self.channelOrder)
					self.data[col].append(pixel[pixelOrder.index("R")][0])
					self.data[col].append(pixel[pixelOrder.index("G")][0])
					self.data[col].append(pixel[pixelOrder.index("B")][0])
					self.data[col].append(pixel[pixelOrder.index("A")][0])
					word = texture.read(4)
					if rowLength + 1 == self.width:
						rowLength = 0
						col += 1
						self.data.append([])
					else:
						rowLength += 1
				if len(self.data[-1]) == 0: # "But it's more pythonic to use if not self.data[-1]!" "It's also less explicit"
					self.data.pop(-1)
		else:
			raise ValueError("DDSLoader needs string filepath or list pixel data")

	def getData(self):
		return self.data

	def getHeight(self):
		return self.height

	def getWidth(self):
		return self.width

	def save(self, path):
		"""Save a new DDS file to the given path"""
		with open(path, "wb") as outputFile:
			outputFile.write("\x44\x44\x53\x20") # Magic numbers
			outputFile.write("\x7C\x00\x00\x00") # Header size
			outputFile.write("\x07\x10\x00\x00") # Header flags: Caps, Height, Width, and PixelFormat are valid, everything else is unset
			outputFile.write(struct.pack("I", self.height)) # Image height
			outputFile.write(struct.pack("I", self.width)) # Image width
			outputFile.write("\x00\x00\x00\x00") # PitchOrLinearSize
			outputFile.write("\x00\x00\x00\x00") # Depth
			outputFile.write("\x00\x00\x00\x00") # MipMap Count
			for i in xrange(11):
				outputFile.write("\x00\x00\x00\x00") # 11 Element DWORD Array
			# Pixel Format begins here
			outputFile.write("\x20\x00\x00\x00") # Pixel Format size
			outputFile.write("\x41\x00\x00\x00") # Pixel Format flags: Alpha and uncompressed RGBA masks are valid, everything else is unset
			outputFile.write("\x00\x00\x00\x00") # Compression format
			outputFile.write("\x20\x00\x00\x00") # Bit depth
			outputFile.write("\x00\x00\xFF\x00") # Red mask; Data is output in the B8G8R8A8 format, as this is what OJ uses natively
			outputFile.write("\x00\xFF\x00\x00") # Green mask; Presumably the less strange R8G8B8A8 would also work, but for the sake
			outputFile.write("\xFF\x00\x00\x00") # Blue mask; of being as accurate to the original game as possible, BGRA is used instead
			outputFile.write("\x00\x00\x00\xFF") # Alpha mask
			outputFile.write("\x02\x10\x00\x00") # Complexity data
			outputFile.write("\x00\x00\x00\x00") # ^
			outputFile.write("\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00") # Unused
			for row in self.data:
				for i in xrange(0, len(row), 4):
					# red = row[i], green = row[i+1], blue = row[i+2], alpha = row[i+3]
					outputFile.write(struct.pack("B",row[i+2])[0]) 
					outputFile.write(struct.pack("B",row[i+1])[0])
					outputFile.write(struct.pack("B",row[i])[0])
					outputFile.write(struct.pack("B",row[i+3])[0])
