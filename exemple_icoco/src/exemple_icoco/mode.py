class Mode:
    Fluid_1 = 1
    Fluid_2 = 2
    Fluid = Fluid_1 + Fluid_2
    Solid = 4
    All = Fluid_1 + Fluid_2 + Solid

    @staticmethod
    def get_modes():
        modes = {}
        for key, elem in Mode.__dict__.items():
            if isinstance(elem, int) and isinstance(key, str):
                modes[elem] = key
        return modes

    def __init__(self, value):
        if value not in self.get_modes():
            raise ValueError(f"unknown mode {value}.")
        self.mode = value

    def is_activated(self, tested_elementary_mode):
        return (self.mode // tested_elementary_mode) % 2

    def get_elementary_modes(self):
        elementary_modes = []
        power = 0
        residual = self.mode
        while residual > 0:
            if residual % 2 == 1:
                elementary_modes.append(2**power)
            residual = residual // 2
            power += 1
        return elementary_modes

    def __eq__(self, other):
        if isinstance(other, Mode):
            return self.mode == other.mode
        return self.mode == other

    def __str__(self):
        modes = self.get_modes()
        return modes[self.mode]
