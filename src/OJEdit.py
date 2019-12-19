# OJ Edit by Blizihguh
# Field and graphics replacement tool for 100% Orange Juice

import tkFileDialog as tkfd
try:
	from PIL import Image, ImageTk, ImageFile
	ImageFile.LOAD_TRUNCATED_IMAGES = True
except:
	print "PIL not found!"
	print "Python Imaging Library (PIL) is necessary for this program to run properly."
	print "Install PIL or Pillow as such:"
	print "pip install python-PIL"
	print "or"
	print "pip install Pillow"
	print "This code was written with PIL in mind, but Pillow is generally preferred; if Pillow isn't working, try PIL instead."

try:
	import png
except:
	print "PyPNG not found!"
	print "If you're running this program to pack files you should be fine. Otherwise, install PyPNG as such:"
	print "pip install pypng"

try:
	import numpy
except:
	print "NumPy not found!"
	print "Install NumPy as such:"
	print "pip install numpy"

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
import hashlib

global mapsTable, graphicsList, fieldSizeTable
mapsTable = {
	# 11x11 Normal
	"field_clover.fld": [968, False, "Clover", None],
	"field_wonderland.fld": [968, False, "Icy Hideout", None],
	"field_nightflight.fld": [968, False, "Night Flight", None],
	"field_practice.fld": [968, False, "Practice Field", None],
	"field_pudding.fld": [968, False, "Pudding Chase", None],
	"field_workshop.fld": [968, False, "Santa's Workshop", None],
	"field_wander.fld": [968, False, "Space Wanderer", None],
	"field_tomomo.fld": [968, False, "Tomomo's Abyss", None],
	"field_vortex.fld": [968, False, "Vortex", None],
	"field_war.fld": [968, False, "Warfare", None],
	# 11x11 Coop
	"field_nightflight_co.fld": [968, True, "Night Flight", None],
	"field_pudding_co.fld": [968, True, "Pudding Chase", None],
	"field_workshop_co.fld": [968, True, "Santa's Workshop", None],
	"field_wander_co.fld": [968, True, "Space Wanderer", None],
	"field_vortex_co.fld": [968, True, "Vortex", None],
	# 13x13 Normal
	"field_christmas.fld": [1352, False, "Christmas Miracle", None],
	"field_frost.fld": [1352, False, "Frost Cave", None],
	"field_lagoon.fld": [1352, False, "Lagoon Flight", None],
	"field_island.fld": [1352, False, "Treasure Island", None],
	"field_islandnight.fld": [1352, False, "Treasure Island (Night)", None],
	"field_oceandive.fld": [1352, False, "Ocean Dive", None],
	# 13x13 Coop
	"field_cyberspace.fld": [1352, True, "Cyberspace", None],
	"field_lagoon2.fld": [1352, True, "Lagoon Flight", None],
	"field_island_co.fld": [1352, True, "Treasure Island", None],
	"field_islandnight_co.fld": [1352, True, "Treasure Island (Night)", None],
	"field_oceandive_co.fld": [1352, True, "Ocean Dive", None],
	# 15x15 Normal
	"field_farm.fld": [1800, False, "Farm", None], 
	"field_highway.fld": [1800, False, "Highway Heist", None],
	"field_planet.fld": [1800, False, "Planet Earth", None],
	"field_sakura.fld": [1800, False, "Sakura Smackdown", None],
	"field_seal.fld": [1800, False, "Sealed Archive", None],
	"field_starcircuit.fld": [1800, False, "Star Circuit", None],
	"field_sunset.fld": [1800, False, "Sunset", None],
	"field_sweetheaven.fld": [1800, False, "Sweet Heaven", None],
	"field_training.fld": [1800, False, "Training Program", None],
	"field_forest.fld": [1800, False, "Witch Forest", None],
	# 15x15 Coop
	"field_farm_co.fld": [1800, True, "Farm", None],
	"field_highway_co.fld": [1800, True, "Highway Heist", None],
	"field_planet_co.fld": [1800, True, "Planet Earth", None],
	"field_poppo.fld": [1800, True, "Poppo's Abyss", None],
	"field_sakura_co.fld": [1800, True, "Sakura Smackdown", None],
	"field_starcircuit_co.fld": [1800, True, "Star Circuit", None],
	"field_sunset2.fld": [1800, True, "Sunset", None],
	"field_training_co.fld": [1800, True, "Training Program", None],
	"field_forest_co.fld": [1800, True, "Witch Forest", None],
	# Misc Normal
	"field_starship.fld": [1152, False, "Starship (12x12)", None],
	"field_shipyard.fld": [1040, False, "Shipyard (13x10)", None],
	"field_winter.fld": [1568, False, "White Winter (14x14)", None],
	# Misc Coop
	"field_shipyard_co.fld": [1248, True, "Shipyard (13x12)", None]
}
graphicsList = [
	"aurora.dat", 
	"christmas_h.dat", "christmas_l.dat", "christmas_o.dat",
	"clover_l.dat",
	"empty.dat",
	"farm_h.dat", "farm_l.dat",
	"frost_l.dat",
	"highway_l.dat", "highway_o.dat",
	"island_h.dat", "island_l.dat",
	"islandnight_h.dat", "islandnight_l.dat",
	"lagoon_h.dat", "lagoon_l.dat",
	"nightflight_h.dat", "nightflight_l.dat", "nightflight_o.dat",
	"planet_h.dat", "planet_l.dat",
	"practice_l.dat",
	"pudding_l.dat",
	"seal_h.dat", "seal_l.dat", "seal_o.dat",
	"shipyard_h.dat", "shipyard_l.dat",
	"snow.dat", # Why isn't this named corresponding to the map it's from? This lead to a really confusing error >:I
	"starcircuit_l.dat", "starcircuit_h.dat",
	"starship_h.dat", "starship_l.dat", "starship_o.dat",
	"sunset_h.dat", "sunset_l.dat", "sunset_o.dat",
	"sweet_h.dat", "sweet_l.dat",
	"tomomo_h.dat", "tomomo_l.dat", "tomomo_o.dat",
	"training_e.dat", "training_h.dat", "training_l.dat",
	"vortex_h.dat", "vortex_l.dat",
	"wander_h.dat", "wander_l.dat",
	"war_h.dat", "war_l.dat", "war_o.dat",
	"winter_l.dat",
	"forest_h.dat", "forest_l.dat", # New in Girl Power update
	"wonderland_h.dat", "wonderland_l.dat", "wonderland_o.dat", # New in Christmas 2017 update
	"sakura_l.dat", # New in Playground update
	"workshop_l.dat", # New in Crossed Christmases update
	"cyberspace_l.dat", "cyberspace_o.dat", # New in 5th Anniversary update
	"poppo_h.dat", "poppo_l.dat", # New in 5th Anniversary update
	"oceandive_h.dat", "oceandive_l.dat" # New in Summer 2019 update
]
fieldSizeTable = {
	968: 88,
	1040: 104,
	1056: 88,
	1152: 96,
	1248: 104,
	1352: 104,
	1568: 112,
	1800: 120
}

