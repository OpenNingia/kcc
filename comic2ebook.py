#!/usr/bin/env python
#
# Copyright (c) 2012 Ciro Mattia Gonano <ciromattia@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all
# copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA
# OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#
# Changelog
#  1.00 - Initial version
#  1.10 - Added support for CBZ/CBR files
#  1.11 - Added support for ZIP/RAR extensions
#  1.20 - Comic optimizations! Split pages not target-oriented (landscape
#       with portrait target or portrait with landscape target), add palette
#       and other image optimizations from Mangle.
#       WARNING: PIL is required for all image mangling!
#
# Todo:
#   - Add gracefully exit for CBR if no rarfile.py and no unrar
#       executable are found
#   - Improve error reporting
#   - recurse into dirtree for multiple comics

__version__ = '1.20'

import os
import sys
import cbxarchive

class HTMLbuilder:

    def getResult(self):
        return getImageFileName(self.file)

    def __init__(self, dstdir, file):
        self.file = file
        filename = getImageFileName(file)
        if (filename != None):
            htmlfile = dstdir + '/' + filename[0] + '.html'
            f = open(htmlfile, "w");
            f.writelines(["<!DOCTYPE html SYSTEM \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n",
                          "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n",
                          "<head>\n",
                          "<title>",filename[0],"</title>\n",
                          "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/>\n",
                          "</head>\n",
                          "<body>\n",
                          "<div><img src=\"",file,"\" /></div>\n",
                          "</body>\n",
                          "</html>"
                          ])
            f.close()
        return None

class NCXbuilder:
    def __init__(self, dstdir, title):
        ncxfile = dstdir + '/content.ncx'
        f = open(ncxfile, "w");
        f.writelines(["<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n",
            "<!DOCTYPE ncx PUBLIC \"-//NISO//DTD ncx 2005-1//EN\" \"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd\">\n",
            "<ncx version=\"2005-1\" xml:lang=\"en-US\" xmlns=\"http://www.daisy.org/z3986/2005/ncx/\">\n",
            "<head>\n</head>\n",
            "<docTitle><text>",title,"</text></docTitle>\n",
            "<navMap></navMap>\n</ncx>"
            ])
        f.close()
        return

class OPFBuilder:
    def __init__(self, dstdir, title, filelist):
        opffile = dstdir + '/content.opf'
        # read the first file resolution
        try:
            from PIL import Image
            im = Image.open(dstdir + "/" + filelist[0][0] + filelist[0][1])
            width, height = im.size
            imgres = str(width) + "x" + str(height)
        except ImportError:
            print "Could not load PIL, falling back on default HD"
            imgres = "758x1024"
        f = open(opffile, "w");
        f.writelines(["<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n",
            "<package version=\"2.0\" unique-identifier=\"PrimaryID\" xmlns=\"http://www.idpf.org/2007/opf\">\n",
            "<metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:opf=\"http://www.idpf.org/2007/opf\">\n",
            "<dc:title>",title,"</dc:title>\n",
            "<dc:language>en-US</dc:language>\n",
            "<meta name=\"book-type\" content=\"comic\"/>\n",
            "<meta name=\"zero-gutter\" content=\"true\"/>\n",
            "<meta name=\"zero-margin\" content=\"true\"/>\n",
            "<meta name=\"fixed-layout\" content=\"true\"/>\n",
            "<meta name=\"orientation-lock\" content=\"portrait\"/>\n",
            "<meta name=\"original-resolution\" content=\"" + imgres + "\"/>\n",
            "</metadata><manifest><item id=\"ncx\" href=\"content.ncx\" media-type=\"application/x-dtbncx+xml\"/>\n"])
        for filename in filelist:
            f.write("<item id=\"page_" + filename[0] + "\" href=\"" + filename[0] + ".html\" media-type=\"application/xhtml+xml\"/>\n")
        for filename in filelist:
            if ('.png' == filename[1]):
                mt = 'image/png';
            else:
                mt = 'image/jpeg';
            f.write("<item id=\"img_" + filename[0] + "\" href=\"" + filename[0] + filename[1] + "\" media-type=\"" + mt + "\"/>\n")
        f.write("</manifest>\n<spine toc=\"ncx\">\n")
        for filename in filelist:
            f.write("<itemref idref=\"page_" + filename[0] + "\" />\n")
        f.write("</spine>\n<guide>\n</guide>\n</package>\n")
        f.close()
        return

def getImageFileName(file):
    filename = os.path.splitext(file)
    if (filename[0].startswith('.') or (filename[1].lower() != '.png' and filename[1].lower() != '.jpg' and filename[1].lower() != '.jpeg')):
        return None
    return filename

def isInFilelist(file,list):
    filename = os.path.splitext(file)
    seen = False
    for item in list:
        if filename[0] == item[0]:
            seen = True
    return seen

if __name__ == "__main__":
    print ('comic2ebook v%(__version__)s. '
       'Written 2012 by Ciro Mattia Gonano.' % globals())
    if len(sys.argv)<3 or len(sys.argv)>4:
        print "Generates HTML, NCX and OPF for a Comic ebook from a bunch of images"
        print "Optimized for creating Mobipockets to be read into Kindle Paperwhite"
        print "Usage:"
        print "    %s <profile> <dir> <title>" % sys.argv[0]
        print " <title> is optional"
        sys.exit(1)
    else:
        profile = sys.argv[1]
        dir = sys.argv[2]
        cbx = cbxarchive.CBxArchive(dir)
        if cbx.isCbxFile():
            cbx.extract()
            dir = cbx.getPath()
        if len(sys.argv)==4:
            title = sys.argv[3]
        else:
            title = "comic"
        filelist = []
        try:
            import image
            print "Splitting double pages..."
            for file in os.listdir(dir):
                if (getImageFileName(file) != None):
                    img = image.ComicPage(dir+'/'+file, profile)
                    img.splitPage(dir)
            for file in os.listdir(dir):
                if (getImageFileName(file) != None):
                    print "Optimizing " + file + " for " + profile
                    img = image.ComicPage(dir+'/'+file, profile)
                    img.resizeImage()
                    img.frameImage()
                    img.quantizeImage()
                    img.saveToDir(dir)
        except ImportError:
            print "Could not load PIL, not optimizing image"

        for file in os.listdir(dir):
            if (getImageFileName(file) != None and isInFilelist(file,filelist) == False):
                filename = HTMLbuilder(dir,file).getResult()
                if (filename != None):
                    filelist.append(filename)
        NCXbuilder(dir,title)
        OPFBuilder(dir,title,filelist)
    sys.exit(0)
