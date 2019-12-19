from ast import literal_eval
import Tkinter as tk
import tempfile
import math
import copy
import re
import pprint
import struct
import platform
import sys
import os

pp = pprint.PrettyPrinter(depth=6)

def BuildPak(outputDir, paddedMaps):
	# Prepare the output file:
	if outputDir[-1] == "/":
		outputPath = outputDir + "fields.pak"
	else:
		outputPath = outputDir + "/fields.pak"
	outputFile = zipfile.ZipFile(outputPath, mode="w")

	global mapsTable
	global graphicsList

	for slot, mapInfo in sorted(mapsTable.iteritems()):
		newPath = ""
		isOfficial = False
		isPadded = False
		# Check if official
		if mapInfo[3].get() == "":
			isOfficial = True
			m = re.search("([^/]+)/?$", slot)
			mapName = m.group(0)
			newPath = "OfficialFiles\\" + mapName
		else:
			m = re.search("([^/]+)/?$", mapInfo[3].get())
			mapName = m.group(0)
			newPath = mapInfo[3].get()
		# Check if padded
		if slot in paddedMaps:
			isPadded = True
			newPath = paddedMaps[slot]
		# Get display name of map slot
		displayName = mapInfo[2]
		if mapInfo[0] not in (968, 1352, 1800):
			m = re.search("(.*)\\(", displayName)
			displayName = m.group(0)
			displayName = displayName[0:-1]
		if mapInfo[1]:
			displayName += " Co-op"
		# Add map to archive and print output info
		PrettyPrintMapDetails(mapName, displayName, isOfficial, isPadded)
		outputFile.write(newPath, arcname=slot)

	for i in graphicsList:
		newPath = "OfficialFiles\\" + i
		outputFile.write(newPath,arcname=i)

	for i in paddedMaps:
		os.unlink(paddedMaps[i])

	outputFile.close()

def LoadBaseFile(baseFieldPath):
	"""
	Returns size of map (in cols*8, the 8 representing the 8 bytes that each tile takes up) and the filesize of a corresponding field
	"""
	baseFieldInfo = os.stat(baseFieldPath)
	baseFieldSize = baseFieldInfo.st_size

	global fieldSizeTable

	return fieldSizeTable[baseFieldSize], baseFieldSize

def PadMaps(isSpecific):
	"""
	For each map in the table, check if it's been replaced with a custom map, and if so, if it must be padded, replace the replacement filename with the padded file
	return: a dict associating custom map filepaths with the name of the temporary file containing a padded verison
	"""
	global mapsTable
	paddedMaps = {}
	for i in mapsTable:
		mapFilePath = mapsTable[i][3].get()
		if mapFilePath != "":
			# Check if it needs to be padded
			mapFileSize = os.stat(mapFilePath).st_size
			if mapFileSize > mapsTable[i][0]:
				# Print an error to the in-GUI console and set the custom map back to ""
				m = re.search("([^/]+)/?$", mapFilePath)
				mapFileName = m.group(0)[0:-4]

				if isSpecific:
					outputErrorText = "Warning! %s is bigger than %s; %s will be used instead.\n" % (mapFileName, i, i)
				else:
					outputErrorText = "Warning! No space could be found for %s; %s will be used instead.\n" % (mapFileName, i)

				PrettyPrintConsoleError(outputErrorText)

				mapsTable[i][3].set("")
			elif mapFileSize < mapsTable[i][0]:
				# Pad the map
				paddedMap = AutoPadMap(mapFilePath, mapsTable[i][0]).name
				paddedMaps[i] = paddedMap
	return paddedMaps

