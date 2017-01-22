# Vidlights
When I learned to breakdance, I took countless videos to track progress. I made progression videos showing my journey from a newbie onward. Editing hours of footage took days, and I knew there was a better way.

What if I could just snap my fingers before practicing a trick, and have a computer take care of the rest?

Vidlights is an automated video clipper that does just that. It listens for a snap and saves that clip of a video. All of the clips are concatenated, resulting in a progression video that gets to the point and is effortless for the user to create!

For demo purposes, I recorded myself learning to roll a coin on my knuckles. The edited video is 59% shorter:

- Original video (1:47): https://www.youtube.com/watch?v=noS8lyJJVaM
- Edited video (1.07): https://www.youtube.com/watch?v=ihAdHhNG_Sk

In the atrium during the hack, I found a Yoyo club meet with some talented members. I asked a boy to perform a difficult trick, showing progression over time. Thanks Nikola! The edited video is 240% shorter:

- Original video (2:51): N/A
- Edited video (1:11): https://www.youtube.com/watch?v=1VFPAv-yLsY

## Features
### Modes
Control:
- Snap to start, and specify fixed duration for clips or
- Snap to start, snap to end (variable durations)

Video:
- Specify single video file or
- Specify folder with videos (the clips will be combined in chronological order)

## Usage
    $ # pip install [necessary packages]
    $ # manually set up directory structure and a video to vidlighten
    $ python vidlights.py
