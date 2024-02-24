"""
    Copyright 2022 bitValence, Inc.
    All Rights Reserved.

    This program is free software; you can modify and/or redistribute it
    under the terms of the GNU Affero General Public License
    as published by the Free Software Foundation; version 3 with
    attribution addendums as found in the LICENSE.txt.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    Purpose:
        Module initialization file

"""
import sys
sys.path.append("..")

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from .appcodetutorial import ManageCodeTutorials
from .appstore import AppStore, AppSpec, ManageUsrApps
from .apptemplate import CreateApp
from .eds import CfeTopicIds, AppEds
from .jsonfile import JsonTblTopicMap
from .pdfviewer import PdfViewer
from .tutorial import ManageTutorials
from .texteditor import TextEditor
from .utils import *

