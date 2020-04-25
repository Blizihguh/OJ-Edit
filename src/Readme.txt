Thank you for downloading OJ Edit v2.1!
For usage information, see the "How to Use" option under the Misc menu in the program itself.

Credits:
Developer - Blizihguh
Playtesting - Hakari, Carnegie
Special Thanks - Roadhog360 (.dat encryption key), Corrodias (100% OJ Music Packer/Voice Packer)

Example Fields:
> Black Lagoon by Blizihguh - Features two islands with homes on them, cut apart and only accessible via warp panels. Much like Lagoon Flight, but with more control over when you want to warp.
> Gotham by Blizihguh - Two very tight circles let you bounce around the home panels; you can loop around your home if you want, but you open yourself up to potential drops and warps, as well as attacks from other players!
> Helix by Blizihguh - Lots of rewards can be found around the center, but whether you try your luck with the x2s or play it safe on the outskirts of the field, you'll need to go inward in order to visit home.
> Ronin by Blizihguh - In between homes are corners where you can bounce indefinitely between an ice panel and a blank panel, allowing you to control where you land, wait to catch up with a player, or wait for a potential bully to get further away before continuing.
> Clover Beyblade by Blizihguh - Features a central loop full of x2 panels, as well as an outer loop that lets you go backwards around the center, in order to stay near your home, catch up to targets, or avoid bullies.
> Skatepark by Hakari - Lots of potential encounters (good or bad) can be had in the middle of the field, but in order to rack up stars and cards, you'll need to skate around the edges!
> Down the Drain by Hakari - You can put off heading towards the center for as long as you want, but eventually you'll find yourself heading into the warp in the middle...
> Whirlpool by Carnegie - A central warp tile flows out in all four directions, leading to a wide circle and then tapering off to homes. It's pretty fast to just head home immediately after warping, but beware of the two drop panels in front of each home!
> (New in 1.3!) Roundabout by Blizihguh - The titular roundabout makes it fast to get back home, but only if you're willing to risk losing stars! The journey around the board can be pretty long otherwise, but has lots of healing. 
> (New in 2.0!) Twister Co-Op by Blizihguh - The twist in the center is full of good rewards if you can warp into it, but the outside path isn't bad either! Just be careful, because the center is full of dangerous drop and battle tiles!
> (New in 2.0!) Pigskin Co-Op by Blizihguh - This asymmetric map branches twice on each side, with each branch prominently featuring certain tiles more. You can try to go on the path that has the tiles you want, but beware: each path has different dangers as well!
> (New in 2.0!) Crossroad Co-Op by Hakari - This map features two long roads that cross each other without actually intersecting. Use the long paths to cut across the main loop, or use the ice paths on the outside to cut the trip short!
> (New in 2.0!) Down the Drain Co-Op by Hakari - With the move panels on the outside, and the tight loop around the center, ambushing the boss has gotten a bit easier. But watch out -- the boss can use the move panels and warp to get away fast!
> (New in 2.1!) Advanced Town by Blizihguh - This high-speed map is designed especially for the new RPG game mode! Take advantage of the Warp Move and Ice tiles to quickly navigate between sections of the map!

Mapmaking Tips:
> When entering a warp, the type of warp you enter determines what happens when you come out, not the type of warp you come out of. For example, if you enter a x2 Move Warp and it warps you to a regular warp, you will instantly roll again with two dice.
> It's entirely possible to have an entire map where the paths go in both directions (represented by magenta paths in the .PNG version of a map). However, note that on large maps, this has the potential to crash the game: if you roll too high and have too many options for movement, OJ will run out of memory!
> When designing a map, it's helpful to think of the incentives you're placing for the players. Do you want to encourage them to take a certain route over another one? How can you avoid players staying around their home indefinitely? Think about what paths would be the most interesting and fun for your players to take, and give them light incentives to take those paths.

