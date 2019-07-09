# pylint: disable=line-too-long
"""
Python plugin to convert the .sif format into TGS Telegram format
input   : FILE_NAME.sif
output  : FILE_NAME.tgs
"""
import os
import sys
import gzip
import shutil

sys.path.insert(1, os.path.join(sys.path[0], '..', 'lottie-exporter'))

import settings
_temp = __import__('lottie-exporter', globals(), locals(), ['parse'], 0)
parse = _temp.parse


def GenerateSticker(file_name):
    with open(file_name, 'rb') as f_in:
        with gzip.open((file_name.rsplit(".")[0])+".tgs", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


if len(sys.argv) < 2:
    sys.exit()
else:
    settings.init()
    FILE_NAME = sys.argv[1]
    new_file_name = parse(FILE_NAME)
    GenerateSticker(new_file_name)