def HowToUse():
	global root

	x = root.winfo_x()
	y = root.winfo_y() 
	w = root.winfo_width()
	h = root.winfo_height()
	popupWidth = 610
	popupHeight = 500
	popup = tk.Toplevel()
	popup.geometry("%dx%d+%d+%d" % (popupWidth, popupHeight, (x + w/2)-popupWidth/2, (y + h/2)-popupHeight/2))
	popup.transient(root)
	popup.iconbitmap("favicon.ico")
	popup.title("Help")

	helpText = "Converting field files to images: First, select \"FLD to PNG\" from the Fields menu. Select any number of OJ field files (.fld) and select an " + \
	"output directory, then click Okay. The fields will be converted to PNG images, allowing them to be edited or shared.\n\n" + \
	"Converting field images to field files: First, create a .png file representing a field using an image editor. Each tile should take up 3x3 pixels, using the " + \
	"palette provided with OJ Edit, with dotted lines representing movement directions (see the example files and readme for reference). Then, select \"PNG to FLD\" " + \
	"in the Fields menu. Select any number of valid field images (.png) and select an output directory, then click Okay. The images will be converted to field files, " + \
	"allowing them to be imported into 100% Orange Juice by replacing the files in fields.pak.\n\n" + \
	"Packaging field files into a .pak: In order to play custom fields in OJ, they must be inserted into the game's fields.pak file, replacing one of the official fields. " + \
	"It is possible to do this manually by renaming the file to fields.zip and replacing fields inside of it, but OJ Edit can automatically build a fields.pak with " + \
	"custom maps in it! First, select \"FLDs to PAK\" from the Fields menu. Select any number of OJ field files (.fld) to be inserted over normal or co-op maps, " + \
	"then select an output directory and click Okay. OJ Edit will automatically find fields to replace with the chosen files and build a .pak with them. Alternatively, " + \
	"go to the Fields menu and select \"...Specify Replacements\" in order to manually choose which files will replace which fields.\n\n" + \
	"Converting texture files: First, select your desired output format from the Graphics menu. Then, select any number of .png, .dds, or OJ .dat files, and " + \
	"OJ Edit will convert them and save them to your chosen output directory. Note that the game previously used a different .dat format, which is still available " + \
	"as an option in OJ Edit, however, these files will no longer work ingame. Also, for a small number of OJ textures, the .dat format used is different, and will " + \
	"not work with OJ Edit. If you are encountering problems converting textures from the game, select \"Decrypt/Encrypt\" in order to simply decrypt the files, then " + \
	"load them with any image editor that accepts .dds files (eg: Paint.NET, Photoshop). After editing them, you can use \"Decrypt/Encrypt\" to automatically convert " + \
	"them back into an OJ .dat file. Note that not all .dat files in OJ are actually textures -- if you can't convert a file, and can't open it in an image editor even " + \
	"after decrypting it, make sure it's actually an image!\n\n" + \
	"For more help, see the included readme, or find contact information in the \"About\" tab." 
	msg = tk.Message(popup, width=600, text=helpText, justify="left", anchor="w")
	msg.pack(anchor="w")

	button = tk.Button(popup, text="Close", command=popup.destroy)
	button.pack(anchor="s", side="bottom", pady=2)

