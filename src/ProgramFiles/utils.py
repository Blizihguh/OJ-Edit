from bisect import bisect_left
import Tkinter as tk

class PopupClosedError(Exception):
	"""The popup was closed early"""
	pass

class BadTextureFiletypeError(Exception):
	"""Invalid texture filetype"""
	pass

def GetNoPreviewImage():
	noPreviewIcons = {0: "alte-icon.png", 1: "kae-icon.png", 2: "kai-icon.png", 3: "krila-icon.png", 4: "saki-icon.png", 
	5: "seagull-icon.png", 6: "sham-icon.png", 7: "starbo-icon.png", 8: "tequila-icon.png"}
	iconPath = "ProgramFiles/" + noPreviewIcons[random.randint(0,len(noPreviewIcons) - 1)]
	return ImageTk.PhotoImage(Image.open(iconPath))

def TakeClosest(myList, myNumber):
	"""
	Assumes myList is sorted. Returns closest value to myNumber.
	If two numbers are equally close, return the smallest number.
	"""
	pos = bisect_left(myList, myNumber)
	if pos == 0:
		return myList[0]
	if pos == len(myList):
		return myList[-1]
	before = myList[pos - 1]
	after = myList[pos]
	if after - myNumber < myNumber - before:
	   return after
	else:
	   return before

def LoadPNG(path):
	r = png.Reader(filename=path)
	read = r.asRGB()
	pixelArray = list(read[2])
	width = read[0]
	height = read[1]

	return width, height, pixelArray

def ParseMultipleFilenames(paths):
	# On Windows Python 2.6-2.7, askopenfilenames returns a Unicode string instead of a tuple >:I
	#print paths
	if type(paths) != tuple:
		if type(paths) is unicode or type(paths) is str:
			if paths[0] == "{":
				# On 2.6-2.7.6, the string returned is formatted as "{filepath1}, {filepath2}"
				paths = root.tk.splitlist(paths)
			else:
				# On 2.7.13, apparently they broke it AGAIN and now it returns the result of calling str() on a tuple?????
				paths = literal_eval(paths)
		else:
			# As far as I know, this should never trigger, but tkinter's already fucked me twice on this.
			# Information is ordered from least to most likely to crash the program
			global console
			console.insert(tk.END, "Unknown variable type for paths!")
			console.insert(tk.END, "Please report this error and the following info to the script author :)")
			console.insert(tk.END, type(paths), type(type(paths)))
			console.insert(tk.END, platform.platform(), platform.system(), platform.python_version())
			console.insert(tk.END, platform.python_implementation(), platform.python_build())
	return paths

def Xor(data, key):
	l = len(key)
	return bytearray(((data[i] ^ key[i % l]) for i in range(0,len(data))))

def PrettyPrintMapDetails(mapName, slot, isOfficial, isPadded):
	global console
	mapTag = "fgGREEN" if isOfficial else "bgGREEN"
	slotTag = "bgRED" if isPadded else "fgRED"
	# Print map name
	startIdx = console.index(readText.index(console, tk.END) + "-1c")
	endIdx = console.index(readText.index(console, tk.END) + "-1l") + "+%ic" % len(mapName)
	console.insert(tk.END, mapName)
	console.tag_add(mapTag, startIdx, endIdx)
	# Etc
	console.insert(tk.END, " will be exported as ")
	# Print map slot
	startIdx = console.index(readText.index(console, tk.END) + "-1c")
	endIdx = console.index(readText.index(console, tk.END) + "-1c") + "+%ic" % len(slot)
	console.insert(tk.END, slot)
	console.tag_add(slotTag, startIdx, endIdx)
	console.insert(tk.END, "\n")
	console.see(tk.END)

def PrettyPrintConsoleError(outputErrorText):
	startIdx = readText.index(console, tk.INSERT)
	endIdx = startIdx + "+%ic" % len(outputErrorText)
	console.insert(tk.END, outputErrorText)
	console.tag_add("fgRED", startIdx, endIdx)

def DEBUGPrintTable(*args):
	"""
	Prints: arg_1\targ_2\t...\targ_n\n
	"""
	for i in args:
		print i, "\t",
	print ""

def DEBUGPrintTilePixelArray(tilePixelArray):
	for i in tilePixelArray:
		for num in i:
			if num == 0:
				print "  .",
			else:
				print "%3d" % num,
		print "\n",

def DEBUGPrintBitflagArray(bitflagArray):
	for row in bitflagArray:
		for px in row:
			if px == 0:
				print ".\t",
			else:
				print hex(px)[2::] + "\t",
		print ""

def DEBUGPrintTileArray(tileArray,width):
	tileWidth = width/3
	count = 0
	for i in tileArray:
		if i == 0:
			print " .\t",
		else:
			print "%2d\t" % i,
		count += 1
		if count >= tileWidth:
			print "\n",
			count = 0

def DEBUGPrintMapPadding(tileArray):
	for rowIdx in tileArray:
		for i in tileArray[rowIdx]:
			print i,"\t",
		print ""

def DEBUGPrintMapLessPadding(tileArray):
	for rowIdx in tileArray:
		for i in tileArray[rowIdx]:
			print i," ",
		print ""

def DEBUGPrintCustomMapTable(cmt):
	# Can't believe I'm writing for the Connecticut Mastery Test
	for key,value in sorted(cmt.iteritems()):
		print key,value

def DEBUGPrintPixelToTileArray(array):
	for i in array:
		for j in i:
			if j == "A":
				print ".",
			else:
				print j,
		print ""