Troubleshooting (OJ Edit):
> If OJ Edit launches with a popup that says "One or more program files missing or corrupted," try redownloading the program. If the error persists, you can run OJ Edit from cmd with command "OJEdit.exe ignore-checksums", which will attempt to run the program despite this error. However, depending on the source of the error, this may result in unstable behavior.
> If the output says, "File "OJEdit.py", line 57, in LoadBaseFile" and "Key Error: [some number]L", make sure you selected a valid file for the option you selected (a .FLD file for FLD to PNG, for instance).
> If the output says, "FormatError: FormatError: PNG file has invalid signature," make sure you selected a valid file for the option you selected (a .PNG file for PNG to FLD, for instance).
> If the output says, "IndexError: string index out of range," make sure you selected an output directory for OJ Edit to save your output file(s) to. 
> If the output says, "IOError: cannot identify image file," make sure you selected a valid file for the option you selected (.dat for DAT to PNG, .png for PNG to DAT). Note that not all DAT files in OJ's files are images -- some may be audio. If you're not sure, ask around, or try Corrodias' 100% OJ Music Packer (for music) and 100% OJ Voice Packer (for other audio files).
> If the output says, "Error: will not convert image with alpha channel to RGB," make absolutely sure that your image contains no transparency. Sometimes images with no transparent pixels will be saved with transparency; to be absolutely certain, I reccomend using Paint.NET and saving your image with 8-bit bit depth.

Troubleshooting (100% Orange Juice):
> If OJ hangs ("100orange.exe is not responding") after importing fields.pak, don't worry! This is normal; OJ doesn't recognize the new fields and needs a minute to process them. Usually subsequent launches will not have this delay, but either way, as long as OJ doesn't crash outright -- and typically it will do so very quickly on launch -- your fields should be loading fine.
> If, when playing online, your party crashes or desyncs, make sure everyone has the same exact fields.pak (or at least, the map you're playing on is exactly the same between them). DO NOT PLAY PUBLIC MATCHES WITH CUSTOM FIELDS, EVERYONE WILL DESYNC OR CRASH!
> If one of your maps is cut off (certain rows/columns of tiles don't appear ingame), there's an issue with the size of the map. If you copied the fields into fields.pak yourself, make sure the custom field file is the same size as the map it's replacing. Otherwise, please post the .FLD file, the .PNG you used to generate it, and the map it's replacing on Discord or the Steam thread for OJ Edit.
> If one of your maps is desynced (rows of tiles appear offset relative to each other, so a square becomes a parallelogram), there's an issue with the size of the map. If you copied the fields into fields.pak yourself, make sure the custom field file is the same size as the map it's replacing. Otherwise, please post the .FLD file, the .PNG you used to generate it, and the map it's replacing on Discord or the Steam thread for OJ Edit.
> If you crash while playing on an "open world" map (one in which every tile uses the magenta bi-directional path markers), be aware that OJ may consume a lot of memory on these maps. Specifically, if you roll a high number on double dice (or quadruple dice, for that matter), OJ may crash while trying to find all the possible paths that you might take. There's really not much to be done about this -- the same crash can be achieved in the unmodified game by simply placing too many trap cards at the same time. If you're concerned about this, try to limit the size of areas in your maps that use bi-directional pathing.
> If the map appears to be missing tiles (perhaps all the tiles) ingame, makes sure that all the tiles are exactly the same colour as they appear in the palette. If your tiles are even slightly off (say, #2A2B2B instead of #2B2B2B), OJ Edit won't recognize them! If you save the palette as a JPG (or a PNG with the wrong settings), it may corrupt the palette; redownload OJ Edit or grab a copy of the palette from someone on the Discord server.
> If nobody can move on your map, or there's an area on the map where units get stuck, there's an error with the pathing in your image. Make sure that you've included paths (look for the dotted lines in the example fields), that the path pixels are the exact right colours (#FFFFFF, #404040, and #FE006E), and that the paths are what you're intending (see the example at the bottom of the palette).

If you need additional help, want to see others' maps or share your maps with others, find people to play custom maps with, would like to contact the developer of OJ Edit, or simply want to talk about OJ, try the 100% OJ Modding Discord server:
https://discord.gg/VQfDFxm