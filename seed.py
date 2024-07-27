from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student, Group, Teacher, Subject, Grade
import random
from datetime import datetime

fake = Faker()

# Підключення до бази даних
engine = create_engine('sqlite:///university.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Створення груп
groups = [Group(name=f'Group {i+1}') for i in range(3)]
session.add_all(groups)
session.commit()

# Створення викладачів
teachers = [Teacher(name=fake.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

# Створення предметів
subjects = [Subject(name=f'Subject {i+1}', teacher=random.choice(teachers)) for i in range(8)]
session.add_all(subjects)
session.commit()

# Створення студентів
students = [Student(name=fake.name(), group=random.choice(groups)) for _ in range(50)]
session.add_all(students)
session.commit()

# Створення оцінок
for student in students:
    for _ in range(20):
        grade = Grade(
            student=student,
            subject=random.choice(subjects),
            date_received=fake.date_this_year(),
            grade=random.randint(1, 100)
        )
        session.add(grade)
session.commit()
