#!/usr/bin/env python
#--------------------------------------------------------------------------
#                           SoftGNSS v3.0
#
# Copyright (C) Darius Plausinaitis and Dennis M. Akos
# Written by Darius Plausinaitis and Dennis M. Akos
# Converted to Python by Colin Beighley
#--------------------------------------------------------------------------
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
#USA.
#--------------------------------------------------------------------------
import sys
sys.path.append("..")

import initSettings
import argparse
import pylab
import math
import numpy
import matplotlib
import get_samples

def probeData(settings):
  samplesPerCode = int(round(settings.samplingFreq / (settings.codeFreqBasis / settings.codeLength)))

  samples = get_samples.int8(settings.fileName,10*samplesPerCode,settings.skipNumberOfBytes)

  #Initialize figure
  fig = pylab.figure()
  pylab.clf()

  #X axis
  timeScale = [x*(1/settings.samplingFreq) for x in \
               range(0,int(round((5e-3 + 1/settings.samplingFreq)*settings.samplingFreq)))]
  #Time domain plot
  pylab.subplot(2,2,1)
  plot_max = int(round(samplesPerCode/50))
  pylab.plot([1000*i for i in timeScale[0:plot_max]],samples[0:plot_max])
  pylab.title('Time domain plot')
  pylab.xlabel('Time (ms)')
  pylab.ylabel('Amplitude')

  #Frequency domain plot
  (Pxx,freqs) = matplotlib.mlab.psd(x = samples-numpy.mean(samples),\
                                                    noverlap = 1024,\
                                                        NFFT = 2048,\
                                     Fs = settings.samplingFreq/1e6)
  pylab.subplot(2,2,2)
  pylab.semilogy(freqs,Pxx)
  pylab.title('Frequency Domain Plot')
  pylab.xlabel('Frequency (MHz)')
  pylab.ylabel('Magnitude')

  #Histogram
  pylab.subplot(2,2,3)
  xticks = pylab.unique(samples)
  pylab.hist(samples,len(xticks))
  axis = pylab.axis()
  pylab.axis([min(samples),max(samples),axis[2],axis[3]])
  xticks = pylab.unique(pylab.round_(xticks))
  pylab.xticks(xticks)
  pylab.title('Histogram');

  return fig

if __name__ == "__main__":
  settings = initSettings.initSettings()
  parser = argparse.ArgumentParser()
  parser.add_argument("file", help="the sample data file to analyse")
  args = parser.parse_args()
  settings.fileName = args.file
  fig = probeData(settings)
  pylab.show()
