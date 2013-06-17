#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2013 Ciro Mattia Gonano <ciromattia@gmail.com>
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

__version__ = '3.0'
__license__ = 'ISC'
__copyright__ = '2012-2013, Ciro Mattia Gonano <ciromattia@gmail.com>, Pawel Jastrzebski <pawelj@vulturis.eu>'
__docformat__ = 'restructuredtext en'

import os
import sys
import shutil
import traceback
import urllib2
import comic2ebook
import kindlestrip
from image import ProfileData
from subprocess import call, STDOUT, PIPE
from PyQt4 import QtGui, QtCore
from xml.dom.minidom import parse


class Icons:
    def __init__(self):
        self.deviceKindle = QtGui.QIcon()
        self.deviceKindle.addPixmap(QtGui.QPixmap(":/Devices/icons/Kindle.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.MOBIFormat = QtGui.QIcon()
        self.MOBIFormat.addPixmap(QtGui.QPixmap(":/Formats/icons/MOBI.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CBZFormat = QtGui.QIcon()
        self.CBZFormat.addPixmap(QtGui.QPixmap(":/Formats/icons/CBZ.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.EPUBFormat = QtGui.QIcon()
        self.EPUBFormat.addPixmap(QtGui.QPixmap(":/Formats/icons/EPUB.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.info = QtGui.QIcon()
        self.info.addPixmap(QtGui.QPixmap(":/Status/icons/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.warning = QtGui.QIcon()
        self.warning.addPixmap(QtGui.QPixmap(":/Status/icons/warning.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.error = QtGui.QIcon()
        self.error.addPixmap(QtGui.QPixmap(":/Status/icons/error.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)


# noinspection PyBroadException
class VersionThread(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent

    def __del__(self):
        self.wait()

    def run(self):
        try:
            XML = urllib2.urlopen('http://kcc.vulturis.eu/Version.php')
            XML = parse(XML)
        except Exception:
            return
        latestVersion = XML.childNodes[0].getElementsByTagName('latest')[0].childNodes[0].toxml()
        if latestVersion != __version__:
            self.emit(QtCore.SIGNAL("addMessage"), 'New version is available!', 'warning')


# noinspection PyBroadException
class WorkerThread(QtCore.QThread):
    def __init__(self, parent):
        QtCore.QThread.__init__(self)
        self.parent = parent

    def __del__(self):
        self.wait()

    def run(self):
        self.emit(QtCore.SIGNAL("modeConvert"), False)
        profile = ProfileData.ProfileLabels[str(GUI.DeviceBox.currentText())]
        argv = ["--profile=" + profile]
        currentJobs = []
        if GUI.MangaBox.isChecked():
            argv.append("--manga-style")
        if GUI.RotateBox.isChecked():
            argv.append("--rotate")
        if not GUI.HQPVBox.isChecked():
            argv.append("--nopanelviewhq")
        if GUI.ProcessingBox.isChecked():
            argv.append("--noprocessing")
        if GUI.UpscaleBox.isChecked() and not GUI.StretchBox.isChecked():
            argv.append("--upscale")
        if GUI.NoRotateBox.isChecked():
            argv.append("--nosplitrotate")
        if GUI.BorderBox.isChecked():
            argv.append("--blackborders")
        if GUI.StretchBox.isChecked():
            argv.append("--stretch")
        if GUI.NoDitheringBox.isChecked():
            argv.append("--nodithering")
        if self.parent.GammaValue > 0.09:
            argv.append("--gamma=" + self.parent.GammaValue)
        if str(GUI.FormatBox.currentText()) == 'CBZ':
            argv.append("--cbz-output")
        if str(GUI.customWidth.text()) != '':
            argv.append("--customwidth=" + str(GUI.customWidth.text()))
        if str(GUI.customHeight.text()) != '':
            argv.append("--customheight=" + str(GUI.customHeight.text()))
        if GUI.ColorBox.isChecked():
            argv.append("--forcecolor")
        for i in range(GUI.JobList.count()):
            currentJobs.append(str(GUI.JobList.item(i).text()))
        GUI.JobList.clear()
        for job in currentJobs:
            self.errors = False
            self.emit(QtCore.SIGNAL("addMessage"), 'Source: ' + job, 'info')
            if str(GUI.FormatBox.currentText()) == 'CBZ':
                self.emit(QtCore.SIGNAL("addMessage"), 'Creating CBZ file...', 'info')
            else:
                self.emit(QtCore.SIGNAL("addMessage"), 'Creating EPUB file...', 'info')
            jobargv = list(argv)
            jobargv.append(job)
            try:
                outputPath = comic2ebook.main(jobargv, self)
                self.emit(QtCore.SIGNAL("hideProgressBar"))
            except Exception as err:
                self.errors = True
                type_, value_, traceback_ = sys.exc_info()
                QtGui.QMessageBox.critical(MainWindow, 'KCC Error',
                                           "Error on file %s:\n%s\nTraceback:\n%s"
                                           % (jobargv[-1], str(err), traceback.format_tb(traceback_)),
                                           QtGui.QMessageBox.Ok)
                self.emit(QtCore.SIGNAL("addMessage"), 'KCC failed to create EPUB!', 'error')
            if not self.errors:
                if str(GUI.FormatBox.currentText()) == 'CBZ':
                    self.emit(QtCore.SIGNAL("addMessage"), 'Creating CBZ file... Done!', 'info', True)
                else:
                    self.emit(QtCore.SIGNAL("addMessage"), 'Creating EPUB file... Done!', 'info', True)
                if str(GUI.FormatBox.currentText()) == 'MOBI':
                    if not os.path.getsize(outputPath) > 314572800:
                        self.emit(QtCore.SIGNAL("addMessage"), 'Creating MOBI file...', 'info')
                        self.emit(QtCore.SIGNAL("progressBarTick"), 1)
                        try:
                            retcode = call('kindlegen "' + outputPath + '"', shell=True)
                        except:
                            continue
                        self.emit(QtCore.SIGNAL("hideProgressBar"))
                        if retcode == 0:
                            self.emit(QtCore.SIGNAL("addMessage"), 'Creating MOBI file... Done!', 'info', True)
                            self.emit(QtCore.SIGNAL("addMessage"), 'Removing SRCS header...', 'info')
                            os.remove(outputPath)
                            mobiPath = outputPath.replace('.epub', '.mobi')
                            shutil.move(mobiPath, mobiPath + '_tostrip')
                            try:
                                kindlestrip.main((mobiPath + '_tostrip', mobiPath))
                            except Exception:
                                self.errors = True
                            if not self.errors:
                                os.remove(mobiPath + '_tostrip')
                                self.emit(QtCore.SIGNAL("addMessage"), 'Removing SRCS header... Done!', 'info', True)
                            else:
                                shutil.move(mobiPath + '_tostrip', mobiPath)
                                self.emit(QtCore.SIGNAL("addMessage"),
                                          'KindleStrip failed to remove SRCS header!', 'warning')
                                self.emit(QtCore.SIGNAL("addMessage"),
                                          'MOBI file will work correctly but it will be highly oversized.', 'warning')
                        else:
                            os.remove(outputPath)
                            os.remove(outputPath.replace('.epub', '.mobi'))
                            self.emit(QtCore.SIGNAL("addMessage"), 'KindleGen failed to create MOBI!', 'error')
                            self.emit(QtCore.SIGNAL("addMessage"), 'Try converting a bit smaller batch.', 'error')
                    else:
                        excess = (os.path.getsize(outputPath) - 314572800)/1024/1024
                        os.remove(outputPath)
                        self.emit(QtCore.SIGNAL("addMessage"), 'Created EPUB file is too big for KindleGen!', 'error')
                        self.emit(QtCore.SIGNAL("addMessage"), 'Limit exceeded by ' + str(excess) +
                                                               ' MB. Try converting smaller batch.', 'error')
        self.parent.needClean = True
        self.emit(QtCore.SIGNAL("addMessage"), 'All jobs completed.', 'info')
        self.emit(QtCore.SIGNAL("modeConvert"), True)


# noinspection PyBroadException
class Ui_KCC(object):
    def selectDir(self):
        # Dialog allow to select multiple directories but we can't parse that. QT Bug.
        if self.needClean:
            self.needClean = False
            GUI.JobList.clear()
        dname = QtGui.QFileDialog.getExistingDirectory(MainWindow, 'Select directory', self.lastPath)
        # Lame UTF-8 security measure
        try:
            str(dname)
        except Exception:
            QtGui.QMessageBox.critical(MainWindow, 'KCC Error', "Path cannot contain non-ASCII characters.",
                                       QtGui.QMessageBox.Ok)
            return
        self.lastPath = os.path.abspath(os.path.join(str(dname), os.pardir))
        GUI.JobList.addItem(dname)
        self.clearEmptyJobs()

    def selectFile(self):
        if self.needClean:
            self.needClean = False
            GUI.JobList.clear()
        if self.UnRAR:
            fname = QtGui.QFileDialog.getOpenFileName(MainWindow, 'Select file', self.lastPath,
                                                      '*.cbz *.cbr *.zip *.rar *.pdf')
        else:
            fname = QtGui.QFileDialog.getOpenFileName(MainWindow, 'Select file', self.lastPath,
                                                      '*.cbz *.zip *.pdf')
        # Lame UTF-8 security measure
        try:
            str(fname)
        except Exception:
            QtGui.QMessageBox.critical(MainWindow, 'KCC Error', "Path cannot contain non-ASCII characters.",
                                       QtGui.QMessageBox.Ok)
            return
        self.lastPath = os.path.abspath(os.path.join(str(fname), os.pardir))
        GUI.JobList.addItem(fname)
        self.clearEmptyJobs()

    def clearJobs(self):
        GUI.JobList.clear()

    def clearEmptyJobs(self):
        # Sometimes empty records appear. Dirty workaround.
        for i in range(GUI.JobList.count()):
            if str(GUI.JobList.item(i).text()) == '':
                GUI.JobList.takeItem(i)
        GUI.JobList.scrollToBottom()

    def modeBasic(self):
        self.currentMode = 1
        MainWindow.setMinimumSize(QtCore.QSize(420, 270))
        MainWindow.setMaximumSize(QtCore.QSize(420, 270))
        MainWindow.resize(420, 270)
        GUI.BasicModeButton.setStyleSheet('font-weight:Bold;')
        GUI.AdvModeButton.setStyleSheet('font-weight:Normal;')
        GUI.ExpertModeButton.setStyleSheet('font-weight:Normal;')
        GUI.FormatBox.setCurrentIndex(0)
        GUI.FormatBox.setEnabled(False)
        GUI.OptionsAdvanced.setEnabled(False)
        GUI.OptionsAdvancedGamma.setEnabled(False)
        GUI.OptionsExpert.setEnabled(False)
        GUI.ProcessingBox.hide()
        GUI.UpscaleBox.hide()
        GUI.NoRotateBox.hide()
        GUI.ProcessingBox.setChecked(False)
        GUI.UpscaleBox.setChecked(False)
        GUI.NoRotateBox.setChecked(False)
        GUI.BorderBox.setChecked(False)
        GUI.StretchBox.setChecked(False)
        GUI.NoDitheringBox.setChecked(False)
        GUI.GammaSlider.setValue(0)
        GUI.customWidth.setText('')
        GUI.customHeight.setText('')
        GUI.ColorBox.setChecked(False)

    def modeAdvanced(self):
        self.currentMode = 2
        MainWindow.setMinimumSize(QtCore.QSize(420, 345))
        MainWindow.setMaximumSize(QtCore.QSize(420, 345))
        MainWindow.resize(420, 345)
        GUI.BasicModeButton.setStyleSheet('font-weight:Normal;')
        GUI.AdvModeButton.setStyleSheet('font-weight:Bold;')
        GUI.ExpertModeButton.setStyleSheet('font-weight:Normal;')
        GUI.FormatBox.setEnabled(True)
        GUI.ProcessingBox.show()
        GUI.UpscaleBox.show()
        GUI.NoRotateBox.show()
        GUI.OptionsAdvancedGamma.setEnabled(True)
        GUI.OptionsAdvanced.setEnabled(True)
        GUI.OptionsExpert.setEnabled(False)
        GUI.customWidth.setText('')
        GUI.customHeight.setText('')
        GUI.ColorBox.setChecked(False)

    def modeExpert(self):
        self.currentMode = 3
        MainWindow.setMinimumSize(QtCore.QSize(420, 380))
        MainWindow.setMaximumSize(QtCore.QSize(420, 380))
        MainWindow.resize(420, 380)
        GUI.BasicModeButton.setStyleSheet('font-weight:Normal;')
        GUI.AdvModeButton.setStyleSheet('font-weight:Normal;')
        GUI.ExpertModeButton.setStyleSheet('font-weight:Bold;')
        GUI.FormatBox.setEnabled(True)
        GUI.ProcessingBox.show()
        GUI.UpscaleBox.show()
        GUI.NoRotateBox.show()
        GUI.OptionsAdvancedGamma.setEnabled(True)
        GUI.OptionsAdvanced.setEnabled(True)
        GUI.OptionsExpert.setEnabled(True)

    def modeConvert(self, enable):
        GUI.BasicModeButton.setEnabled(enable)
        GUI.AdvModeButton.setEnabled(enable)
        GUI.ExpertModeButton.setEnabled(enable)
        GUI.DirectoryButton.setEnabled(enable)
        GUI.ClearButton.setEnabled(enable)
        GUI.FileButton.setEnabled(enable)
        GUI.DeviceBox.setEnabled(enable)
        GUI.ConvertButton.setEnabled(enable)
        GUI.FormatBox.setEnabled(enable)
        GUI.OptionsBasic.setEnabled(enable)
        GUI.OptionsAdvanced.setEnabled(enable)
        GUI.OptionsAdvancedGamma.setEnabled(enable)
        GUI.OptionsExpert.setEnabled(enable)
        if enable:
            if self.currentMode == 1:
                self.modeBasic()
            elif self.currentMode == 2:
                self.modeAdvanced()
            elif self.currentMode == 3:
                self.modeExpert()

    def changeGamma(self, value):
        if value <= 9:
            value = 'Auto'
        else:
            value = float(value)
            value = '%.2f' % (value/100)
            self.GammaValue = value
        GUI.GammaLabel.setText('Gamma: ' + str(value))

    def addMessage(self, message, icon=None, replace=False):
        if icon:
            icon = eval('self.icons.' + icon)
            item = QtGui.QListWidgetItem(icon, message)
        else:
            item = QtGui.QListWidgetItem(message)
        if replace:
            GUI.JobList.takeItem(GUI.JobList.count()-1)
        GUI.JobList.addItem(item)
        GUI.JobList.scrollToBottom()

    def updateProgressbar(self, new=False, status=False):
        if new == "status":
            pass
            GUI.ProgressBar.setFormat(status)
        elif new:
            GUI.ProgressBar.setMaximum(new - 1)
            GUI.ProgressBar.reset()
            GUI.ProgressBar.show()
        else:
            GUI.ProgressBar.setValue(GUI.ProgressBar.value() + 1)

    def convertStart(self):
        if self.needClean:
            self.needClean = False
            GUI.JobList.clear()
        if GUI.JobList.count() == 0:
            self.addMessage('No files selected! Please choose files to convert.', 'error')
            self.needClean = True
            return
        self.worker.start()

    def hideProgressBar(self):
        GUI.ProgressBar.hide()

    # noinspection PyUnusedLocal
    def saveSettings(self, event):
        self.settings.setValue('lastPath', self.lastPath)
        self.settings.setValue('lastDevice', GUI.DeviceBox.currentIndex())
        self.settings.sync()

    def __init__(self, UI, KCC):
        global GUI, MainWindow
        GUI = UI
        MainWindow = KCC
        profiles = sorted(ProfileData.ProfileLabels.iterkeys())
        self.icons = Icons()
        self.settings = QtCore.QSettings('KindleComicConverter', 'KindleComicConverter')
        self.lastPath = self.settings.value('lastPath', '', type=str)
        self.lastDevice = self.settings.value('lastDevice', 10, type=int)
        self.worker = WorkerThread(self)
        self.versionCheck = VersionThread(self)
        self.needClean = True
        self.GammaValue = 0

        self.addMessage('Welcome!', 'info')
        self.addMessage('Remember: All options have additional informations in tooltips.', 'info')
        if call('kindlegen', stdout=PIPE, stderr=STDOUT, shell=True) == 0:
            self.KindleGen = True
            formats = ['MOBI', 'EPUB', 'CBZ']
        else:
            self.KindleGen = False
            formats = ['EPUB', 'CBZ']
            self.addMessage('Not found KindleGen! Creating MOBI files is disabled.', 'warning')
        if call('unrar', stdout=PIPE, stderr=STDOUT, shell=True) == 0:
            self.UnRAR = True
        else:
            self.UnRAR = False
            self.addMessage('Not found UnRAR! Processing of CBR/RAR files is disabled.', 'warning')

        GUI.BasicModeButton.clicked.connect(self.modeBasic)
        GUI.AdvModeButton.clicked.connect(self.modeAdvanced)
        GUI.ExpertModeButton.clicked.connect(self.modeExpert)
        GUI.DirectoryButton.clicked.connect(self.selectDir)
        GUI.ClearButton.clicked.connect(self.clearJobs)
        GUI.FileButton.clicked.connect(self.selectFile)
        GUI.ConvertButton.clicked.connect(self.convertStart)
        GUI.GammaSlider.valueChanged.connect(self.changeGamma)
        KCC.connect(self.worker, QtCore.SIGNAL("progressBarTick"), self.updateProgressbar)
        KCC.connect(self.worker, QtCore.SIGNAL("modeConvert"), self.modeConvert)
        KCC.connect(self.worker, QtCore.SIGNAL("addMessage"), self.addMessage)
        KCC.connect(self.worker, QtCore.SIGNAL("hideProgressBar"), self.hideProgressBar)
        KCC.connect(self.versionCheck, QtCore.SIGNAL("addMessage"), self.addMessage)
        KCC.closeEvent = self.saveSettings

        for profile in profiles:
            GUI.DeviceBox.addItem(self.icons.deviceKindle, profile)
        GUI.DeviceBox.setCurrentIndex(self.lastDevice)
        for f in formats:
            GUI.FormatBox.addItem(eval('self.icons.' + f + 'Format'), f)
        GUI.FormatBox.setCurrentIndex(0)

        self.modeBasic()
        self.versionCheck.start()
        self.hideProgressBar()
