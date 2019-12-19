def XORImage(data):
	# This is the key used to XOR all graphics files for OJ. Note that, in ASCII, this would be:
	# a8Yb5$IpVobR,1Xph!k(#!B9h$V[o[r-I'x.37Q%E;lt2wGgk)hNF_p_!mF?Ds54.*8ErbCK,30
	# If ever modifying this code to use the key as a string, beware of the %E in the middle of it; this will be need to be escaped as %%E in Python
	key = bytearray(
		[0x61,0x38,0x59,0x62,0x35,0x24,0x49,0x70,0x56,0x6f,0x62,0x52,0x2c,0x31,0x58,0x70,
		0x68,0x21,0x6b,0x28,0x23,0x21,0x42,0x39,0x68,0x24,0x56,0x5b,0x6f,0x5b,0x72,0x2d,
		0x49,0x27,0x78,0x2e,0x33,0x37,0x51,0x25,0x45,0x3b,0x6c,0x74,0x32,0x77,0x47,0x67,
		0x6b,0x29,0x68,0x4e,0x46,0x5f,0x70,0x5f,0x21,0x6d,0x46,0x3f,0x44,0x73,0x35,0x34,
		0x2e,0x2a,0x38,0x45,0x72,0x62,0x43,0x4b,0x2c,0x33,0x30])
	# Please make key shorter next time, OJ devs ;_;

	try:
		# data is a path
		encryptedImage = bytearray(open(data, "rb").read())
		decryptedHex = Xor(encryptedImage,key)
	except:
		# data is raw data
		encryptedImage = bytearray(data)
		decryptedHex = Xor(encryptedImage,key)

	return decryptedHex

def XORTextureFile(path, outDir):
	with open(path, "rb") as texture:
		data = texture.read()

	magicNumbers = {
		"44445320": "DDS",
		"89504e47": "PNG",
		"257c0a42": "DDS-DAT",
		"e8681725": "PNG-DAT"
	}
	if data[:4].encode("hex") in magicNumbers:
		inFormat = magicNumbers[data[:4].encode("hex")]
		if inFormat == "DDS" or inFormat == "PNG":
			outFormat = ".dat"
		elif inFormat == "DDS-DAT":
			outFormat = ".dds"
		elif inFormat == "PNG-DAT":
			outFormat = ".png"
		else:
			outFormat = ".dat" # Should be redundant, but can't hurt
	else:
		outFormat = ".dat"

	m = re.search("([^/]+)/?$", path)
	outPath = outDir + ("" if outDir[-1] == "/" else "/") + m.group(0)[0:-4] + outFormat

	with open(outPath, "wb") as output:
		print outPath
		output.write(XORImage(data))

