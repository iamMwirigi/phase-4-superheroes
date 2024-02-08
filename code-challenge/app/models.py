# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    @classmethod
    def create(cls, powers_data):
        powers = [cls(**power) for power in powers_data]
        db.session.add_all(powers)
        db.session.commit()
        return powers

class Hero(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    super_name = db.Column(db.String(255), nullable=False)

    @classmethod
    def create(cls, heroes_data):
        heroes = [cls(**hero) for hero in heroes_data]
        db.session.add_all(heroes)
        db.session.commit()
        return heroes

class HeroPower(db.Model):
    __tablename__ = 'hero_power'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)

    hero = db.relationship('Hero', backref=db.backref('hero_powers', lazy=True))
    power = db.relationship('Power', backref=db.backref('hero_powers', lazy=True))

    @classmethod
    def create(cls, hero, power, strength):
        hero_power = cls(hero=hero, power=power, strength=strength)
        db.session.add(hero_power)
        db.session.commit()
        return hero_power