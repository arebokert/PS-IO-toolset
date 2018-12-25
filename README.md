### PS-IO toolset
The purpose of this tool is to mass-add bins to your PS-IO library. It takes three folders, one containing images, one containing CU2 files and one containing bin files and automatically matches the CU2s and images to the bin files in their respective folders. It also merges folders that contain multiple bin files.

#### Preparation

 - All bin files need to be separated in to folders
 - The CU2 files need to have gameIDs in their filenames
	 - Can be found [here](http://www.cybdyn-systems.com.au/forum/viewtopic.php?f=72&t=1247&p=13413&hilit=all_redump.org_cu2#p13413) ([or here if the forums are ever taken down](https://mega.nz/#!wpxRhKQY!bL1qmtR4_jPfqBdvcfo5tqwTQxe3NQghrZuJ_ZdyeQg))
 - The image files need to have gameIDs in their filenames
	 - Can be found [here](http://www.cybdyn-systems.com.au/forum/viewtopic.php?f=17&t=872)
#### Requirements
 - [Binmerge](https://github.com/putnam/binmerge)
 - [read-game-id](https://www.legroom.net/software/read-game-id) (including specified requirements [bchunk](http://he.fi/bchunk/) [read-sfo, from PS3 Tools](https://github.com/Rancido/PS3-Tools) [7z, from p7zip](https://sourceforge.net/projects/p7zip/))
#### How to
Place binmerge and read-game-id.sh in the same directory as ps-io-toolset.py. Run ps-io-toolset.py -h for instructions. 

#### Output of help flag

    usage: ps-io-toolset.py [-h] [-c CU2S] [-i IMGS] -g GAMES
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CU2S, --cu2s CU2S  Input folder containing CU2 files. If not supplied,
                            CU2s will not be copied
      -i IMGS, --imgs IMGS  Input folder containing image files (need to be bmp format). If not supplied,
                            images will not be copied
      -g GAMES, --games GAMES
                            Input folder containing bin files (need to be
                            separated in to folders)

#### Caution
This tool will delete the separated bin files after merging them all in to one single bin.

If multiple matching CU2 files are found for the gameID in question, the tool will first check version of the bin. If version is not found in the file name it will pick the last one in order of found CU2 files.