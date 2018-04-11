from enum import Enum


class CriticalMoment(Enum):
    NMD = 'NMD'
    TEC = 'TEC'
    DS = 'DS'
    MAT = 'MAT'  # because if it is mathematical discussion we don't want to tag it
    IDLENESS = 'IDLENESS'  # for alerter use
    NONE = 'NONE'  # for alerter use
