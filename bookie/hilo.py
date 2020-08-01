import random

from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class Roll():
    user_id: str
    value: int

@dataclass
class HiLo():
    quantity: int
    unit: str
    rolls: List[Roll] = field(default_factory=list)
    response_url: str = None

    def add_roll(self, roll: Roll):
        for r in self.rolls:
            if r.user_id == roll.user_id:
                raise "cannot reroll"
        self.rolls.append(roll)

    def roll(self, user_id: str) -> Roll:
        roll = Roll(user_id, random.randint(0, self.quantity))
        self.add_roll(roll)
        return roll

    def finalize(self) -> Tuple[Roll, Roll]:
        winner_roll: Roll = None
        loser_roll: Roll = None

        for roll in self.rolls:
            if winner_roll is None:
                winner_roll = roll
            if loser_roll is None:
                loser_roll = roll

            if roll.value > loser_roll.value:
                loser_roll = roll
            if roll.value < winner_roll.value:
                winner_roll = roll

        if winner_roll.user_id == loser_roll.user_id:
            raise "winner and loser are the same person"
        return (winner_roll, loser_roll)
