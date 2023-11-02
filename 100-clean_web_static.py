#!/usr/bin/python3
"""Define a do_clean function"""
import os
from fabric.api import run
from fabric.api import local
from fabric.api import env
from fabric.api import lcd
from fabric.api import cd

env.hosts = ["100.26.18.88", "54.197.46.69"]


def do_clean(number=0):
    """deletes out-of-date archives"""

    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
