# APCJ40_MKII
by chris joseph

A custom remote script for the APC40 MKII for Ableton Live 11. For Ableton Live 10 please see: https://github.com/CJmusic/APC40_MkIIx

Changes:

- nudge + + copies a clip
- nudge + - deletes a clip
- shift + nudge now nudges
- shift + bank turns on VU meters
- user mode is a step sequencer
- shift + clip view is undo
- shift + detail view is redo
- shift + record is capture midi
- press and hold select clip to expand or collapse a group

Known Bugs:

- Velocity slider doesn't work (it doesn't play the note at that velocity, but it sequences it at it)
- Pads are always lit upon disconnect, velocity slider pads always lit (issue is with the make_button command ControlElementUtils.py)
-VU meters doesn't zero out the session matrix when it's switched to

Features to be added: 

- Shift + User mode will become an instrument mode with scales and playable midi notes on the pads

For installation instructions please visit: 
https://help.ableton.com/hc/en-us/articles/209072009-Installing-third-party-remote-scripts

NOTE: When downloading the .zip file GitHub adds a "-master" suffix. Please remove this before installing the script, the remote script folder name should be "APCJ40_MKII". 

Please contact chrisjosephsongs@gmail.com for any questions/suggestions/improvements! Subscribe to [youtube.com/c/chrisjosephyt](https://youtube.com/c/chrisjosephyt) for a Video tutorial once the Script is fully functional! 

Special Thanks to:

gluon: https://github.com/gluon/AbletonLive11_MIDIRemoteScripts

xnamanahx: https://github.com/xnamahx/APC40_MkIIx

cylab: https://github.com/cylab/APCequencer

martinpechmann: https://github.com/martinpechmann/APC400000

hanzpetrov: http://remotescripts.blogspot.com/p/apc-64-40.html

fabriziopoce: https://github.com/matthewcieplak/APC_64_40_9l

willmarshall: https://github.com/willrjmarshall/AbletonDJTemplateUnsupported
