# app.py
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS

from models import db, Hero, Power, HeroPower
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for development
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'instance/app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy only if not already registered
if 'sqlalchemy' not in app.extensions:
    db.init_app(app)

migrate = Migrate(app, db)


@app.route('/heroes', methods=['GET'])
def get_heroes():
    try:
        heroes = Hero.query.all()
        heroes_data = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
        return jsonify(heroes_data)
    except Exception as e:
        print(f"Error fetching heroes: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero_by_id(hero_id):
    print(f"Inside get_hero_by_id function for hero_id: {hero_id}")  # Add this line for debugging

    try:
        hero = Hero.query.get(hero_id)

        if hero:
            powers_data = [{'id': power.id, 'name': power.name,
                            'description': power.description} for power in hero.hero_powers]
            hero_data = {'id': hero.id, 'name': hero.name,
                         'super_name': hero.super_name, 'powers': powers_data}
            return jsonify(hero_data)
        else:
            return jsonify({'error': 'Hero not found'}), 404

    except Exception as e:
        print(f"Error processing get_hero_by_id: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/powers', methods=['GET'])
def get_powers(): 
    powers = Power.query.all()
    powers_data = [{'id': power.id, 'name': power.name,
                    'description': power.description} for power in powers]
    return jsonify(powers_data)


@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power_by_id(power_id):
    power = Power.query.get(power_id)

    if power:
        power_data = {'id': power.id, 'name': power.name,
                      'description': power.description}
        return jsonify(power_data)
    else:
        return jsonify({'error': 'Power not found'}), 404


@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)

    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()

    if 'description' in data:
        new_description = data['description']
        if len(new_description) >= 20:
            power.description = new_description
            db.session.commit()
            return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
        else:
            return jsonify({'errors': ['Validation error: Description must be at least 20 characters']}), 400
    else:
        return jsonify({'errors': ['No valid data provided']}), 400


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    required_fields = ['strength', 'power_id', 'hero_id']
    if not all(field in data for field in required_fields):
        return jsonify({'errors': ['Validation error: Missing required fields']}), 400

    valid_strengths = ['Strong', 'Weak', 'Average']
    if data['strength'] not in valid_strengths:
        return jsonify({'errors': ['Validation error: Invalid strength']}), 400

    # Create HeroPower
    hero_power = HeroPower(
        strength=data['strength'], power_id=data['power_id'], hero_id=data['hero_id'])
    db.session.add(hero_power)
    db.session.commit()

    # Fetch updated Hero data
    hero = Hero.query.get(data['hero_id'])
    powers_data = [{'id': power.id, 'name': power.name,
                    'description': power.description} for power in hero.hero_powers]
    hero_data = {'id': hero.id, 'name': hero.name,
                 'super_name': hero.super_name, 'powers': powers_data}

    return jsonify(hero_data), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
