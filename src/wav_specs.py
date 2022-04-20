# Copyright 2012 Free Software Foundation, Inc.
#
# This file is part of The BPM Detector Python
#
# The BPM Detector Python is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# The BPM Detector Python is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with The BPM Detector Python; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

import array
import wave
import soundfile as sf

"""ob = sf.SoundFile('example.wav')
print('Sample rate: {}'.format(ob.samplerate))
print('Channels: {}'.format(ob.channels))
print('Subtype: {}'.format(ob.subtype))"""


def read_wav(filename):
    # open file, get metadata for audio
    try:
        wf = wave.open(filename, "rb")
    except IOError as e:
        print(e)
        return

    # typ = choose_type( wf.getsampwidth() ) # TODO: implement choose_type
    nsamps = wf.getnframes()
    assert nsamps > 0

    sampling_freq = wf.getframerate()
    assert sampling_freq > 0

    channels = wf.getnchannels()
    # Returns number of audio channels (1 for mono, 2 for stereo).
    sample_width = wf.getsampwidth()
    # Returns sample width in bytes.


    # Read entire file and make into an array
    samps = list(array.array("i", wf.readframes(nsamps)))

    try:
        assert nsamps == len(samps)
    except AssertionError:
        print(nsamps, "not equal to", len(samps))

    return sampling_freq, channels, sample_width
