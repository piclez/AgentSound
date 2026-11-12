"""Amazon Fires - "Elegy with hope": identical arc to the devastation version through the sting (hushed forest,
the falling minor-3rd motif F5->D5, a brief violent tutti), but the aftermath resolves instead of just fading -
the motif returns INVERTED (rising: D5->F5, the same 3 semitones, now ascending) and the final chord raises the
minor 3rd (F) to a major 3rd (F#, a picardy third, +1 semitone) under a warm high choir - devastation giving way
to resilience rather than pure loss. D minor -> D major close, 100 BPM, 26 bars (~63 s). Built on
bands.film_orchestra (agentsound.bandlib.orchestra).

Shaped to sit under narration like the other two arcs: loud/dense only in the 4-bar sting.

Build: python -m agentsound build songs/amazon-fires-hope
"""
from agentsound import *
from agentsound import bands
from agentsound.bandlib import orchestra as orch
from agentsound.theory import note as nn

ANALYSIS = {'profile': 'film'}
METADATA = {'title': 'Amazon Fires - Elegy With Hope', 'artist': 'AgentSound', 'album': 'Amazon Fires Sketches',
            'genre': 'Soundtrack'}

W = 4
CHORDS = ['D', 'Bb', 'F', 'C']                        # i - VI - III - VII, two bars each in 'build'
ROOT = {'D': 'D', 'Bb': 'Bb', 'F': 'F', 'C': 'C'}
TRIAD = {'D': ['D', 'F', 'A'], 'Bb': ['Bb', 'D', 'F'], 'F': ['F', 'A', 'C'], 'C': ['C', 'E', 'G']}


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


def two_bars(seq):
    return [c for c in seq for _ in range(2)]


def chords(voicings, vels, beats=W):
    return [[(0, beats, v, vel)] for v, vel in zip(voicings, vels)]


BUILD_V = [34, 38, 42, 46, 50, 54, 58, 62]
PEAK_V = [108, 112, 116, 112, 118, 114, 120, 122]
ROOTS8 = two_bars(CHORDS)


def build() -> Song:
    s = Song('Amazon Fires - Elegy With Hope', tempo=100, key='D minor', seed=11, tail=10)
    intro = s.section('intro', bars=8)
    rise = s.section('rise', bars=8, prog=s.prog('i'))
    sting = s.section('sting', bars=4)
    after = s.section('after', bars=6)
    o = bands.film_orchestra(s, hybrid=True)
    s.master.add_fx(fx.width(monobass=120), first=True)   # keep < 120 Hz mono - phone/mono playback safe
    P = lambda role, rows, sec, **kw: orch.perform(o, role, part(rows), sec, seed=sum(map(ord, role)), **kw)  # noqa

    # ---------------------------------------------------------------- intro: the forest, almost still (as devastation)
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
    o.percussion.note(k['cymbal_roll'], sting.start - 4.0, 4, 90)

    # ---------------------------------------------------------------- sting: the fire hits (as devastation)
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

    # ---------------------------------------------------------------- after: the motif returns INVERTED (rising,
    # D5->F5, same 3 semitones) and the final chord raises F to F# - a picardy third (+1 semitone) into D major
    P('cellos', [[(0, 2, 'D3', 40), (2.5, 1.5, 'F3', 42)]] + [[]] * 5, after, articulations='sustain')
    P('violins1', [[], [(0, 1.5, 'D5', 38), (1.5, 2.5, 'F5', 40)], [], [(0, 4, ['D5', 'F#5'], 44)], [], []], after,
      articulations='sustain')
    P('oboes', [[], [], [(0, 1.5, 'D4', 34), (1.5, 2.5, 'F#4', 38)], [], [], []], after, articulations='sustain')
    P('choir', [[], [], [], [(0, 4, ['D4', 'F#4', 'A4'], 24)], [(0, 4, ['D4', 'F#4', 'A4'], 22)], []], after)
    P('basses', [[(0, 3, 'D1', 30)], [], [], [(0, 8, 'D1', 26)]] + [[]] * 2, after, articulations='sustain')
    o.percussion.note(k['tam_tam'], after.bar(3), 12, 70)
    orch.ring(o, after.bar(5), length=6, db=3, roles=[r for r in o.roles if r not in ('drums', 'sub', 'pulse')])
    return s
