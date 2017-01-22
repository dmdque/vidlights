import os
import re
from subprocess import PIPE
from subprocess import Popen
from subprocess import call



CONFIG_CLAP_AMPLITUDE_THRESHOLD = 0.7
CONFIG_CLAP_ENERGY_THRESHOLD = 0.3
CONFIG_CLAP_MAX_DURATION = 1500
CONFIG_SPLIT_INCREMENT = 0.2


def extract_audio(video_file, output_audio_file):
    call(['ffmpeg', '-i', video_file, '-q:a', '0', '-map', 'a', output_audio_file])


def split_audio_files(input_file, output_file, duration=1):
    """Split input_file into segments of length t."""
    call(['cd', 'tmp'])
    call(['sox', input_file, output_file, 'trim', '0', str(duration), ':', 'newfile', ':', 'restart'])


def trim_silence():
    for f in os.listdir('tmp'):
        file_relative_path = 'tmp/{}'.format(f)
        call(['sox', file_relative_path, '-t', 'wav', file_relative_path, 'silence', '0.5', '0.0001', '10%', '1', '0.1', '10%'])


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



# TODO: exclude things like .DS_STORE
def get_clap_times():
    clap_times = []
    for i, f in enumerate(os.listdir('tmp')):
        file_relative_path = 'tmp/{}'.format(f)
        stats = get_stats(file_relative_path)
        print file_relative_path, stats
        stat_dict = parse_stats(stats)
        if is_clap(stat_dict):
            clap_times.append(i * CONFIG_SPLIT_INCREMENT)
    return clap_times


def clap_detect(video_file, output_audio_file, output_split_audio_file):
    extract_audio(video_file, output_audio_file)
    call(['rm', '-rf', 'tmp'])
    call(['mkdir', 'tmp'])
    split_audio_files(output_audio_file, output_split_audio_file, CONFIG_SPLIT_INCREMENT)
    trim_silence()
    clap_times = get_clap_times()
    return clap_times