def AssignSlots(normalPaths, coopPaths):
	"""
	Automatically assign fields to appropriate map slots in the global maps table
	<normalPaths> A tk.askopenfilenames object containing normal mode paths
	<coopPaths> A tk.askopenfilenames object containing coop mode paths
	"""
	normalFields = ParseMultipleFilenames(normalPaths)
	coopFields = ParseMultipleFilenames(coopPaths)
	for field in normalFields:
		found = False
		for mapSlot in mapsTable.values():
			if mapSlot[3].get() == "" and mapSlot[0] >= os.stat(field).st_size and mapSlot[1] == False:
				mapSlot[3].set(field)
				found = True
				break
		if not found:
			m = re.search("([^/]+)/?$", field)
			mapFileName = m.group(0)[0:-4]
			PrettyPrintConsoleError("Warning! No space could be found for %s" % mapFileName)
	for field in coopFields:
		found = False
		for mapSlot in mapsTable.values():
			if mapSlot[3].get() == "" and mapSlot[0] >= os.stat(field).st_size and mapSlot[1] == True:
				mapSlot[3].set(field)
				found = True
				break
		if not found:
			m = re.search("([^/]+)/?$", field)
			mapFileName = m.group(0)[0:-4]
			PrettyPrintConsoleError("Warning! No space could be found for %s" % mapFileName)

def ConvertImageToField(inputPath, outputPath):
	"""
	Converts a PNG image to a FLD file, and outputs it to the specified directory.
	<inputPath> The filepath of the PNG image to be converted
	<outputPath> The filepath of the directory to output the new file to
	<return> The file object for the new field file
	"""
	width, height, fullPixelArray = LoadPNG(inputPath)
	for i in range(height):
		fullPixelArray[i] = list(fullPixelArray[i])
	# Cut out all the movement pixels so that we can process just the tiles
	tilePixelArray = copy.deepcopy(fullPixelArray)
	tilePixelArray = DownsizePixelArray(tilePixelArray)
	tileArray = GenerateArrayFromPicture(tilePixelArray)
	movementArray = GenerateMovementPixelArray(fullPixelArray)
	return CreateMapFromTileAndBitflags(tileArray,movementArray,inputPath,outputPath)

def ConvertFieldToImage(inputPath, outputPath):
	"""
	Converts a FLD file to a PNG image, and outputs it to the specified directory.
	<inputPath> The filepath of the FLD file to be converted
	<outputPath> The filepath of the directory to output the new file to
	<return> The filename for the new image file
	"""
	# Here we load the FLD file, create an array from it, convert the tile IDs into appropriate pixels, and save an image of it
	size, fileSize = LoadBaseFile(inputPath)
	FieldArray = CreateFieldArray(inputPath, size)

	#DEBUGPrintMapLessPadding(FieldArray)
	pixelVer = TurnArrayIntoPixelsWithPath(FieldArray)

	#pixelVer = TurnArrayIntoPixels(FieldArray)
	return CreateImageFromPixels(pixelVer, fileSize, size, inputPath, outputPath)

def AutoPadMap(cMap, necessarySize):
	"""
	Make a new temporary file that contains a padded version of cMap.
	cMap: The filepath of the custom map to be padded
	necessarySize: The bytesize to pad it to
	return: A (closed) file object referencing a temp file of the padded map
	"""
	# If a map is originally a smaller size than the size it's being imported as, we need to pad to make sure the width of the map matches the width of the slot it's going into
	mapSize = os.stat(cMap).st_size
	# fileSize: width in bytes
	global fieldSizeTable
	# We need to increase the width of the map to match the new size, so every row should gain (nWidth - oWidth) bytes, where one tile is 8 bytes
	widthIncrement = fieldSizeTable[necessarySize] - fieldSizeTable[mapSize]
	mapWidth = fieldSizeTable[mapSize]/8
	fieldData = [] # Format: [[Tile, Flags, Tile, Flags, Tile, Flags...], [Tile, Flags, Tile, Flags...]]
	for i in xrange(mapWidth):
		fieldData.append([])

	# Create an array containing the map data
	with open(cMap, "rb") as file:
		value = file.read(4) # Read four bytes at a time, since OJ maps are stored as a series of four-byte ints
		widthCounter = 0
		col = 0
		while value != "":
			fieldData[col].append(struct.unpack("i", value)[0])
			widthCounter += 1
			if widthCounter >= mapWidth*2: #2x map width because we're putting flags in with tile IDs
				# We pad out the extra columns here, adding two 0s (one for the tile, one for its flags) for every tile we need to increase the width by
				for i in xrange(widthIncrement/8):
					fieldData[col].append(0)
					fieldData[col].append(0)
				# Move onto the next row
				widthCounter = 0
				col += 1
			value = file.read(4)

	# Create a new temporary file (not using with, because we'll need information from it after closing it)
	tempMapFile = tempfile.NamedTemporaryFile(delete=False,dir=os.path.dirname(os.path.abspath(sys.argv[0])))

	# Save our array into the file
	bytesWritten = 0 # Keep track of this so we can add extra rows later
	for row in fieldData:
		for i in row:
			tempMapFile.write(struct.pack("i", i))
			bytesWritten += 4
	# To ensure the map isn't missing rows (which hypothetically should not matter, but just in case), we add tiles until the file is the right size:
	while bytesWritten < necessarySize:
		tempMapFile.write(buffer("\x00\x00\x00\x00\x00\x00\x00\x00"))
		bytesWritten += 8

	tempMapFile.close()
	return tempMapFile

