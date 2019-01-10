from finances.database.models import DbTransaction, DbInsuranceClaim


DIR_BASE = '/Users/julie/Code/github.com/finances/finances/history'
CSV_INGEST_INFO = {
    'INSURANCE_CLAIMS': {
        'DB_MODEL': DbInsuranceClaim,
        'CSV_COL_TO_DB_COL': {
            # 'CLAIM NUMBER': 'claim_id',
            'PATIENT': 'patient',
            'SERVICE DATE': 'service_date',
            'PROVIDED BY': 'provider',
            'BILLED': 'billed',
            'ALLOWED Amount': 'allowed_amount',
            'PAID': 'paid',
            'DEDUCTIBLE': 'deductible',
            'COINSURANCE': 'coinsurance',
            # 'COPAY': 'copay',
            'NOT COVERED': 'not_covered',
            'YOUR COST': 'personal_cost',
            'STATUS': 'status',
        },
        'OPTIONAL_COLS': {
            'claim_id',
            'patient',
        },
        'SKIP_IF_MISSING': {'provider'},
        'CSV_DIRECTORY': '{}/insurance/'.format(DIR_BASE),
    },

    'TRANSACTIONS': {
        'DB_MODEL': DbTransaction,
        'CSV_COL_TO_DB_COL': {
            'AMOUNT': 'amount',
            'TRANS DATE': 'date',
            'POSTING DATE': 'date',
            'DATE': 'date',
            'DESCRIPTION': 'description',
            'TYPE': 'type',
        },
        'OPTIONAL_COLS': {'type'},
        'SKIP_IF_MISSING': {'amount', 'description'},
        'CSV_DIRECTORY': '{}/expenses/'.format(DIR_BASE),
    },
}
