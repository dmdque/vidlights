import arrow
import csv
import re
from subprocess import call
from subprocess import PIPE


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


def generate_concat_file(n, file_extension='avi', output_dir='output'):
    """Generate file containing list of files to concatenate for use by ffmpeg. """
    with open('concat_files.txt', 'w') as f:
        for i in range(n):
            f.write("file '{}/tmp{}.{}'\n".format(output_dir, i, file_extension))


def split_from_highlights(video_file, highlight_times, output_dir='output'):
    # TODO: ensure output folder exists
    for i, time_pair in enumerate(highlight_times):
        start_time, end_time = time_pair
        print ['ffmpeg', '-i', video_file, '-ss', start_time, '-t', end_time, '{}/tmp{}.avi'.format(output_dir, i)]
        call(['ffmpeg', '-i', video_file, '-ss', start_time, '-t', end_time, '{}/tmp{}.avi'.format(output_dir, i)])


def concat_files(output_file='output.avi'):
    call(['ffmpeg', '-f', 'concat', '-i', 'concat_files.txt', '-c', 'copy', output_file])


def cleanup_temp_files():
    # TODO: replace with python calls
    call(['rm', '-rf', 'output'])
    call(['mkdir', 'output'])
    call(['rm', 'output.avi'])


def vidlight_bee():
    cleanup_temp_files()
    highlight_times = get_highlights_from_transcript('be', 'transcripts/bee-movie-trailer-transcript.csv')
    split_from_highlights(
        video_file='data/bee-movie-trailer.mp4',
        highlight_times=highlight_times
    )
    num_clips = len(highlight_times)
    generate_concat_file(num_clips)
    concat_files()


vidlight_bee()