def ChecksumError():
	popup = tk.Tk()
	popup.geometry("420x69") # I swear this was unintentional, it happens to be the exact right dimensions
	popup.iconbitmap("favicon.ico")
	popup.title("Error")
	msg = tk.Label(popup, text="One or more program files missing or corrupted. Try reinstalling the program?\nIf that fails, check Readme.txt for other suggestions and contact information.")
	msg.grid(row=0, column=0, columnspan=3)

	button = tk.Button(popup, text="Exit", command=popup.destroy)
	button.grid(row=2, column=1)

	try:
		while True:
			if popup.winfo_exists() == False:
				exitProgram()
			else:
				popup.update_idletasks()
				popup.update()
	except:
		exitProgram()

def AboutWindow():
	global root

	x = root.winfo_x()
	y = root.winfo_y() 
	w = root.winfo_width()
	h = root.winfo_height()
	popupWidth = 225
	popupHeight = 200
	popup = tk.Toplevel()
	popup.geometry("%dx%d+%d+%d" % (popupWidth, popupHeight, (x + w/2)-popupWidth/2, (y + h/2)-popupHeight/2))
	popup.transient(root)
	popup.iconbitmap("favicon.ico")
	popup.title("About")

	aboutText = "OJ Edit was made possible by these people!\n\n" + \
		"Developer: Blizihguh\n" + \
		"Playtesting: Hakari, Carnegie\n" + \
		"Special Thanks: Roadhog360\n\n" + \
		"For more information about OJ Edit, or to contact the developer, try the 100% OJ Modding Discord Server at:"
	msg = tk.Message(popup, text=aboutText, justify="left", anchor="w")
	msg.pack(anchor="w")

	discordLink = readText(popup, width=40, height=1)
	discordLink.pack(anchor="w")
	discordLink.insert(tk.END, "https://discord.gg/VQfDFxm")

	button = tk.Button(popup, text="Close", command=popup.destroy)
	button.pack(anchor="s", side="bottom", pady=2)

