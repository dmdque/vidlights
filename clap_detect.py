import re
from subprocess import PIPE
from subprocess import Popen
from subprocess import call


CONFIG_CLAP_AMPLITUDE_THRESHOLD = 0.7
CONFIG_CLAP_ENERGY_THRESHOLD = 0.3
CONFIG_CLAP_MAX_DURATION = 1500


def extract_audio(video_file, output_audio_file):
    call(['ffmpeg', '-i', video_file, '-q:a', '0', '-map', 'a', output_audio_file])


def split_audio_files(input_file, output_file, duration=1):
    """Split input_file into segments of length t."""
    call(['cd', 'tmp'])
    call(['sox', input_file, output_file, 'trim', '0', str(duration), ':', 'newfile', ':', 'restart'])


def trim_silence():
    # for each file
    # sox in out silence 1 0.0001 ...
    call(['sox', 'clap-corridor-01.wav', '-t', 'wav', 'tmp/output001.wav', 'silence' '1', '0.0001', '10%', '1', '0.1', '10%'])
    pass


def get_stats(input_file):
    p = Popen(['sox', input_file, '-t', 'wav', 'tmpout', 'stat'], stderr=PIPE)
    _, stderr = p.communicate()
    return stderr


def parse_stats(stats):
    stats = re.sub(r' +', ' ', stats)  # remove extra spaces
    stat_dict = {}
    stat_list = stats.split('\n')
    for stat in stat_list:
        elements = re.split(':\s*', stat)
        if len(elements) != 2:
            continue
        key, val = elements
        stat_dict[key] = float(val)
    return stat_dict


def is_clap(stat_dict):
    duration = stat_dict['Length (seconds)']
    rms = stat_dict['RMS amplitude']
    max_amplitude = stat_dict['Maximum amplitude']
    return (duration < CONFIG_CLAP_MAX_DURATION and
            max_amplitude > CONFIG_CLAP_AMPLITUDE_THRESHOLD and
            rms < CONFIG_CLAP_ENERGY_THRESHOLD)


# extract_audio('data/bee-movie-trailer.mp4', 'tmp/audio.mp3')
split_audio_files('clap-corridor-01.wav', 'tmp/output.wav', .5)
trim_silence()
stats = get_stats('tmp/output001.wav')
stat_dict = parse_stats(stats)
print is_clap(stat_dict)

