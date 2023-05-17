
class DTOProcessEvent:

    def __init__(self, run, scale, move_x, move_y, mouse_x, mouse_y, show_distance, draw_line, timestep, pause):
        self.run = run
        self.scale = scale
        self.move_x = move_x
        self.move_y = move_y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.show_distance = show_distance
        self.draw_line = draw_line
        self.timestep = timestep
        self.pause = pause