class readText(tk.Text):
	def __init__(self, *args, **kwargs):
		tk.Text.__init__(self, *args, **kwargs)
		self.redirector = WidgetRedirector(self)
		self.insert = self.redirector.register("insert", lambda *args, **kw: "break")
		self.delete = self.redirector.register("delete", lambda *args, **kw: "break")

		self.tag_config("bgGREEN", background="green", foreground="black")
		self.tag_config("bgRED", background="red", foreground="black")
		self.tag_config("fgGREEN", background="black", foreground="green")
		self.tag_config("fgRED", background="black", foreground="red")

def GUI():
	# Because we're referencing these GUI elements in other functions, we need to make them globals
	# Names are deliberately chosen such that they'd be unlikely to come up in other places outside of GUI stuff
	global root
	global canvas
	global currentImage
	global topPane
	global rightPane
	global currentName
	global currentSize
	global currentHeight
	global currentWidth
	global console
	global scrollbar

	root = tk.Tk()
	menu = tk.Menu(root)
	root.config(menu=menu)
	root.geometry("507x507")
	root.wm_title("OJ Edit")
	root.iconbitmap('favicon.ico')

	# We'll be calling winfo_exists() on this later, and we want to make sure it returns 0 even if there's never been a scrollbar displayed
	scrollbar = tk.Scrollbar(root)
	scrollbar.destroy()
	# Define StringVars for all maps in the mapsTable
	DefineStringVars()

	filemenu = tk.Menu(menu, tearoff=0)
	menu.add_cascade(label="Fields", menu=filemenu)
	filemenu.add_command(label="FLD to PNG", command=FLDtoPNG)
	filemenu.add_command(label="PNG to FLD", command=PNGtoFLD)
	filemenu.add_command(label="FLDs to PAK", command=FLDtoPAK)
	filemenu.add_command(label="...Specify Replacements", command=SpecificFLDPAK)

	graphicsmenu = tk.Menu(menu, tearoff=0)
	menu.add_cascade(label="Graphics", menu=graphicsmenu)
	graphicsmenu.add_command(label="Convert files to:", command=lambda: None)
	graphicsmenu.add_command(label="...PNG", command=lambda:ConvertMultipleImages("PNG"))
	graphicsmenu.add_command(label="...DDS", command=lambda:ConvertMultipleImages("DDS"))
	graphicsmenu.add_command(label="...DAT", command=lambda:ConvertMultipleImages("DDS-DAT"))
	graphicsmenu.add_command(label="...DAT (Old)", command=lambda:ConvertMultipleImages("PNG-DAT"))
	graphicsmenu.add_command(label="Decrypt/Encrypt", command=XORMultipleImages)

	helpmenu = tk.Menu(menu, tearoff=0)
	menu.add_cascade(label="Misc", menu=helpmenu)
	helpmenu.add_command(label="How to use", command=HowToUse)
	helpmenu.add_command(label="About", command=AboutWindow)
	helpmenu.add_command(label="Exit", command=exitProgram)

	# In order to have the names auto-update later, they need to be converted from string vars to StringVars
	currentName = tk.StringVar()
	currentSize = tk.StringVar()
	currentHeight = tk.StringVar()
	currentWidth = tk.StringVar()

	root.grid_columnconfigure(0, weight=1)

	topPane = tk.Frame(root, width=300, height=150)
	topPane.grid(row=0, column=0, sticky="w")

	rightPane = tk.Frame(root, width=150, height=150, bg="black")
	rightPane.grid(row=0, column=1, sticky="e")

	bottomPane = tk.Frame(root, width=300, height=150)
	bottomPane.grid(row=2, columnspan=2, padx=2, pady=2)

	canvas = tk.Canvas(rightPane, width=150, height=150, bg="dark slate gray")
	canvas.pack(side="right")


	currentName.set("Name:\n")
	currentSize.set("Size:\n")
	currentHeight.set("Height:\n")
	currentWidth.set("Width:\n")
	nameLbl = tk.Label(topPane, textvariable=currentName, anchor="w", justify="left")
	sizeLbl = tk.Label(topPane, textvariable=currentSize, anchor="w", justify="left")
	heightLbl = tk.Label(topPane, textvariable=currentHeight, anchor="w", justify="left")
	widthLbl = tk.Label(topPane, textvariable=currentWidth, anchor="w", justify="left")
	scrollbar = ImageScrollbar(rightPane)
	console = readText(bottomPane, width=300, height=23, font=(None,9), background="black", fg="white")
	console.insert(tk.END, "Welcome to the 100% Orange Juice field and image editing tool, OJ Edit!\nTo get started, click on the File menu in the upper left and choose what you'd like to do.\n")
	console.insert(tk.END, "For PNG to FLD conversions, movement data is necessary.\n")
	console.insert(tk.END, "For FLD to PAK conversions, green highlight means the map is a custom map, and red\nhighlight means the map had to be padded to fit the size of the map it's replacing\n")
	console.insert(tk.END, "To see the full output of FLD to PAK conversions, you may need to scroll this console\nupwards with the mouse wheel.\n")
	console.insert(tk.END, "For technical reasons, a preview image will not be displayed when converting non-PNG\ntexture files to non-PNG output formats.\n")
	nameLbl.pack(fill="x")
	sizeLbl.pack(fill="x")
	heightLbl.pack(fill="x")
	widthLbl.pack(fill="x")
	console.pack(fill="both")
	scrollbar.pack(side="left", fill="y")

	root.protocol("WM_DELETE_WINDOW", exitProgram)
	root.mainloop()
	sys.exit()

