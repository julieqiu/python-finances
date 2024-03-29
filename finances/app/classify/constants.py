# FOOD
def phrases_list(filename: str) -> list:
    with open('/Users/julie/Code/github.com/finances/finances/app/classify/filters/' + filename, 'r') as f:
        words = f.readlines()
        return [
            word[:-1] if word[-1] == '\n' else word
            for word in words
        ]

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
            'grocery': ['TRADER JOE', 'WHOLEFDS', 'GROCERY', 'GRACEFULLY'],
        },

        'Health': {
            'health': ['MOUNT SINAI'],
            'physical_therapy': ['RECOVERY PHYSICAL THERAPY'],
            'therapy': [],
        },

        'Shopping': {
            'amazon': ['Amazon', 'AMZN', ],
            'audible': ['Audible'],
            'aws': ['AWS'],
            'interview_prep': ['INTERVIEWCAKE'],
            'repairs': ['MAX SHOE REPAIR'],
            'shopping': ['BOOK', 'BEST BUY', 'EXPRESS#'],
            'stitch_fix': ['STITCH FIX'],
            'walgreens_cvs': ['WALGREENS', 'CVS'],
        },

        'Transportation': {
            'lyft': ['Lyft', 'Uber', 'Via'],
            'mta': ['MTA'],
            'taxi': ['NYCTAXI', 'TAXI SVC'],
        },

        'Withdrawal': {
            'atm': ['ATM WITHDRAW', 'ATM DEBIT'],
            'customer_withdrawal': ['Customer Withdrawal Image'],
            'paypal': ['PAYPAL'],
            'venmo': ['VENMO', 'Zelle'],
        },

    },

    'SKIPPED': {
        'Skipped': {
            'skipped': phrases_list('skipped.txt'),
        }
    },

    'INCOME': {
        'Income': {
            'bonus': ['IRS TREAS', '$150 for New Savings', '$200 for New Checking'],
            'checks': ['ATM CHECK DEPOSIT', 'DEPOSIT *MOBILE NY'],
            'income': ['GOOGLE', 'SPRING NYC', 'SHOPSPRING', 'JELLO LABS DES:DIR DEP ID'],
            'reimbursed': ['Expensify', 'ELASTICSEARCH JAN3'],
            'interest': ['INTEREST'],
        },
        'Health': {
            'reimbursements': ['REMOTE ONLINE DEPOSIT'],
        },
        'Invesment': {
            'investment': ['Vanguard', 'Betterment'],
        }

    },

    'SUBSCRIPTIONS': {
        'Monthly': {
            'monthly': ['EQUINOX', 'LAUNDRY', 'WEIGHTWATCHERS'],
            'rent': [
                'STUYVESANT TOWN',
                'NOVELPAY PROPRTYPAY',
                'CLICKPAY PROPRTYPAY PPD',
            ],
        },
        'Annual': {
            'annual': ['headspace', 'todoist', '8fit', 'ANNUAL MEMBERSHIP FEE'],
        },
    },
}
