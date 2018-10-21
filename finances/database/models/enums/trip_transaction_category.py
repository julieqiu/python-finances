from enum import Enum


class TripTransactionCategory(Enum):
    HOUSING = 'housing'
    TRAVEL = 'travel'
    LOCAL_TRANSPORTATION = 'local_transportation'
    ENTERTAINMENT = 'entertainment'
    FOOD = 'food'
    OTHER = 'other'
