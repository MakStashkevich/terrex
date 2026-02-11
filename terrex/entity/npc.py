from terrex.entity.entity import Entity


class NPC(Entity):
    # size
    width = 10
    height = 10

    # ladybug
    lady_bug_good_luck_time: int = 43200
    lady_bug_bad_luck_time: int = -10800
    lady_bug_rain_time: int = 1800
    maximum_amount_of_times_lady_bug_rain_can_stack: int = 10 * lady_bug_rain_time
