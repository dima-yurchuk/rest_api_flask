from app import db
import enum
from datetime import datetime

class MyEnum(enum.Enum):
    lecture = 1
    practical = 2
    laboratory = 3
    seminar = 4


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    teacher = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Enum(MyEnum), default='lecture')
    is_exam = db.Column(db.Boolean, default=False)
    specialty = db.Column(db.String(25), nullable=False)
    semester = db.Column(db.Integer)

    def __repr__(self):
        return f'<Task {self.id} {self.name} {self.teacher} {self.type} {self.is_exam} {self.specialty} {self.semester}>'