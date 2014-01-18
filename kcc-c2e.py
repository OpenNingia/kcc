#!/usr/bin/env python3
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

__version__ = '4.0'
__license__ = 'ISC'
__copyright__ = '2012-2013, Ciro Mattia Gonano <ciromattia@gmail.com>, Pawel Jastrzebski <pawelj@vulturis.eu>'
__docformat__ = 'restructuredtext en'

import sys
if sys.version_info[0] != 3:
    print('ERROR: This is Python 3 script!')
    exit(1)

# Dependiences check
missing = []
try:
    # noinspection PyUnresolvedReferences
    from psutil import TOTAL_PHYMEM, Popen
except ImportError:
    missing.append('psutil')
try:
    # noinspection PyUnresolvedReferences
    from slugify import slugify
except ImportError:
    missing.append('python-slugify')
try:
    # noinspection PyUnresolvedReferences
    from PIL import Image, ImageOps, ImageStat, ImageChops
    if tuple(map(int, ('2.3.0'.split(".")))) > tuple(map(int, (Image.PILLOW_VERSION.split(".")))):
        missing.append('Pillow 2.3.0+')
except ImportError:
    missing.append('Pillow 2.3.0+')
if len(missing) > 0:
    try:
        # noinspection PyUnresolvedReferences
        import tkinter
        # noinspection PyUnresolvedReferences
        import tkinter.messagebox
        importRoot = tkinter.Tk()
        importRoot.withdraw()
        tkinter.messagebox.showerror('KCC - Error', 'ERROR: ' + ', '.join(missing) + ' is not installed!')
    except ImportError:
        print('ERROR: ' + ', '.join(missing) + ' is not installed!')
    exit(1)

from multiprocessing import freeze_support
from kcc.comic2ebook import main, Copyright

if __name__ == "__main__":
    freeze_support()
    Copyright()
    main(sys.argv[1:])
    sys.exit(0)