def CreateFieldArray(path,size):
	"""
	Create an array containing the field data
	"""
	fieldArray = []
	baseField = open(path, "rb")

	try:
		bytes = baseField.read(2)
		while bytes != "":
			fieldArray.append(struct.unpack("h", bytes)[0])
			bytes = baseField.read(2)
	finally:
		baseField.close()	

	prettyFieldArray = {0: []}

	count = 0
	pFARow = 0
	for i in fieldArray:
		if count%2 == 0:
			#print hex(i)[2:],
			prettyFieldArray[pFARow].append(hex(i)[2:])

		count += 1

		if count == size/2:
			#print "\n"
			count = 0
			pFARow += 1
			prettyFieldArray[pFARow] = []

	return prettyFieldArray

def TurnArrayIntoPixelsWithPath(array):
	"""
	Turn a field data array (ie, from CreateFieldArray()) into an array containing a PNG image of the field
	"""
	tileStringConversionTable = {
		0: "A",
		1: "B",
		2: "C",
		3: "D",
		4: "E",
		5: "F",
		6: "G",
		7: "H",
		8: "I",
		9: "J",
		10: "K",
		11: "L",
		12: "M",
		13: "N",
		14: "O",
		15: "P",
		16: "Q",
		17: "R",
		18: "S",
		19: "T",
		20: "U",
		21: "V",
		22: "W",
		23: "X",
		24: "Y",
		25: "Z",
		26: "a",
		27: "b", # New in Playground update
		28: "c", # New in Playground update
		29: "d", # New in Playground update
		30: "e", # New in ??? update
		31: "f" # New in 5th Anniversary update
	}
	palette = {
		"A": (0x00,0x00,0x00), # Void +
		"B": (0x7f,0x7f,0x7f), # Blank +
		"C": (0xff,0x7f,0x27), # Home +
		"D": (0xed,0x1c,0x24), # Battle
		"E": (0x22,0xb1,0x4c), # Draw
		"F": (0xff,0xc9,0x0e), # Bonus
		"G": (0x3f,0x48,0xcc), # Drop
		"H": (0xa3,0x49,0xa4), # Warp
		"I": (0x0b,0x62,0x0f), # Draw x2
		"J": (0xae,0x87,0x00), # Bonus x2
		"K": (0x1c,0x21,0x66), # Drop x2
		"L": (0x2b,0x2b,0x2b), # Flat Wall
		"M": (0xf0,0xf0,0xf0), # Void
		"N": (0xf0,0xf0,0xf0), # Void
		"O": (0xf0,0xf0,0xf0), # Void
		"P": (0xf0,0xf0,0xf0), # Void
		"Q": (0xf0,0xf0,0xf0), # Void
		"R": (0xf0,0xf0,0xf0), # Void
		"S": (0x98,0x47,0x0c), # Deck +
		"T": (0xf0,0xf0,0xf0), # Void
		"U": (0x88,0x00,0x15), # Battle x2
		"V": (0x00,0xa2,0xe8), # Move
		"W": (0x00,0x83,0xbb), # Move x2
		"X": (0xe2,0x38,0x9a), # Warp Move
		"Y": (0xa2,0x17,0x67), # Warp Move x2
		"Z": (0x99,0xd9,0xea), # Ice
		"a": (0x47,0x7a,0x7c), # Snow -- Tiles below added in Playground update
		"b": (0x72,0xff,0x00), # Heal
		"c": (0x00,0xc4,0x00), # Heal x2
		"d": (0xff,0xb5,0x84), # Event (Blank Tile)
		"e": (0xbe,0xff,0xe9), # ??? -- Tiles below added in 5th Anniversary update
		"f": (0xb7,0x00,0x46) # Co-op Boss +
	}

	pixelToTileArray = [] # One array value = one pixel; tile or movement flag encoded
	pixelList = [[]] # Three array values = one pixel; R/G/B

	# First, we convert an array if tile and movement flags to a 1:1 pixel:value array
	# That is, every pixel in our resulting image will be represented by one value in the array
	# If the value is an integer, it represents a movement flag, and if it is a string, it represents a tile colour pixel

	# In order to create the 1:1 array, we first fill an array with 3x3 blocks of pixels for each tile...
	rowCount = 0
	colCount = 0
	for row in array:
		tempList = []
		for i in array[row]:
			if colCount == 0:
				# Tile value
				# I didn't think these were stored as hex, so if this fucks up check here first lol
				tempList.append(tileStringConversionTable[int(i, 16)])
				tempList.append(tileStringConversionTable[int(i, 16)])
				tempList.append(tileStringConversionTable[int(i, 16)])
				colCount = 1
			else:
				# Movement flag
				# Pass for now; we'll edit these in on a second go
				colCount = 0
		pixelToTileArray.append(tempList)
		pixelToTileArray.append(copy.copy(tempList))
		pixelToTileArray.append(copy.copy(tempList))
		rowCount += 3

	pixelToTileArray.pop()
	pixelToTileArray.pop()
	pixelToTileArray.pop()

	# ...then we go back and edit in movement flags where appropriate.
	rowCount = 0
	colCount = 0
	for row in array:
		for i in array[row]:
			if colCount % 2 == 0:
				# Tile value
				# We already handled this!
				colCount += 1
			else:
				# Movement flag
				# First, we generate a tuple denoting which pixels will be what colour
				movementPixels = ["0","0","0","0"] # 0-4 represent north, west, east, then south; this is equivalent to the order we use them in
				j = int(i, 16)
				if j & 1 != 0:
					# Exit west
					movementPixels[1] = "W" # W for white; the pixel might be changed to magenta later in this process
				if j & 2 != 0:
					# Exit north
					movementPixels[0] = "W"
				if j & 4 != 0:
					# Exit east
					movementPixels[2] = "W"
				if j & 8 != 0:
					# Exit south
					movementPixels[3] = "W"
				if j & 16 != 0:
					# Enter west
					if movementPixels[1] == "W":
						movementPixels[1] = "M" # M for magenta
					else:
						movementPixels[1] = "B" # B for black
				if j & 32 != 0:
					# Enter north
					if movementPixels[0] == "W":
						movementPixels[0] = "M"
					else:
						movementPixels[0] = "B"
				if j & 64 != 0:
					# Enter east
					if movementPixels[2] == "W":
						movementPixels[2] = "M"
					else:
						movementPixels[2] = "B"
				if j & 128 != 0:
					# Enter south
					if movementPixels[3] == "W":
						movementPixels[3] = "M"
					else:
						movementPixels[3] = "B"

				# Next, we change the relevant pixels on the pixelToTileArray to represent their movement flag values
				# colCount*3, rowCount*3 = up-left most pixel of tile; add 1 or 2 to either to get other pixels
				halvedColCount = colCount/2 # Because only every other value in the original array is a tile, we halve the column count to use it as an index for the new array
				#print halvedColCount, rowCount, movementPixels, j
				if movementPixels[0] == "W":
					pixelToTileArray[rowCount*3][1+halvedColCount*3] = 1
				elif movementPixels[0] == "B":
					pixelToTileArray[rowCount*3][1+halvedColCount*3] = 2
				elif movementPixels[0] == "M":
					pixelToTileArray[rowCount*3][1+halvedColCount*3] = 3
				#DEBUGPrintPixelToTileArray(pixelToTileArray)
				
				if movementPixels[1] == "W":
					pixelToTileArray[1+rowCount*3][halvedColCount*3] = 1
				elif movementPixels[1] == "B":
					pixelToTileArray[1+rowCount*3][halvedColCount*3] = 2
				elif movementPixels[1] == "M":
					pixelToTileArray[1+rowCount*3][halvedColCount*3] = 3
				#DEBUGPrintPixelToTileArray(pixelToTileArray)

				if movementPixels[2] == "W":
					pixelToTileArray[1+rowCount*3][2+halvedColCount*3] = 1
				elif movementPixels[2] == "B":
					pixelToTileArray[1+rowCount*3][2+halvedColCount*3] = 2
				elif movementPixels[2] == "M":
					pixelToTileArray[1+rowCount*3][2+halvedColCount*3] = 3
				#DEBUGPrintPixelToTileArray(pixelToTileArray)

				if movementPixels[3] == "W":
					pixelToTileArray[2+rowCount*3][1+halvedColCount*3] = 1
				elif movementPixels[3] == "B":
					pixelToTileArray[2+rowCount*3][1+halvedColCount*3] = 2
				elif movementPixels[3] == "M":
					pixelToTileArray[2+rowCount*3][1+halvedColCount*3] = 3
				#DEBUGPrintPixelToTileArray(pixelToTileArray)
				colCount += 1
		colCount = 0
		rowCount += 1

	#DEBUGPrintPixelToTileArray(pixelToTileArray)

	# Finally, we convert the intermediate array to a PNG image
	imageArray = []
	for row in pixelToTileArray:
		imageArray.append([])
		for pixel in row:
			if type(pixel) is str:
				# Add pixel data from palette
				imageArray[-1].append(palette[pixel][0])
				imageArray[-1].append(palette[pixel][1])
				imageArray[-1].append(palette[pixel][2])
			elif type(pixel) is int:
				# Add pixel data manually for movement flag
				if pixel == 1:
					imageArray[-1].append(0xff)
					imageArray[-1].append(0xff)
					imageArray[-1].append(0xff)
				elif pixel == 2:
					imageArray[-1].append(0x40)
					imageArray[-1].append(0x40)
					imageArray[-1].append(0x40)
				elif pixel == 3:
					imageArray[-1].append(0xfe)
					imageArray[-1].append(0x00)
					imageArray[-1].append(0x6e)
			else:
				# Add 0, 0, 0
				imageArray[-1].append(0x00)
				imageArray[-1].append(0x00)
				imageArray[-1].append(0x00)
	return imageArray

