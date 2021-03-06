#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Creates an archive of a BOSS release, putting it in the 'build' folder.

# Files and folders that need to go in (relative to repository root):
#
# build/BOSS.exe
# resources/l10n/es/LC_MESSAGES/boss.mo
# resources/l10n/es/LC_MESSAGES/wxstd.mo
# resources/l10n/ru/LC_MESSAGES/boss.mo
# resources/l10n/ru/LC_MESSAGES/wxstd.mo
# resources/l10n/fr/LC_MESSAGES/boss.mo
# resources/l10n/fr/LC_MESSAGES/wxstd.mo
# resources/l10n/zh/LC_MESSAGES/boss.mo
# resources/l10n/zh/LC_MESSAGES/wxstd.mo
# resources/l10n/pl/LC_MESSAGES/boss.mo
# resources/l10n/pl/LC_MESSAGES/wxstd.mo
# resources/polyfill.js
# resources/script.js
# resources/style.css
# docs/images
# docs/licenses
# docs/BOSS Metadata Syntax.html
# docs/BOSS Readme.html

#   BOSS
#
#   A plugin load order optimiser for games that use the esp/esm plugin system.
#
#   Copyright (C) 2013-2014    WrinklyNinja
#
#   This file is part of BOSS.
#
#   BOSS is free software: you can redistribute
#   it and/or modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation, either version 3 of
#   the License, or (at your option) any later version.
#
#   BOSS is distributed in the hope that it will
#   be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with BOSS.  If not, see
#   <http://www.gnu.org/licenses/>.

import sys
import os
import shutil
import zipfile

temp_path = os.path.join('..', 'build', 'archive.tmp')
archive_name = 'BOSS Archive.zip'

# Set archive name if alternative is given.
if (len(sys.argv) > 1):
    archive_name = sys.argv[1]

# First make sure that the temporary folder for the archive exists.
if not os.path.exists(temp_path):
    os.makedirs(temp_path)

# Now copy everything into the temporary folder.
shutil.copy( os.path.join('..', 'build', 'BOSS.exe'), temp_path )

for lang in ['es', 'ru', 'fr', 'zh', 'pl']:
    os.makedirs(os.path.join(temp_path, 'resources', 'l10n', lang, 'LC_MESSAGES'))
    shutil.copy( os.path.join('..', 'resources', 'l10n', lang, 'LC_MESSAGES', 'boss.mo'), os.path.join(temp_path, 'resources', 'l10n', lang, 'LC_MESSAGES') )
    shutil.copy( os.path.join('..', 'resources', 'l10n', lang, 'LC_MESSAGES', 'wxstd.mo'), os.path.join(temp_path, 'resources', 'l10n', lang, 'LC_MESSAGES') )


shutil.copy( os.path.join('..', 'resources', 'polyfill.js'), os.path.join(temp_path, 'resources') )
shutil.copy( os.path.join('..', 'resources', 'script.js'), os.path.join(temp_path, 'resources') )
shutil.copy( os.path.join('..', 'resources', 'style.css'), os.path.join(temp_path, 'resources') )

shutil.copytree( os.path.join('..', 'docs', 'images'), os.path.join(temp_path, 'docs', 'images') )
shutil.copytree( os.path.join('..', 'docs', 'licenses'), os.path.join(temp_path, 'docs', 'licenses') )
shutil.copy( os.path.join('..', 'docs', 'BOSS Metadata Syntax.html'), os.path.join(temp_path, 'docs') )
shutil.copy( os.path.join('..', 'docs', 'BOSS Readme.html'), os.path.join(temp_path, 'docs') )


# Now compress the temporary folder. (Creating a zip because I can't get pylzma to work...)
os.chdir(temp_path)
zip = zipfile.ZipFile( os.path.join('..', archive_name), 'w', zipfile.ZIP_DEFLATED )
for root, dirs, files in os.walk('.'):
    for file in files:
        zip.write(os.path.join(root, file))
zip.close()
os.chdir('..')


# And finally, delete the temporary folder.
shutil.rmtree('archive.tmp')
