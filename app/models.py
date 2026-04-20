from app import db
from datetime import datetime

class Formation(db.Model):
    __tablename__ = 'formations'

    id          = db.Column(db.Integer, primary_key=True)
    titre       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duree       = db.Column(db.String(50), nullable=False)
    niveau      = db.Column(db.String(100), nullable=False)
    categorie   = db.Column(db.String(100), nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':          self.id,
            'titre':       self.titre,
            'description': self.description,
            'duree':       self.duree,
            'niveau':      self.niveau,
            'categorie':   self.categorie,
            'created_at':  self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Formation {self.titre}>'
