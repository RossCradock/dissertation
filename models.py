from config import db


class Coin(db.Model):
    __tablename__ = 'coin'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String(255))
    image_file = db.Column(db.String(255))
    coin_hashrates = db.relationship('CoinHashrate', backref='coin', lazy=True)
    pool_hashrates = db.relationship('PoolHashrate', backref='coin', lazy=True)


class CoinHashrate(db.Model):
    __tablename__ = 'coin_hashrate'
    coin_id = db.Column(db.Integer(), db.ForeignKey('coin.id'), nullable=False)
    hashrate = db.Column(db.Integer)
    week = db.Column(db.Integer())


class MiningPool(db.Model):
    __tablename__ = 'mining_pool'
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    pool_hashrates = db.relationship('PoolHashrate', backref='mining_pool', lazy=True)
    mining_location = db.relationship('MiningLocation', backref='mining_pool', lazy=True)


class PoolHashrate(db.Model):
    __tablename__ = 'pool_hashrate'
    mining_pool_id = db.Column(db.Integer(), db.ForeignKey('mining_pool.id'), nullable=False)
    coin_id = db.Column(db.Integer(), db.ForeignKey('coin.id'), nullable=False)
    hashrate = db.Column(db.Integer())
    week = db.Column(db.Integer())


class MiningLocation(db.Model):
    __tablename__ = 'mining_location'
    mining_pool_id = db.Column(db.Integer(), db.ForeignKey('mining_pool.id'), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
