#-*- coding:utf-8 -*-

from distutils.core import setup
from glob import glob

setup(name = "hosttweak",
    version = "0.1",
    author = "thebye85",
    author_email = "thebye85@gmail.com",
    packages = ["hosttweak"],
    #data_files=[('share/webpad/pixmaps', glob("pixmaps/*"), ('share/webpad/templates', ['templates/webpad.tpl'])],
    scripts = ["main.py", "host_tweak_ui.py", "host_tweak_handler.py", "host_config.py", "encrypt_util.py"]
)