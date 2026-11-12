"""Amazon Fires - "Devastation arc": a hushed, almost-still forest (solo strings/oboe stating a falling minor-3rd
motif, F5->D5, 3 semitones) swells into a brief, violent tutti (the fire), then collapses to a solo cello alone
restating the same motif - the aftermath. D minor, 100 BPM, 26 bars (~63 s). Built on bands.film_orchestra
(agentsound.bandlib.orchestra); only the preset plus ordinary composition code.

Shaped to sit under narration: the loud/dense tutti is kept to a single 4-bar sting (bars 19-22) rather than a
sustained wall, so a voiceover can run under the hushed open, the rising build and the quiet tail, with the
sting landing on a narration pause / cut. Everything outside that sting stays out of a dense midrange pocket
(bass/sub low, strings/winds high, nothing chordal and loud in the 300 Hz - 2 kHz vocal range).

Build: python -m agentsound build songs/amazon-fires-devastation
"""
from agentsound import *
from agentsound import bands
from agentsound.bandlib import orchestra as orch
from agentsound.theory import note as nn

ANALYSIS = {'profile': 'film'}
METADATA = {'title': 'Amazon Fires - Devastation', 'artist': 'AgentSound', 'album': 'Amazon Fires Sketches',
            'genre': 'Soundtrack'}

W = 4
CHORDS = ['D', 'Bb', 'F', 'C']                        # i - VI - III - VII, two bars each in 'build'
ROOT = {'D': 'D', 'Bb': 'Bb', 'F': 'F', 'C': 'C'}
TRIAD = {'D': ['D', 'F', 'A'], 'Bb': ['Bb', 'D', 'F'], 'F': ['F', 'A', 'C'], 'C': ['C', 'E', 'G']}
SUB = {'D': 'D1', 'Bb': 'F1', 'F': 'F1', 'C': 'C1'}


def part(rows, scale=1.0) -> Clip:
    notes = []
    for i, bar in enumerate(rows):
        for t, d, p, v in bar:
            for q in (p if isinstance(p, (list, tuple)) else [p]):
                notes.append((i * W + t, d, q, max(1, min(127, round(v * scale)))))
    return Clip(notes, length=len(rows) * W)


def ostinato(roots, octave, vel, fifth=False):
    """8ths accented 3+3+2 on each bar's root (the fifth above for the violas)."""
    rows = []
    for r, v in zip(roots, vel):
        p = nn(f"{r}{octave}") + (7 if fifth else 0)
        rows.append([(k * 0.5, 0.35, p + (12 if k == 7 else 0), v + (10 if k in (0, 3, 6) else 0)) for k in range(8)])
    return rows


def two_bars(seq):
    return [c for c in seq for _ in range(2)]


def chords(voicings, vels, beats=W):
    return [[(0, beats, v, vel)] for v, vel in zip(voicings, vels)]


BUILD_V = [34, 38, 42, 46, 50, 54, 58, 62]            # quiet throughout build - the sting carries the shock
PEAK_V = [108, 112, 116, 112, 118, 114, 120, 122]
ROOTS8 = two_bars(CHORDS)


