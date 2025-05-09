#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: LoadAudioFile
# Author: Bryson
# GNU Radio version: v3.9.2.0-85-g08bb05c1

from gnuradio import audio
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import configparser




class LoadFile(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "LoadAudioFile", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self._Storage_File_config = configparser.ConfigParser()
        self._Storage_File_config.read('LimeSDRConf.ini')
        try: Storage_File = self._Storage_File_config.get('Storage', 'File')
        except: Storage_File = 'Recordings\\SDRdata'
        self.Storage_File = Storage_File

        ##################################################
        # Blocks
        ##################################################
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_float*1, Storage_File, False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.audio_sink_0 = audio.sink(48000, '', True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.audio_sink_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_Storage_File(self):
        return self.Storage_File

    def set_Storage_File(self, Storage_File):
        self.Storage_File = Storage_File
        self.blocks_file_source_0.open(self.Storage_File, False)




def main(top_block_cls=LoadFile, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
