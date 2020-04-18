def verify_valid_position(func):
    def function_wrapper(self, position: int):
        if position <= 32 and position >= 1:
            return func(self, position)
        raise InvalidPiecePosition
    return function_wrapper


def verify_valid_player(func):
    def function_wrapper(self, player: int):
        if player <= 2 and player >= 1:
            return func(self, player)
        raise InvalidPlayer
    return function_wrapper


class InvalidPiecePosition(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, "The position must be between 1 and 32.")


class InvalidPlayer(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, "The player must be either 1 or 2.")


class Piece:
    def __init__(self, position=1, player=1, king=False):
        self.position: int
        self.player: int
        self.king: bool

        self.set_position(position)
        self.set_player(player)
        self.set_king(king)

    def get_position(self):
        return self.position

    def get_player(self):
        return self.player

    def is_king(self):
        return self.king

    @verify_valid_position
    def set_position(self, position: int):
        self.position = position

    @verify_valid_player
    def set_player(self, player: int):
        self.player = player

    def set_king(self, king: bool):
        self.king = king


class Move:
    def __init__(self, origin=1, target=1):
        self.origin: int
        self.target: int

        self.set_origin(origin)
        self.set_target(target)

    def get_origin(self):
        return self.origin

    def get_target(self):
        return self.target

    @verify_valid_position
    def set_origin(self, origin: int):
        self.origin = origin

    @verify_valid_position
    def set_target(self, target: int):
        self.target = target
