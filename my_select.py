from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student, Subject, Grade, Group, Teacher

# Підключення до бази даних
engine = create_engine('sqlite:///university.db')
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    subquery = session.query(
        Grade.student_id,
        func.avg(Grade.grade).label('average_grade')
    ).group_by(Grade.student_id).subquery()

    results = session.query(Student, subquery.c.average_grade).join(
        subquery, Student.id == subquery.c.student_id
    ).order_by(subquery.c.average_grade.desc()).limit(5).all()

    return [(student, average_grade) for student, average_grade in results]

def select_2(subject_id):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    subquery = session.query(
        Grade.student_id,
        func.avg(Grade.grade).label('average_grade')
    ).filter(Grade.subject_id == subject_id).group_by(Grade.student_id).subquery()

    result = session.query(Student, subquery.c.average_grade).join(
        subquery, Student.id == subquery.c.student_id
    ).order_by(subquery.c.average_grade.desc()).first()

    return result

def select_3(subject_id):
    """Знайти середній бал у групах з певного предмета."""
    subquery = session.query(
        Student.group_id,
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).filter(Grade.subject_id == subject_id).group_by(Student.group_id).subquery()

    results = session.query(Group, subquery.c.average_grade).join(
        subquery, Group.id == subquery.c.group_id
    ).all()

    return [(group, average_grade) for group, average_grade in results]

def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    average_grade = session.query(func.avg(Grade.grade)).scalar()
    return average_grade

def select_5(teacher_id):
    """Знайти які курси читає певний викладач."""
    courses = session.query(Subject).filter(Subject.teacher_id == teacher_id).all()
    return courses

def select_6(group_id):
    """Знайти список студентів у певній групі."""
    students = session.query(Student).filter(Student.group_id == group_id).all()
    return students

def select_7(group_id, subject_id):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    grades = session.query(Grade).join(Student).filter(
        Student.group_id == group_id,
        Grade.subject_id == subject_id
    ).all()
    return grades

def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    subquery = session.query(
        Grade.subject_id,
        func.avg(Grade.grade).label('average_grade')
    ).join(Subject).filter(Subject.teacher_id == teacher_id).group_by(Grade.subject_id).subquery()

    average_grade = session.query(func.avg(subquery.c.average_grade)).scalar()
    return average_grade

def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент."""
    subjects = session.query(Subject).join(Grade).filter(Grade.student_id == student_id).distinct().all()
    return subjects

def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач."""
    subjects = session.query(Subject).join(Grade).filter(
        Grade.student_id == student_id,
        Subject.teacher_id == teacher_id
    ).distinct().all()
    return subjects

def select_11(student_id, teacher_id):
    """Середній бал, який певний викладач ставить певному студентові."""
    average_grade = session.query(func.avg(Grade.grade)).join(Subject).filter(
        Grade.student_id == student_id,
        Subject.teacher_id == teacher_id
    ).scalar()
    return average_grade

def select_12(group_id, subject_id):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    subquery = session.query(
        func.max(Grade.date_received).label('last_date'),
        Grade.student_id
    ).filter(
        Grade.subject_id == subject_id
    ).group_by(Grade.student_id).subquery()

    grades = session.query(Grade).join(subquery, 
        (Grade.student_id == subquery.c.student_id) &
        (Grade.date_received == subquery.c.last_date)
    ).join(Student).filter(Student.group_id == group_id).all()

    return grades

if __name__ == '__main__':

    #1
    top_students = select_1()
    print("Top 5 students with highest average grade:")
    for student, average_grade in top_students:
        print(f"{student} - Average Grade: {average_grade}")

    print()
    #2
    best_student = select_2(subject_id=1)
    print("Student with the highest average grade in a specific subject:")
    print(best_student)

    print()
    #3
    average_grade_per_group = select_3(subject_id=1)
    print("Average grade per group for a specific subject:")
    for group, average_grade in average_grade_per_group:
        print(f"{group} - Average Grade: {average_grade}")

    print()
    #4
    overall_average_grade = select_4()
    print("Overall average grade across all grades:")
    print(overall_average_grade)

    print()
    #5
    courses_by_teacher = select_5(teacher_id=1)
    print("Courses taught by a specific teacher:")
    for course in courses_by_teacher:
        print(course)

    print()
    #6
    students_in_group = select_6(group_id=1)
    print("List of students in a specific group:")
    for student in students_in_group:
        print(student)

    print()
    #7
    grades_in_group_for_subject = select_7(group_id=1, subject_id=1)
    print("Grades of students in a specific group for a specific subject:")
    for grade in grades_in_group_for_subject:
        print(grade)

    print()
    #8
    average_grade_by_teacher = select_8(teacher_id=1)
    print("Average grade given by a specific teacher for their subjects:")
    print(average_grade_by_teacher)

    print()
    #9
    courses_by_student = select_9(student_id=1)
    print("Courses attended by a specific student:")
    for course in courses_by_student:
        print(course)

    print()
    #10
    courses_by_teacher_for_student = select_10(student_id=1, teacher_id=1)
    print("Courses taught by a specific teacher to a specific student:")
    for course in courses_by_teacher_for_student:
        print(course)

    print()
    #11
    average_grade_by_teacher_for_student = select_11(student_id=1, teacher_id=1)
    print("Average grade given by a specific teacher to a specific student:")
    print(average_grade_by_teacher_for_student)
    
    print()
    #12
    grades_in_group_for_subject_last_session = select_12(group_id=1, subject_id=1)
    print("Grades of students in a specific group for a specific subject on the last session:")
    for grade in grades_in_group_for_subject_last_session:
        print(grade) 
