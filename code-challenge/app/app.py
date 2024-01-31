from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Sample API route to get all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    print("Received GET request at /heroes")
    heroes = Hero.query.all()
    heroes_list = [{
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name
    } for hero in heroes]

    response = make_response(jsonify(heroes_list), 200)
    return response

# Sample API route to get a specific hero by ID
@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    print(f"Received GET request at /heroes/{hero_id}")
    hero = Hero.query.get(hero_id)

    if hero is not None:
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        }
        response = make_response(jsonify(hero_data), 200)
    else:
        response = make_response(jsonify({'error': 'Hero not found'}), 404)

    return response

# Sample API route to get all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    print("Received GET request at /powers")
    powers = Power.query.all()
    powers_list = [{
        'id': power.id,
        'name': power.name,
        'description': power.description
    } for power in powers]

    response = make_response(jsonify(powers_list), 200)
    return response

# Sample API route to get a specific power by ID
@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    print(f"Received GET request at /powers/{power_id}")
    power = Power.query.get(power_id)

    if power is not None:
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        response = make_response(jsonify(power_data), 200)
    else:
        response = make_response(jsonify({'error': 'Power not found'}), 404)

    return response

# Sample API route to get all hero powers
@app.route('/hero_powers', methods=['GET'])
def get_hero_powers():
    print("Received GET request at /hero_powers")
    hero_powers = HeroPower.query.all()
    hero_powers_list = [{
        'hero_id': hero_power.hero_id,
        'power_id': hero_power.power_id,
        'strength': hero_power.strength
    } for hero_power in hero_powers]

    response = make_response(jsonify(hero_powers_list), 200)
    return response

# Sample API route to get a specific hero power by ID
@app.route('/hero_powers/<int:hero_power_id>', methods=['GET'])
def get_hero_power(hero_power_id):
    print(f"Received GET request at /hero_powers/{hero_power_id}")
    hero_power = HeroPower.query.get(hero_power_id)

    if hero_power is not None:
        hero_power_data = {
            'hero_id': hero_power.hero_id,
            'power_id': hero_power.power_id,
            'strength': hero_power.strength
        }
        response = make_response(jsonify(hero_power_data), 200)
    else:
        response = make_response(jsonify({'error': 'Hero Power not found'}), 404)

    return response

# Sample API route to create a new hero power
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    new_hero_power = HeroPower(
        hero_id=data['hero_id'],
        power_id=data['power_id'],
        strength=data['strength']
    )
    db.session.add(new_hero_power)
    db.session.commit()

    response_data = {
        'hero_id': new_hero_power.hero_id,
        'power_id': new_hero_power.power_id,
        'strength': new_hero_power.strength
    }

    response = make_response(jsonify(response_data), 201)
    return response

# Sample API route to update a hero power by ID
@app.route('/hero_powers/<int:hero_power_id>', methods=['PATCH'])
def update_hero_power(hero_power_id):
    hero_power = HeroPower.query.get(hero_power_id)

    if hero_power is not None:
        data = request.json
        hero_power.hero_id = data.get('hero_id', hero_power.hero_id)
        hero_power.power_id = data.get('power_id', hero_power.power_id)
        hero_power.strength = data.get('strength', hero_power.strength)
        db.session.commit()

        response_data = {
            'hero_id': hero_power.hero_id,
            'power_id': hero_power.power_id,
            'strength': hero_power.strength
        }

        response = make_response(jsonify(response_data), 200)
    else:
        response = make_response(jsonify({'error': 'Hero Power not found'}), 404)

    return response

if __name__ == '__main__':
    app.run(port=5555)
