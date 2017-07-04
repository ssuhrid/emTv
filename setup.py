from distutils.core import setup
import py2exe

import bcrypt
import _cffi_backend

# Mydata_files = [('data', ['data\\control.txt']),('src', ['src\\About.py','src\\Preferences.py'])]
Mydata_files = [('data', ['data\\control.txt','data\\emFooter.jpg','data\\transparent.ico'])]
setup(windows=['emTv.py'],
      data_files = Mydata_files,
      options = {"py2exe": {"unbuffered": True,
                      "optimize": 2}}
)

