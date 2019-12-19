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
import random

def XORMultipleImages():
	try:
		global root
		global xorFilesPopup
		global xorString
		global xorOutputDir
		global scrollbar
		global console

		xorString = tk.StringVar()
		xorString.set("")
		xorOutputDir = tk.StringVar()
		xorOutputDir.set("")

		x = root.winfo_x()
		y = root.winfo_y()
		w = root.winfo_width()
		h = root.winfo_height()
		popupWidth = 275
		popupHeight = 100
		xorFilesPopup = tk.Toplevel()
		xorFilesPopup.geometry("%dx%d+%d+%d" % (popupWidth, popupHeight, (x + w/2)-popupWidth/2, (y + h/2)-popupHeight/2))
		xorFilesPopup.transient(root)
		xorFilesPopup.iconbitmap("favicon.ico")
		xorFilesPopup.title("Decrypt/Encrypt texture files")

		# Set widgets
		tk.Label(xorFilesPopup, text="File(s): ").grid(row=1, column=0)
		tk.Entry(xorFilesPopup, textvariable=xorString).grid(row=1, column=1, columnspan=2)
		tk.Button(xorFilesPopup, text="Browse", command=lambda: xorString.set(tkfd.askopenfilenames(parent=xorFilesPopup))).grid(row=1, column=3)

		tk.Label(xorFilesPopup, text="Output Directory: ").grid(row=2, column=0)
		tk.Entry(xorFilesPopup, textvariable=xorOutputDir).grid(row=2, column=1, columnspan=2)
		tk.Button(xorFilesPopup, text="Browse", command=lambda: xorOutputDir.set(tkfd.askdirectory(parent=root))).grid(row=2, column=3)

		proceed = [False] # Python 2 won't let you do assignment in lambdas... unless you're assigning to a list :V

		okayButton = tk.Button(xorFilesPopup, text="Okay", command=lambda: proceed.__setitem__(0,True)).grid(row=3, column=1)

		# Loop the convertFilesPopup dialogue while we wait for the Okay button to be pressed
		while True:
			if xorFilesPopup.winfo_exists() == False:
				raise PopupClosedError()
			elif proceed[0] == True:
				xorFilesPopup.destroy()
				break
			else:
				xorFilesPopup.update_idletasks()
				xorFilesPopup.update()

		fileList = ParseMultipleFilenames(xorString.get())
		outDir = xorOutputDir.get()

		for path in fileList:
			XORTextureFile(path, outDir)

		scrollbar.setNoPreview(None, None)

		lineToBeOutput = str(len(fileList)) + " image(s) exported to " + xorOutputDir.get() + "!\n"
		console.insert(tk.END, lineToBeOutput)

	except PopupClosedError as e:
		pass
	except Exception as e:
		console.insert(tk.END, traceback.format_exc())

def ConvertMultipleImages(outputFormat):
	try:
		global root
		global convertFilesPopup
		global convertString
		global convertOutputDir
		global console
		global scrollbar

		convertString = tk.StringVar()
		convertString.set("")
		convertOutputDir = tk.StringVar()
		convertOutputDir.set("")

		# Set the popup geometry and screen location
		x = root.winfo_x()
		y = root.winfo_y()
		w = root.winfo_width()
		h = root.winfo_height()
		popupWidth = 275
		popupHeight = 100
		convertFilesPopup = tk.Toplevel()
		convertFilesPopup.geometry("%dx%d+%d+%d" % (popupWidth, popupHeight, (x + w/2)-popupWidth/2, (y + h/2)-popupHeight/2))
		convertFilesPopup.transient(root)
		convertFilesPopup.iconbitmap("favicon.ico")
		convertFilesPopup.title("Convert texture files")

		# Set widgets
		tk.Label(convertFilesPopup, text="File(s): ").grid(row=1, column=0)
		tk.Entry(convertFilesPopup, textvariable=convertString).grid(row=1, column=1, columnspan=2)
		tk.Button(convertFilesPopup, text="Browse", command=lambda: convertString.set(tkfd.askopenfilenames(parent=convertFilesPopup))).grid(row=1, column=3)

		tk.Label(convertFilesPopup, text="Output Directory: ").grid(row=2, column=0)
		tk.Entry(convertFilesPopup, textvariable=convertOutputDir).grid(row=2, column=1, columnspan=2)
		tk.Button(convertFilesPopup, text="Browse", command=lambda: convertOutputDir.set(tkfd.askdirectory(parent=root))).grid(row=2, column=3)

		proceed = [False] # Python 2 won't let you do assignment in lambdas... unless you're assigning to a list :V

		tk.Button(convertFilesPopup, text="Okay", command=lambda: proceed.__setitem__(0,True)).grid(row=3, column=1)

		if outputFormat == "PNG-DAT":
			console.insert(tk.END, "\nWarning! The old DAT format is no longer supported by 100% Orange Juice. Your output\nfiles will not work in the current version of the game.\n")

		# Loop the convertFilesPopup dialogue while we wait for the Okay button to be pressed
		while True:
			if convertFilesPopup.winfo_exists() == False:
				raise PopupClosedError()
			elif proceed[0] == True:
				convertFilesPopup.destroy()
				break
			else:
				convertFilesPopup.update_idletasks()
				convertFilesPopup.update()

		fileList = ParseMultipleFilenames(convertString.get())

		counter = 0
		imagePathList = []
		for path in fileList:
			GetTextureInfo(path)
			outputTuple = ConvertTextureFile(path, outputFormat)
			outputData, outputName = outputTuple[0], outputTuple[1] 

			newPath = convertOutputDir.get() + "/" + outputName
			if newPath == path:
				continue # If newPath == path, that means we didn't convert the file, and we shouldn't try to rewrite it
			outputFile = open(newPath, "wb")
			outputFile.write(outputData)
			outputFile.close()

			imagePathList.append(GetTextureInfo(newPath))

		scrollbar.setImageList(imagePathList)

		# Finally, add a line to console saying how many images have been exported and where to
		lineToBeOutput = str(len(fileList)) + " image(s) exported to " + convertOutputDir.get() + "!\n"
		console.insert(tk.END, lineToBeOutput)
	except PopupClosedError as e:
		pass
	except Exception as e:
		console.insert(tk.END, traceback.format_exc())
