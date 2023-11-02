#!/usr/bin/python3
"""Defines a do_pack function"""
import os
import datetime
from fabric.api import local


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    if not os.path.exists("versions"):
        os.makedirs("versions")
    date = datetime.datetime.now()
    tgz_file_path = "versions/web_static_{}{}{}{}{}{}.tgz".format(
            date.year,
            date.month,
            date.day,
            date.hour,
            date.minute,
            date.second
            )
    result = local("tar -cvzf {} web_static".format(tgz_file_path))
    if result.failed:
        return None
    return tgz_file_path
