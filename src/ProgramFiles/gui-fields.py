from ast import literal_eval
from idlelib.WidgetRedirector import WidgetRedirector
import Tkinter as tk
import traceback
import zipfile
import math
import copy
import struct
import platform
import sys
import os


###############################################################################################
### Main Functions                                                                          ###
###############################################################################################

def FLDtoPNG():
	"""
	GUI function to convert .fld files to .png files
	"""
	try:
		# First, we set up the popup, which prompts the user for the file to convert and output directory:
		# Set global variables for the popup
		global fldFileOpenPopup
		global fldString
		global outputDirFldPng
		fldString = tk.StringVar()
		outputDirFldPng = tk.StringVar()
		fldString.set("")
		outputDirFldPng.set("")
		# Set the popup geometry and screen location
		x = root.winfo_x()
		y = root.winfo_y() 
		w = root.winfo_width()
		h = root.winfo_height()
		popupWidth = 275
		popupHeight = 100
		fldFileOpenPopup = tk.Toplevel()
		fldFileOpenPopup.geometry("%dx%d+%d+%d" % (popupWidth, popupHeight, (x + w/2)-popupWidth/2, (y + h/2)-popupHeight/2))
		fldFileOpenPopup.transient(root)
		fldFileOpenPopup.iconbitmap("favicon.ico")
		fldFileOpenPopup.title("Open field files")
		# Set widgets
		tk.Label(fldFileOpenPopup, text="File(s): ").grid(row=1, column=0)
		tk.Entry(fldFileOpenPopup, textvariable=fldString).grid(row=1, column=1, columnspan=2)
		tk.Button(fldFileOpenPopup, text="Browse", command=lambda: fldString.set(tkfd.askopenfilenames(parent=fldFileOpenPopup))).grid(row=1, column=3)

		tk.Label(fldFileOpenPopup, text="Output Directory: ").grid(row=2, column=0)
		tk.Entry(fldFileOpenPopup, textvariable=outputDirFldPng).grid(row=2, column=1, columnspan=2)
		tk.Button(fldFileOpenPopup, text="Browse", command=lambda: outputDirFldPng.set(tkfd.askdirectory(parent=root))).grid(row=2, column=3)

		proceed = [False] # Python 2 won't let you do assignment in lambdas... unless you're assigning to a list :V

		tk.Button(fldFileOpenPopup, text="Okay", command=lambda: proceed.__setitem__(0,True)).grid(row=3, column=1)

		# Loop the fldFileOpenPopup dialogue while we wait for the Okay button to be pressed
		while True:
			if fldFileOpenPopup.winfo_exists() == False:
				raise PopupClosedError()
			elif proceed[0] == True:
				fldFileOpenPopup.destroy()
				break
			else:
				fldFileOpenPopup.update_idletasks()
				fldFileOpenPopup.update()

		filePaths = ParseMultipleFilenames(fldString.get())
		outputPath = outputDirFldPng.get()
		scrollbarPathList = []
		for path in filePaths:
			newMapName = ConvertFieldToImage(path, outputPath)
			pilImage = Image.open(newMapName)
			pilImage = pilImage.transform((pilImage.width*3,pilImage.height*3),Image.EXTENT,(0,0,pilImage.width,pilImage.height))
			newImage = ImageTk.PhotoImage(pilImage)
			scrollbarPathList.append((newImage, path, os.stat(path).st_size, pilImage.height/9, pilImage.width/9))

		scrollbar.setImageList(scrollbarPathList)

		# Next we print the relevant text for this map
		global console
		console.insert(tk.END, str(len(scrollbarPathList)) + " field(s) successfully converted to PNG!\n")
		console.see(tk.END)
	except PopupClosedError as e:
		pass
	except Exception as e:
		console.insert(tk.END, "\nUh oh! Looks like there was an error. The conversion to PNG has been stopped.\n")
		console.insert(tk.END, "If the conversion already finished, you may find your PNG has been saved successfully.\n")
		console.insert(tk.END, "Otherwise, make sure you selected a valid FLD file, and if the error persists, send the FLD you used and the following information to the program author:\n")
		console.insert(tk.END, traceback.format_exc())
		console.see(tk.END)	


