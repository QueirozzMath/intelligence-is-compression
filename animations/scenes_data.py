"""Cenas B1–B6: resultados 2D do pipeline."""
from manimlib import *
import numpy as np

from animations.common import *


class B1NCDHeatmap(Scene):
    def construct(self):
        frame = table("exp2_ncd_lzma.csv", index_col=0)
        heading = title("A matriz NCD ganha estrutura")
        cells = VGroup()
        maximum = frame.to_numpy().max()
        for row in range(len(frame)):
            for column in range(len(frame)):
                value = frame.iloc[row, column]
                square = Square(side_length=0.52, fill_color=interpolate_color(BLUE_E, YELLOW, value / maximum), fill_opacity=0.9, stroke_width=0.5)
                number = Text(f"{value:.2f}", font_size=13).move_to(square)
                cells.add(VGroup(square, number).shift(RIGHT * column * 0.52 + DOWN * row * 0.52))
        cells.center().shift(DOWN * 0.35)
        self.play(Write(heading))
        self.play(LaggedStart(*[FadeIn(cell) for cell in cells], lag_ratio=0.015), run_time=5)
        self.wait(3)


class B2GrowingDendrogram(Scene):
    def construct(self):
        links = table("dendrogram_linkage.csv")
        labels = table("mds3d_areas.csv").area.tolist()
        heading = title("A árvore cresce das fusões mais próximas")
        nodes = {index: area_label(area).move_to(LEFT * 5 + UP * (3 - index * 0.65)) for index, area in enumerate(labels)}
        self.play(Write(heading), LaggedStart(*[FadeIn(node) for node in nodes.values()], lag_ratio=0.08))
        for step, row in enumerate(links.itertuples()):
            left, right = nodes[int(row.left)], nodes[int(row.right)]
            parent_position = np.array([min(4.5, -4 + 7 * row.height / max(links.height)), (left.get_y() + right.get_y()) / 2, 0])
            parent = Dot(parent_position, color=YELLOW)
            branches = VGroup(Line(left.get_right(), parent_position), Line(right.get_right(), parent_position))
            self.play(ShowCreation(branches), FadeIn(parent), run_time=0.7)
            nodes[len(labels) + step] = parent
        self.wait(3)


class B3WordsCarryBits(Scene):
    def construct(self):
        data = table("exp5_word_contributions.csv")
        heading = title("Palavras especializadas carregam os bits")
        self.play(Write(heading))
        for pair_type, group in data.groupby("pair_type", sort=False):
            group = group.nsmallest(10, "rank").sort_values("contribution")
            bars = VGroup()
            scale = 6 / max(group.contribution.max(), 1e-9)
            for row in group.itertuples():
                bar = Rectangle(width=max(0.05, row.contribution * scale), height=0.38, fill_color=BLUE, fill_opacity=0.8, stroke_width=0)
                label = Text(row.word, font_size=22).next_to(bar, LEFT)
                bars.add(VGroup(label, bar))
            bars.arrange(DOWN, aligned_edge=LEFT, buff=0.09).shift(DOWN * 0.4)
            caption = Text(f"{pair_type}: {group.area_a.iloc[0]} → {group.area_b.iloc[0]}", font_size=30).next_to(heading, DOWN)
            self.play(Write(caption), LaggedStart(*[GrowFromEdge(row[1], LEFT) for row in bars], lag_ratio=0.08), FadeIn(VGroup(*[row[0] for row in bars])))
            self.wait(2)
            self.play(FadeOut(caption), FadeOut(bars))


class B4LossVsData(Scene):
    def construct(self):
        data = table("exp4_loss_curve.csv")
        area = data.groupby("area").bpc.apply(lambda values: values.iloc[0] - values.iloc[-1]).idxmax()
        group = data[data.area == area].sort_values("train_chars")
        heading = title("Mais dados compram menos bits por caractere")
        x = np.log10(group.train_chars.to_numpy())
        y = group.bpc.to_numpy()
        points = np.column_stack(((x - x.min()) / max(np.ptp(x), 1e-9) * 10 - 5, (y - y.min()) / max(np.ptp(y), 1e-9) * 4 - 2, np.zeros(len(x))))
        curve = VMobject(color=AREA_COLORS[area], stroke_width=6).set_points_smoothly(points)
        dot = Dot(points[0], color=YELLOW)
        counter = Text(f"{y[0]:.2f} bpc", font_size=34).to_corner(UR)
        self.play(Write(heading), ShowCreation(curve))
        for point, value in zip(points[1:], y[1:]):
            new_counter = Text(f"{value:.2f} bpc", font_size=34).to_corner(UR)
            self.play(dot.animate.move_to(point), Transform(counter, new_counter), run_time=0.8)
        self.wait(3)


class B5ClassifyingAbstract(Scene):
    def construct(self):
        examples = json_data("manim_classification_examples.json")
        heading = title("Vence o modelo que gasta menos bits")
        self.play(Write(heading))
        for example in examples:
            excerpt = Text(example["text"][:260] + "…", font_size=23, line_spacing=1.2).set_width(11).next_to(heading, DOWN)
            ordered = sorted(example["bpc"].items(), key=lambda item: item[1])[:5]
            scores = VGroup(*[Text(f"{area}: {score:.2f} bpc", font_size=28, color=AREA_COLORS[area]) for area, score in ordered]).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN)
            verdict = Text(f"{example['kind']}: {example['true_area']} → {example['predicted_area']}", font_size=32).to_corner(DR)
            self.play(FadeIn(excerpt), LaggedStart(*[FadeIn(score) for score in scores], lag_ratio=0.15))
            self.play(Write(verdict))
            self.wait(2)
            self.play(FadeOut(excerpt), FadeOut(scores), FadeOut(verdict))


class B6KLAsymmetry(Scene):
    def construct(self):
        data = table("exp4_asymmetry.csv").head(5)
        heading = title("KL tem direção: A → B não é B → A")
        self.play(Write(heading))
        rows = VGroup()
        maximum = max(data.kl_a_b.max(), data.kl_b_a.max(), 1e-9)
        for record in data.itertuples():
            left = area_label(record.area_a)
            right = area_label(record.area_b)
            arrow_ab = Arrow(LEFT, RIGHT, stroke_width=2 + 12 * record.kl_a_b / maximum, color=ORANGE)
            arrow_ba = Arrow(RIGHT, LEFT, stroke_width=2 + 12 * record.kl_b_a / maximum, color=BLUE).shift(DOWN * 0.2)
            row = VGroup(left, VGroup(arrow_ab, arrow_ba), right).arrange(RIGHT, buff=0.45)
            rows.add(row)
        rows.arrange(DOWN, buff=0.45).shift(DOWN * 0.4)
        self.play(LaggedStart(*[FadeIn(row) for row in rows], lag_ratio=0.2), run_time=4)
        self.wait(3)
