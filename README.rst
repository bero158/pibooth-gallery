
==============
pibooth-gallery
==============

|PythonVersions|

``pibooth-gallery`` is a plugin for the `pibooth`_ application.

This plugin shows in random order already taken photos at the first (waiting) screen after defined delay.
The gallery is closed when the waiting screen exits or the screen is clicked (touched)

Install
-------

The plugin doesn't require additional modules.
Upload the plugin somewhere and appent the absolute path to your pibooth.cfg (~/.config/pigooth/pibooth.cfg) to parameter 'plugins'
aka: plugins = "/home/pi/pibooth/pibooth-myip/pibooth_myip.py"

Configuration
-------------

Configure the initial delay and path to your gallery in case it's not the photobooth default folder.

Example
-------


.. --- Links ------------------------------------------------------------------

.. _`pibooth`: https://pypi.org/project/pibooth

.. |PythonVersions| image:: https://img.shields.io/badge/python-3.6+-red.svg
   :target: https://www.python.org/downloads
   :alt: Python 3.6+