def PNGtoFLD():
	"""
	GUI function to convert .png files to .fld files
	"""
	try:
		# First, we set up the popup, which prompts the user for the file to convert and output directory:
		# Set global variables for the popup
		global pngFileOpenPopup
		global pngString
		global outputDirPngFld
		pngString = tk.StringVar()
		outputDirPngFld = tk.StringVar()
		pngString.set("")
		outputDirPngFld.set("")
		# Set the popup geometry and screen location
		x = root.winfo_x()
		y = root.winfo_y() 
		w = root.winfo_width()
		h = root.winfo_height()
		popupWidth = 275
		popupHeight = 100
		pngFileOpenPopup = tk.Toplevel()
		pngFileOpenPopup.geometry("%dx%d+%d+%d" % (popupWidth, popupHeight, (x + w/2)-popupWidth/2, (y + h/2)-popupHeight/2))
		pngFileOpenPopup.transient(root)
		pngFileOpenPopup.iconbitmap("favicon.ico")
		pngFileOpenPopup.title("Open image files")
		# Set widgets
		tk.Label(pngFileOpenPopup, text="File(s): ").grid(row=1, column=0)
		tk.Entry(pngFileOpenPopup, textvariable=pngString).grid(row=1, column=1, columnspan=2)
		tk.Button(pngFileOpenPopup, text="Browse", command=lambda: pngString.set(tkfd.askopenfilenames(parent=pngFileOpenPopup))).grid(row=1, column=3)

		tk.Label(pngFileOpenPopup, text="Output Directory: ").grid(row=2, column=0)
		tk.Entry(pngFileOpenPopup, textvariable=outputDirPngFld).grid(row=2, column=1, columnspan=2)
		tk.Button(pngFileOpenPopup, text="Browse", command=lambda: outputDirPngFld.set(tkfd.askdirectory(parent=pngFileOpenPopup))).grid(row=2, column=3)

		proceed = [False] # Python 2 won't let you do assignment in lambdas... unless you're assigning to a list :V

		tk.Button(pngFileOpenPopup, text="Okay", command=lambda: proceed.__setitem__(0,True)).grid(row=3, column=1)

		# Loop the pngFileOpenPopup dialogue while we wait for the Okay button to be pressed
		while True:
			if pngFileOpenPopup.winfo_exists() == False:
				raise PopupClosedError()
			elif proceed[0] == True:
				pngFileOpenPopup.destroy()
				break
			else:
				pngFileOpenPopup.update_idletasks()
				pngFileOpenPopup.update()

		filePaths = ParseMultipleFilenames(pngString.get())
		outputPath = outputDirPngFld.get()
		scrollbarPathList = []
		for path in filePaths:
			newMap = ConvertImageToField(path, outputPath)
			pilImage = Image.open(path)
			pilImage = pilImage.transform((pilImage.width*3,pilImage.height*3),Image.EXTENT,(0,0,pilImage.width,pilImage.height))
			newImage = ImageTk.PhotoImage(pilImage)
			scrollbarPathList.append((newImage, path, os.stat(newMap.name).st_size, pilImage.height/9, pilImage.width/9))

		scrollbar.setImageList(scrollbarPathList)

		# Print the relevant text for this map
		global console
		console.insert(tk.END, str(len(scrollbarPathList)) + " field(s) successfully converted to FLD!\n")
		console.see(tk.END)
	except PopupClosedError as e:
		pass
	except Exception as e:
		console.insert(tk.END, "\nUh oh! Looks like there was an error. The conversion to FLD has been stopped.\n")
		console.insert(tk.END, "If the conversion already finished, you may find your FLD has been saved successfully.\n")
		console.insert(tk.END, "Otherwise, make sure you selected a valid PNG file with no alpha channels (save in MS Paint, or in Paint.NET as an 8-bit PNG).")
		console.insert(tk.END, "If the error persists, send the PNG you used and the following information to the program author:\n")
		console.insert(tk.END, traceback.format_exc())
		console.see(tk.END)


