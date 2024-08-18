# -*- coding: utf-8 -*-

"""Pibooth plugin to display IP addresses at first run"""

import time
import os
import pibooth
import pibooth.booth
from pibooth.utils import LOGGER
from pggallery.pg.pggallery import PgGallery
import pygame
__version__ = "1.0.0"
PLUGIN_NAME="pibooth-gallery"
SECTION = 'Gallery'
GALLERY_DELAY = 'Delay'
GALLERY_DELAY_VAL = '30'
GALLERY_FOLDER = 'Path'
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
            "active": False, #informs other plugins that the gallery is active
            "cfg": {"delay": float(unescape(cfg.get(SECTION, GALLERY_DELAY ))),
                    "folder":fix_abs_path(cfg.get(SECTION, GALLERY_FOLDER ))}
        }    

        
@pibooth.hookimpl
def state_wait_exit(cfg, app, win):
    if hasattr(app,"plugin_gallery"):
        del app.plugin_gallery


def createGallery(surface, app):
     source = None
     url = None
     path = app.plugin_gallery["cfg"]["folder"]
     if path:
        if path[:4].lower() == "http":
               source = PgGallery.SOURCE.URL
        else:
               source = PgGallery.SOURCE.FOLDER
        LOGGER.debug(f"{PLUGIN_NAME} - Creating gallery" )
        gallery = PgGallery(surface, path = path, source = source.value )
        return gallery
     
def closeGallery(app):
    if "gallery" in app.plugin_gallery: #closing the gallery
        del app.plugin_gallery["gallery"]
        app.plugin_gallery["active"] = False
     
@pibooth.hookimpl
def state_wait_do(app, win, events):
    if hasattr(app,"plugin_gallery"):
        if events:
            if (pygame.MOUSEBUTTONDOWN or pygame.USEREVENT+1) in [d.type for d in events]: #mouseclick detection
                app.plugin_gallery["start"] = time.time()
                closeGallery(app)
                return

            if pibooth.booth.BUTTONDOWN  in [d.type for d in events]: #button detection
                app.plugin_gallery["start"] = time.time()
                closeGallery(app)
                return
        else:        
            # no event
            
            now = time.time()
            if ( now - app.plugin_gallery["start"] > app.plugin_gallery["cfg"]["delay"]):
                if not "gallery" in app.plugin_gallery:
                    app.plugin_gallery["gallery"] = createGallery(win.surface, app)
                    app.plugin_gallery["active"] = True
                app.plugin_gallery["gallery"].do()
