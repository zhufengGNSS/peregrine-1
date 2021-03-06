# Copyright (C) 2012 Swift Navigation Inc.
#
# This source is subject to the license found in the file 'LICENSE' which must
# be be distributed together with this source. All other rights reserved.
#
# THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.

import numpy as np

def generateCAcode(PRN):
  #--- Make the code shift array. The shift depends on the PRN number -----
  # The g2s vector holds the appropriate shift of the g2 code to generate
  # the C/A code (ex. for SV#19 - use a G2 shift of g2s(19) = 471)
  g2s = [  5,   6,   7,   8,  17,  18, 139, 140, 141, 251, \
         252, 254, 255, 256, 257, 258, 469, 470, 471, 472, \
         473, 474, 509, 512, 513, 514, 515, 516, 859, 860, \
         861, 862, \
         #Shifts for the ground GPS transmitter are not included
         #Shifts for EGNOS and WAAS satellites (true_PRN = PRN + 87)
                   145, 175,  52,  21, 237, 235, 886, 657, \
         634, 762, 355, 1012, 176, 603, 130, 359, 595, 68, \
         386]
  
  #--- Pick right shift for the given PRN number --------------------------
  g2shift = g2s[PRN]
  
  #--- Generate G1 code ---------------------------------------------------
  
  #--- Initialize g1 output to speed up the function -
#  g1 = [0]*1023
  g1 = [0 for i in range(1023)]
  #--- Load shift register -
#  reg = [-1]*10
  reg = [-1 for i in range(10)]
  
  #--- Generate all G1 signal chips based on the G1 feedback polynomial ---
  for i in range(0,1023):
    g1[i] = reg[9]
    saveBit  = reg[2]*reg[9]
    reg[1:10] = reg[0:9]
    reg[0]   = saveBit
  
  #--- Generate G2 code -----------------------------------------------------
  
  #--- Initialize g2 output to speed up the function ---
#  g2 = [0]*1023
  g2 = [0 for i in range(1023)]
  #--- Load shift register ---
#  reg = [-1]*10
  reg = [-1 for i in range(10)]
  
  #--- Generate all G2 signal chips based on the G2 feedback polynomial -----
  for i in range(0,1023):
    g2[i]    = reg[9]
    saveBit  = reg[1]*reg[2]*reg[5]*reg[7]*reg[8]*reg[9]
    reg[1:10] = reg[0:9]
    reg[0]   = saveBit
  
  #--- Shift G2 code --------------------------------------------------------
  #The idea: g2 = concatenate[ g2_right_part, g2_left_part ];
  g2 = [g2[i-g2shift] for i in range(0,1023)]
  
  #--- Form single sample C/A code by multiplying G1 and G2 -----------------
  CAcode = [-g1[i]*g2[i] for i in range(0,1023)]

  return CAcode

caCodes = np.empty((51, 1023), dtype=np.int8)
for PRN in range(51):
  caCodes[PRN][:] = generateCAcode(PRN)