def FLDtoPAK():
	"""
	GUI function to automatically pack .fld files into a .pak file
	"""
	try:
		# First, we set up the popup, which prompts the user for the files to convert and output directory:
		# Set global variables for the popup
		global fldsFileOpenPopup
		global fldsString
		global coopFldsString
		global outputDirFldPak
		fldsString = tk.StringVar()
		coopFldsString = tk.StringVar()
		outputDirFldPak = tk.StringVar()
		fldsString.set("")
		coopFldsString.set("")
		outputDirFldPak.set("")
		# Set the popup geometry and screen location
		x = root.winfo_x()
		y = root.winfo_y() 
		w = root.winfo_width()
		h = root.winfo_height()
		popupWidth = 275
		popupHeight = 100
		fldsFileOpenPopup = tk.Toplevel()
		fldsFileOpenPopup.geometry("%dx%d+%d+%d" % (popupWidth, popupHeight, (x + w/2)-popupWidth/2, (y + h/2)-popupHeight/2))
		fldsFileOpenPopup.transient(root)
		fldsFileOpenPopup.iconbitmap("favicon.ico")
		fldsFileOpenPopup.title("Open field files")
		# Set widgets
		tk.Label(fldsFileOpenPopup, text="Normal Field(s): ").grid(row=1, column=0)
		tk.Entry(fldsFileOpenPopup, textvariable=fldsString).grid(row=1, column=1, columnspan=2)
		tk.Button(fldsFileOpenPopup, text="Browse", command=lambda: fldsString.set(tkfd.askopenfilenames(parent=fldsFileOpenPopup))).grid(row=1, column=3)

		tk.Label(fldsFileOpenPopup, text="Co-op Field(s): ").grid(row=2, column=0)
		tk.Entry(fldsFileOpenPopup, textvariable=coopFldsString).grid(row=2, column=1, columnspan=2)
		tk.Button(fldsFileOpenPopup, text="Browse", command=lambda: coopFldsString.set(tkfd.askopenfilenames(parent=fldsFileOpenPopup))).grid(row=2, column=3)

		tk.Label(fldsFileOpenPopup, text="Output Directory: ").grid(row=3, column=0)
		tk.Entry(fldsFileOpenPopup, textvariable=outputDirFldPak).grid(row=3, column=1, columnspan=2)
		tk.Button(fldsFileOpenPopup, text="Browse", command=lambda: outputDirFldPak.set(tkfd.askdirectory(parent=root))).grid(row=3, column=3)

		proceed = [False]

		tk.Button(fldsFileOpenPopup, text="Okay", command=lambda: proceed.__setitem__(0,True)).grid(row=4, column=1)

		# Loop the pngFileOpenPopup dialogue while we wait for the Okay button to be pressed
		while True:
			if fldsFileOpenPopup.winfo_exists() == False:
				raise PopupClosedError()
			elif proceed[0] == True:
				fldsFileOpenPopup.destroy()
				break
			else:
				fldsFileOpenPopup.update_idletasks()
				fldsFileOpenPopup.update()

		normalPaths = fldsString.get()
		coopPaths = coopFldsString.get()
		outputDir = outputDirFldPak.get()

		AssignSlots(normalPaths, coopPaths)
		paddedMaps = PadMaps(False)
		BuildPak(outputDir, paddedMaps)

		global scrollbar
		if outputDir[-1] == "/":
			outputPath = outputDir + "fields.pak"
		else:
			outputPath = outputDir + "/fields.pak"
		scrollbar.setNoPreview(outputPath, os.stat(outputPath).st_size)
	except PopupClosedError as e:
		pass
	except Exception as e:
		console.insert(tk.END, "\nUh oh! Looks like there was an error. The creation of a PAK has been stopped.\n")
		console.insert(tk.END, "If there exists one or several temporary files in the OJ Edit directory, you are safe to delete them.\n")
		console.insert(tk.END, "Your PAK will likely not work correctly, and may not have all the maps or all the background images in it.\n")
		console.insert(tk.END, "Make sure you selected one or several valid FLDs and nothing else, and also make sure you have an extracted copy of the official fields.pak file in a folder called OfficialFields in the same directory as your copy of OJ Edit.\n")
		console.insert(tk.END, "If the problem persists after verifying the above, please send the program author any maps you used to generate the PAK, and the PAK that was generated when this error was raised, as well as the following information:\n")
		console.insert(tk.END, traceback.format_exc())
		console.see(tk.END)

def CreateField(label, file, frame, row, col):
	"""
	Create a field, err... field for Specific FLD to PAK.
	<label> The name of the field to place on the label
	<file> The text variable for the file
	<frame> The frame to create the field in
	<row> The row to place the field in
	<col> The col to place the field in
	"""
	text = label + ": "
	tk.Label(frame, text=text, anchor="w").grid(row=row, column=col, sticky="w")
	tk.Entry(frame, textvariable=file).grid(row=row, column=col+1, columnspan=2)
	tk.Button(frame, text="Browse", command= lambda: AskOpenFile(file, frame)).grid(row=row, column=col+3)

