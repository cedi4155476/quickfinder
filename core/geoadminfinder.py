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

class GeoAdminFinder(HttpFinder):

    name = 'geoadmin'

    def __init__(self, parent):
        HttpFinder.__init__(self, parent)

    def start(self, toFind, bbox=None):
        super(GeoAdminFinder, self).start(toFind, bbox)

        url = self.settings.value('geoadminUrl')
        header = self.settings.value('geoadminReferer')

        params = {
            'type'            : 'locations',
            'searchText'        : toFind, 
            'limit'        : str(self.settings.value('totalLimit'))
        }
        if header:
            header =  {'Referer' :  header}
        else:
            header = {}
        self._sendRequest(url, params, header)

    def loadData(self, data):
        for result in data['results']:
            if not self.settings.value('geoadminReferer') and result['attrs']['origin'] == 'address':
                continue
            attrs = result['attrs']
            label = attrs['label']
            label = label.replace('<b>', '').replace('</b>', '')
            try:
                wkt = 'POINT(%s %s)' % (attrs['lon'], attrs['lat'])
                geometry = QgsGeometry.fromWkt(wkt)
            except KeyError:
                geometry = QgsGeometry()
            self.resultFound.emit(self,
                                    attrs['origin'],
                                    label,
                                    geometry,
                                    4326)
        self._finish()
