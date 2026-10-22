from manim import *
import numpy as np

class RocketOrbitMission(Scene):
    def construct(self):

        # -----------------------------
        # 1️⃣ GROUND & SKY
        # -----------------------------
        sky = Rectangle(width=20, height=12, fill_color=BLUE_E, fill_opacity=1)
        ground = Rectangle(width=20, height=3, fill_color=GREEN_D, fill_opacity=1)
        ground.move_to(DOWN*3)

        self.add(sky, ground)

        # -----------------------------
        # 2️⃣ ROCKET DESIGN
        # -----------------------------
        body = Rectangle(height=1.8, width=0.4, fill_color=WHITE, fill_opacity=1)
        nose = Triangle(fill_color=RED, fill_opacity=1).scale(0.3)
        nose.next_to(body, UP, buff=0)

        left_fin = Triangle(fill_color=GRAY, fill_opacity=1).scale(0.2)
        right_fin = left_fin.copy()

        left_fin.next_to(body, DOWN+LEFT, buff=-0.1)
        right_fin.next_to(body, DOWN+RIGHT, buff=-0.1)

        rocket = VGroup(body, nose, left_fin, right_fin)
        rocket.move_to(DOWN*2)

        # Flame
        flame = Triangle(fill_color=ORANGE, fill_opacity=0.9).scale(0.25)
        flame.rotate(PI)
        flame.next_to(body, DOWN, buff=0)

        self.play(FadeIn(rocket))
        self.wait(1)

        # -----------------------------
        # 3️⃣ LAUNCH ANIMATION
        # -----------------------------
        self.play(
            rocket.animate.shift(UP*4),
            FadeIn(flame),
            run_time=3,
            rate_func=smooth
        )

        # Sky darkens
        self.play(sky.animate.set_fill(BLACK), run_time=2)

        self.remove(ground)

        # -----------------------------
        # 4️⃣ EARTH APPEARS
        # -----------------------------
        earth = Circle(radius=2, color=BLUE, fill_opacity=1)
        earth.set_fill(BLUE_D)
        earth.move_to(ORIGIN)

        self.play(
            rocket.animate.move_to(UP*2.5),
            FadeIn(earth),
            run_time=2
        )

        # -----------------------------
        # 5️⃣ CIRCULAR ORBIT
        # -----------------------------
        orbit_path = Circle(radius=3, color=WHITE)
        self.play(Create(orbit_path))

        # Move rocket into orbit position
        rocket.move_to(orbit_path.point_from_proportion(0))

        self.play(
            MoveAlongPath(rocket, orbit_path),
            run_time=8,
            rate_func=linear
        )

        # -----------------------------
        # 6️⃣ ORBIT CHANGES TO ELLIPSE
        # -----------------------------
        ellipse_path = Ellipse(width=8, height=5, color=YELLOW)

        self.play(
            Transform(orbit_path, ellipse_path),
            run_time=4
        )

        self.play(
            MoveAlongPath(rocket, orbit_path),
            run_time=6,
            rate_func=linear
        )

        self.wait(2)