def CreateFields(frame, bytesize, isCoop, row):
	"""
	Create all the fields necessary for a given section of the frame
	<frame> The frame to create fields for
	<bytesize> The size necessary for a field to be placed in the frame. If None, any fields not of size (968, 1352, 1800) will be placed
	<isCoop> Are we doing normal maps or co-op?
	<row> The row to start placing fields in
	"""
	# First, find all fields that we need and create a dictionary of only the relevant info
	global mapsTable
	fieldDict = {}
	for filename, fieldInfo in mapsTable.iteritems():
		if bytesize == None:
			if (fieldInfo[1] == isCoop) and (fieldInfo[0] not in (968, 1352, 1800)):
				fieldDict[fieldInfo[2]] = fieldInfo[3]
		elif fieldInfo[0] == bytesize and fieldInfo[1] == isCoop:
			fieldDict[fieldInfo[2]] = fieldInfo[3]
	# Now, iterate over the fieldDict and populate the frame
	fieldsPerRow = 3
	curRow = row
	curCol = 0
	for fieldName, fieldVar in iter(sorted(fieldDict.iteritems())):
		CreateField(fieldName, fieldVar, frame, curRow, curCol*4)
		curCol += 1
		if curCol >= fieldsPerRow:
			curRow += 1
			curCol = 0
	# Return the next empty row
	if curCol == 0:
		return curRow
	return curRow+1

def PadRows(frame, startRow, num):
	"""
	Pad for an arbitrary number of rows
	<frame> The frame to pad in
	<startRow> The row to start padding in
	<num> The number of rows to pad for
	"""
	for i in range(num):
		tk.Label(frame, text="").grid(row=startRow+i, column=0)