def ConvertTextureFile(path,outFormat):
	with open(path, "rb") as texture:
		data = texture.read()
		filename = texture.name

	# Check magic numbers of provided file in order to determine conversion direction
	magicNumbers = {
		"44445320": "DDS",
		"89504e47": "PNG",
		"257c0a42": "DDS-DAT",
		"e8681725": "PNG-DAT"
	}
	if data[:4].encode("hex") in magicNumbers:
		inFormat = magicNumbers[data[:4].encode("hex")]
	else:
		# Not a supported filetype
		return (data, filename)

	m = re.search("([^/]+)/?$", path)
	outputFilename = m.group(0)[0:-4] + "." + outFormat[-3:].lower()

	# Convert to the proper format and return
	if inFormat == outFormat:
		##### PNG -> PNG
		##### DDS -> DDS
		##### DAT -> DAT
		##### ODAT -> ODAT
		# File is already in the correct format
		return (data, outputFilename)
	elif inFormat[0:3] == outFormat[0:3]:
		##### PNG -> ODAT
		##### ODAT -> PNG
		##### DDS -> DAT
		##### DAT -> DDS
		# File is in the correct encoding and merely needs to be XOR'd
		return (XORImage(path), outputFilename)
	# File is not in the correct encoding; decrypt if necessary and then convert
	elif inFormat[-3:] == "DAT":
		##### DAT -> PNG X
		##### DAT -> ODAT
		##### ODAT -> DDS
		##### ODAT -> DAT
		data = XORImage(path)
		tempConvertedFile = tempfile.NamedTemporaryFile(delete=False,dir=os.path.dirname(os.path.abspath(sys.argv[0])))
		tempConvertedFile.write(data)
		tempConvertedFile.close()
		newPath = tempConvertedFile.name
	else:
		##### PNG -> DAT
		##### PNG -> DDS
		##### DDS -> PNG
		##### DDS -> ODAT
		newPath = None

	# Convert data to the opposite format
	if inFormat[0:3] == "PNG":
		##### PNG -> DAT
		##### PNG -> DDS
		##### ODAT -> DDS
		##### ODAT -> DAT
		# If we had to convert from DAT, open the temporary file where the converted data is. Otherwise, open the original.
		if newPath != None:
			pngFile = open(newPath, "rb")
		else:
			pngFile = open(path, "rb")
		# Use PyPNG to read the data and dimensions of the file to be converted
		r = png.Reader(file=pngFile)
		pngData = r.asRGBA()
		# Because PyPNG throws a mysterious error with the PNG-DAT format (thinking the number of pixels is wrong when it isn't), we write our own iterator
		pngPixels = []
		height = pngData[1]
		width = pngData[0]
		try:
			for channel in pngData[2]:
				pngPixels.append(channel)
		except:
			pass
		d = DDSLoader(pngPixels, height, width)
		# Save as a DDS file, temporarily, then load its contents into data
		tempOutputFile = tempfile.NamedTemporaryFile(delete=False,dir=os.path.dirname(os.path.abspath(sys.argv[0])))
		d.save(tempOutputFile.name)
		data = tempOutputFile.read()
		# Close all files and unlink any temporary files we've created
		tempOutputFile.close()
		os.unlink(tempOutputFile.name)
		pngFile.close()
		if newPath != None:
			os.unlink(tempConvertedFile.name)
	elif inFormat[0:3] == "DDS":
		##### DDS -> PNG
		##### DDS -> ODAT
		##### DAT -> PNG
		##### DAT -> ODAT
		if newPath != None:
			d = DDSLoader(newPath)
		else:
			d = DDSLoader(path)
		# Save as a PNG file, temporarily, then load its contents into data
		tempOutputFile = tempfile.NamedTemporaryFile(delete=False,dir=os.path.dirname(os.path.abspath(sys.argv[0])))
		png.from_array(d.getData(), mode="RGBA").save(tempOutputFile.name)
		data = tempOutputFile.read()
		tempOutputFile.close()
		os.unlink(tempOutputFile.name)
		if newPath != None:
			os.unlink(tempConvertedFile.name)

	if outFormat[-3:] == "DAT":
		data = XORImage(data)

	return (data, outputFilename)

def GetTextureInfo(path):
	try:
		with open(path, "rb") as texture:
			data = texture.read(4).encode("hex")
			magicNumbers = {
				"44445320": "DDS",
				"89504e47": "PNG",
				"257c0a42": "DDS-DAT",
				"e8681725": "PNG-DAT"
			}
			try:
				inFormat = magicNumbers[data]
			except:
				raise BadTextureFiletypeError()

		# Get height, width, and load the image as a PIL image
		if inFormat[:3] == "PNG":
			if inFormat == "PNG-DAT":
				# Encrypted; XOR first
				with open(path, "rb") as texture:
					data = texture.read()
				data = XORImage(data)
				temp = tempfile.NamedTemporaryFile(dir=os.path.dirname(os.path.abspath(sys.argv[0])))
				temp.write(data)
				image = ImageTk.PhotoImage(Image.open(temp))
				temp.close()
			else:
				# Not encrypted; simply load file
				image = ImageTk.PhotoImage(Image.open(path))
			# Get info
			height = image.height()
			width = image.width()
		elif inFormat[:3] == "DDS":
			if inFormat == "DDS-DAT":
				# Encrypted; XOR first
				with open(path, "rb") as texture:
					data = texture.read()
				data = XORImage(data)
				temp = tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(os.path.abspath(sys.argv[0])))
				temp.write(data)
				temp.close()
				d = DDSLoader(temp.name)
				os.unlink(temp.name)
			else:
				# Not encrypted, simply make DDS object
				d = DDSLoader(path)
			# Save a PNG temporarily and use it to load an Image object
			temp = tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(os.path.abspath(sys.argv[0])))
			temp.close()
			png.from_array(d.getData(), mode="RGBA").save(temp.name)
			image = ImageTk.PhotoImage(Image.open(temp.name))
			height = image.height()
			width = image.width()
			os.unlink(temp.name)

		byteSize = os.stat(path).st_size
		return image, path, byteSize, height, width
	except BadTextureFiletypeError as e:
		global console
		console.insert(tk.END, "Bad filetype: " + path)
		return GetNoPreviewImage(), path, os.stat(path).st_size, "", ""