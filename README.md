# KindleComicConverter

`KindleComicConverter` is a Python app to convert comic files or folders to ePub or Panel View Mobipocket.
It was initally developed for Kindle but as of version 2.2 it outputs valid ePub 2.0 so you can use in nearly
 any eReader.
It also optimizes comic images by:
- enhancing contrast
- cutting page numbering
- cropping white borders
- resizing larger images to device's native resolution
- quantizing images to device's palette

## BINARY RELEASES
You can find the latest released binary at the following links:  
- OS X: [https://dl.dropbox.com/u/16806101/KindleComicConverter_osx_2.2.zip](https://dl.dropbox.com/u/16806101/KindleComicConverter_osx_2.2.zip)
- Win32: 
- Linux: just download sourcecode and launch `python kcc.py` *(provided you have Python and Pillow installed)*

## INPUT FORMATS
`kcc` can understand and convert, at the moment, the following file types:  
- CBZ, ZIP
- CBR, RAR *(with `unrar` executable)*
- ~flat folders~ AT THE MOMENT `kcc` CAN NOT MANAGE FOLDERS!
- PDF *(extracting only contained **JPG** images)*

~~For now the script does not understand folder depth, so it will work on flat folders/archives only.~~
As of v. 1.50, KCC supports subfolders!

## OPTIONAL REQUIREMENTS
- `kindlegen` in /usr/local/bin/ *(for .mobi generation)*
- [unrar](http://www.rarlab.com/download.htm) *(for CBR support)*

### for compiling/running from source:
- Python 2.7+ (included in MacOS and Linux, follow the [official documentation](http://www.python.org/getit/windows/) to install on Windows)
- [Python Imaging Library](http://www.pythonware.com/products/pil/) for comic optimizations like split double pages, resize to optimal resolution, improve contrast and palette, etc.
  Please refer to official documentation for installing into your system.

## USAGE

### GUI

Should be pretty self-explanatory, just keep in mind that it's still in development ;)

### Standalone `comic2ebook.py` usage:

```
comic2ebook.py [options] comic_file|comic_folder
  Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -p PROFILE, --profile=PROFILE
                          Device profile (choose one among K1, K2, K3, K4, KDX,
                          KDXG or KHD) [default=KHD]
    -t TITLE, --title=TITLE
                          Comic title [default=filename]
    -m, --manga-style     Split pages 'manga style' (right-to-left reading)
                          [default=False]
    -v, --verbose         Verbose output [default=False]
    --no-image-processing
                          Do not apply image preprocessing (page splitting and
                          optimizations) [default=True]
    --upscale-images      Resize images smaller than device's resolution
                          [default=False]
    --stretch-images      Stretch images to device's resolution [default=False]
    --no-cut-page-numbers
                          Do not try to cut page numbering on images
                          [default=True]
```

The script takes care of unzipping/unrarring the file if it's an archive, creating a directory of images which should be then filled with a `.opf`, `.ncx`, and many `.html` files, then:  
1. Run `Kindlegen` on `content.opf`. Depending on how many images you have, this may take awhile. Once completed, the `.mobi` file should be in the directory.  
2. (optionally) remove the SRCS record to reduce the `.mobi` filesize in half. You can use [Kindlestrip](http://www.mobileread.com/forums/showthread.php?t=96903).
3. Copy the `.mobi` file to your Kindle!

### AppleScript Droplet (may be outdated)

Drop a folder or a CBZ/CBR file over the app, after a while you'll get a comic-type .mobi to sideload on your Kindle.
The script takes care of calling `comic2ebook.py`, `kindlegen` and `kindlestrip.py`.

> **WARNING:** at the moment the droplet *ALWAYS* uses the **KHD** profile (*Kindle Paperwhite*).
> If you want to specify other profiles, please use the script from command line.


## CREDITS
This script born as a cross-platform alternative to `KindleComicParser` by **Dc5e** (published in [this mobileread forum thread](http://www.mobileread.com/forums/showthread.php?t=192783))

The app relies and includes the following scripts/binaries:

 - the `KindleStrip` script &copy; 2010-2012 by **Paul Durrant** and released in public domain
([mobileread forum thread](http://www.mobileread.com/forums/showthread.php?t=96903))
 - the `rarfile.py` script &copy; 2005-2011 **Marko Kreen** <markokr@gmail.com>, released with ISC License
 - the free version `unrar` executable (downloadable from [here](http://www.rarlab.com/rar_add.htm), refer to `LICENSE_unrar.txt` for further details)
 - the icon is by **Nikolay Verin** ([http://ncrow.deviantart.com/](http://ncrow.deviantart.com/)) and released under [CC Attribution-NonCommercial-ShareAlike 3.0 Unported](http://creativecommons.org/licenses/by-nc-sa/3.0/) License
 - the `image.py` class from **Alex Yatskov**'s [Mangle](http://foosoft.net/mangle/) with subsequent [proDOOMman](https://github.com/proDOOMman/Mangle)'s and [Birua](https://github.com/Birua/Mangle)'s patches

Also, you need to have `kindlegen` v2.7 (with KF8 support) which is downloadable from Amazon website
and installed in `/usr/local/bin/`


## CHANGELOG
  - 1.00: Initial version
  - 1.10: Added support for CBZ/CBR files in comic2ebook.py
  - 1.11: Added support for CBZ/CBR files in KindleComicConverter
  - 1.20: Comic optimizations! Split pages not target-oriented (landscape with portrait target or portrait
   with landscape target), add palette and other image optimizations from Mangle.
   WARNING: PIL is required for all image mangling!
  - 1.30: Fixed an issue in OPF generation for device resolution
   Reworked options system (call with -h option to get the inline help)
  - 1.40: Added some options for controlling image optimization
        Further optimization (ImageOps, page numbering cut, autocontrast)
  - 1.41: Fixed a serious bug on resizing when img ratio was bigger than device one
  - 1.50: Added subfolder support for multiple chapters.
  - 2.0: GUI! AppleScript is gone and Tk is used to provide cross-platform GUI support.
  - 2.1: Added basic error reporting
  - 2.2: Added (valid!) ePub 2.0 output
        Rename .zip files to .cbz to avoid overwriting
  - 2.3: Fixed win32 ePub generation, folder handling, filenames with spaces and subfolders.

## TODO
  - Add gracefully exit for CBR if no rarfile.py and no unrar executable are found
  - Try to get filetype from magic number (found some CBR that was actually CBZ)
  - Improve GUI displaying what file we're processing and giving an explicit progress status
  - Better GUI design
  - Make window take focus on app launch
  - [OSX] Finder-launched app does not take into account user local $PATH

## COPYRIGHT

Copyright (c) 2012-2013 Ciro Mattia Gonano. See LICENSE.txt for further details.
