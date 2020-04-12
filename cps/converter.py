# -*- coding: utf-8 -*-

#  This file is part of the Calibre-Web (https://github.com/janeczku/calibre-web)
#    Copyright (C) 2016-2019 Ben Bennett, OzzieIsaacs
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import division, print_function, unicode_literals
import os
import re
from flask_babel import gettext as _

from . import config, logger
from .subproc_wrapper import process_wait


log = logger.create()

# _() necessary to make babel aware of string for translation
_NOT_CONFIGURED = _('not configured')
_NOT_INSTALLED = 'not installed'
_EXECUTION_ERROR = 'Execution permissions missing'


def _get_command_version(path, pattern, argument=None):
    if os.path.exists(path):
        command = [path]
        if argument:
            command.append(argument)
        try:
            for line in process_wait(command):
                if re.search(pattern, line):
                    return line
        except Exception as ex:
            log.warning("%s: %s", path, ex)
            return _EXECUTION_ERROR
    return _NOT_INSTALLED


def get_version():
    version = None
    if config.config_ebookconverter == 1:
        version = _get_command_version(config.config_converterpath, r'Amazon kindlegen\(')
    elif config.config_ebookconverter == 2:
        version = _get_command_version(config.config_converterpath, r'ebook-convert.*\(calibre', '--version')
    return version or _NOT_CONFIGURED
