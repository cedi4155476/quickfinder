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

from qgis.core import QgsGeometry, QgsPoint
import re

from quickfinder.core.httpfinder import HttpFinder

class CoordinatesFinder(HttpFinder):

    name = 'coordinate'

    def __init__(self, parent):
        HttpFinder.__init__(self, parent)

    def start(self, crd, bbox=None):
        super(CoordinatesFinder, self).start(crd, bbox)

        lvdd = re.match(u'^([0-9]+\\.?[0-9]*)\u00B0?,?[\\s]*([0-9]+\\.?[0-9]*)\u00B0?$', crd)
        dm = re.match(u'^([0-9]+)\u00B0([0-9]+\\.?[0-9]*)[\u2032\u0027\u02BC\u2019]([NnSsEeWw]),?[\\s]*([0-9]+)\u00B0([0-9]+\\.?[0-9]*)[\u2032\u0027\u02BC\u2019]([NnSsEeWw])$', crd)
        dms = re.match(u'^([0-9]+)\u00B0([0-9]+)[\u2032\u0027\u02BC\u2019]([0-9]+\\.?[0-9]*)\u2033([NnSsEeWw]),?[\\s]*([0-9]+)\u00B0([0-9]+)[\u2032\u0027\u02BC\u2019]([0-9]+\\.?[0-9]*)\u2033([NnSsEeWw])$', crd)

        if lvdd:
            long = float(lvdd.group(1))
            lat = float(lvdd.group(2))
            if (long >= -180 and long <= 180) and (lat >= -90 and lat <= 90):
                crs = 4326
            elif (long >= 470000 and long <= 850000) and (lat >= 60000 and lat <= 310000):
                crs = 21781
            elif (long >= 2450000 and long <= 2850000) and (lat >= 1050000 and lat <= 1300000):
                crs = 2056
            geometry = QgsGeometry.fromPoint(QgsPoint(long,  lat))
            self.resultFound.emit(self,
                                        "coordinates",
                                        crd,
                                        geometry,
                                        crs)
        elif dm:
            if (re.match('^[NnSs]$', dm.group(3)) and re.match('^[EeWw]$', dm.group(6))) or (re.match('^[EeWw]$', dm.group(3)) and re.match('^[NnSs]$', dm.group(6))):
                if re.match('^[NnSs]$', dm.group(3)):
                    #latitude
                    latd = float(dm.group(1))
                    latm = float(dm.group(2))
                    
                    #longitude
                    longd = float(dm.group(4))
                    longm = float(dm.group(5))
                else:
                    #longitude
                    longd = float(dm.group(1))
                    longm = float(dm.group(2))
                    
                    #latitude
                    latd = float(dm.group(4))
                    latm = float(dm.group(5))
                long = longd + 1./60. * longm
                lat = latd + 1./60. * latm
                geometry = QgsGeometry.fromPoint(QgsPoint(long,  lat))
                crs = 4326
                self.resultFound.emit(self,
                                        "coordinates",
                                        crd,
                                        geometry,
                                        crs)
        elif dms:
            if (re.match('^[NnSs]$', dms.group(4)) and re.match('^[EeWw]$', dms.group(8))) or (re.match('^[EeWw]$', dms.group(4)) and re.match('^[NnSs]$', dms.group(8))):
                if re.match('^[NnSs]$', dms.group(4)):
                    #latitude
                    latd = float(dms.group(1))
                    latm = float(dms.group(2))
                    lats = float(dms.group(3))
                    
                    #longitude
                    longd = float(dms.group(5))
                    longm = float(dms.group(6))
                    longs = float(dms.group(7))
                else:
                    #longitude
                    longd = float(dms.group(1))
                    longm = float(dms.group(2))
                    longs = float(dms.group(3))
                    
                    #latitude
                    latd = float(dms.group(5))
                    latm = float(dms.group(6))
                    lats = float(dms.group(7))
                long = longd + 1./60. * (longm + 1./60. * longs)
                lat = latd + 1./60. * (latm + 1./60. * lats)
                geometry = QgsGeometry.fromPoint(QgsPoint(long,  lat))
                crs = 4326
                self.resultFound.emit(self,
                                        "coordinates",
                                        crd,
                                        geometry,
                                        crs)
        self._finish()