def DEBUGPrintPixelToTileArray(array):
	for i in array:
		for j in i:
			if j == "A":
				print ".",
			else:
				print j,
		print ""

def TurnArrayIntoPixels(array):
	"""	Deprecated -- produces PNGs without movement paths.
		Use TurnArrayIntoPixelsWithPath() instead"""
	palette = {
		0: (0x00,0x00,0x00),
		1: (0x7f,0x7f,0x7f),
		2: (0xff,0x7f,0x27),
		3: (0xed,0x1c,0x24),
		4: (0x22,0xb1,0x4c),
		5: (0xff,0xc9,0x0e),
		6: (0x3f,0x48,0xcc),
		7: (0xa3,0x49,0xa4),
		8: (0x0b,0x62,0x0f),
		9: (0xae,0x87,0x00),
		10: (0x1c,0x21,0x66),
		11: (0x2b,0x2b,0x2b),
		12: (0xf0,0xf0,0xf0),
		13: (0xf0,0xf0,0xf0),
		14: (0xf0,0xf0,0xf0),
		15: (0xf0,0xf0,0xf0),
		16: (0xf0,0xf0,0xf0),
		17: (0xf0,0xf0,0xf0),
		18: (0x98,0x47,0x0c),
		19: (0xf0,0xf0,0xf0),
		20: (0x88,0x00,0x15),
		21: (0x00,0xa2,0xe8),
		22: (0x00,0x83,0xbb),
		23: (0xe2,0x38,0x9a),
		24: (0xa2,0x17,0x67),
		25: (0x99,0xd9,0xea),
		26: (0x47,0x7a,0x7c),
		27: (0x72,0xff,0x00),
		28: (0x00,0xc4,0x00),
		29: (0xff,0xb5,0x84),
		30: (0xbe,0xff,0xe9),
		31: (0xb7,0x00,0x46)
	}

	pixelList = [[]]

	rowCount = 0
	colCount = 0
	for row in array:
		for i in array[row]:
			if colCount == 0:
				pixel = palette[int(i, 16)]
				pixelList[rowCount].append(pixel[0])
				pixelList[rowCount].append(pixel[1])
				pixelList[rowCount].append(pixel[2])
				colCount = 1
			else:
				colCount = 0
		pixelList.append([])
		rowCount += 1

	pixelList.pop()
	pixelList.pop()

	return pixelList

