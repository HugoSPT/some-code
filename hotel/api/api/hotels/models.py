from api import db


class Base(db.Model):

    __abstract__  = True

    id = db.Column(db.Integer, primary_key=True)

    def to_json(self):
        return {key.name: getattr(self, key.name) for key in self.__table__.columns}

"""
    Represents a Accommodation type object stored in MySQL

    An accommodation type is typically Hotel, Hostel, etc
"""
class Accommodation(Base):

    __tablename__ = 'accommodation'

    type = db.Column(db.String(255), nullable=False)

    hotels = db.relationship("Hotel", backref='accommodation')

"""
    Represents a StarsRating object stored in MySQL

    A star rating is typically a number from 1 to 5
"""
class StarsRating(Base):

    __tablename__ = 'stars_rating'

    rating = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.Integer, nullable=False)

    hotels = db.relationship("Hotel", backref='stars_rating')

"""
    Represents a Hotel object stored in MySQL

    A Hotel has a name, an address, an accommodation type and stars
"""
class Hotel(Base):

    __tablename__ = 'hotel'

    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    accommodation_id = db.Column(db.Integer, db.ForeignKey('accommodation.id'))
    stars_rating_id = db.Column(db.Integer, db.ForeignKey('stars_rating.id'))

    """
        Creates a Hotel object instance

        Args:
            name: the hotel's name
            address: the hotel's address
    """
    def __init__(self, name, address):
        self.name = name
        self.address = address

    """
        Builds a Hotel object (by assigning his variables) from a JSON

        Args:
            data: the JSON to be converted
    """
    def parse(self, data):
        for key, value in data.items():
            if key in self.__table__.columns:
                setattr(self, key, value)

    """
        Hotel insertion into MySQL

        Returns:
            id: the ID of the new hotel

        Raises:
            Exception: when something goes wrong with MySQL
    """
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self.id
        except Exception as e:
            raise Exception('Problems inserting into the DB: {}'.format(e))

    """
        Hotel update into MySQL

        Raises:
            Exception: when something goes wrong with MySQL
    """
    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            raise Exception('Problems updating hotel {}: {}'.format(self.id, e))

    """
        Hotel deletion from MySQL

        Raises:
            Exception: when something goes wrong with MySQL
    """
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            raise Exception('Problems deleting hotel {}: {}'.format(self.id, e))

    """
        Matches a given (sub) string to the hotel's name or address
        
        Args:
            term: the term to be searched

        Returns:
            results: all the hotels with a matched name or address
    """
    @classmethod
    def search(kls, term):
        response =  db.engine.execute("SELECT id, name, address FROM hotel WHERE name LIKE \"%%" + term + "%%\" OR address LIKE \"%%" + term + "%%\" GROUP BY id")
        results = []
        for result in response:
            results.append({
                'id': result['id'],
                'name': result['name'],
                'address': result['address'],
            })
        return results
