# -*- coding: utf-8

"""
Python implementation of Non-Stationary Gabor Transform (NSGT)
derived from MATLAB code by NUHAG, University of Vienna, Austria

Thomas Grill, 2011-2015
http://grrrr.org/nsgt

Austrian Research Institute for Artificial Intelligence (OFAI)
AudioMiner project, supported by Vienna Science and Technology Fund (WWTF)
"""

import numpy as np
import subprocess as sp
import os.path
import re
import sys
from functools import reduce
from warnings import warn
import torchaudio
import torch



def sndreader(filepath, blksz=2**16, dtype=np.float32):
    waveform, sample_rate = torchaudio.load(filepath)
    num_frames = waveform.size(1)
    if blksz < 0:
        blksz = num_frames
    channels = waveform.size(0)
    for offs in range(0, num_frames, blksz):
        yield waveform[:, offs:offs + blksz].numpy().astype(dtype)

def sndwriter(filepath, waveform, sample_rate, format='wav'):
    torchaudio.save(filepath, waveform, sample_rate, format=format)

class SndReader:
    def __init__(self, fn, sr=None, chns=None, blksz=2**16, dtype=np.float32):
        self.waveform, self.samplerate = torchaudio.load(fn)
        self.channels = self.waveform.size(0)
        self.frames = self.waveform.size(1)
        if sr and sr != self.samplerate:
            self.waveform = torchaudio.transforms.Resample(orig_freq=self.samplerate, new_freq=sr)(self.waveform)
            self.samplerate = sr
        if chns and chns != self.channels:
            original_channels = self.channels
            if original_channels == 1 and chns == 2:
                # Mono to stereo: duplicate the channel
                self.waveform = self.waveform.repeat(2, 1)
                warn("Converted mono audio to stereo by duplicating the channel.")
            elif original_channels == 2 and chns == 1:
                # Stereo to mono: average the channels
                self.waveform = torch.mean(self.waveform, dim=0, keepdim=True)
                warn("Converted stereo audio to mono by averaging the channels.")
            else:
                raise ValueError(f"Unsupported channel conversion from {original_channels} to {chns}.")
                
        self.rdr = sndreader(fn, blksz, dtype=dtype)

    def __call__(self):
        return self.rdr

class SndWriter:
    def __init__(self, fn, samplerate, filefmt='wav', datafmt='pcm16', channels=1):
        self.fn = fn
        self.samplerate = samplerate
        self.filefmt = filefmt
        self.channels = channels

    def __call__(self, sigblks, maxframes=None):
        waveform = torch.cat([torch.from_numpy(b) for b in sigblks], dim=1)
        sndwriter(self.fn, waveform, self.samplerate, format=self.filefmt)

