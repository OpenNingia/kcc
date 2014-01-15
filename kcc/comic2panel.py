# -*- coding: utf-8 -*-
#
# Copyright (c) 2012-2013 Ciro Mattia Gonano <ciromattia@gmail.com>
# Copyright (c) 2013 Pawel Jastrzebski <pawelj@vulturis.eu>
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
__version__ = '4.0'
__license__ = 'ISC'
__copyright__ = '2012-2013, Ciro Mattia Gonano <ciromattia@gmail.com>, Pawel Jastrzebski <pawelj@vulturis.eu>'
__docformat__ = 'restructuredtext en'

import os
import sys
from shutil import rmtree, copytree, move
from optparse import OptionParser, OptionGroup
from multiprocessing import Pool
try:
    # noinspection PyUnresolvedReferences
    from PIL import Image, ImageStat
    if tuple(map(int, ('2.3.0'.split(".")))) > tuple(map(int, (Image.PILLOW_VERSION.split(".")))):
        print("ERROR: Pillow 2.3.0 or newer is required!")
        if sys.platform.startswith('linux'):
            import tkinter
            import tkinter.messagebox
            importRoot = tkinter.Tk()
            importRoot.withdraw()
            tkinter.messagebox.showerror("KCC - Error", "Pillow 2.3.0 or newer is required!")
        exit(1)
except ImportError:
    print("ERROR: Pillow is not installed!")
    if sys.platform.startswith('linux'):
        import tkinter
        import tkinter.messagebox
        importRoot = tkinter.Tk()
        importRoot.withdraw()
        tkinter.messagebox.showerror("KCC - Error", "Pillow 2.3.0 or newer is required!")
    exit(1)
try:
    from PyQt5 import QtCore
except ImportError:
    QtCore = None


def getImageFileName(imgfile):
    filename = os.path.splitext(imgfile)
    if filename[0].startswith('.') or\
            (filename[1].lower() != '.png' and
             filename[1].lower() != '.jpg' and
             filename[1].lower() != '.gif' and
             filename[1].lower() != '.tif' and
             filename[1].lower() != '.tiff' and
             filename[1].lower() != '.bmp' and
             filename[1].lower() != '.jpeg'):
        return None
    return filename


def walkLevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


def mergeDirectory_tick(output):
    if output:
        mergeWorkerOutput.append(output)
        mergeWorkerPool.terminate()
    if GUI:
        GUI.emit(QtCore.SIGNAL("progressBarTick"))
        if not GUI.conversionAlive:
            mergeWorkerPool.terminate()


def mergeDirectory(work):
    try:
        directory = work[0]
        images = []
        imagesClear = []
        sizes = []
        for root, dirs, files in walkLevel(directory, 0):
            for name in files:
                if getImageFileName(name) is not None:
                    images.append([Image.open(os.path.join(root, name)), os.path.join(root, name)])
        if len(images) > 0:
            for i in images:
                sizes.append(i[0].size[0])
            mw = max(set(sizes), key=sizes.count)
            for i in images:
                if i[0].size[0] == mw:
                    i[0] = i[0].convert('RGB')
                    imagesClear.append(i)
            h = sum(i[0].size[1] for i in imagesClear)
            result = Image.new('RGB', (mw, h))
            y = 0
            for i in imagesClear:
                result.paste(i[0], (0, y))
                y += i[0].size[1]
            for i in imagesClear:
                os.remove(i[1])
            savePath = os.path.split(imagesClear[0][1])
            result.save(os.path.join(savePath[0], os.path.splitext(savePath[1])[0] + '.png'), 'PNG')
    except Exception:
        return str(sys.exc_info()[1])


