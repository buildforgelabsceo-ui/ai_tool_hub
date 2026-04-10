from datetime import datetime
from . import db

class Tool(db.Model):
    __tablename__ = 'tools'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(280))
    website_url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    logo_url = db.Column(db.String(500), default='/static/logo.png')
    pricing = db.Column(db.String(80), default='Freemium')
    tags = db.Column(db.String(500), default='')
    featured = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'short_description': self.short_description,
            'website_url': self.website_url,
            'category': self.category,
            'logo_url': self.logo_url,
            'pricing': self.pricing,
            'tags': self.tags.split(',') if self.tags else [],
            'featured': self.featured,
            'date_added': self.date_added.isoformat()
        }

    def __repr__(self):
        return f'<Tool {self.name}>'