def CreateImageFromPixels(pixelList, fileSize, size, path, outputPath):
	"""Given pixels, the file size of the field, the path of the field file, the output path, create a png of the field and return its path"""
	m = re.search("([^/]+)/?$", path)
	newName = m.group(0)[0:-4] + ".png"

	if outputPath[-1] == "/":
		newPath = outputPath + newName
	else:
		newPath = outputPath + "/" + newName

	outputImage = open(newPath, "wb")
	height = fileSize/size
	width = size/8

	writer = png.Writer(width*3, height*3)
	writer.write(outputImage, pixelList)
	outputImage.close()

	return os.path.realpath(outputImage.name)

def GenerateArrayFromPicture(pixels):
	"""
	Creates a tile array from a PNG pixel array
	"""
	tileArray = []
	for i in pixels:
		numberOfPixels = len(i)/3
		for j in range(0,numberOfPixels):
			nextPixel = (i.pop(0), i.pop(0), i.pop(0))
			pixelID = CheckIfPixelInPalette(nextPixel)
			tileArray.append(pixelID)

	return tileArray


def CheckIfPixelInPalette(pixel):
	"""
	Checks if the given pixel index is in the palette for OJ Edit images
	"""
	palette = {
		0: (0x00,0x00,0x00),
		1: (0x7f,0x7f,0x7f),
		2: (0xff,0x7f,0x27),
		3: (0xed,0x1c,0x24),
		4: (0x22,0xb1,0x4c),
		5: (0xff,0xc9,0x0e),
		6: (0x3f,0x48,0xcc),
		7: (0xa3,0x49,0xa4),
		8: (0x0b,0x62,0x0f),
		9: (0xae,0x87,0x00),
		10: (0x1c,0x21,0x66),
		11: (0x2b,0x2b,0x2b),
		12: (0xf0,0xf0,0xf0),
		13: (0xf0,0xf0,0xf0),
		14: (0xf0,0xf0,0xf0),
		15: (0xf0,0xf0,0xf0),
		16: (0xf0,0xf0,0xf0),
		17: (0xf0,0xf0,0xf0),
		18: (0x98,0x47,0x0c),
		19: (0xf0,0xf0,0xf0),
		20: (0x88,0x00,0x15),
		21: (0x00,0xa2,0xe8),
		22: (0x00,0x83,0xbb),
		23: (0xe2,0x38,0x9a),
		24: (0xa2,0x17,0x67),
		25: (0x99,0xd9,0xea),
		26: (0x47,0x7a,0x7c),
		27: (0x72,0xff,0x00),
		28: (0x00,0xc4,0x00),
		29: (0xff,0xb5,0x84),
		30: (0xbe,0xff,0xe9),
		31: (0xb7,0x00,0x46)
	}

	for i in palette:
		if pixel[0] == palette[i][0]:
			if pixel[1] == palette[i][1]:
				if pixel[2] == palette[i][2]:
					return i
	return 99

