"""Jazz Orchestral Sketch - jazz harmony arranged with an orchestral color (strings pad + brass stabs) under a
piano lead, fretless bass and soft drums. An original sketch, not a repo demo. Built entirely from bundled sounds
(GeneralUser GS SoundFont for piano/strings/brass/bass, the synthesized drum machine for drums) - no sample-pack
downloads (a real string/brass section would need the vsco2-ce or sso packs; this is the zero-download version).
Build: python -m agentsound build songs/jazz-orchestral-sketch
"""
from agentsound import *

ANALYSIS = {'profile': 'jazz'}


def build() -> Song:
    s = Song('Jazz Orchestral Sketch', tempo=92, key='D minor', seed=3)

    prog = s.prog('i VI iv v')                                  # Dm Bb Gm A, one bar each
    intro = s.section('intro', bars=4, prog=prog)
    theme = s.section('theme', bars=8, prog=prog)
    bridge = s.section('bridge', bars=8, prog=prog)
    theme2 = s.section('theme2', bars=8, prog=prog)
    outro = s.section('outro', bars=4, prog=prog)

    hook = s.motif('1:1/4 3:1/8 5:1/8 6:1/4 5:1/4 | 3:1/2 r:1/4 1:1/4 '
                   '| 6:1/4 5:1/8 3:1/8 1:1/4 2:1/4 | 1:1/2. r:1/4')   # 4-bar piano phrase

    beat = drums({'kick': 'x.......x.......', 'snare': '....x.......x...', 'hat': 'x.x.x.x.x.x.x.x.'})

    s.hall(), s.plate()
    s.master.add(fx.limiter(ceiling=-1.0, gain=3.0))

    piano = s.track('piano', 'gm/piano_lead', gain_db=0, pan=-0.15)
    strings = s.track('strings', 'gm/strings', gain_db=-4, pan=0.0)
    brass = s.track('brass', 'gm/brass_section', gain_db=-3, pan=0.15)
    bass = s.track('bass', 'gm/fretless', gain_db=-2, pan=0.0)
    kit = s.track('drums', 'synthwave/drums_linn', gain_db=-9, pan=0.0)

    strings.chords(s.sections, voicing='spread', register=('C3', 'C5'))
    brass.chords(theme, theme2, voicing='close', register=('C4', 'C5'), rhythm='x...............')
    bass.bassline('octave', theme, bridge, theme2, rate='1/4')
    kit.plan({theme: beat, outro: None})

    piano.play(hook.clip(octave=5), theme, times=2)
    piano.play(hook.clip(octave=5), theme2, times=2)

    strings.automate('gainDb', ramp(intro.start, theme.start, -8, -4))
    return s
