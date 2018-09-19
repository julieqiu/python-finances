def generate_category_to_phrases() -> dict:
    def phrases_list(filename: str) -> list:
        with open('/Users/julie/Code/finances/finances/app/classify/filters/' + filename, 'r') as f:
            words = f.readlines()
            return [word[:-1] for word in words]

    PHRASES_ALCOHOL = phrases_list('alcohol.txt')
    PHRASES_COFFEE = phrases_list('coffee.txt')
    PHRASES_ENTERTAINMENT = phrases_list('entertainment.txt')
    PHRASES_FOOD = phrases_list('food.txt')
    PHRASES_SKIPPED = phrases_list('skipped.txt')
    PHRASES_TRAVEL = phrases_list('travel.txt')

    return {
        'aws': ['AWS'],
        'alcohol': PHRASES_ALCOHOL,
        'amazon': ['Amazon'],
        'atm': ['ATM WITHDRAW', 'ATM DEBIT'],
        'audible': ['Audible'],
        'checks': ['REMOTE ONLINE DEPOSIT', 'ATM CHECK DEPOSIT', 'DEPOSIT *MOBILE NY'],
        'coffee': PHRASES_COFFEE,
        'customer_withdrawal': ['Customer Withdrawal Image'],
        'entertainment': PHRASES_ENTERTAINMENT,
        'equinox': ['EQUINOX'],
        'food': PHRASES_FOOD,
        'grocery': ['TRADER JOE', 'WHOLEFDS'],
        'income': ['SPRING NYC', 'SHOPSPRING', 'JELLO LABS DES:DIR DEP ID'],
        'bonus': ['$150 for New Savings', '$200 for New Checking'],
        'laundry': ['LAUNDRY LAND'],
        'lyft': ['Lyft', 'Uber'],
        'mta': ['MTA'],
        'beauty': ['NAILS', 'DREAM BLUE BEAUTY', 'SPA'],
        'paypal': ['PAYPAL'],
        'physical_therapy': ['RECOVERY PHYSICAL THERAPY'],
        'reimbursed': ['Expensify', 'ELASTICSEARCH JAN3'],
        'rent': ['STUYVESANT TOWN'],
        'skipped': PHRASES_SKIPPED,
        'stitch_fix': ['STITCH FIX'],
        'taxi': ['NYCTAXI', 'TAXI SVC'],
        'travel':PHRASES_TRAVEL,
        'venmo': ['Venmo', 'Zelle'],
        'weight_watchers': ['WEIGHTWATCHERS'],
        'walgreens_cvs': ['WALGREENS', 'CVS'],
        'shopping': ['BOOK', 'BEST BUY'],
        'interview_prep': ['INTERVIEWCAKE'],
        'repairs': ['MAX SHOE REPAIR'],
        'health': ['MOUNT SINAI'],
        'wedding': ['ZOLA'],
    }

CATEGORY_TO_PHRASES = generate_category_to_phrases()