def DownsizePixelArray(pixelArray):
	"""
	Downsizes the pixel array, saving every third pixel
	This effectively removes movement data, leaving only tile data
	"""
	downsizedPixelArray = []
	# Iterate over each row of pixels
	rowCount = 0
	for row in pixelArray:
		downsizedPixelArray.append([])
		colCount = 0
		for j in row:
			if colCount <3: #<3
				# If this is the first pixel, take all three RGB channels and insert them into the downsized array
				downsizedPixelArray[rowCount].append(j)
				colCount += 1
			elif colCount <8:
				# If this isn't the first pixel, ignore it
				colCount += 1
			else:
				# If this is the 9th byte, loop the counter and ignore it
				colCount = 0
		colCount = 0
		rowCount += 1

	# Only every third row is relevant to us, so we'll make a new list that only has the rows we want
	downsizedArrayFixed = []
	for i in range(len(downsizedPixelArray)):
		if (i+1)%3 == 1:
			downsizedArrayFixed.append(copy.deepcopy(downsizedPixelArray[i]))

	return downsizedArrayFixed

def GenerateMovementPixelArray(pixelArray):
	"""
	We need to check the colour of each pixel. If it's #404040 (64 64 64) it's an entrance;
	if it's pure white (255 255 255) it's an exit. For any pixel,
	we immediately disregard it.
	"""
	movementArray = []
	count = 0
	for i in pixelArray:
		movementArray.append([])
		for j in xrange(0,len(i),3):
			if i[j] == 255: # Check if the R value is 255
				if i[j+1] == 255: # Check G
					if i[j+2] == 255: # Check B
						movementArray[count].append(255)
					else:
						movementArray[count].append(0)
				else:
					movementArray[count].append(0)
			elif i[j] == 64: # Check if the R value is 64
				if i[j+1] == 64: # Check G
					if i[j+2] == 64: # Check B
						movementArray[count].append(64)
					else:
						movementArray[count].append(0)
				else:
					movementArray[count].append(0)
			elif i[j] == 254 or i[j] == 253: # Check for FE006E, for a double direction flag
				if i[j+1] == 0:
					if i[j+2] == 110:
						movementArray[count].append(110)
					else:
						movementArray[count].append(0)
				else:
					movementArray[count].append(0)
			else: # Not a movement tile!
				movementArray[count].append(0)
		count += 1

	#DEBUGPrintTilePixelArray(movementArray)

	# Now we want to turn the pixel array into an array of bitflags
	bitflagArray = []
	# TODO: Combine this code with the above to make it more efficient
	for rowIdx in xrange(0,len(movementArray)):
		# Set up movementArray to be clearer for later
		for pxIdx in xrange(0,len(movementArray[rowIdx])):
			if movementArray[rowIdx][pxIdx] == 64:
				movementArray[rowIdx][pxIdx] = "N"
			elif movementArray[rowIdx][pxIdx] == 255:
				movementArray[rowIdx][pxIdx] = "X"
			elif movementArray[rowIdx][pxIdx] == 110:
				movementArray[rowIdx][pxIdx] = "B"
			else:
				movementArray[rowIdx][pxIdx] = "0"
		tileLength = len(movementArray[0])/3
		colCount = 0
		bitflagArray.append([])
		for i in xrange(0,tileLength):
			bitflagArray[rowIdx].append([])

		# Depending on which row we're in, we care about different pixels
		if rowIdx % 3 == 0: # We care about every other pixel starting at 1
			for pxIdx in xrange(1,tileLength*3,3): # If we're on an odd row, we only care about the second pixel of every tile (every third pixel, starting at 1)
				flag = movementArray[rowIdx][pxIdx]
				# Append the flag to the current tile's (row one) flag list 
				bitflagArray[rowIdx][colCount].append(flag)
				colCount += 1
		elif rowIdx % 3 == 1: # If we're on an even row, we care about the first and third pixel of every tile (every other, starting at 0)
			pxIdxList = range(0,tileLength*3)
			del pxIdxList[1::3]
			for pxIdx in pxIdxList:
				flag = movementArray[rowIdx][pxIdx]
				# We append both left and right flags to the same tile's list here. Later, we'll combine the three lists for each tile into one
				if pxIdx % 3 == 0:
					bitflagArray[rowIdx][int(math.floor(colCount/2))].append(flag)
				elif pxIdx % 3 == 2:
					bitflagArray[rowIdx][int(math.floor(colCount/2))].append(flag)
				colCount += 1

		else: 
			for pxIdx in xrange(1,tileLength*3,3):
				flag = movementArray[rowIdx][pxIdx]

				bitflagArray[rowIdx][colCount].append(flag)
				colCount += 1

	#for i in bitflagArray:
	#	print i

	# Next, we need to condense our rows, as currently we have the information for each tile split across three rows
	condensedBitflagArray = []
	for rowIdx in xrange(0,len(bitflagArray),3):
		condensedBitflagArray.append([])
		for tileIdx in xrange(0,len(bitflagArray[rowIdx])):
			condensedTile = [bitflagArray[rowIdx][tileIdx][0], 
			bitflagArray[rowIdx+1][tileIdx][0], 
			bitflagArray[rowIdx+1][tileIdx][1], 
			bitflagArray[rowIdx+2][tileIdx][0]]
			condensedBitflagArray[rowIdx/3].append(condensedTile)

	# Finally, for each tile, we compile the movement info into a single bitflag
	finalBitflagArray = []
	for rowIdx in xrange(0,len(condensedBitflagArray)):
		finalBitflagArray.append([])
		for tileIdx in xrange(0,len(condensedBitflagArray[rowIdx])):
			bitflag = 0
			tileData = condensedBitflagArray[rowIdx][tileIdx]
			if tileData[0] == "X":
				bitflag += 2
			elif tileData[0] == "N":
				bitflag += 32
			elif tileData[0] == "B":
				bitflag += 34

			if tileData[1] == "X":
				bitflag += 1
			elif tileData[1] == "N":
				bitflag += 16
			elif tileData[1] == "B":
				bitflag += 17

			if tileData[2] == "X":
				bitflag += 4
			elif tileData[2] == "N":
				bitflag += 64
			elif tileData[2] == "B":
				bitflag += 68

			if tileData[3] == "X":
				bitflag += 8
			elif tileData[3] == "N":
				bitflag += 128
			elif tileData[3] == "B":
				bitflag += 136

			finalBitflagArray[rowIdx].append(bitflag)

	return finalBitflagArray

def CreateMapFromTileAndBitflags(tileArray,bitflagArray,path,outputDir):
	"""
	Creates a map file from a tile array and movement information array
	"""
	m = re.search("([^/]+)/?$", path)
	newPath = m.group(0)[0:-4] + ".fld"

	if outputDir[-1] == "/":
		outputPath = outputDir + newPath
	else:
		outputPath = outputDir + "/" + newPath

	outputFile = open(outputPath, "wb")
	oneDBitflagTable = []
	for i in xrange(0,len(bitflagArray)):
		for j in xrange(0,len(bitflagArray[i])):
			oneDBitflagTable.append(bitflagArray[i][j])

	#print len(tileArray),len(oneDBitflagTable)
	for i in xrange(len(tileArray)):
		outputFile.write(struct.pack("h",tileArray[i]))
		outputFile.write(buffer("\x00\x00"))
		outputFile.write(struct.pack("h",oneDBitflagTable[i]))
		outputFile.write(buffer("\x00\x00"))

	outputFile.close()
	return outputFile