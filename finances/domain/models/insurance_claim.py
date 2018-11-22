class InsuranceClaim:

    def __init__(self,
                 id,
                 service_date,
                 claim_type,
                 claim_id,
                 patient,
                 provider,
                 billed,
                 allowed_amount,
                 paid,
                 deductible,
                 coinsurance,
                 copay,
                 not_covered,
                 personal_cost,
                 status):

        self.id = id
        self.date = service_date
        self.type = claim_type
        self.claim_id = claim_id
        self.patient = patient
        self.provider = provider
        self.billed = billed
        self.allowed_amount = allowed_amount
        self.paid = paid if paid else 0
        self.deductible = deductible if deductible else 0
        self.coinsurance = coinsurance if coinsurance else 0
        self.copay = copay if copay else 0
        self.not_covered = not_covered if not_covered else 0
        self.personal_cost = personal_cost if personal_cost else 0
        self.status = status


    @property
    def month(self):
        return self.date.month

    @property
    def year(self):
        return self.date.year
