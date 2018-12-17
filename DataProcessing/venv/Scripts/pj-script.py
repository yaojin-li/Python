#!E:\ZX_workspace\Python\DataProcessing\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'javascripthon==0.10','console_scripts','pj'
__requires__ = 'javascripthon==0.10'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('javascripthon==0.10', 'console_scripts', 'pj')()
    )
