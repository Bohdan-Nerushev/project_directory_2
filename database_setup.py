from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship("Student", back_populates="group")
    
    def __repr__(self):
        return f"Group(id={self.id}, name='{self.name}')"

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship("Group", back_populates="students")
    
    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}', group_id={self.group_id})"

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"Teacher(id={self.id}, name='{self.name}')"

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    teacher = relationship("Teacher")
    
    def __repr__(self):
        return f"Subject(id={self.id}, name='{self.name}', teacher_id={self.teacher_id})"

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    date_received = Column(Date)
    grade = Column(Integer)
    student = relationship("Student")
    subject = relationship("Subject")
    
    def __repr__(self):
        return f"Grade(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id}, date_received={self.date_received}, grade={self.grade})"

# Підключення до бази даних SQLite
engine = create_engine('sqlite:///university.db')
Base.metadata.create_all(engine)
