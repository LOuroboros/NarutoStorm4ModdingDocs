## Requisites

* Icons and names contained in .xfbin files extracted from the game's .cpk files to use as a base.

* A hexadecimal editor, such as [HxD](https://mh-nexus.de/en/downloads.php?product=HxD20).

* [Noesis](../tools/Noesis)

## Initial Notes

* The icons can be found in the `ui\flash\OTHER\charicon_p` folder of the different .cpk files. Depending on the character you intend to modify, your may find one icon in one .cpk file and another icon inside another one.

* Character names are located in `ui\flash\OTHER\name_m` and `ui\flash\OTHER\name_l`.

  * The names in `name_m` are those you see during battle, right besides a character's icon above the health bars.

  * The names in `name_l` are those you see in the character select screen.

* In this case, I'll be using Kabuto's stuff. I got his original icon *(`p_kbt1.xfbin`)* and name *(`nl_kbt1.xfbin` and `nm_kbt1.xfbin`)* from the aforementioned paths, inside the game's `data\launch\dataRegion.cpk` file.

* The .xfbin files must be decrypted. To decrypt them you can use [QuickBMS](../tools/QuickBMS) and its XFBIN Decrypter script.

  * Long story short: Open QuickBMS, load CC2_XFBIN_Decrypter.bms, your .xfbin, choose a folder to save the result, and that's it.

  * Here's a comparison as HxD shows Kabuto's `nl_kbt1.xfbin`: [Encrypted](../pics/adding_custom_icons_and_names_1.png), [Decrypted](../pics/adding_custom_icons_and_names_2.png).

## Instructions

1) To make our 3 files editable, we'll first open them in HxD and then we'll select everything starting from the offset 0x120, and ending with the file's size, which can be seen in the 2 bytes just before 0x120, [like this](../pics/adding_custom_icons_and_names_3.png).

    * In this case, B367 = 45927 bytes. That's the true size of the picture embedded in this `nl_kbt1.xfbin` file.

2) Now we'll press Ctrl + C to copy our selection, Ctrl+N to start a new file, and Ctrl+V to paste it. Then we'll go to File -> Save As, and save this as a .png file, preferably keeping the same filename as the original .xfbin file, meaning that if I copied the png contents of Kabuto's `nl_kbt1.xfbin`, I'd name its .png as `nl_kbt1.png`.

    * And now I can check that, effectively, [it has a file size of 45927 bytes](../pics/adding_custom_icons_and_names_4.png).

3) Do this with all 3 files, and then edit each .png to your heart's content using a software such as Adobe Photoshop, Paint.NET or whatever.

4) Once you're ready, open each .png on HxD and select their contents with Ctrl+A.

5) Go to the equivalent .xfbin opened in HxD, and select every byte starting at 0x120 and ending with `IEND®B`, basically, the same chunk we first isolated and turned into a .png file. You can help yourself using HxD's Select Block feature.

6) Now, simply copy the contents of the .png, and paste them over the selected portion of the .xfbin file.

7) Adjust the image file size inside our freshly cooked .xfbin file. Again, it's the 2 bytes just before 0x120. You'll also have to write 12 bytes before those 2, the file size + 4 *(in Hex obviously)*.

    * For example, I made a custom icon for Kabuto which has a size of 28101 bytes. As such, I will replace the bytes before 0x120 containing the original icon's size, "39 85", with "6D C5". Similarly, 12 bytes before that "39 85", there's a "39 89". I'll replace it with "6D C9", [like this](../pics/adding_custom_icons_and_names_5.png).

8) Follow the same process with the remaining pairs of .xfbin and .png files.

9) Save and test.

## Ending Notes

* Each file must be put inside the game's data_win32 folder *(if there isn't one, make it)*, respecting the paths given in the initial notes.

  * In other words, the 3 xfbin files you'll end up with have to be put in the following locations:

  * `Game_Folder\data_win32\ui\flash\OTHER\charicon_p`

  * `Game_Folder\data_win32\ui\flash\OTHER\name_m`

  * `Game_Folder\data_win32\ui\flash\OTHER\name_l`

* Game_Folder refers to the folder containing the game's basic files, such as NSUNS4.exe.

* In this case, my intention is to give an icon and a name for the 2nd costume I gave to Kabuto, whose ID is `4kbt`. As I result, I will want to make sure that all 3 .xfbin files point to the character ID `4kbt` instead of the original `1kbt`. That goes for the files' filenames, but also their contents. This is no different than [the process to perform a model swap](../docs/doing_a_model_swap.md).

## Credits

* [Burn You](https://www.youtube.com/watch?v=tlRMvPyfftU)

* [Clavilux](https://www.youtube.com/channel/UC6ThnFNtIOaWldCwiqNRB0Q/videos), who shared the XFBIN decrypting script for QuickBMS with me.

* [Magastem](https://www.youtube.com/watch?v=xjFTM967Nds&t=0s)