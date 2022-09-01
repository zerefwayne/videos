from manim import *

g = 9.8


class Projectile(Circle):

    def __init__(self,
                 radius=0.075, color=YELLOW, fill_opacity=1,
                 u=0, theta=45,  # mandatory
                 p=np.array([0, 0, 0]), a=np.array([0, -g, 0]),
                 animation_speed=1,
                 x_contrib=1, y_contrib=1,
                 **kwargs):
        super().__init__(radius=radius, color=color, fill_opacity=fill_opacity, **kwargs)

        self.animation_speed = animation_speed
        self.p, self.u, self.a, self.theta = p, u, a, theta
        self.x_contrib, self.y_contrib = x_contrib, y_contrib
        self.theta_rad = np.deg2rad(theta)
        self.v = self.calc_v()
        self.max_height = 0

    def compute_position(self, dt):
        dt = dt * self.animation_speed
        self.v = self.v + self.a * dt
        self.p = self.p + self.v * dt
        self.max_height = max(self.max_height, self.p[1])

        self.p = np.array([self.p[0] * self.x_contrib,
                          self.p[1] * self.y_contrib, 0])

    def calc_v(self):
        return np.array([self.u * np.cos(self.theta_rad), self.u * np.sin(self.theta_rad), 0])


class IntroScenarioScene(Scene):

    def construct(self):
        plane = Axes(
            x_range=[0, 100 * config.aspect_ratio, 10],
            y_range=[0, 100, 10],
            x_length=6 * config.aspect_ratio,
            y_length=6,
            axis_config={
                "include_ticks": False,
                "tip_width": 0.1,
                "tip_height": 0.1
            }
        )

        u = 35
        theta = ValueTracker(0.0)
        theta_final = 45.00

        projectile = Projectile(radius=0.075, color=YELLOW,
                                u=u, theta=theta_final, animation_speed=1.5).move_to(plane.c2p(0, 0))

        def projectile_updater(mob, dt):
            if self.stop_animation:
                mob.clear_updaters()
                return

            mob.compute_position(dt)

            if mob.x_contrib == 1 and mob.y_contrib == 1 and mob.p[1] <= 0.05 and mob.p[0] > 0:
                self.stop_animation = True
                return

            mob.move_to(plane.c2p(*mob.p))

        u_vector = always_redraw(lambda: Arrow(start=plane.c2p(0, 0), end=plane.c2p(30, np.tan(np.deg2rad(
            theta.get_value())) * 30), buff=0, stroke_width=0.5 * DEFAULT_STROKE_WIDTH, tip_length=0.5 * DEFAULT_ARROW_TIP_LENGTH, fill_color=BLUE, fill_opacity=1, stroke_color=BLUE))
        u_label = always_redraw(lambda: MathTex(
            "u = " + str(round(u, 2)) + "m/s", font_size=0.5 * DEFAULT_FONT_SIZE, color=BLUE).next_to(u_vector.get_end(), UR, buff=0.1))

        u_angle = always_redraw(lambda: Angle(plane.get_axis(
            0), u_vector, color=BLACK if theta.get_value() == 0 else BLUE))
        u_angle_value = always_redraw(lambda: MathTex(
            r"\theta = " + str(round(theta.get_value(), 2)) + r"^\circ", font_size=0.5 * DEFAULT_FONT_SIZE, color=BLACK if theta.get_value() == 0 else BLUE).next_to(u_angle.get_critical_point(UR), buff=0.1))

        self.play(Create(plane))
        self.wait()
        self.play(FadeIn(projectile))
        self.wait()
        self.play(Create(u_vector))
        self.wait()
        self.play(Create(u_angle), Write(u_label), Write(u_angle_value))
        self.wait()
        self.play(theta.animate.set_value(theta_final),
                  run_time=3, rate_func=smooth)
        self.wait(2)

        self.stop_animation = False
        projectile.add_updater(projectile_updater)
        self.wait(10)

        h_arrow = Arrow(start=plane.c2p(0, 0), end=plane.c2p(
            0, projectile.max_height), buff=0, stroke_width=3, tip_length=0.5 * DEFAULT_ARROW_TIP_LENGTH, color=ORANGE).shift(0.15 * LEFT)

        h_label = MathTex("height(H)", font_size=24).next_to(h_arrow, LEFT, buff=0.1)

        r_arrow = Arrow(start=plane.c2p(0, 0), end=plane.c2p(
            *projectile.p), buff=0, stroke_width=3, tip_length=0.5 * DEFAULT_ARROW_TIP_LENGTH, color=ORANGE).shift(0.15 * DOWN)

        r_label = MathTex("range(R)", font_size=24).next_to(r_arrow, DOWN, buff=0.1)

        self.play(Create(h_arrow), Write(h_label))
        self.wait()
        self.play(Create(r_arrow), Write(r_label))
        self.wait()
