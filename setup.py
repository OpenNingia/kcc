#!/usr/bin/env python3
"""
cx_Freeze build script for KCC.

Usage (Mac OS X):
    python setup.py py2app

Usage (Windows/Linux):
    python setup.py build
"""
from sys import platform, version_info
if version_info[0] != 3:
    print('ERROR: This is Python 3 script!')
    exit(1)

NAME = "KindleComicConverter"
VERSION = "4.0"
MAIN = "kcc.py"

if platform == "darwin":
    from setuptools import setup
    extra_options = dict(
        setup_requires=['py2app'],
        app=[MAIN],
        options=dict(
            py2app=dict(
                argv_emulation=True,
                iconfile='icons/comic2ebook.icns',
                includes=['PIL', 'sip', 'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtNetwork', 'PyQt5.QtWidgets',
                          'PyQt5.QtPrintSupport'],
                resources=['LICENSE.txt', 'other/qt.conf', 'other/Additional-LICENSE.txt', 'other/unrar', 'other/7za'],
                plist=dict(
                    CFBundleName=NAME,
                    CFBundleShortVersionString=VERSION,
                    CFBundleGetInfoString=NAME + " " + VERSION +
                    ", written 2012-2013 by Ciro Mattia Gonano and Pawel Jastrzebski",
                    CFBundleExecutable=NAME,
                    CFBundleIdentifier='com.github.ciromattia.kcc',
                    CFBundleSignature='dplt',
                    CFBundleDocumentTypes=[
                        dict(
                            CFBundleTypeExtensions=['cbz', 'cbr', 'cb7', 'zip', 'rar', '7z', 'pdf'],
                            CFBundleTypeName='Comics',
                            CFBundleTypeIconFile='comic2ebook.icns',
                            CFBundleTypeRole='Editor',
                        )
                    ],
                    LSMinimumSystemVersion='10.8.0',
                    LSEnvironment=dict(
                        PATH='/usr/local/bin:/usr/bin:/bin'
                    ),
                    NSHumanReadableCopyright='ISC License (ISCL)'
                )
            )
        )
    )
elif platform == "win32":
    import platform as arch
    from cx_Freeze import setup, Executable
    if arch.architecture()[0] == '64bit':
        library = 'libEGL64.dll'
    else:
        library = 'libEGL32.dll'
    base = "Win32GUI"
    extra_options = dict(
        options={"build_exe": {"optimize": 2,
                               "include_files": ['LICENSE.txt',
                                                 ['other/UnRAR.exe', 'UnRAR.exe'],
                                                 ['other/7za.exe', '7za.exe'],
                                                 ['other/Additional-LICENSE.txt', 'Additional-LICENSE.txt'],
                                                 ['other/' + library, 'libEGL.dll']
                                                 ],
                               "copy_dependent_files": True,
                               "create_shared_zip": False,
                               "append_script_to_exe": True,
                               "excludes": ['tkinter']}},
        executables=[Executable(MAIN,
                                base=base,
                                targetName="KCC.exe",
                                icon="icons/comic2ebook.ico",
                                compress=False)])
else:
    import platform as arch
    import os
    from cx_Freeze import setup, Executable
    if arch.architecture()[0] == '64bit':
        library = 'x86_64'
    else:
        library = 'x86'
    extra_options = dict(
        options={"build_exe": {"optimize": 2,
                               "copy_dependent_files": True,
                               "create_shared_zip": False,
                               "append_script_to_exe": True,
                               "init_script": os.path.join(os.getcwd(), 'other', 'LinuxInit.py'),
                               "excludes": ['tkinter']}},
        executables=[Executable(MAIN,
                                base=None,
                                compress=False)])

#noinspection PyUnboundLocalVariable
setup(
    name=NAME,
    version=VERSION,
    author="Ciro Mattia Gonano, Pawel Jastrzebski",
    author_email="ciromattia@gmail.com, pawelj@vulturis.eu",
    description="A tool to convert comics (CBR/CBZ/PDFs/image folders) to MOBI.",
    license="ISC License (ISCL)",
    keywords="kindle comic mobipocket mobi cbz cbr manga",
    url="http://github.com/ciromattia/kcc",
    packages=['kcc'], requires=['Pillow'],
    **extra_options
)

if platform == "darwin":
    from os import chmod, makedirs
    from shutil import copyfile
    makedirs('dist/' + NAME + '.app/Contents/PlugIns/platforms')
    copyfile('other/libqcocoa.dylib', 'dist/' + NAME + '.app/Contents/PlugIns/platforms/libqcocoa.dylib')
    chmod('dist/' + NAME + '.app/Contents/Resources/unrar', 0o777)
    chmod('dist/' + NAME + '.app/Contents/Resources/7za', 0o777)

if platform == "linux":
    from os import chmod, makedirs, remove
    from shutil import copyfile, copytree
    makedirs('dist/kcc/bin')
    # noinspection PyUnboundLocalVariable
    copyfile('build/exe.linux-' + library + '-3.3/kcc', 'dist/kcc/bin/kcc')
    chmod('dist/kcc/bin/kcc', 0o755)
    # noinspection PyUnboundLocalVariable
    copytree('build/exe.linux-' + library + '-3.3', 'dist/kcc/lib')
    remove('dist/kcc/lib/kcc')
    copyfile('LICENSE.txt', 'dist/kcc/LICENSE.txt')
    copyfile('icons/comic2ebook.png', 'dist/kcc/kcc.png')