def DefineStringVars():
    global mapsTable, root
    for key in mapsTable.keys():
        mapsTable[key][3] = tk.StringVar(root)
        mapsTable[key][3].set("")

def DEBUGCallback():
	global console
	try:
		convertedData = ConvertTextureFile("C:/Users/JEcha/Desktop/OJ Edit/ball256.dds", "PNG")
		with open(convertedData[1], "wb") as file:
			file.write(convertedData[0])
		"""
		ddsFile = DDSLoader("C:/Users/JEcha/Desktop/OJ Edit/Working/dds.dds")
		png.from_array(ddsFile.data, mode="RGBA").save("dds_file.png")
		ddsFileTwo = DDSLoader(ddsFile.data, 256, 256)
		ddsFileTwo.save("testOutput.dat")"""
	except Exception as e:
		console.insert(tk.END, traceback.format_exc())
		console.see(tk.END)

def exitProgram():
	sys.exit()

def checksum(filename):
	hash_sha256 = hashlib.sha256()
	with open(filename, "rb") as f:
		for chunk in iter(lambda: f.read(4096), b""):
			hash_sha256.update(chunk)
	return hash_sha256.hexdigest()

# We use a tuple instead of a dict so that we can ensure utils.py executes first
sourceList = (
	("utils.py", "5b83258016f94289557fe9522270132cbfa3c8334d29a1cccec8175f0eaca217"), 
	("dds-reader.py", "96e4e815c8b0f41657be40b4b8a4f86855b058348ae046bfff3016f8e33b1d17"), 
	("fields.py", "8aeec57280455a8e88d0d6de087df21a50dddaba422912e30ee60c797b99bb4b"), 
	("textures.py", "bcd3b161fbd2d45649cc72e5d9a8b7ddace388044e2a60ab60053de43e39a7bd"), 
	("gui-fields.py", "01bc862f4f1082f61340f35a6fe0825fc3741e68e6ee5112237e727dec6e3392"), 
	("gui-textures.py", "1567497a0798646e11f70bc606485613c4f96bb2a3e9a88934e5bdc5184e62bb"),
	("scrollbar.py", "fd60f8f5b46fbb8ad77a7a9242913747ee23e7e8735d0c5a400e7aa16bf424f9")
	)

args = sys.argv
if len(args) < 2:
	args.append(None)

if sys.argv[1] == "ignore-checksums":
	# Display checksums for all program source files
	for i in sourceList:
		print i[0] + " " + checksum("ProgramFiles/" + i[0])
		execfile("ProgramFiles/" + i[0])
else:
	# Verify checksums and exit if one is invalid
	for i in sourceList:
		try:
			if checksum("ProgramFiles/" + i[0]) != i[1]:
				ChecksumError()
			else:
				execfile("ProgramFiles/" + i[0])
		except:
			ChecksumError()

GUI()