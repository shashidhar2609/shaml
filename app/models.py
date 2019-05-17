from app import db


class Result(db.Model):
    """
    Create a Result table
    """

    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(60), nullable=False)
    file_name = db.Column(db.String(60), nullable=False)
    attr1 = db.Column(db.String(60), nullable=False)
    ratio1 = db.Column(db.Float(6, 4), nullable=False)
    attr2 = db.Column(db.String(60), nullable=False)
    ratio2 = db.Column(db.Float(6, 4), nullable=False)
    attr3 = db.Column(db.String(60), nullable=False)
    ratio3 = db.Column(db.Float(6, 4), nullable=False)
    algo1=db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '{} - {}\'s top 3 attributes {}-{}, {}-{}, {}-{}'.format(
            self.company_name, self.perform,
            self.attr1, self.ratio1,
            self.attr2, self.ratio2,
            self.attr3, self.ratio3,
            Self.algo1
            
        )
