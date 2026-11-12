"""Amazon Fires - "Rising alarm": tense from bar one (a grinding minor-2nd drone, D2/Eb2, 1 semitone, under a
low timpani "clock"), an 8-bar chromatic bass climb (D1 up to A1, one semitone per bar - unbroken, unresolved
tension) into the same violent tutti sting as the devastation arc, but landing on a tritone (D-Ab, 6 semitones)
instead of an open fifth - and then it just stops, hard, no fade. D minor, 100 BPM, 21 bars (~50 s). Built on
bands.film_orchestra (agentsound.bandlib.orchestra).

Shaped to sit under narration like the devastation arc: dense/loud only in the 4-bar sting, everything else stays
low (bass/sub/low strings) or sparse so a voiceover has room. No resolution anywhere, including the ending - this
is the "still happening, still urgent" cut rather than the elegiac one.

Build: python -m agentsound build songs/amazon-fires-alarm
"""
from agentsound import *
from agentsound import bands
from agentsound.bandlib import orchestra as orch
from agentsound.theory import note as nn

ANALYSIS = {'profile': 'film'}
METADATA = {'title': 'Amazon Fires - Rising Alarm', 'artist': 'AgentSound', 'album': 'Amazon Fires Sketches',
            'genre': 'Soundtrack'}

W = 4
CHROM = ['D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A']   # chromatic bass climb, one semitone per bar


def part(rows, scale=1.0) -> Clip:
    notes = []
    for i, bar in enumerate(rows):
        for t, d, p, v in bar:
            for q in (p if isinstance(p, (list, tuple)) else [p]):
                notes.append((i * W + t, d, q, max(1, min(127, round(v * scale)))))
    return Clip(notes, length=len(rows) * W)


def ostinato(roots, octave, vel, fifth=False):
    rows = []
    for r, v in zip(roots, vel):
        p = nn(f"{r}{octave}") + (7 if fifth else 0)
        rows.append([(k * 0.5, 0.35, p + (12 if k == 7 else 0), v + (10 if k in (0, 3, 6) else 0)) for k in range(8)])
    return rows


def chords(voicings, vels, beats=W):
    return [[(0, beats, v, vel)] for v, vel in zip(voicings, vels)]


BUILD_V = [36, 42, 46, 50, 56, 62, 68, 76]             # escalates harder than the devastation arc's 'rise'
PEAK_V = [112, 116, 120, 116, 122, 118, 124, 127]


def build() -> Song:
    s = Song('Amazon Fires - Rising Alarm', tempo=100, key='D minor', seed=12, tail=1)
    intro = s.section('intro', bars=6)
    climb = s.section('climb', bars=8)
    sting = s.section('sting', bars=4)
    cut = s.section('cut', bars=3)
    o = bands.film_orchestra(s, hybrid=True)
    P = lambda role, rows, sec, **kw: orch.perform(o, role, part(rows), sec, seed=sum(map(ord, role)), **kw)  # noqa

    # ---------------------------------------------------------------- intro: a grinding minor 2nd, a slow clock
    P('cellos', [[(0, 24, 'D2', 28)]] + [[]] * 5, intro, articulations='sustain')
    P('basses', [[(0, 24, ['D1', 'D#1'], 26)]] + [[]] * 5, intro, articulations='sustain')   # D-D#: 1 semitone
    P('sub', [[(0, 24, 'D0', 20)]] + [[]] * 5, intro)
    P('timpani', [[(0, 0.5, 'D2', 44)], [], [(0, 0.5, 'D2', 46)], [], [(0, 0.5, 'D2', 50)], []], intro)  # the clock

    # ---------------------------------------------------------------- climb: chromatic bass, one semitone a bar
    P('cellos', ostinato(CHROM, 2, BUILD_V), climb, articulations='staccato')
    P('violas', ostinato(CHROM, 3, [v - 8 for v in BUILD_V], fifth=True), climb, articulations='staccato')
    P('basses', chords([nn(r + '1') for r in CHROM], BUILD_V), climb, shapes='cresc')
    P('sub', chords([nn(r + '0') for r in CHROM], [v - 6 for v in BUILD_V]), climb)
    P('choir', chords([[nn(r + '4'), nn(r + '4') + 1] for r in CHROM], [v - 22 for v in BUILD_V]), climb,
      shapes='cresc')                                  # a tone cluster, not a triad - no resolution to lean on
    P('horns', chords([[nn(r + '3')] for r in CHROM], [v - 16 for v in BUILD_V]), climb)
    P('timpani', [[(0, 0.5, 'D2', v), (2, 0.5, 'D2', v)] for v in BUILD_V], climb)   # the clock, faster, louder
    k = orch.PERCUSSION_KEYS
    o.percussion.note(k['cymbal_roll'], sting.start - 4.0, 4, 100)

    # ---------------------------------------------------------------- sting: the hit lands on a tritone (D-Ab, 6 st)
    P('low_brass', [[(0, 3.5, ['D2', 'Ab2'], 126)]] + [[]] * 3, sting, articulations='marcato')
    P('tuba', [[(0, 3.5, 'D2', 124)]] + [[]] * 3, sting, articulations='marcato')
    P('horns', [[(0, 3.5, ['D3', 'Ab3'], 120)]] + [[]] * 3, sting, articulations='marcato')
    P('trumpets', [[(0, 1, ['F4', 'Ab4'], 114)]] + [[]] * 3, sting, articulations='marcato')
    P('trombones', [[(0, 1, ['D3', 'Ab3'], 112)]] + [[]] * 3, sting, articulations='marcato')
    P('violins1', ostinato(['D', 'D#', 'E', 'F'], 5, PEAK_V[:4]), sting, articulations='tremolo')
    P('violins2', ostinato(['D', 'D#', 'E', 'F'], 4, [v - 6 for v in PEAK_V[:4]]), sting, articulations='tremolo')
    P('cellos', ostinato(['D', 'D#', 'E', 'F'], 2, [v - 10 for v in PEAK_V[:4]]), sting, articulations='staccato')
    P('basses', chords([nn(r + '1') for r in ['D', 'D#', 'E', 'F']], PEAK_V[:4]), sting)
    P('sub', chords([nn(r + '0') for r in ['D', 'D#', 'E', 'F']], PEAK_V[:4]), sting)
    P('choir', chords([[nn('D4'), nn('Ab4')] for _ in range(4)], [v - 6 for v in PEAK_V[:4]]), sting)
    P('timpani', [[(0, 1, 'D2', 122), (2, 1, 'Ab2', 118)]] * 4, sting)
    o.percussion.note(k['crash'], sting.start, 4, 120).note(k['bass_drum'], sting.start, 2, 122)

    # ---------------------------------------------------------------- cut: it just stops - one hit, then nothing
    P('low_brass', [[(0, 1, ['D2', 'Ab2'], 110)]] + [[]] * 2, cut, articulations='marcato')
    P('choir', [[(0, 1, ['D4', 'Ab4'], 100)]] + [[]] * 2, cut)
    P('timpani', [[(0, 0.3, 'D2', 110)]] + [[]] * 2, cut)
    o.percussion.note(k['bass_drum'], cut.start, 0.5, 115)
    return s
