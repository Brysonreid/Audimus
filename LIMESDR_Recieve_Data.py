#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: LIMESDR_Recieve_Data
# Author: Bryson
# GNU Radio version: v3.9.2.0-85-g08bb05c1

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import configparser




class LIMESDR_Recieve_Data(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "LIMESDR_Recieve_Data", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self._samp_rate_config = configparser.ConfigParser()
        self._samp_rate_config.read('LimeSDRConf.ini')
        try: samp_rate = self._samp_rate_config.getfloat('Radio', 'Sample_Rate')
        except: samp_rate = 2400000
        self.samp_rate = samp_rate
        self._Storage_File_config = configparser.ConfigParser()
        self._Storage_File_config.read('LimeSDRConf.ini')
        try: Storage_File = self._Storage_File_config.get('Storage', 'File')
        except: Storage_File = 'Recordings\\SDRdata'
        self.Storage_File = Storage_File
        self._Filter_Decimation_config = configparser.ConfigParser()
        self._Filter_Decimation_config.read('LimeSDRConf.ini')
        try: Filter_Decimation = self._Filter_Decimation_config.getint('Filter', 'Decimation')
        except: Filter_Decimation = 1
        self.Filter_Decimation = Filter_Decimation
        self._File_Size_config = configparser.ConfigParser()
        self._File_Size_config.read('LimeSDRConf.ini')
        try: File_Size = self._File_Size_config.getint('Storage', 'FileSize')
        except: File_Size = 57600000
        self.File_Size = File_Size
        self._Center_Frequency_config = configparser.ConfigParser()
        self._Center_Frequency_config.read('LimeSDRConf.ini')
        try: Center_Frequency = self._Center_Frequency_config.getfloat('Radio', 'Frequency')
        except: Center_Frequency = 138000000
        self.Center_Frequency = Center_Frequency

        ##################################################
        # Blocks
        ##################################################
        self.soapy_limesdr_source_0_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_limesdr_source_0_0 = soapy.source(dev, "fc32", 1, "",
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_source_0_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_source_0_0.set_bandwidth(0, 40000000)
        self.soapy_limesdr_source_0_0.set_frequency(0, Center_Frequency)
        self.soapy_limesdr_source_0_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_source_0_0.set_gain(0, min(max(80, -12.0), 61.0))
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=10,
                taps=[],
                fractional_bw=0.2)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            Filter_Decimation,
            firdes.low_pass(
                1,
                samp_rate,
                samp_rate/4,
                samp_rate/8,
                window.WIN_HAMMING,
                6.76))
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, File_Size)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, Storage_File, False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.analog_agc_xx_0 = analog.agc_cc(5e-3, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_head_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.soapy_limesdr_source_0_0, 0), (self.low_pass_filter_0_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/4, self.samp_rate/8, window.WIN_HAMMING, 6.76))
        self.soapy_limesdr_source_0_0.set_sample_rate(0, self.samp_rate)

    def get_Storage_File(self):
        return self.Storage_File

    def set_Storage_File(self, Storage_File):
        self.Storage_File = Storage_File
        self.blocks_file_sink_0_0.open(self.Storage_File)

    def get_Filter_Decimation(self):
        return self.Filter_Decimation

    def set_Filter_Decimation(self, Filter_Decimation):
        self.Filter_Decimation = Filter_Decimation

    def get_File_Size(self):
        return self.File_Size

    def set_File_Size(self, File_Size):
        self.File_Size = File_Size
        self.blocks_head_0.set_length(self.File_Size)

    def get_Center_Frequency(self):
        return self.Center_Frequency

    def set_Center_Frequency(self, Center_Frequency):
        self.Center_Frequency = Center_Frequency
        self.soapy_limesdr_source_0_0.set_frequency(0, self.Center_Frequency)




def main(top_block_cls=LIMESDR_Recieve_Data, options=None):
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
