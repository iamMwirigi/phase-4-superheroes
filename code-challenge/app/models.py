from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)

    # Define the relationship between Hero and HeroPower
    powers = db.relationship('HeroPower', back_populates='hero')
    
class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Define the relationship between Power and HeroPower
    heroes = db.relationship('HeroPower', back_populates='power')

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    strength = db.Column(db.String(50), nullable=True)

    # Define the relationship between HeroPower and Hero
    hero = db.relationship('Hero', back_populates='powers')
    # Define the relationship between HeroPower and Power
    power = db.relationship('Power', back_populates='heroes')
    