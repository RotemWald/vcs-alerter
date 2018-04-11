from enum import Enum


class MessageTag(Enum):
    NMD = 'NMD'
    TEC = 'TEC'
    MAT = 'MAT'  # because if it is mathematical discussion we don't want to tag it
    NONE = 'NONE'
