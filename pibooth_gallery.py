# -*- coding: utf-8 -*-

"""Pibooth plugin to display IP addresses at first run"""

import time
import os
import pibooth
from pibooth.utils import LOGGER
from pggallery.pggallery import PgGallery
import pygame

__version__ = "1.0.0"
PLUGIN_NAME="pibooth-gallery"
SECTION = 'Gallery'
GALLERY_DELAY = 'Delay'
GALLERY_DELAY_VAL = '30'
GALLERY_FOLDER = 'Folder'
GALLERY_FOLDER_VAL = '~/Pictures/pibooth'

def unescape(text):
    if (len(text)>1):
        if (text[0] == '"' and text[-1] == '"'):
            text = text[1:][:-1]
    return text

def fix_path(path):
    if (not path):
        return path
    return unescape(path)

def fix_abs_path(path):
    path = fix_path(path)
    if (path):
        path = os.path.expanduser(path)
    return path

# --- Pibooth state-independent hooks ------------------------------------------

@pibooth.hookimpl
def pibooth_configure(cfg):
    """Actions performed after loading of the configuration file or when the
    plugin is enabled for the first time. The ``cfg`` object is an instance
    of :py:class:`ConfigParser` class.

    :param cfg: application configuration
    """
    """Declare the new configuration options"""
    cfg.add_option(SECTION, GALLERY_DELAY , GALLERY_DELAY_VAL ,
                   "Delay is seconds before gallery starts",
                   GALLERY_DELAY , GALLERY_DELAY_VAL )
    cfg.add_option(SECTION, GALLERY_FOLDER , GALLERY_FOLDER_VAL ,
                   "Folder with photos",
                   GALLERY_FOLDER , GALLERY_FOLDER_VAL )
    
    LOGGER.debug(f"{PLUGIN_NAME} - Configure options added" )



@pibooth.hookimpl
def pibooth_startup(cfg):
    LOGGER.info(f"{PLUGIN_NAME} - Hello from {PLUGIN_NAME} plugin")


@pibooth.hookimpl
def state_wait_enter(cfg, app, win):
    if not hasattr(app,"plugin_gallery"):
        app.plugin_gallery = {
            "start": time.time(),
            "active": False,
            "cfg": {"delay": float(cfg.get(SECTION, GALLERY_DELAY )),
                    "folder":fix_abs_path(cfg.get(SECTION, GALLERY_FOLDER ))}
        }    

        
@pibooth.hookimpl
def state_wait_exit(cfg, app, win):
    if hasattr(app,"plugin_gallery"):
        del app.plugin_gallery

@pibooth.hookimpl
def state_wait_do(app, win, events):
    if hasattr(app,"plugin_gallery"):
        now = time.time()
        if pygame.MOUSEBUTTONDOWN in [d.type for d in events]: #mouseclick
                app.plugin_gallery["start"] = now
                if "gallery" in app.plugin_gallery:
                    del app.plugin_gallery["gallery"]
                    app.plugin_gallery["active"] = False
                return

        if ( now - app.plugin_gallery["start"] > app.plugin_gallery["cfg"]["delay"]):
            if not "gallery" in app.plugin_gallery:
                LOGGER.debug(f"{PLUGIN_NAME} - Starting gallery" )
                app.plugin_gallery["gallery"] = PgGallery(win.surface, app.plugin_gallery["cfg"]["folder"] )
                app.plugin_gallery["active"] = True
            app.plugin_gallery["gallery"].do()
    