from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

## MANY to MANY relationships
personajesFavoritos = db.Table("personajesFav",
     db.Column("users_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
     db.Column("personajes_id", db.Integer, db.ForeignKey("personajes.id"), primary_key=True)
)

planetasFavoritos = db.Table("planetasFav",
     db.Column("users_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
     db.Column("planetas_id", db.Integer, db.ForeignKey("planetas.id"), primary_key=True)
)

class Personajes(db.Model):
    __tablename__ = "personajes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    genero = db.Column(db.String(20))
    colorPelo = db.Column(db.String(150))
    colorOjos = db.Column(db.String(150))

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "colorPelo": self.colorPelo,
            "colorOjos": self.colorOjos,
    }

class Planetas(db.Model):
    __tablename__ = "planetas"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    habitantes = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "habitantes": self.habitantes,
    }

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    personajesFav = db.relationship(Personajes,
                    secondary=personajesFavoritos,
                    lazy='subquery',
                    backref=db.backref('usuarios', lazy=True))
    planetasFav = db.relationship(Planetas,
                    secondary=planetasFavoritos,
                    lazy='subquery',
                    backref=db.backref('usuarios', lazy=True))
    
    def __repr__(self):
         return '<User %r>' % self.nickname

    def serialize(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "email": self.email,
            "personajesFav": self.obtener_personajesFav(),
            "planetasFav": self.obtener_planetasFav(),
            # do not serialize the password, its a security breach
        }
    
    def obtener_personajesFav(self):
        return list(map(lambda x: x.serialize(), self.personajesFav))

    def obtener_planetasFav(self):
        return list(map(lambda x: x.serialize(), self.planetasFav))