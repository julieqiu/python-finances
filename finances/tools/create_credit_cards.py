from recipes.database import db_session
from recipes.models import Blog

CHASE_RESERVE_CC = 'https://www.domesticate-me.com'

HOST_FOOD_FAITH_FITNESS = 'https://www.foodfaithfitness.com'
HOST_ORGANIZE_YOURSELLF_SKINNY = 'https://www.organizeyourselfskinny.com'
HOST_ANDIE_MITCHELL = 'https://www.andiemitchell.com'

BLOGS = [
    Blog(
        id=1,
        host=HOST_DOMESTICATE_ME,
        seed='{}/recipes-2'.format(HOST_DOMESTICATE_ME),
        categories_root='{}/recipes-2'.format(HOST_DOMESTICATE_ME),
        recipes_root=HOST_DOMESTICATE_ME,
    ),
    Blog(
        id=2,
        host=HOST_FOOD_FAITH_FITNESS,
        seed=HOST_FOOD_FAITH_FITNESS,
        categories_root='{}/category'.format(HOST_FOOD_FAITH_FITNESS),
        recipes_root=HOST_FOOD_FAITH_FITNESS,
    ),
    Blog(
        id=3,
        host=HOST_ORGANIZE_YOURSELLF_SKINNY,
        seed='{}/category/recipes'.format(HOST_ORGANIZE_YOURSELLF_SKINNY),
        categories_root='{}/category'.format(HOST_ORGANIZE_YOURSELLF_SKINNY),
        recipes_root='{}/201'.format(HOST_ORGANIZE_YOURSELLF_SKINNY),
    ),
    Blog(
        id=4,
        host=HOST_ANDIE_MITCHELL,
        seed='{}/category/recipes'.format(HOST_ANDIE_MITCHELL),
        categories_root='{}/category/recipes'.format(HOST_ANDIE_MITCHELL),
        recipes_root=HOST_ANDIE_MITCHELL,
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
