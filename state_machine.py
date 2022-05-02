class State():
    def __init__(self, enemy):
        self.enemy = enemy

    def start(self):
        pass

    def update(self):
        pass

    def end(self):
        pass


class GoBackToIdle(State):
    def __init__(self, enemy):
        super().__init__(enemy)
        self.spawnPointReached = False
        self.speakerSpawned = False

    def end(self):
        self.spawnPointReached = False
        self.speakerSpawned = False

    def update(self):
        if self.spawnPointReached:
            self.enemy.set_state(self.enemy.idle)
        if self.speakerSpawned:
            self.enemy.set_state(self.enemy.goToSpeaker)


class DestroySpeakerState(State):
    def __init__(self, enemy, timer):
        super().__init__(enemy)
        self.timer = timer
        self.startTimer = self.timer

    def start(self):
        self.timer = self.startTimer

    def update(self):
        if self.timer < 0:
            self.enemy.set_state(self.enemy.goBackToIdle)
        self.timer -= 1


class GoToSpeakerState(State):
    def __init__(self, enemy):
        super().__init__(enemy)
        self.speakerReached = False

    def end(self):
        self.speakerReached = False

    def update(self):
        if self.speakerReached:
            self.enemy.set_state(self.enemy.destroySpeaker)


class IdleState(State):
    def __init__(self, enemy):
        super().__init__(enemy)
        self.speakerSpawned = False

    def end(self):
        self.speakerSpawned = False

    def update(self):
        if self.speakerSpawned:
            self.enemy.set_state(self.enemy.goToSpeaker)


class EnemySM:
    def __init__(self, destroySpeakerTime):
        self.idle = IdleState(self)
        self.goToSpeaker = GoToSpeakerState(self)
        self.destroySpeaker = DestroySpeakerState(self, destroySpeakerTime)
        self.goBackToIdle = GoBackToIdle(self)
        self.state = self.idle

    def update(self):
        self.state.update()

    def set_state(self, state):
        self.state.end()
        self.state = state
        self.state.start()

    def get_state(self):
        return self.state

    def speaker_spawned(self):
        self.state.speakerSpawned = True

    def speaker_reached(self):
        self.state.speakerReached = True

    def spawn_point_reached(self):
        self.state.spawnPointReached = True
