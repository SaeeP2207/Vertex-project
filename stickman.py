from manim import *
import numpy as np

class Moving_Stickman(Scene):
    def construct(self):

        self.add_sound("trimmed_music.wav") 

        bg = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            stroke_width=0
        ).set_fill(
            color=["#2C2C54", "#40407A"],  
            opacity=1,

        )
        self.add(bg)

        ground = Rectangle(
            width=14,
            height=1.5,
            fill_color=[GREEN],
            fill_opacity=1,
            stroke_color=GREEN
        )
        ground.move_to([0, -2.7, 0])
        self.play(Create(ground), run_time=2)

        def create_tree(x_pos):
            trunk = Rectangle(width=0.3,height=1.5,fill_color="#6B3E26",fill_opacity=1,stroke_width=0)
            trunk.move_to([x_pos, -1.9, 0])
            leaves = VGroup(Circle(radius=0.8, color=GREEN, fill_opacity=1),Circle(radius=0.7, color=GREEN_D, fill_opacity=1),Circle(radius=0.6, color=GREEN_E, fill_opacity=1),)
            leaves.arrange(DOWN, buff=-0.4)
            leaves.move_to(trunk.get_top() + UP*0.6)
            tree = VGroup(trunk, leaves)
            return tree

        tree_left = create_tree(-6)
        tree_right = create_tree(6)
        self.play(FadeIn(tree_left), FadeIn(tree_right))




        grass = VGroup()
        for i in range(2500):
            x = np.random.uniform(-7, 7)
            y = np.random.uniform(-2.7, -2) 

            blade = Line([x, y, 0],[x + np.random.uniform(-0.1, 0.1), y + np.random.uniform(0.1, 0.3), 0],stroke_width=2,color=GREEN_E)
            grass.add(blade)
            self.add(grass)

        walk = ValueTracker(-5)
        dance_t = ValueTracker(0)

        core = 1.0
        thigh = 0.5
        shin = 0.7
        arm = 0.4
        forearm = 0.4
        head = Circle(radius=0.3, color=WHITE)
        body = Line(ORIGIN, ORIGIN, color=WHITE)
        thigh_L = Line(ORIGIN, ORIGIN)
        shin_L  = Line(ORIGIN, ORIGIN)
        foot_L  = Line(ORIGIN, ORIGIN)
        thigh_R = Line(ORIGIN, ORIGIN)
        shin_R  = Line(ORIGIN, ORIGIN)
        foot_R  = Line(ORIGIN, ORIGIN)
        arm_L = Line(ORIGIN, ORIGIN)
        forearm_L = Line(ORIGIN, ORIGIN)
        arm_R = Line(ORIGIN, ORIGIN)
        forearm_R = Line(ORIGIN, ORIGIN)

        bow_left = Triangle(
            fill_color=RED,
            fill_opacity=1,
            stroke_color=RED
        )
        bow_left.scale(0.09)
        bow_left.rotate(-PI/2)
        bow_right = Triangle(
            fill_color=RED,
            fill_opacity=1,
            stroke_color=RED
        )
        bow_right.scale(0.09)
        bow_right.rotate(PI/2)
        bow_knot = Circle(
            radius=0.02,
            fill_color=RED,
            fill_opacity=1,
            stroke_color=RED
        )

        stickman = VGroup(
            head, body,
            thigh_L, shin_L,
            thigh_R, shin_R,
            arm_L, forearm_L,
            arm_R, forearm_R,
            bow_left, bow_right, bow_knot
        )
        self.add(stickman)
        direction = ValueTracker(1)

        def update_man(m):
            t = self.time
            freq = 3
            bounce = 0.05 * abs(np.sin(freq*t))
            hip = np.array([walk.get_value(), -1.5 + bounce, 0])
            shoulder = hip + UP * 1.0
            body.put_start_and_end_on(shoulder, hip)
            head.move_to(shoulder + UP*0.3)
            swing = 0.6 * np.sin(freq*t)
            knee_L = hip + 0.5 * np.array([
                direction.get_value()*np.sin(swing),
                -np.cos(swing),
                0
            ])
            ankle_L = knee_L + 0.7 * np.array([
                direction.get_value()*np.sin(swing),
                -np.cos(swing),
                0
            ])
            thigh_L.put_start_and_end_on(hip, knee_L)
            shin_L.put_start_and_end_on(knee_L, ankle_L)
            foot_L.put_start_and_end_on(ankle_L, ankle_L + direction.get_value()*RIGHT*0.4)
            swing_R = -swing
            knee_R = hip + 0.5 * np.array([
                direction.get_value()*np.sin(swing_R),
                -np.cos(swing_R),
                0
            ])
            ankle_R = knee_R + 0.7 * np.array([
                direction.get_value()*np.sin(swing_R),
                -np.cos(swing_R),
                0
            ])
            thigh_R.put_start_and_end_on(hip, knee_R)
            shin_R.put_start_and_end_on(knee_R, ankle_R)
            foot_R.put_start_and_end_on(ankle_R, ankle_R + direction.get_value()*RIGHT*0.4)
            arm_swing = -swing
            elbow_L = shoulder + 0.5 * np.array([
                direction.get_value()*np.sin(arm_swing),
                -np.cos(arm_swing),
                0
            ])
            hand_L = elbow_L + 0.4 * np.array([
                np.sin(arm_swing),
                -np.cos(arm_swing),
                0
            ])
            arm_L.put_start_and_end_on(shoulder, elbow_L)
            forearm_L.put_start_and_end_on(elbow_L, hand_L)
            elbow_R = shoulder + 0.5 * np.array([
                direction.get_value()*np.sin(-arm_swing),
                -np.cos(-arm_swing),
                0
            ])
            hand_R = elbow_R + 0.4 * np.array([
                np.sin(-arm_swing),
                -np.cos(-arm_swing),
                0
            ])
            arm_R.put_start_and_end_on(shoulder, elbow_R)
            forearm_R.put_start_and_end_on(elbow_R, hand_R)
            bow_center = shoulder + DOWN*0.05
            bow_knot.move_to(bow_center)
            bow_left.next_to(bow_knot , LEFT, buff=0)
            bow_right.next_to(bow_knot ,RIGHT, buff=0)

        stickman.add_updater(update_man)

        self.play(
            walk.animate.set_value(4),
            run_time=6,
            rate_func=linear
        )
        self.play(direction.animate.set_value(-1),run_time=0.4)
        self.play(walk.animate.set_value(0),run_time=4,rate_func=linear)
        self.wait()
        arm_open = ValueTracker(0)
        wave_t = ValueTracker(0)
        stickman.remove_updater(update_man)

        def pose_front():
            hip = np.array([0 , -1.5, 0])
            shoulder = hip + UP*1
            body.put_start_and_end_on(neck,hip)
            head.move_to(neck + UP * 0.3)
            knee_L = hip + DOWN * 0.5
            ankle_L = knee_L + DOWN * 0.7
            thigh_L.put_start_and_end_on(hip,knee_L)
            shin_L.put_start_and_end_on(knee_L,ankle_L)
            foot_L.put_start_and_end_on(ankle_L,ankle_L+LEFT*0.3)
            knee_L = hip + DOWN*0.5
            ankle_L = knee_L + DOWN*0.7
            thigh_L.put_start_and_end_on(hip, knee_L)
            shin_L.put_start_and_end_on(knee_L, ankle_L)
            foot_L.put_start_and_end_on(ankle_L, ankle_L + LEFT*0.3)
            knee_R = hip + DOWN*0.5
            ankle_R = knee_R + DOWN*0.7
            thigh_R.put_start_and_end_on(hip, knee_R)
            shin_R.put_start_and_end_on(knee_R, ankle_R)
            foot_R.put_start_and_end_on(ankle_R, ankle_R + RIGHT*0.3)
            elbow_L = neck + DOWN*0.6 + LEFT*0.2
            hand_L  = elbow_L + DOWN*0.5
            elbow_R = neck + DOWN*0.6 + RIGHT*0.2
            hand_R  = elbow_R + DOWN*0.5
            arm_L.put_start_and_end_on(neck, elbow_L)
            forearm_L.put_start_and_end_on(elbow_L, hand_L)
            arm_R.put_start_and_end_on(neck, elbow_R)
            forearm_R.put_start_and_end_on(elbow_R, hand_R)
            bow_center = neck + DOWN*0.05
            bow_knot.move_to(bow_center)
            bow_left.next_to(bow_knot, LEFT, buff=0)
            bow_right.next_to(bow_knot, RIGHT, buff=0)
            stickman.add_updater(open_arms)

        def open_arms(m):
            hip = np.array([0, -1.5, 0])
            neck = hip + UP*1.0
            angle = arm_open.get_value()
            elbow_L = neck + np.array([
                -0.9*np.sin(angle),
                -0.9*np.cos(angle),
                0
            ])
            hand_L = elbow_L + np.array([
                -0.5*np.sin(angle),
                -0.5*np.cos(angle),
                0
            ])
            elbow_R = neck + np.array([
                0.9*np.sin(angle),
                -0.9*np.cos(angle),
                0
            ])
            hand_R = elbow_R + np.array([
                0.5*np.sin(angle),
                -0.5*np.cos(angle),
                0
            ])
            arm_L.put_start_and_end_on(neck, elbow_L)
            forearm_L.put_start_and_end_on(elbow_L, hand_L)
            arm_R.put_start_and_end_on(neck, elbow_R)
            forearm_R.put_start_and_end_on(elbow_R, hand_R)
            bow_center = neck + DOWN*0.05
            bow_knot.move_to(bow_center)
            bow_left.next_to(bow_knot, LEFT, buff=0)
            bow_right.next_to(bow_knot, RIGHT, buff=0)
        stickman.add_updater(open_arms)
        self.play(arm_open.animate.set_value(PI/2),run_time=2)
        stickman.remove_updater(open_arms)

        def arm_wave(m):
            hip = np.array([0, -1.5, 0])
            neck = hip + UP*1.0
            t = wave_t.get_value()
            phase_shoulder = t
            phase_elbow = t - 0.6
            phase_hand  = t - 1.2
            wave_shoulder = 0.25 * np.sin(phase_shoulder)
            wave_elbow = 0.25*np.sin(phase_elbow)
            wave_hand  = 0.25*np.sin(phase_hand)
            elbow_L = neck + LEFT*0.9 + UP*wave_elbow
            hand_L  = elbow_L + LEFT*0.5 + UP*wave_hand
            arm_L.put_start_and_end_on(neck, elbow_L)
            forearm_L.put_start_and_end_on(elbow_L, hand_L)
            wave_shoulder = 0.25 * np.sin(phase_shoulder + PI)
            wave_elbow = 0.25*np.sin(phase_elbow + PI)
            wave_hand  = 0.25*np.sin(phase_hand + PI) 
            elbow_R = neck + RIGHT*0.9 + UP*wave_elbow
            hand_R  = elbow_R + RIGHT*0.5 + UP*wave_hand
            arm_R.put_start_and_end_on(neck, elbow_R)
            forearm_R.put_start_and_end_on(elbow_R, hand_R)
            bow_center = neck + DOWN*0.05
            bow_knot.move_to(bow_center)
            bow_left.next_to(bow_knot, LEFT, buff=0)
            bow_right.next_to(bow_knot, RIGHT, buff=0)
        stickman.add_updater(arm_wave)
        self.play(wave_t.animate.set_value(6), run_time=3)
        self.play(wave_t.animate.set_value(0), run_time=3)
        stickman.remove_updater(arm_wave)

        def shinchan_dance(m):

            t = dance_t.get_value()

            x = 5*np.sin(t)   
            hip = np.array([x, -1.5, 0])
            neck = hip + UP*1.0

            body.put_start_and_end_on(neck, hip)
            head.move_to(neck + UP*0.3)

            swing = 0.8*np.sin(3*t)

            elbow_L = neck + LEFT*0.6 + UP*0.2
            hand_L  = elbow_L + np.array([
                -0.6*np.cos(swing),
                0.6*np.sin(swing),
                0
            ])

            elbow_R = neck + RIGHT*0.6 + UP*0.2
            hand_R  = elbow_R + np.array([
                0.6*np.cos(swing),
                -0.6*np.sin(swing),
                0
            ])

            arm_L.put_start_and_end_on(neck, elbow_L)
            forearm_L.put_start_and_end_on(elbow_L, hand_L)

            arm_R.put_start_and_end_on(neck, elbow_R)
            forearm_R.put_start_and_end_on(elbow_R, hand_R)

            jiggle = 0.25*np.cos(4*t)

            knee_L = hip + DOWN*0.5 + LEFT*0.1
            ankle_L = knee_L + DOWN*0.7 + RIGHT*jiggle

            thigh_L.put_start_and_end_on(hip, knee_L)
            shin_L.put_start_and_end_on(knee_L, ankle_L)
            foot_L.put_start_and_end_on(ankle_L, ankle_L + LEFT*0.3)

            knee_R = hip + DOWN*0.5 + RIGHT*0.1
            ankle_R = knee_R + DOWN*0.7 + LEFT*jiggle

            thigh_R.put_start_and_end_on(hip, knee_R)
            shin_R.put_start_and_end_on(knee_R, ankle_R)
            foot_R.put_start_and_end_on(ankle_R, ankle_R + RIGHT*0.3)

            bow_center = neck + DOWN*0.05
            bow_knot.move_to(bow_center)
            bow_left.next_to(bow_knot, LEFT, buff=0)
            bow_right.next_to(bow_knot, RIGHT, buff=0)
            
        stickman.add_updater(shinchan_dance)
        self.play(dance_t.animate.set_value(6),run_time=8,rate_func=linear)
        self.play(stickman.animate.scale([-1,1,1]),run_time=0.5)
        self.play(dance_t.animate.set_value(8), run_time=8)
        stickman.remove_updater(shinchan_dance)

        hip = np.array([5, -1.5, 0])   
        neck = hip + UP*1.0

        body.put_start_and_end_on(neck, hip)
        head.move_to(neck + UP*0.3)

        knee_L = hip + DOWN*0.5
        ankle_L = knee_L + DOWN*0.7
        thigh_L.put_start_and_end_on(hip, knee_L)
        shin_L.put_start_and_end_on(knee_L, ankle_L)
        foot_L.put_start_and_end_on(ankle_L, ankle_L + LEFT*0.3)

        knee_R = hip + DOWN*0.5
        ankle_R = knee_R + DOWN*0.7
        thigh_R.put_start_and_end_on(hip, knee_R)
        shin_R.put_start_and_end_on(knee_R, ankle_R)
        foot_R.put_start_and_end_on(ankle_R, ankle_R + RIGHT*0.3)

        elbow_L = neck + DOWN*0.6 + LEFT*0.2
        hand_L  = elbow_L + DOWN*0.5

        elbow_R = neck + DOWN*0.6 + RIGHT*0.2
        hand_R  = elbow_R + DOWN*0.5

        arm_L.put_start_and_end_on(neck, elbow_L)
        forearm_L.put_start_and_end_on(elbow_L, hand_L)

        arm_R.put_start_and_end_on(neck, elbow_R)
        forearm_R.put_start_and_end_on(elbow_R, hand_R)

        bow_center = neck + DOWN*0.05
        bow_knot.move_to(bow_center)
        bow_left.next_to(bow_knot, LEFT, buff=0)
        bow_left.rotate(PI)
        bow_right.next_to(bow_knot, RIGHT, buff=0)
        bow_right.rotate(PI)
        moon_x = ValueTracker(5)

        def update_stickman(mob):
            t = self.time
            freq = 3
            x = walk.get_value()
            hip = np.array([x, -1.5, 0])
            shoulder = hip + UP * core
            body.put_start_and_end_on(shoulder, hip)
            head.move_to(shoulder + UP * 0.4)
            swing = 0.6 * np.sin(freq * t)
            bend_L = 0.6 * max(0, np.sin(freq * t))
            bend_R = 0.6 * max(0, -np.sin(freq * t))
            knee_L = hip + thigh * np.array([
                np.sin(swing),
                -np.cos(swing),
                0
            ])
            thigh_L.put_start_and_end_on(hip, knee_L)
            shin_angle_L = swing - bend_L
            ankle_L = knee_L + shin * np.array([
                np.sin(shin_angle_L),
                -np.cos(shin_angle_L),
                0
            ])
            shin_L.put_start_and_end_on(knee_L, ankle_L)
            foot_L.put_start_and_end_on(ankle_L, ankle_L + RIGHT * 0.4)
            swing_R = -swing
            knee_R = hip + thigh * np.array([
                np.sin(swing_R),
                -np.cos(swing_R),
                0
            ])
            thigh_R.put_start_and_end_on(hip, knee_R)
            shin_angle_R = swing_R - bend_R
            ankle_R = knee_R + shin * np.array([
                np.sin(shin_angle_R),
                -np.cos(shin_angle_R),
                0
            ])
            shin_R.put_start_and_end_on(knee_R, ankle_R)
            foot_R.put_start_and_end_on(ankle_R, ankle_R + RIGHT * 0.4)
            arm_swing = -swing
            elbow_L = shoulder + arm * np.array([
                np.sin(arm_swing),
                -np.cos(arm_swing),
                0
            ])
            arm_L.put_start_and_end_on(shoulder, elbow_L)
            hand_L = elbow_L + forearm * np.array([
                np.sin(arm_swing),
                -np.cos(arm_swing),
                0
            ])
            forearm_L.put_start_and_end_on(elbow_L, hand_L)
            wave_angle = 0.8 * np.sin(6 * t)
            elbow_R = shoulder + arm * np.array([0.8,-0.2,0])
            arm_R.put_start_and_end_on(shoulder, elbow_R)
            hand_R = elbow_R + forearm * np.array([
                np.sin(wave_angle),
                np.cos(wave_angle),
                0
            ])
            forearm_R.put_start_and_end_on(elbow_R, hand_R)
            bounce = 0.05 * abs(np.sin(freq * t))
            body.shift(UP * bounce)
            head.shift(UP * bounce)
            bow_center = shoulder + DOWN*0.05
            bow_knot.move_to(bow_center)
            bow_left.next_to(bow_knot , LEFT, buff=0)
            bow_right.next_to(bow_knot ,RIGHT, buff=0)

        stickman.add_updater(update_stickman)
        self.play(
            walk.animate.set_value(5),
            run_time=8,
            rate_func=linear
        )
        stickman.remove_updater(update_stickman)


        self.play(FadeOut(stickman))
