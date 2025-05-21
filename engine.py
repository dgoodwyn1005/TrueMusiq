import pygame

class Engine:
    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        self.state.mouse = pygame.mouse.get_pos()  # Update mouse position for hover detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)

    def flip_state(self):
        print(f"Switching from {self.state_name} to {self.state.next_state}")
        self.state.done = False
        if not self.state.next_state or self.state.next_state not in self.states:
            raise ValueError(f"Invalid or missing next state: {self.state.next_state}")
        self.state_name = self.state.next_state
        self.state = self.states[self.state_name]
        print(f"New active state: {self.state_name}")

    def update(self, delta_time):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(delta_time)

    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps) / 1000.0  # Convert to seconds
            self.event_loop()
            self.update(delta_time)
            self.draw()
            pygame.display.flip()
