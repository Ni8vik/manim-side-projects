

"""
Fatemeh's 17th Birthday Animation
-----------------------------------
Run with:  manim -pqh fatemeh_birthday.py BirthdayScene
 
-pqh = preview, quality high. Use -pql for a quick low-quality preview instead.
"""
 
from manim import *
import random
 
 
def make_jet(color=WHITE, accent=GREY_B):
    """A simple sleek fighter-jet silhouette pointing right (+X direction)."""
    body_pts = [
        [1.5, 0, 0],
        [0.55, 0.13, 0],
        [0.15, 0.6, 0],
        [-0.05, 0.6, 0],
        [-0.25, 0.16, 0],
        [-1.4, 0.11, 0],
        [-1.4, -0.11, 0],
        [-0.25, -0.16, 0],
        [-0.05, -0.6, 0],
        [0.15, -0.6, 0],
        [0.55, -0.13, 0],
    ]
    jet = Polygon(*body_pts, color=accent, fill_color=color, fill_opacity=1, stroke_width=1.5)
    cockpit = Ellipse(width=0.35, height=0.16, color=BLUE_C, fill_opacity=0.9).move_to([0.7, 0, 0])
    jet_group = VGroup(jet, cockpit)
    return jet_group
 
 
class BirthdayScene(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
 
        # ---------- Part 1: Name intro ----------
        name = Text("Fatemeh", font_size=96, weight=BOLD, gradient=(PINK, GOLD, PURPLE))
        self.play(Write(name), run_time=2)
        self.play(
            name.animate.scale(0.6).to_edge(UP, buff=1),
            run_time=1.2,
        )
 
        # ---------- Part 2: Jet flyby ----------
        jets = VGroup()
        trails = VGroup()
        heights = [2.6, 1.8, 1.0]
        for h in heights:
            jet = make_jet().scale(0.6)
            jet.move_to([-9, h, 0])
            trail = TracedPath(
                jet.get_center,
                stroke_color=WHITE,
                stroke_width=3,
                stroke_opacity=0.5,
                dissipating_time=0.4,
            )
            trails.add(trail)
            jets.add(jet)
 
        self.add(trails, jets)
        self.play(
            LaggedStart(
                *[
                    jet.animate.move_to([9, jet.get_center()[1], 0])
                    for jet in jets
                ],
                lag_ratio=0.25,
            ),
            run_time=2.2,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.remove(trails, jets)
        self.wait(0.2)
 
        # ---------- Part 3: Balloons rising ----------
        balloon_colors = [RED, BLUE, YELLOW, GREEN, PINK, ORANGE, PURPLE]
        balloons = VGroup()
        for i in range(9):
            color = random.choice(balloon_colors)
            balloon = Ellipse(width=0.8, height=1.0, color=color, fill_opacity=0.9)
            string = Line(balloon.get_bottom(), balloon.get_bottom() + DOWN * 0.6, stroke_width=1.5)
            group = VGroup(balloon, string)
            x = -5.5 + i * 1.4 + random.uniform(-0.3, 0.3)
            group.move_to([x, -4, 0])
            balloons.add(group)
 
        self.play(
            LaggedStart(
                *[
                    b.animate.move_to([b.get_center()[0], random.uniform(0.5, 2.2), 0])
                    for b in balloons
                ],
                lag_ratio=0.1,
            ),
            run_time=2.5,
        )
 
        # ---------- Part 4: "Happy Birthday" text ----------
        happy = Text("Happy Birthday!", font_size=64, color=WHITE, weight=BOLD)
        happy.move_to(ORIGIN)
        self.play(FadeIn(happy, shift=UP), run_time=1.2)
        self.wait(0.5)
        self.play(FadeOut(happy, shift=UP))
 
        # ---------- Part 5: The big number 17 ----------
        seventeen = Text("17", font_size=220, weight=BOLD)
        seventeen.set_color_by_gradient(GOLD, YELLOW, PINK)
        self.play(
            FadeOut(balloons, shift=DOWN * 0.3),
            GrowFromCenter(seventeen),
            run_time=1.5,
        )
        self.play(
            seventeen.animate.set_color_by_gradient(PINK, PURPLE, GOLD),
            run_time=1.5,
        )
        self.wait(0.3)
 
        # A jet streaks behind the number for extra flair
        hero_jet = make_jet().scale(0.9).move_to([-9, 0, 0])
        hero_trail = TracedPath(
            hero_jet.get_center,
            stroke_color=GOLD,
            stroke_width=4,
            stroke_opacity=0.6,
            dissipating_time=0.5,
        )
        self.add(hero_trail, hero_jet)
        seventeen_z = seventeen.z_index if hasattr(seventeen, "z_index") else 0
        hero_jet.set_z_index(seventeen_z + 1)
        self.play(
            hero_jet.animate.move_to([9, 0, 0]),
            run_time=1.4,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.remove(hero_trail, hero_jet)
 
        # ---------- Part 6: Confetti burst ----------
        confetti = VGroup()
        for _ in range(60):
            shape_type = random.choice(["square", "circle", "triangle"])
            color = random.choice(balloon_colors)
            if shape_type == "square":
                shape = Square(side_length=0.15, color=color, fill_opacity=1)
            elif shape_type == "circle":
                shape = Circle(radius=0.08, color=color, fill_opacity=1)
            else:
                shape = Triangle(color=color, fill_opacity=1).scale(0.1)
            shape.move_to(ORIGIN)
            confetti.add(shape)
 
        self.add(confetti)
        anims = []
        for piece in confetti:
            angle = random.uniform(0, TAU)
            distance = random.uniform(3, 7)
            target = np.array(
                [distance * np.cos(angle), distance * np.sin(angle) + random.uniform(-1, 1), 0]
            )
            anims.append(
                piece.animate.move_to(target).rotate(random.uniform(-3, 3)).set_opacity(0)
            )
        self.play(*anims, run_time=2.5, rate_func=rate_functions.ease_out_cubic)
 
        # ---------- Part 7: Final message ----------
        self.play(seventeen.animate.scale(0.35).to_edge(UP, buff=1.5), FadeOut(name))
        final_msg = Text(
            "  Wishing you a year full of joy,\nlaughter, and amazing memories!\n     with me ;)",
            font_size=40,
            line_spacing=1.2,
        ).set_color_by_gradient(WHITE, PINK)
        final_msg.move_to(ORIGIN)
        self.play(Write(final_msg), run_time=2.5)
        self.wait(1)
 
        signature = Text("From your nima, with love!", font_size=28, color=GRAY_B)
        signature.next_to(final_msg, DOWN, buff=0.8)
        self.play(FadeIn(signature, shift=UP * 0.3))
        self.wait(2)
 
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)
 
