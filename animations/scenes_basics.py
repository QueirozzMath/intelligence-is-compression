"""Cenas A1–A4: conceitos fundamentais com valores exportados."""
from manimlib import *
import numpy as np

from animations.common import *


class A1CompressionPrediction(Scene):
    def construct(self):
        data = table("manim_next_char.csv")
        heading = title("Comprimir é prever")
        context = Text(f"Contexto real: …{data.context.iloc[0]}", font_size=34)
        context.next_to(heading, DOWN)
        bars = VGroup()
        for row in data.head(8).itertuples():
            bar = Rectangle(width=max(0.12, 8 * row.probability), height=0.48, fill_color=BLUE, fill_opacity=0.8, stroke_width=0)
            label = Text(repr(row.symbol), font_size=25).next_to(bar, LEFT)
            bits = Text(f"{(-np.log2(row.probability)):.2f} bits", font_size=23).next_to(bar, RIGHT)
            bars.add(VGroup(label, bar, bits))
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.15).shift(DOWN * 0.7)
        self.play(Write(heading), FadeIn(context))
        self.play(LaggedStart(*[GrowFromEdge(group[1], LEFT) for group in bars], lag_ratio=0.12), run_time=4)
        self.play(LaggedStart(*[FadeIn(VGroup(group[0], group[2])) for group in bars], lag_ratio=0.1))
        self.wait(3)


class A2CrossEntropyWaste(Scene):
    def construct(self):
        matrix = table("exp4_cross_entropy.csv", index_col=0)
        kl = table("exp4_kl.csv", index_col=0)
        area_a, area_b = matrix.index[0], matrix.index[1]
        hp = matrix.loc[area_a, area_a]
        hpq = matrix.loc[area_a, area_b]
        divergence = kl.loc[area_a, area_b]
        heading = title("Entropia cruzada mede os bits desperdiçados")
        base = Rectangle(width=3, height=hp, fill_color=BLUE, fill_opacity=0.85).to_edge(DOWN)
        extra = Rectangle(width=3, height=divergence, fill_color=ORANGE, fill_opacity=0.9).next_to(base, UP, buff=0)
        equation = Text(f"H({area_a},{area_b}) = H({area_a}) + KL = {hpq:.2f} bpc", font_size=32).next_to(heading, DOWN)
        self.play(Write(heading), Write(equation))
        self.play(GrowFromEdge(base, DOWN), GrowFromEdge(extra, DOWN), run_time=3)
        self.play(Indicate(extra, color=YELLOW))
        self.wait(3)


class A3NCDMechanism(Scene):
    def construct(self):
        data = table("manim_ncd_examples.csv")
        heading = title("NCD pergunta quanto A ajuda a comprimir B")
        self.play(Write(heading))
        for row in data.itertuples():
            bars = VGroup(
                Rectangle(width=4, height=0.7, color=AREA_COLORS[row.area_a], fill_opacity=0.8),
                Rectangle(width=4, height=0.7, color=AREA_COLORS[row.area_b], fill_opacity=0.8),
            ).arrange(DOWN).shift(LEFT * 2)
            result = Text(f"{row.pair_type}: {row.area_a} + {row.area_b}\nNCD = {row.ncd:.3f}", font_size=34).shift(RIGHT * 3)
            self.play(FadeIn(bars), Write(result))
            compressed_widths = [4 * row.compressed_a / row.bytes_a, 4 * row.compressed_b / row.bytes_b]
            targets = VGroup(*[Rectangle(width=max(0.2, width), height=0.7, color=bars[i].get_color(), fill_opacity=0.8) for i, width in enumerate(compressed_widths)]).arrange(DOWN).move_to(bars)
            self.play(Transform(bars, targets), run_time=2)
            self.wait(2)
            self.play(FadeOut(bars), FadeOut(result))
        self.wait(2)


class A4GzipWindow(Scene):
    def construct(self):
        data = table("exp3_window.csv")
        heading = title("O gzip esquece relações além de sua janela")
        strip = Rectangle(width=11, height=0.8, color=GREY_B, fill_opacity=0.35)
        window = Rectangle(width=2.3, height=1.1, color=YELLOW).move_to(strip.get_left() + RIGHT * 1.2)
        window_kb = int(data.gzip_window_bytes.iloc[0] / 1024)
        label = Text(f"{window_kb} KB", font_size=28).next_to(window, UP)
        self.play(Write(heading), FadeIn(strip), ShowCreation(window), Write(label))
        self.play(window.animate.shift(RIGHT * 8.5), run_time=4, rate_func=linear)
        rows = VGroup(*[Text(f"{row.compressor}: {row.separation:.3f} em {int(row.bytes):,} bytes", font_size=26) for row in data.groupby("compressor").tail(1).itertuples()]).arrange(DOWN).to_edge(DOWN)
        self.play(FadeIn(rows))
        self.wait(3)
