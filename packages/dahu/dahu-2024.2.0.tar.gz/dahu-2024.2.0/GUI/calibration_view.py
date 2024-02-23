#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Project: Azimuthal integration
#             https://github.com/kif/pyFAI
#
#    Copyright (C) European Synchrotron Radiation Facility, Grenoble, France
#
#    Principal author:       Jérôme Kieffer (Jerome.Kieffer@ESRF.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
pyFAI-calib

A tool for determining the position of a detector using a reference
sample called calibrant using Debye-Scerrer rings.

"""

__author__ = u"Jérôme Kieffer"
__contact__ = "Jerome.Kieffer@ESRF.eu"
__license__ = "GPLv3+"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"
__date__ = "03/09/2014"
__status__ = "development"

from PyQt4.QtGui import  QSizePolicy
import logging
import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy
import os
import pyFAI
from pyFAI.gui_utils import pylab, QtGui, QtCore, uic, matplotlib
import sys
from math import ceil


SIGNAL = pyFAI.gui_utils.QtCore.SIGNAL

logger = logging.getLogger("calibration_view")
from input_view import InputWidget

# for debug
cw = None


class CalibrationWindow(QtGui.QMainWindow):
    """
    Order on the layers in the right tab

    mask > data > massif > solid_angle
    """
    ZORDER = {"contour":5,
              "point": 4,
              "mask": 3,
              "data": 2,
              "massif": 1,
              "solidangle": 0,
              }
    INTERPOLATION = "nearest"
    ORIGIN = "lower"

    def __init__(self,):
        QtGui.QWidget.__init__(self)
        uic.loadUi("calibration_main.ui", self)
        self.connect(self.actionAbout_calibrate, SIGNAL("triggered()"), self.on_about)
        self.dpi = 100
        self.fig = self.canvas = self.mpl_toolbar = self.pix_coords_label = None
        self.axes = None
        # ar is for artists: plot, images or labels...
        self.ar_data = self.ar_mask = self.ar_massif = self.ar_contour = self.ar_solidangle = self.ar_points = None
        self.data = self.massif = self.solid_angle = self.mask = None
        self.display_checks = {}
        self.display_widget = None
        self.input_widget = None
        self.build_right_frame()
        self.build_input_tab()

    def on_about(self):
        msg = [__doc__,
               "",
               "Version date: \t%s" % __date__,
               "PyFAI version: \t%s" % pyFAI.version,
               "FabIO version: \t%s" % fabio.version,
               "Author: \t\t%s" % __author__,
               "Copyright: \t\t%s" % __copyright__,
               "License: \t\t%s" % __license__]
        QtGui.QMessageBox.about(self, "About calibrate", os.linesep.join(msg))

    def build_right_frame(self):
        "build the right frame that contains matplotlib widgets"

        self.fig = Figure(dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.image_frame)

        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.image_frame, coordinates=False)

        self.axes = self.fig.add_subplot(111)
        self.axes.set_visible(False)
        # Bind the 'pick' event for clicking on one of the bars
        self.canvas.mpl_connect('motion_notify_event', self.on_pick)

        self.pix_coords_label = QtGui.QLabel("x= None , y= None , i= None ", self)
        self.mpl_toolbar.addWidget(self.pix_coords_label)

        self.display_widget = uic.loadUi("display_widget.ui")

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.mpl_toolbar, alignment=QtCore.Qt.AlignTop)
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.display_widget, alignment=QtCore.Qt.AlignBottom)
        self.image_frame.setLayout(vbox)

        # Enforce the size Policy of sub-widgets
        pol = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.mpl_toolbar.setSizePolicy(pol)
        self.display_widget.setSizePolicy(pol)
        self.canvas.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

        # few signals about those new widgets:
        self.display_checks = {"data": self.display_widget.show_data,
                               "mask": self.display_widget.show_mask,
                               "massif": self.display_widget.show_massif,
                               "points": self.display_widget.show_points,
                               "contour": self.display_widget.show_contour,
                               "solidangle": self.display_widget.show_solidangle}
        for v in self.display_checks.itervalues():
            self.connect(v, SIGNAL("stateChanged(int)"), self.toggle_show)

    def build_input_tab(self):
        self.input_widget = InputWidget()
        self.scrollArea_input.setWidget(self.input_widget)

#        area->setWidget(widget);
#        box = QtGui.QHBoxLayout()
#        box.addWidget(self.input_widget)
#        self.input_frame.setLayout(box)
#        self.input_widget.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))
#        self.input_frame.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred))


    def on_pick(self, event):
        if event.inaxes and self.data is not None and self.data.any():
            if int(event.xdata) <= self.data.shape[1] and int(event.ydata) <= self.data.shape[0]:
                x = int(round(event.xdata))
                y = int(round(event.ydata))
                i = self.data[y, x]
                self.pix_coords_label.setText("x=%6d, y=%6d, I=%6g" % (x, y, i))
            else:
                self.pix_coords_label.setText("x= None , y= None , I= None ")
        else:
            self.pix_coords_label.setText("x= None , y= None , I= None ")

    def set_data(self, data, display=True, target="data"):
        """
        Display an array in the  data layer
        @param data: the numpy array with the data in it
        @param display: shall the data be displayed
        """
        self.__setattr__(target, data)
        artist = self.__getattribute__("ar_%s" % target)

        if self.axes is None:
            return
        show_data = self.calc_RGBA(data, target)

        if artist is None:
            artist = self.axes.imshow(show_data,
                                      zorder=self.ZORDER[target],
                                      interpolation=self.INTERPOLATION,
                                      origin=self.ORIGIN)
            self.__setattr__("ar_%s" % target, artist)
        else:
            artist.set_data(show_data)
        artist.set_visible(display)
        self.canvas.draw()
        if display:
            self.display_checks[target].setChecked(True)

    def calc_RGBA(self, data, target="data"):
        """
        Apply the colormap depending on the target

        @param data: array of floats
        @return: y,x,4 array of uint8

        TODO: one day, replace with cython implementation
        """
        if target == "mask":
            shape = data.shape
            mask = numpy.ascontiguousarray(data, dtype=bool)
            self.mask = mask
            res = numpy.zeros((shape[0], shape[1], 4), dtype=numpy.uint8)
            res[:, :, 0] = numpy.uint8(255) * mask
            res[:, :, 3] = numpy.uint8(255) * mask
            return res
        elif target == "data":
            npt_hist = 1000      # Number of data point in histogramming
            eps = 1e-3  # fraction to keep out

            if self.mask is not None:
                mask = numpy.ascontiguousarray(self.mask, dtype=bool)
                valid = data[numpy.logical_not(mask)]
                valid_min = valid.min()
                log_data = numpy.log1p(data - valid_min)
                valid = numpy.log1p(valid - valid_min)
            else:
                log_data = numpy.log1p(data - data.min())
                valid = log_data.ravel()

            size = valid.size
            sorted_v = numpy.sort(valid)
            start_idx = int(size * eps)
            end_idx = int(ceil(size * (1.0 - eps)))
            # remove first and last per thousand
            sorted_v = sorted_v[start_idx:end_idx]
            hist = numpy.histogram(sorted_v, npt_hist)[0].cumsum(dtype="float")
            x_range = numpy.linspace(sorted_v[0], sorted_v[-1], npt_hist, endpoint=False)
            eq_data = numpy.interp(log_data, x_range , hist / hist[-1], left=0, right=1)
            return matplotlib.cm.jet(eq_data, bytes=True)
        elif target == "solidangle":
            # should always be between 0 and 1 ...
            dmin = data.min()
            dmax = data.max()
            return matplotlib.cm.jet((data * 1.0 - dmin) / (dmax - dmin), bytes=True)
        elif target == "massif":
            mask = (data != 0)
            show_data = matplotlib.cm.jet(data * 1.0 / data.max(), bytes=True)
            show_data[:, :, 3] = mask * numpy.uint8(255)
            return show_data

    def any_display(self):
        if self.axes is not None:
            display = False
            for v in self.display_checks.values():
                display = display or v.isChecked()
            self.axes.set_visible(display)
            self.canvas.draw()

    def toggle_show(self):
        if self.axes is not None:
            display = False
            for k, v in self.display_checks.iteritems():
                artist = self.__getattribute__("ar_" + k)
                if artist is not None:
                    display_artsist = v.isChecked()
                    artist.set_visible(display_artsist)
                    display = display or display_artsist
            self.axes.set_visible(display)
            self.canvas.draw()


if __name__ == "__main__":
    import fabio
    import pyFAI.massif

    filename = os.path.join(os.environ["HOME"], "workspace", "pyFAI", "test",
                            "testimages", "Pilatus1M.edf")
    app = QtGui.QApplication(sys.argv)
    cw = CalibrationWindow()

    cw.show()
    det = pyFAI.detectors.Pilatus1M()
    cw.set_data(det.mask, target="mask")
    data = fabio.open(filename).data
    cw.set_data(data)
    massif = pyFAI.massif.Massif(data)
    cw.set_data(massif.getLabeledMassif(), target="massif")
    ai = pyFAI.load(filename[:-3] + "poni")
    cw.set_data(ai.solidAngleArray(data.shape), target="solidangle")
    sys.exit(app.exec_())
