from recipes.database import db_session
from recipes.models import Blog

CHASE = 'CHASE'
BOA = 'BANK OF AMERICA'


BANK_ACCOUNTS = [
    BankAccount(
        id=1,
        name=(BOA + 'SAVINGS'),
    ),
    BankAccount(
        id=2,
        name=(BOA + 'CHECKINGS'),
    ),
    BankAccount(
        id=3,
        name=(BOA + 'CHECKINGS'),
    ),
    BankAccount(
        id=4,
        name=(BOA + 'SAVINGS'),
    ),
]

def main():
    with db_session() as session:
        hosts = {blog.host for blog in session.query(Blog).all()}

        for blog in BLOGS:
            if blog.host not in hosts:
                print('Creating blog for {}'.format(blog.host))
                session.add(blog)
                session.commit()

if __name__ == '__main__':
    main()
