class missile:
    def __init__(self, type):
        self.kill_type = type


class inst_kill(missile):
    def __init__(self):
        missile.__init__(self, 0)


class slow_kill(missile):
    def __init__(self):
        missile.__init__(self, 1)
