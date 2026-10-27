from pico2d import *
from transitions import Machine


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')

        self.idle_start_time = get_time()
        self.sleep_time = 5.0
        self.auto_run_start_time = 0

        self.state_machine = Machine(model=self, states=['IDLE', 'RUN', 'SLEEP', 'AUTO_RUN'], initial='IDLE', auto_transitions=False)

        self.state_machine.add_transition(trigger='go_run', source=['IDLE', 'SLEEP'], dest='RUN')
        self.state_machine.add_transition(trigger='stop_run', source='RUN', dest='IDLE', after='reset_idle_timer')
        self.state_machine.add_transition(trigger='go_sleep', source='IDLE', dest='SLEEP')
        self.state_machine.add_transition(trigger='wake_up', source='SLEEP', dest='IDLE', after='reset_idle_timer')
        self.state_machine.add_transition(trigger='go_auto_run', source=['IDLE', 'SLEEP'], dest='AUTO_RUN', after='start_auto_run_timer')
        self.state_machine.add_transition(trigger='stop_auto_run', source='AUTO_RUN', dest='IDLE', after='reset_idle_timer')

        self.dir = 0
        self.speed = 200
        self.auto_speed = 600

    def start_auto_run_timer(self):
        self.auto_run_start_time = get_time()

    def reset_idle_timer(self):
        self.idle_start_time = get_time()

    def reset_idle_timer(self):
        self.idle_start_time = get_time()

    def update(self):
        if self.state == 'IDLE':
            self.frame = (self.frame + 1) % 8
            if get_time() - self.idle_start_time > self.sleep_time:
                self.go_sleep()
        elif self.state == 'RUN':
            self.frame = (self.frame + 1) % 8
            self.x += self.dir * self.speed * 0.01
            if self.x < 0:
                self.x = 800
            elif self.x > 800:
                self.x = 0
        elif self.state == 'AUTO_RUN':
            self.frame = (self.frame + 1) % 8
            self.x += self.dir * self.auto_speed * 0.01
            if self.x <= 0:
                self.x = 0
                self.dir = 1
                self.face_dir = 1
            elif self.x >= 800:
                self.x = 800
                self.dir = -1
                self.face_dir = -1
            if get_time() - self.auto_run_start_time > 5.0:
                self.stop_auto_run()
        elif self.state == 'SLEEP':
            self.frame = 0

    def handle_event(self, event):
        if self.state == 'SLEEP':
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_SPACE:
                    self.wake_up()
                    return
                if event.key == SDLK_LEFT:
                    self.face_dir = -1
                    self.dir = -1
                    self.go_run()
                    return
                if event.key == SDLK_RIGHT:
                    self.face_dir = 1
                    self.dir = 1
                    self.go_run()
                    return
                if event.key == SDLK_a:
                    self.dir = self.face_dir
                    self.go_auto_run()
                    return
            return

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.face_dir = -1
                self.dir = -1
                if self.state == 'IDLE':
                    self.go_run()
            elif event.key == SDLK_RIGHT:
                self.face_dir = 1
                self.dir = 1
                if self.state == 'IDLE':
                    self.go_run()
            elif event.key == SDLK_a and self.state == 'IDLE':
                self.dir = self.face_dir
                self.go_auto_run()
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT and self.dir == -1:
                self.dir = 0
                if self.state == 'RUN':
                    self.stop_run()
            elif event.key == SDLK_RIGHT and self.dir == 1:
                self.dir = 0
                if self.state == 'RUN':
                    self.stop_run()

    def draw(self):
        if self.state == 'IDLE':
            if self.face_dir == 1:
                self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
        elif self.state == 'RUN':
            if self.face_dir == 1:
                self.image.clip_draw(self.frame * 100, 100, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)
        elif self.state == 'AUTO_RUN':
            if self.face_dir == 1:
                self.image.clip_draw(self.frame * 100, 100, 100, 100, self.x, self.y + 15, 150, 150)
            else:
                self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y + 15, 150, 150)
        elif self.state == 'SLEEP':
            self.image.clip_composite_draw(0, 0, 100, 100, 3.141592 / 2.0, 'h', self.x, self.y - 15, 100, 100)
        else:
            if self.face_dir == 1:
                self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