def sanitizePanelSize(panel, opt):
    newPanels = []
    if panel[2] > 8 * opt.height:
        diff = int(panel[2] / 8)
        newPanels.append([panel[0], panel[1] - diff*7, diff])
        newPanels.append([panel[1] - diff*7, panel[1] - diff*6, diff])
        newPanels.append([panel[1] - diff*6, panel[1] - diff*5, diff])
        newPanels.append([panel[1] - diff*5, panel[1] - diff*4, diff])
        newPanels.append([panel[1] - diff*4, panel[1] - diff*3, diff])
        newPanels.append([panel[1] - diff*3, panel[1] - diff*2, diff])
        newPanels.append([panel[1] - diff*2, panel[1] - diff, diff])
        newPanels.append([panel[1] - diff, panel[1], diff])
    elif panel[2] > 4 * opt.height:
        diff = int(panel[2] / 4)
        newPanels.append([panel[0], panel[1] - diff*3, diff])
        newPanels.append([panel[1] - diff*3, panel[1] - diff*2, diff])
        newPanels.append([panel[1] - diff*2, panel[1] - diff, diff])
        newPanels.append([panel[1] - diff, panel[1], diff])
    elif panel[2] > 2 * opt.height:
        newPanels.append([panel[0], panel[1] - int(panel[2] / 2), int(panel[2] / 2)])
        newPanels.append([panel[1] - int(panel[2] / 2), panel[1], int(panel[2] / 2)])
    else:
        newPanels = [panel]
    return newPanels


def splitImage_tick(output):
    if output:
        splitWorkerOutput.append(output)
        splitWorkerPool.terminate()
    if GUI:
        GUI.emit(QtCore.SIGNAL("progressBarTick"))
        if not GUI.conversionAlive:
            splitWorkerPool.terminate()


#noinspection PyUnboundLocalVariable
def splitImage(work):
    try:
        path = work[0]
        name = work[1]
        opt = work[2]
        # Harcoded opttions
        threshold = 1.0
        delta = 15
        print(".", end=' ')
        fileExpanded = os.path.splitext(name)
        filePath = os.path.join(path, name)
        image = Image.open(filePath)
        image = image.convert('RGB')
        widthImg, heightImg = image.size
        if heightImg > opt.height:
            if opt.debug:
                from PIL import ImageDraw
                debugImage = Image.open(filePath)
                draw = ImageDraw.Draw(debugImage)

            # Find panels
            y1 = 0
            y2 = 15
            panels = []
            while y2 < heightImg:
                while ImageStat.Stat(image.crop([0, y1, widthImg, y2])).var[0] < threshold and y2 < heightImg:
                    y2 += delta
                y2 -= delta
                y1Temp = y2
                y1 = y2 + delta
                y2 = y1 + delta
                while ImageStat.Stat(image.crop([0, y1, widthImg, y2])).var[0] >= threshold and y2 < heightImg:
                    y1 += delta
                    y2 += delta
                if y1 + delta >= heightImg:
                    y1 = heightImg - 1
                y2Temp = y1
                if opt.debug:
                    draw.line([(0, y1Temp), (widthImg, y1Temp)], fill=(0, 255, 0))
                    draw.line([(0, y2Temp), (widthImg, y2Temp)], fill=(255, 0, 0))
                panelHeight = y2Temp - y1Temp
                if panelHeight > delta:
                    # Panels that can't be cut nicely will be forcefully splitted
                    panelsCleaned = sanitizePanelSize([y1Temp, y2Temp, panelHeight], opt)
                    for panel in panelsCleaned:
                        panels.append(panel)
            if opt.debug:
                debugImage.save(os.path.join(path, fileExpanded[0] + '-debug.png'), 'PNG')

            # Create virtual pages
            pages = []
            currentPage = []
            pageLeft = opt.height
            panelNumber = 0
            for panel in panels:
                if pageLeft - panel[2] > 0:
                    pageLeft -= panel[2]
                    currentPage.append(panelNumber)
                    panelNumber += 1
                else:
                    if len(currentPage) > 0:
                        pages.append(currentPage)
                    pageLeft = opt.height - panel[2]
                    currentPage = [panelNumber]
                    panelNumber += 1
            if len(currentPage) > 0:
                pages.append(currentPage)

            # Create pages
            pageNumber = 1
            for page in pages:
                pageHeight = 0
                targetHeight = 0
                for panel in page:
                    pageHeight += panels[panel][2]
                if pageHeight > delta:
                    newPage = Image.new('RGB', (widthImg, pageHeight))
                    for panel in page:
                        panelImg = image.crop([0, panels[panel][0], widthImg, panels[panel][1]])
                        newPage.paste(panelImg, (0, targetHeight))
                        targetHeight += panels[panel][2]
                    newPage.save(os.path.join(path, fileExpanded[0] + '-' +
                                              str(pageNumber) + '.png'), 'PNG')
                    pageNumber += 1
            os.remove(filePath)
    except Exception:
        return str(sys.exc_info()[1])


