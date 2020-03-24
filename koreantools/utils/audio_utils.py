""" Utily functions to process audio files """

import os
import sys
import wave

def pcm_to_wave(pcm_file_path, num_channels=1, num_bytes=2, frame_rate=16000,
                nframes=0, comp_type="NONE", comp_name="NONE"):
    """ Converts a raw .pcm file to .wav file

        Args:
            pcm_file_path (str): Full path to pcm file
            num_channels (int): 1 for Mono, 2 for stereo
            num_bytes (int): Number of bytes per sample width
            frame_rate (int): Frame rate
            nframes (int): n frames
            comp_type (str): Compression type
            comp_name (str): Compression description
    """
    with open(pcm_file_path, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    wav_name = pcm_file_path.split('.')[0] + '.wav'
    wavfile = wave.open(wav_name, 'wb')
    wavfile.setparams((num_channels, num_bytes, frame_rate, nframes, comp_type, comp_name))
    wavfile.writeframes(pcmdata)
    wavfile.close()


def main():
    """ Main entry """
    if len(sys.argv) < 2:
        print("Please provide root dir for the pcm files")
        sys.exit(1)

    num_channels = 1
    num_bytes = 2
    frame_rate = 16000
    nframes = 0
    comp_type = 'NONE'
    comp_name = 'NONE'

    i = 0
    filename = ''
    for root, _, files in os.walk(sys.argv[1]):
        for name in files:
            if ".pcm" in name:
                filename = os.path.join(root, name)
                pcm_to_wave(filename, num_channels=num_channels, num_bytes=num_bytes,
                            frame_rate=frame_rate, nframes=nframes, comp_type=comp_type,
                            comp_name=comp_name)
                i += 1
                if i % 200 == 0:
                    print("Completed converting: %d files, current file: %s" % (i, filename))

if __name__ == "__main__":
    main()
