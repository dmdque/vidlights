# Vidlights
Video highlights. Made for U of T Hacks 2017.

This is an automated progression video maker. Given a long video with countless attempts to master some skill, it shortens the video to just the important parts. Vidlights listens for a clap to mark the beginning of an attempt. It then strings the important clips together, omitting the in-between junk. We're left with a progression video that gets to the point and is effortless for the user to create!

For demo purposes, I recorded myself learning to roll a coin on my knuckles. The edited video is 59% shorter:
- Original video (1:47): https://www.youtube.com/watch?v=noS8lyJJVaM
- Edited video (1.07): https://www.youtube.com/watch?v=ihAdHhNG_Sk

In the atrium during the hack, I found a Yoyo club meet with some talented members. I asked a boy to perform a difficult trick, showing progression over time. Thanks Nikola! The edited video is 240% shorter:
- Original video (2:51): N/A
- Edited video (1:11): https://www.youtube.com/watch?v=1VFPAv-yLsY

## Usage

    $ # pip install [necessary packages]
    $ # manually set up directory structure and a video to vidlighten
    $ python vidlights.py
