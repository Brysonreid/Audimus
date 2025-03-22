#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: LoadAudioFile
# Author: Bryson
# GNU Radio version: v3.9.2.0-85-g08bb05c1

from gnuradio import analog
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




class LoadFile2(gr.top_block):

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
        self._Demod_Quadrature_config = configparser.ConfigParser()
        self._Demod_Quadrature_config.read('LimeSDRConf.ini')
        try: Demod_Quadrature = self._Demod_Quadrature_config.getfloat('Demodulation', 'Quadrature')
        except: Demod_Quadrature = 240000
        self.Demod_Quadrature = Demod_Quadrature
        self._Demod_Decimation_config = configparser.ConfigParser()
        self._Demod_Decimation_config.read('LimeSDRConf.ini')
        try: Demod_Decimation = self._Demod_Decimation_config.getint('Demodulation', 'Decimation')
        except: Demod_Decimation = 16
        self.Demod_Decimation = Demod_Decimation
        self._Audio_Decimation_config = configparser.ConfigParser()
        self._Audio_Decimation_config.read('LimeSDRConf.ini')
        try: Audio_Decimation = self._Audio_Decimation_config.getint('Demodulation', 'Audio_Decimation')
        except: Audio_Decimation = 5
        self.Audio_Decimation = Audio_Decimation

        ##################################################
        # Blocks
        ##################################################
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, Storage_File, False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=Demod_Quadrature,
        	audio_decimation=Audio_Decimation,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.analog_wfm_rcv_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_Storage_File(self):
        return self.Storage_File

    def set_Storage_File(self, Storage_File):
        self.Storage_File = Storage_File
        self.blocks_file_source_0.open(self.Storage_File, False)

    def get_Demod_Quadrature(self):
        return self.Demod_Quadrature

    def set_Demod_Quadrature(self, Demod_Quadrature):
        self.Demod_Quadrature = Demod_Quadrature

    def get_Demod_Decimation(self):
        return self.Demod_Decimation

    def set_Demod_Decimation(self, Demod_Decimation):
        self.Demod_Decimation = Demod_Decimation

    def get_Audio_Decimation(self):
        return self.Audio_Decimation

    def set_Audio_Decimation(self, Audio_Decimation):
        self.Audio_Decimation = Audio_Decimation




def main(top_block_cls=LoadFile2, options=None):
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
