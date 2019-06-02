from app import db
from app import source

m=source.query.filter_by(id=1).first()
db.session.delete(m)
db.session.commit()
