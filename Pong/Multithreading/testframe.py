#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
""" bla bla bla"""   #TODO: Write summary about this file!

__author__ = "Daniel Speck, Florian Kock"
__copyright__ = "Copyright 2014, Praktikum Neuronale Netze"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Daniel Speck, Florian Kock"
__email__ = "2speck@informatik.uni-hamburg.de, 2kock@informatik.uni-hamburg.de"
__status__ = "Development"

from data_frame import DataFrame
x = DataFrame('test')

x.add('data' , 1234)

print(x.instruction)
print(x.getdata('data') + 4)

