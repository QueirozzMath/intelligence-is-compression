"""Cenas C1–C3 em 3D, com coordenadas derivadas dos resultados."""
from manimlib import *
import numpy as np

from animations.common import *


class C1KnowledgeMap3D(ThreeDScene):
    def construct(self):
        data = table("mds3d_areas.csv")
        points = normalized_points(data, ("x", "y", "z"), 3.2)
        heading = title("Áreas próximas compartilham regularidades comprimíveis")
        heading.fix_in_frame()
        objects = VGroup()
        for point, row in zip(points, data.itertuples()):
            sphere = Sphere(radius=0.14, color=AREA_COLORS[row.area]).move_to(point)
            label = area_label(row.area, 22).next_to(sphere, UP)
            label.fix_orientation()
            objects.add(VGroup(sphere, label))
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.add_fixed_in_frame_mobjects(heading)
        self.play(LaggedStart(*[FadeIn(item) for item in objects], lag_ratio=0.12), run_time=4)
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(8)
        self.stop_ambient_camera_rotation()


class C2ArticlesCloud3D(ThreeDScene):
    def construct(self):
        data = table("pca3d_articles.csv")
        points = normalized_points(data, ("x", "y", "z"), 3.4)
        heading = title(f"{len(data):,} resumos formam regiões — sem embeddings")
        heading.fix_in_frame()
        self.set_camera_orientation(phi=70 * DEGREES, theta=-55 * DEGREES)
        self.add_fixed_in_frame_mobjects(heading)
        clouds = VGroup()
        for area in data.area.unique():
            mask = data.area.to_numpy() == area
            cloud = DotCloud(points[mask], color=AREA_COLORS[area], radius=0.035)
            clouds.add(cloud)
            self.play(FadeIn(cloud), run_time=0.7)
        if data.cross_list.any():
            mask = data.cross_list.astype(bool).to_numpy()
            cross = DotCloud(points[mask], color=WHITE, radius=0.08)
            self.play(FadeIn(cross), Flash(cross.get_center()))
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(10)
        self.stop_ambient_camera_rotation()


class C3CrossEntropyLandscape(ThreeDScene):
    def construct(self):
        data = table("manim_simplex_p.csv")
        p = data.probability.to_numpy(float)
        epsilon = 0.025

        def entropy_height(u, v):
            q = np.array([u, v, max(epsilon, 1 - u - v)])
            q = np.maximum(q, epsilon)
            q /= q.sum()
            return -float(np.sum(p * np.log2(q)))

        surface = ParametricSurface(
            lambda u, v: np.array([(u - 0.5) * 7, (v - 0.5) * 7, entropy_height(u, v) - 1]),
            u_range=(epsilon, 1 - 2 * epsilon), v_range=(epsilon, 1 - 2 * epsilon),
            resolution=(28, 28), color=BLUE_D, opacity=0.75,
        )
        heading = title("A entropia cruzada é mínima quando Q = P")
        heading.fix_in_frame()
        self.set_camera_orientation(phi=68 * DEGREES, theta=-52 * DEGREES)
        self.add_fixed_in_frame_mobjects(heading)
        self.play(ShowCreation(surface), run_time=4)
        q = np.array([0.75, 0.15, 0.10])
        path = []
        for _ in range(18):
            q = 0.78 * q + 0.22 * p
            path.append(np.array([(q[0] - 0.5) * 7, (q[1] - 0.5) * 7, entropy_height(q[0], q[1]) - 0.85]))
        ball = Sphere(radius=0.10, color=YELLOW).move_to(path[0])
        self.play(FadeIn(ball))
        for point in path[1:]:
            self.play(ball.animate.move_to(point), run_time=0.18, rate_func=linear)
        self.wait(4)
