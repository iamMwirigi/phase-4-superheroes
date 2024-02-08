# seed.py
from app import app, db
from models import Power, Hero, HeroPower
import random

def seed_data():
    print("🦸‍♀️ Seeding powers...")
    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]

    # Initialize SQLAlchemy only if not already registered
    if 'sqlalchemy' not in app.extensions:
        db.init_app(app)

    powers = Power.create(powers_data)



    print("🦸‍♀️ Seeding heroes...")
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    heroes = Hero.create(heroes_data)

    print("🦸‍♀️ Adding powers to heroes...")
    strengths = ["Strong", "Weak", "Average"]

    for hero in heroes:
        for _ in range(random.randint(1, 3)):  # Randomly assigning 1 to 3 powers to each hero
            # get a random power
            power = Power.query.get(random.choice(Power.query.with_entities(Power.id).all())[0])

            HeroPower.create(hero=hero, power=power, strength=random.choice(strengths))

    print("🦸‍♀️ Done seeding!")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()