def build() -> Song:
    s = Song('Amazon Fires - Devastation', tempo=100, key='D minor', seed=11, tail=8)
    intro = s.section('intro', bars=8)
    rise = s.section('rise', bars=8, prog=s.prog('i'))
    sting = s.section('sting', bars=4)
    after = s.section('after', bars=6)
    o = bands.film_orchestra(s, hybrid=True)
    P = lambda role, rows, sec, **kw: orch.perform(o, role, part(rows), sec, seed=sum(map(ord, role)), **kw)  # noqa

    # ---------------------------------------------------------------- intro: the forest, almost still
    # the motif: a falling minor 3rd (F5 -> D5, 3 semitones), stated alone, then echoed an octave down by oboe
    P('violins1', [[], [(0, 2, 'F5', 34), (2.5, 1.5, 'D5', 30)], [], [], [], [], [], []], intro,
      articulations='sustain')
    P('oboes', [[], [], [], [(0, 2, 'F4', 36), (2.5, 1.5, 'D4', 30)], [], [], [], []], intro,
      articulations='sustain')
    P('basses', [[(0, 16, 'D1', 26)]] + [[]] * 7, intro, articulations='sustain')
    P('sub', [[(0, 16, 'D0', 22)]] + [[]] * 7, intro)

    # ---------------------------------------------------------------- rise: the fire catching, still hushed
    P('cellos', ostinato([ROOT[c] for c in ROOTS8], 2, BUILD_V), rise, articulations='staccato')
    P('violas', ostinato([ROOT[c] for c in ROOTS8], 3, [v - 6 for v in BUILD_V], fifth=True), rise,
      articulations='staccato')
    P('basses', chords([nn(ROOT[c] + '1') for c in ROOTS8], BUILD_V), rise, shapes='cresc')
    P('sub', chords([nn(ROOT[c] + '0') for c in ROOTS8], [v - 6 for v in BUILD_V]), rise)
    P('choir', chords([[nn(p + '4') for p in TRIAD[c]] for c in ROOTS8], [v - 20 for v in BUILD_V]), rise,
      shapes='cresc')
    P('horns', chords([[nn(ROOT[c] + '3')] for c in ROOTS8], [v - 18 for v in BUILD_V]), rise)
    P('timpani', [[]] * 5 + [[(0, 0.5, 'D2', 50)]] + [[]] + [[(0, 0.5, 'A2', 58), (2, 0.5, 'D2', 62)]], rise)
    k = orch.PERCUSSION_KEYS
    o.percussion.note(k['cymbal_roll'], sting.start - 4.0, 4, 90)      # the swell into the sting

    # ---------------------------------------------------------------- sting: the fire hits (brief - a hit, not a wall)
    P('low_brass', [[(0, 3.5, ['D2', 'A2'], 124)]] + [[]] * 3, sting, articulations='marcato')
    P('tuba', [[(0, 3.5, 'D2', 122)]] + [[]] * 3, sting, articulations='marcato')
    P('horns', [[(0, 3.5, ['D3', 'A3'], 118)]] + [[]] * 3, sting, articulations='marcato')
    P('trumpets', [[(0, 1, ['F4', 'A4'], 112)]] + [[]] * 3, sting, articulations='marcato')
    P('trombones', [[(0, 1, ['D3', 'F3'], 110)]] + [[]] * 3, sting, articulations='marcato')
    P('violins1', ostinato(['D', 'Bb', 'F', 'C'], 5, PEAK_V[:4]), sting, articulations='tremolo')
    P('violins2', ostinato(['D', 'Bb', 'F', 'C'], 4, [v - 6 for v in PEAK_V[:4]]), sting, articulations='tremolo')
    P('cellos', ostinato(['D', 'Bb', 'F', 'C'], 2, [v - 10 for v in PEAK_V[:4]]), sting, articulations='staccato')
    P('basses', chords([nn(c + '1') for c in ['D', 'Bb', 'F', 'C']], PEAK_V[:4]), sting)
    P('sub', chords([nn(c + '0') for c in ['D', 'Bb', 'F', 'C']], PEAK_V[:4]), sting)
    P('choir', chords([[nn(p + '4') for p in TRIAD[c]] for c in ['D', 'Bb', 'F', 'C']],
                      [v - 8 for v in PEAK_V[:4]]), sting)
    P('timpani', [[(0, 1, 'D2', 120), (2, 1, 'A2', 112)]] * 4, sting)
    o.percussion.note(k['crash'], sting.start, 4, 118).note(k['bass_drum'], sting.start, 2, 120)
    o.percussion.note(k['tam_tam'], sting.bar(2), 6, 96)

    # ---------------------------------------------------------------- after: the aftermath, the motif alone
    P('cellos', [[(0, 2, 'F3', 44), (2.5, 1.5, 'D3', 36)]] + [[]] * 5, after, articulations='sustain')
    P('violins1', [[], [(0, 3, ['D5', 'F5'], 24)], [], [], [], []], after, articulations='tremolo')
    P('choir', [[], [], [(0, 4, ['D4', 'F4'], 22)], [], [], []], after)
    P('basses', [[(0, 6, 'D1', 20)]] + [[]] * 5, after, articulations='sustain')
    o.percussion.note(k['tam_tam'], after.bar(4), 10, 60)
    orch.ring(o, after.bar(5), length=4, db=2, roles=[r for r in o.roles if r not in ('drums', 'sub', 'pulse')])
    return s
