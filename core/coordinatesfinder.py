#-----------------------------------------------------------
#
# QGIS Quick Finder Plugin
# Copyright (C) 2015 Cedric Christen
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from qgis.core import QgsGeometry

from quickfinder.core.httpfinder import HttpFinder

class CoordinatesFinder(HttpFinder):

    name = 'coordinate'

    def __init__(self, parent):
        HttpFinder.__init__(self, parent)

    def start(self, crd, bbox=None):
        super(CoordinatesFinder, self).start(crd, bbox)

        try:
            x, y = crd.split(',')
            wkt = 'POINT(%s %s)' % (x, y)
            geometry = QgsGeometry.fromWkt(wkt)
            
            self.resultFound.emit(self,
                                        "coordinates",
                                        str(crd),
                                        geometry,
                                        self.parent().iface.mapCanvas().mapRenderer().destinationCrs())
        except:
            pass
        self._finish()
