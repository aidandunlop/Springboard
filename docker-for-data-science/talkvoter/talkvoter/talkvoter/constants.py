from enum import Enum


class VoteValue(Enum):
    in_person = "in_person"
    watch_later = "watch_later"


vote_mapping = {
    VoteValue.in_person.value: 1,
    VoteValue.watch_later.value: 0, }