def SpecificFLDPAK():
	"""
	GUI function to non-automatically pack .fld files into a .pak file
	"""
	try:
		global root
		global specificPAKPopup

		# Set the popup geometry and screen location
		x = root.winfo_x()
		y = root.winfo_y() 
		w = root.winfo_width()
		h = root.winfo_height()
		popupWidth = 860
		popupHeight = 500
		specificPAKPopup = tk.Toplevel()
		specificPAKPopup.geometry("%dx%d+%d+%d" % (popupWidth, popupHeight, (x + w/2)-popupWidth/2, (y + h/2)-popupHeight/2))
		specificPAKPopup.transient(root)
		specificPAKPopup.iconbitmap("favicon.ico")
		specificPAKPopup.title("FLD to PAK (specific replacements)")

		# Navigation Frames
		navFrame = tk.Frame(specificPAKPopup)
		container = tk.Frame(specificPAKPopup)
		navFrame.pack(side="bottom", fill="x", expand=False)
		container.pack(side="top", fill="both", expand=True)

		################## 11x11s
		page1 = tk.Frame(specificPAKPopup)
		page1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		# Populate normal maps
		tk.Label(page1, text="Normal Maps:", anchor="w").grid(row=0, column=0, columnspan=2, sticky="w")
		nextRow = CreateFields(page1, 968, False, 1) # Create fields, return the next row to continue on
		# Pad for three rows
		PadRows(page1, nextRow, 2)
		nextRow += 2
		# Populate coop maps
		tk.Label(page1, text="Co-op Maps:", anchor="w").grid(row=nextRow, column=0, columnspan=2, sticky="w")
		CreateFields(page1, 968, True, nextRow+1)

		################## 13x13s
		page2 = tk.Frame(specificPAKPopup)
		page2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		# Populate normal maps
		tk.Label(page2, text="Normal Maps:", anchor="w").grid(row=0, column=0, columnspan=2, sticky="w")
		nextRow = CreateFields(page2, 1352, False, 1) # Create fields, return the next row to continue on
		# Pad for three rows
		PadRows(page2, nextRow, 4)
		nextRow += 4
		# Populate coop maps
		tk.Label(page2, text="Co-op Maps:", anchor="w").grid(row=nextRow, column=0, columnspan=2, sticky="w")
		CreateFields(page2, 1352, True, nextRow+1)

		################## 15x15s
		page3 = tk.Frame(specificPAKPopup)
		page3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		# Populate normal maps
		tk.Label(page3, text="Normal Maps:", anchor="w").grid(row=0, column=0, columnspan=2, sticky="w")
		nextRow = CreateFields(page3, 1800, False, 1) # Create fields, return the next row to continue on
		# Pad for three rows
		PadRows(page3, nextRow, 2)
		nextRow += 2
		# Populate coop maps
		tk.Label(page3, text="Co-op Maps:", anchor="w").grid(row=nextRow, column=0, columnspan=2, sticky="w")
		CreateFields(page3, 1800, True, nextRow+1)

		################## Misc
		page4 = tk.Frame(specificPAKPopup)
		page4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

		# Populate normal maps
		tk.Label(page4, text="Normal Maps:", anchor="w").grid(row=0, column=0, columnspan=2, sticky="w")
		nextRow = CreateFields(page4, None, False, 1) # Create fields, return the next row to continue on
		# Pad for three rows
		PadRows(page4, nextRow, 5)
		nextRow += 5
		# Populate coop maps
		tk.Label(page4, text="Co-op Maps:", anchor="w").grid(row=nextRow, column=0, columnspan=2, sticky="w")
		CreateFields(page4, None, True, nextRow+1)

		################## Navigation Elements
		global outputDirFldPak
		outputDirFldPak = tk.StringVar()
		outputDirFldPak.set("")
		b1 = tk.Button(navFrame, text="11x11 Maps", command=page1.lift).pack(side="left")
		b2 = tk.Button(navFrame, text="13x13 Maps", command=page2.lift).pack(side="left")
		b3 = tk.Button(navFrame, text="15x15 Maps", command=page3.lift).pack(side="left")
		b4 = tk.Button(navFrame, text="Other Maps", command=page4.lift).pack(side="left")

		proceed = [False]

		okayButton = tk.Button(navFrame, text="Build PAK", command=lambda: proceed.__setitem__(0,True)).pack(side="right")
		tk.Label(navFrame, text="               ").pack(side="right") # This was the fastest way to pad and seems to work quite well
		outputBrowse = tk.Button(navFrame, text="Browse", command=lambda: outputDirFldPak.set(tkfd.askdirectory(parent=root))).pack(side="right")
		outputBar = tk.Entry(navFrame, textvariable=outputDirFldPak).pack(side="right")
		outputLbl = tk.Label(navFrame, text="Output Directory: ").pack(side="right")

		# Display page 1 and wait for the user to proceed
		page1.lift()

		while True:
			if specificPAKPopup.winfo_exists() == False:
				raise PopupClosedError()
			elif proceed[0] == True:
				specificPAKPopup.destroy()
				break
			else:
				specificPAKPopup.update_idletasks()
				specificPAKPopup.update()

		# And now we build a pak!
		outputDir = outputDirFldPak.get()
		paddedMaps = PadMaps(True)
		BuildPak(outputDir, paddedMaps)

		global scrollbar
		if outputDir[-1] == "/":
			outputPath = outputDir + "fields.pak"
		else:
			outputPath = outputDir + "/fields.pak"
		scrollbar.setNoPreview(outputPath, os.stat(outputPath).st_size)
	except PopupClosedError as e:
		pass
	except Exception as e:
		console.insert(tk.END, "\nUh oh! Looks like there was an error. The creation of a PAK has been stopped.\n")
		console.insert(tk.END, "If there exists one or several temporary files in the OJ Edit directory, you are safe to delete them.\n")
		console.insert(tk.END, "Your PAK will likely not work correctly, and may not have all the maps or all the background images in it.\n")
		console.insert(tk.END, "Make sure you selected one or several valid FLDs and nothing else, and also make sure you have an extracted copy of the official fields.pak file in a folder called OfficialFields in the same directory as your copy of OJ Edit.\n")
		console.insert(tk.END, "If the problem persists after verifying the above, please send the program author any maps you used to generate the PAK, and the PAK that was generated when this error was raised, as well as the following information:\n")
		console.insert(tk.END, traceback.format_exc())
		console.see(tk.END)

###############################################################################################
### File Open Popup Callbacks                                                               ###
###############################################################################################

def AskOpenFile(file, frame):
	"""
	Callback for tkfd.askopenfilename
	"""
	path = tkfd.askopenfilename(parent=frame)
	file.set(path)
