import sys, os
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

import time
import asyncio
import json
import uuid
import random
import base64
import threading as threadinglib
import webbrowser
from collections import OrderedDict

import webview
import requests
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

version = '1.0'
repo = 'R3CI/DiscordReaper'

if sys.platform == 'win32':
    APPDATA = os.path.join(os.getenv('APPDATA', os.path.expanduser('~')), 'DiscordReaper')
elif sys.platform == 'darwin':
    APPDATA = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'DiscordReaper')
else:
    _xdg = os.getenv('XDG_CONFIG_HOME', os.path.join(os.path.expanduser('~'), '.config'))
    APPDATA = os.path.join(_xdg, 'DiscordReaper')
