def phrases_list(filename: str) -> list:
    with open(filename, 'r') as f:
        words = f.readlines()
        return words

PHRASES_ALCOHOL = phrases_list('alcohol.txt')
PHRASES_COFFEE = phrases_list('coffee.txt')
PHRASES_ENTERTAINMENT = phrases_list('entertainment.txt')
PHRASES_FOOD = phrases_list('food.txt')
PHRASES_SKIPPED = phrases_list('skipped.txt')
PHRASES_TRAVEL = phrases_list('travel.txt')
