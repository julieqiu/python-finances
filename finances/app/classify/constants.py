# FOOD
def phrases_list(filename: str) -> list:
    with open('/Users/julie/Code/finances/finances/app/classify/filters/' + filename, 'r') as f:
        words = f.readlines()
        return [word[:-1] for word in words]

# L1: List of items that are L2 for that L2
#


CLASSIFICATION_TO_PHRASES = {
    'EXPENSES': {
        'Beauty': {
            'nails': ['NAILS', 'DREAM BLUE BEAUTY'],
            'spa': ['SPA'],
        },

        'Entertainment': {
            'entertainment': phrases_list('entertainment.txt'),
            'travel': phrases_list('travel.txt'),
            'wedding': ['ZOLA'],
        },

        'Food': {
            'alcohol': phrases_list('alcohol.txt'),
            'coffee': phrases_list('coffee.txt'),
            'food': phrases_list('food.txt'),
            'grocery': ['TRADER JOE', 'WHOLEFDS'],
        },

        'Health': {
            'health': ['MOUNT SINAI'],
            'physical_therapy': ['RECOVERY PHYSICAL THERAPY'],
        }

        'Shopping': {
            'amazon': ['Amazon'],
            'audible': ['Audible'],
            'aws': ['AWS'],
            'interview_prep': ['INTERVIEWCAKE'],
            'repairs': ['MAX SHOE REPAIR'],
            'shopping': ['BOOK', 'BEST BUY'],
            'stitch_fix': ['STITCH FIX'],
            'walgreens_cvs': ['WALGREENS', 'CVS'],
        },

        'Transportation': {
            'lyft': ['Lyft', 'Uber'],
            'mta': ['MTA'],
            'taxi': ['NYCTAXI', 'TAXI SVC'],
        },

        'Withdrawal': {
            'atm': ['ATM WITHDRAW', 'ATM DEBIT'],
            'customer_withdrawal': ['Customer Withdrawal Image'],
            'paypal': ['PAYPAL'],
            'venmo': ['Venmo', 'Zelle'],
        },
    },

    'SKIPPED': {
        'Skipped': {
            'skipped': {'skipped': phrases_list('skipped.txt')},
        }
    },

    'INCOME': {
        'Income': {
            'bonus': ['$150 for New Savings', '$200 for New Checking'],
            'checks': ['REMOTE ONLINE DEPOSIT', 'ATM CHECK DEPOSIT', 'DEPOSIT *MOBILE NY'],
            'income': ['SPRING NYC', 'SHOPSPRING', 'JELLO LABS DES:DIR DEP ID'],
            'reimbursed': ['Expensify', 'ELASTICSEARCH JAN3'],
        },
    },

    'MONTHLY': {
        'Monthly': {
            'equinox': ['EQUINOX'],
            'laundry': ['LAUNDRY LAND'],
            'rent': ['STUYVESANT TOWN'],
            'weight_watchers': ['WEIGHTWATCHERS'],
        },
    },
}
