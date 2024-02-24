from typing import Any
pyomp: Any = __import__('pyomp.PyOMP')


class EquityCalculator:
    def __init__(self, time_limit=0.1):
        self.eq = pyomp.PyOMP.PyEquityCalculator()
        self.eq.set_time_limit(time_limit)
        self.players = None
        self.equity = None
        self.wins = None
        self.ties = None
        self.wins_by_player_mask = None
        self.hands = None
        self.interval_hands = None
        self.speed = None
        self.interval_speed = None
        self.time = None
        self.interval_time = None
        self.stdev = None
        self.stdev_per_hand = None
        self.progress = None
        self.preflop_combos = None
        self.evaluated_preflop_combos = None
        self.evaluations = None
        self.enumerate_all = None
        self.finished = None

    def run(self, hands, board_cards, dead_cards=None, enumerate_all=False, stdev_target=5e-5, update_interval=0.2,
            thread_count=0):
        if len(hands) == 2:
            enumerate_all = True
        self.eq.start(hands,
                      board_cards=board_cards,
                      dead_cards=dead_cards,
                      enumerate_all=enumerate_all,
                      stdev_target=stdev_target,
                      update_interval=update_interval,
                      thread_count=thread_count)
        self.eq.wait()
        results = self.eq.get_results()
        self.players = results['players']
        self.equity = results['equity']
        self.wins = results['wins']
        self.ties = results['ties']
        self.wins_by_player_mask = results['wins_by_player_mask']
        self.hands = results['hands']
        self.interval_hands = results['interval_hands']
        self.speed = results['speed']
        self.interval_speed = results['interval_speed']
        self.time = results['time']
        self.interval_time = results['interval_time']
        self.stdev = results['stdev']
        self.stdev_per_hand = results['stdev_per_hand']
        self.progress = results['progress']
        self.preflop_combos = results['preflop_combos']
        self.evaluated_preflop_combos = results['evaluated_preflop_combos']
        self.evaluations = results['evaluations']
        self.enumerate_all = results['enumerate_all']
        self.finished = results['finished']
