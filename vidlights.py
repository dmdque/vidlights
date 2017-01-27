import arrow
import csv
import os
import re
from enum import Enum
from subprocess import call

from clap_detect import clap_detect


class ClipMode(Enum):
    start_only = 1
    start_and_end = 2


DEMO = 'single'
CONFIG = {
    'video_mode': 'multiple',
    'video_dir': 'data/vids',
    'extension_filter': 'MOV',
    'input_video': 'data/rainbow.MOV',
    'output_audio_file': 'tmp/rainbow.wav',
    'output_video': 'generated/rainbow.avi',
    'clip_mode': ClipMode.start_and_end,
    'clip_duration': 12
}


def get_highlights_from_transcript(keyword, transscript_file):
    """Return list of time pairs corresponding to occurences of the keyword."""
    highlight_times = []
    csv_rows = []
    # get file as a list, because we need to look ahead
    with open(transscript_file, 'r') as transcript:
        reader = csv.reader(transcript, delimiter=',')
        for row in reader:
            assert len(row) == 2
            csv_rows.append(row)
    for i, row in enumerate(csv_rows):
        timestamp, text = row
        match = re.search(r'\b{}\b'.format(keyword), text)
        if match is None:
            continue
        start_time = timestamp
        end_time = csv_rows[i + 1][0]
        duration = arrow.get(
            (arrow.get(end_time, 'm:ss') - arrow.get(start_time, 'm:ss')).seconds
        ).format('m:ss')
        highlight_times.append((start_time, duration))
    return highlight_times


def generate_concat_file(n,
                         file_extension='avi',
                         output_dir='output'):
    """Generate concat file for ffmpeg.

    Consists of a list of filenames to be concatenated """
    with open('concat_files.txt', 'w') as f:
        for i in range(n):
            file_path = "file '{}/tmp{}.{}'\n".format(output_dir, i, file_extension)
            f.write(file_path)


def split_from_highlights(video_file,
                          highlight_times,
                          output_file='output',
                          base_count=0):
    # TODO: ensure output folder exists
    for i, time_pair in enumerate(highlight_times):
        start_time, end_time = time_pair
        print ['ffmpeg', '-i', video_file, '-ss', start_time, '-t', end_time, '{}/tmp{}.avi'.format(output_file, base_count + i)]
        call(['ffmpeg', '-i', video_file, '-ss', start_time, '-t', end_time, '{}/tmp{}.avi'.format(output_file, base_count + i)])


def concat_files(output_file=CONFIG['output_video']):
    call(['ffmpeg', '-f', 'concat', '-i', 'concat_files.txt', '-c', 'copy', output_file])


def setup_and_clean():
    # TODO: replace with python calls
    call(['rm', '-rf', 'output'])
    call(['mkdir', 'output'])
    call(['mkdir', '-p', 'generated'])
    call(['mkdir', '-p', 'tmp/audio'])
    call(['mkdir', '-p', 'tmp/video'])
    call(['mkdir', '-p', 'data/vids'])
    call(['rm', 'output.avi'])
    call(['rm', 'tmp_audio.mp3'])


def vidlight_bee():
    setup_and_clean()
    highlight_times = get_highlights_from_transcript('be', 'transcripts/bee-movie-trailer-transcript.csv')
    split_from_highlights(
        video_file='data/bee-movie-trailer.mp4',
        highlight_times=highlight_times
    )
    num_clips = len(highlight_times)
    generate_concat_file(num_clips)
    concat_files()


def clean_clap_times(threshold=2):
    """Remove consecutive claps if they're too close to each other."""
    pass


def time_delta(start_time, end_time):
    """Converts start and end time in seconds to a duration in m:ss string format."""
    duration = arrow.get(end_time - start_time).format('m:ss')
    return duration


def interpret_claps(clap_times, mode):
    """Process claps.

    clap_times: list of times
    """
    if mode == ClipMode.start_only:
        formatted_clap_times = [
            (arrow.get(time).format('m:ss'), arrow.get(12).format('m:ss')) for time in clap_times
        ]
        return formatted_clap_times
    elif mode == ClipMode.start_and_end:
        if len(clap_times) % 2 != 0:
            clap_times.pop()
        formatted_clap_times = []
        for i in range(0, len(clap_times), 2):
            formatted_clap_times.append(
                (arrow.get(clap_times[i]).format('m:ss'),
                 time_delta(clap_times[i], clap_times[i + 1]))
            )
        return formatted_clap_times


def progression_slice():
    setup_and_clean()
    clap_times = clap_detect(CONFIG['input_video'], 'tmp_audio.mp3', CONFIG['output_audio_file'])
    formatted_clap_times = interpret_claps(clap_times, CONFIG['clip_mode'])
    print 'formatted_clap_times', formatted_clap_times
    split_from_highlights(
        video_file=CONFIG['input_video'],
        highlight_times=formatted_clap_times
    )
    num_clips = len(formatted_clap_times)
    generate_concat_file(num_clips)
    concat_files()


def get_video_list_chronological():
    video_date_list = []
    for f in os.listdir(CONFIG['video_dir']):
        if f[-3:] == CONFIG['extension_filter']:
            file_path = '{}/{}'.format(CONFIG['video_dir'], f)
            stat = os.stat(file_path)
            video_date_list.append((file_path, stat.st_birthtime))
    video_date_list = sorted(video_date_list, key=lambda e: e[1])
    return [video for (video, date) in video_date_list]


def vidlight_multiple():
    setup_and_clean()
    video_list = get_video_list_chronological()
    num_clips = 0
    for i, video in enumerate(video_list):
        call(['rm', 'tmp_audio.mp3'])  # hacky, but need to clear this to prevent ffmpeg from asking to overwrite each time
        clap_times = clap_detect(video, 'tmp_audio.mp3', CONFIG['output_audio_file'])
        formatted_clap_times = interpret_claps(clap_times, CONFIG['clip_mode'])
        split_from_highlights(
            video_file=video,
            highlight_times=formatted_clap_times,
            base_count=num_clips
        )
        num_clips += len(formatted_clap_times)
    generate_concat_file(num_clips)
    concat_files()


if DEMO == 'bee':
    vidlight_bee()
elif DEMO == 'single':
    progression_slice()
elif DEMO == 'multiple':
    vidlight_multiple()