def Copyright():
    print(('comic2panel v%(__version__)s. Written by Ciro Mattia Gonano and Pawel Jastrzebski.' % globals()))


def main(argv=None, qtGUI=None):
    global options, GUI, splitWorkerPool, splitWorkerOutput, mergeWorkerPool, mergeWorkerOutput
    parser = OptionParser(usage="Usage: %prog [options] comic_folder", add_help_option=False)
    mainOptions = OptionGroup(parser, "MANDATORY")
    otherOptions = OptionGroup(parser, "OTHER")
    mainOptions.add_option("-y", "--height", type="int", dest="height", default=0,
                           help="Height of the target device screen")
    mainOptions.add_option("-i", "--in-place", action="store_true", dest="inPlace", default=False,
                           help="Overwrite source directory")
    mainOptions.add_option("-m", "--merge", action="store_true", dest="merge", default=False,
                           help="Combine every directory into a single image before splitting")
    otherOptions.add_option("-d", "--debug", action="store_true", dest="debug", default=False,
                            help="Create debug file for every splitted image")
    otherOptions.add_option("-h", "--help", action="help",
                            help="Show this help message and exit")
    parser.add_option_group(mainOptions)
    parser.add_option_group(otherOptions)
    options, args = parser.parse_args(argv)
    if qtGUI:
        GUI = qtGUI
    else:
        GUI = None
    if len(args) != 1:
        parser.print_help()
        return
    if options.height > 0:
        options.sourceDir = args[0]
        options.targetDir = args[0] + "-Splitted"
        print("\nSplitting images...")
        if os.path.isdir(options.sourceDir):
            rmtree(options.targetDir, True)
            copytree(options.sourceDir, options.targetDir)
            work = []
            pagenumber = 0
            splitWorkerOutput = []
            splitWorkerPool = Pool()
            if options.merge:
                directoryNumer = 1
                mergeWork = []
                mergeWorkerOutput = []
                mergeWorkerPool = Pool()
                mergeWork.append([options.targetDir])
                for root, dirs, files in os.walk(options.targetDir, False):
                    for directory in dirs:
                        directoryNumer += 1
                        mergeWork.append([os.path.join(root, directory)])
                if GUI:
                    GUI.emit(QtCore.SIGNAL("progressBarTick"), 'status', 'Combining images')
                    GUI.emit(QtCore.SIGNAL("progressBarTick"), directoryNumer)
                for i in mergeWork:
                    mergeWorkerPool.apply_async(func=mergeDirectory, args=(i, ), callback=mergeDirectory_tick)
                mergeWorkerPool.close()
                mergeWorkerPool.join()
                if GUI and not GUI.conversionAlive:
                    rmtree(options.targetDir, True)
                    raise UserWarning("Conversion interrupted.")
                if len(mergeWorkerOutput) > 0:
                    rmtree(options.targetDir, True)
                    raise RuntimeError("One of workers crashed. Cause: " + mergeWorkerOutput[0])
            for root, dirs, files in os.walk(options.targetDir, False):
                for name in files:
                    if getImageFileName(name) is not None:
                        pagenumber += 1
                        work.append([root, name, options])
                    else:
                        os.remove(os.path.join(root, name))
            if GUI:
                GUI.emit(QtCore.SIGNAL("progressBarTick"), 'status', 'Splitting images')
                GUI.emit(QtCore.SIGNAL("progressBarTick"), pagenumber)
                GUI.emit(QtCore.SIGNAL("progressBarTick"))
            if len(work) > 0:
                for i in work:
                    splitWorkerPool.apply_async(func=splitImage, args=(i, ), callback=splitImage_tick)
                splitWorkerPool.close()
                splitWorkerPool.join()
                if GUI and not GUI.conversionAlive:
                    rmtree(options.targetDir, True)
                    raise UserWarning("Conversion interrupted.")
                if len(splitWorkerOutput) > 0:
                    rmtree(options.targetDir, True)
                    raise RuntimeError("One of workers crashed. Cause: " + splitWorkerOutput[0])
                if options.inPlace:
                    rmtree(options.sourceDir)
                    move(options.targetDir, options.sourceDir)
            else:
                rmtree(options.targetDir, True)
                raise UserWarning("Source directory is empty.")
        else:
            raise UserWarning("Provided path is not a directory.")
    else:
        raise UserWarning("Target height is not set.")