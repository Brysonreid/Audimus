#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: LIMESDR_Recieve_Data
# Author: Bryson
# GNU Radio version: v3.9.2.0-85-g08bb05c1

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
        except: samp_rate = 768000
        self.samp_rate = samp_rate
        self._Storage_File_config = configparser.ConfigParser()
        self._Storage_File_config.read('LimeSDRConf.ini')
        try: Storage_File = self._Storage_File_config.get('Storage', 'File')
        except: Storage_File = 'Recordings\\SDRdata'
        self.Storage_File = Storage_File
        self._Interpolation_config = configparser.ConfigParser()
        self._Interpolation_config.read('LimeSDRConf.ini')
        try: Interpolation = self._Interpolation_config.getint('Demodulation', 'Interpolation')
        except: Interpolation = 5
        self.Interpolation = Interpolation
        self._Filter_Transmission_Width_config = configparser.ConfigParser()
        self._Filter_Transmission_Width_config.read('LimeSDRConf.ini')
        try: Filter_Transmission_Width = self._Filter_Transmission_Width_config.getfloat('Filter', 'Transmission_Width')
        except: Filter_Transmission_Width = 25000
        self.Filter_Transmission_Width = Filter_Transmission_Width
        self._Filter_Decimation_config = configparser.ConfigParser()
        self._Filter_Decimation_config.read('LimeSDRConf.ini')
        try: Filter_Decimation = self._Filter_Decimation_config.getint('Filter', 'Decimation')
        except: Filter_Decimation = 1
        self.Filter_Decimation = Filter_Decimation
        self._Filter_Cut_Off_Frequency_config = configparser.ConfigParser()
        self._Filter_Cut_Off_Frequency_config.read('LimeSDRConf.ini')
        try: Filter_Cut_Off_Frequency = self._Filter_Cut_Off_Frequency_config.getfloat('Filter', 'Cut_Off_Frequency')
        except: Filter_Cut_Off_Frequency = 75000
        self.Filter_Cut_Off_Frequency = Filter_Cut_Off_Frequency
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
        self._Center_Frequency_config = configparser.ConfigParser()
        self._Center_Frequency_config.read('LimeSDRConf.ini')
        try: Center_Frequency = self._Center_Frequency_config.getfloat('Radio', 'Frequency')
        except: Center_Frequency = 138000000
        self.Center_Frequency = Center_Frequency
        self._Audio_Decimation_config = configparser.ConfigParser()
        self._Audio_Decimation_config.read('LimeSDRConf.ini')
        try: Audio_Decimation = self._Audio_Decimation_config.getint('Demodulation', 'Audio_Decimation')
        except: Audio_Decimation = 5
        self.Audio_Decimation = Audio_Decimation

        ##################################################
        # Blocks
        ##################################################
        self.soapy_limesdr_source_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_limesdr_source_0 = soapy.source(dev, "fc32", 1, "",
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_source_0.set_bandwidth(0, 40000000)
        self.soapy_limesdr_source_0.set_frequency(0, Center_Frequency)
        self.soapy_limesdr_source_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_source_0.set_gain(0, min(max(80, -12.0), 61.0))
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=Interpolation,
                decimation=Demod_Decimation,
                taps=[],
                fractional_bw=0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            Filter_Decimation,
            firdes.low_pass(
                1,
                samp_rate ,
                samp_rate/4,
                samp_rate/8,
                window.WIN_HAMMING,
                6.76))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(1)
        self.blocks_head_0_0 = blocks.head(gr.sizeof_gr_complex*1, 14400000)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, Storage_File, False)
        self.blocks_file_sink_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_head_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_head_0_0, 0))
        self.connect((self.soapy_limesdr_source_0, 0), (self.low_pass_filter_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate , self.samp_rate/4, self.samp_rate/8, window.WIN_HAMMING, 6.76))
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_Storage_File(self):
        return self.Storage_File

    def set_Storage_File(self, Storage_File):
        self.Storage_File = Storage_File
        self.blocks_file_sink_0.open(self.Storage_File)

    def get_Interpolation(self):
        return self.Interpolation

    def set_Interpolation(self, Interpolation):
        self.Interpolation = Interpolation

    def get_Filter_Transmission_Width(self):
        return self.Filter_Transmission_Width

    def set_Filter_Transmission_Width(self, Filter_Transmission_Width):
        self.Filter_Transmission_Width = Filter_Transmission_Width

    def get_Filter_Decimation(self):
        return self.Filter_Decimation

    def set_Filter_Decimation(self, Filter_Decimation):
        self.Filter_Decimation = Filter_Decimation

    def get_Filter_Cut_Off_Frequency(self):
        return self.Filter_Cut_Off_Frequency

    def set_Filter_Cut_Off_Frequency(self, Filter_Cut_Off_Frequency):
        self.Filter_Cut_Off_Frequency = Filter_Cut_Off_Frequency

    def get_Demod_Quadrature(self):
        return self.Demod_Quadrature

    def set_Demod_Quadrature(self, Demod_Quadrature):
        self.Demod_Quadrature = Demod_Quadrature

    def get_Demod_Decimation(self):
        return self.Demod_Decimation

    def set_Demod_Decimation(self, Demod_Decimation):
        self.Demod_Decimation = Demod_Decimation

    def get_Center_Frequency(self):
        return self.Center_Frequency

    def set_Center_Frequency(self, Center_Frequency):
        self.Center_Frequency = Center_Frequency
        self.soapy_limesdr_source_0.set_frequency(0, self.Center_Frequency)

    def get_Audio_Decimation(self):
        return self.Audio_Decimation

    def set_Audio_Decimation(self, Audio_Decimation):
        self.Audio_Decimation = Audio_Decimation




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
