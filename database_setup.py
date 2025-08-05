import sqlite3
import random
from datetime import datetime, timedelta

def create_database():
    """Create and populate the database with mock data"""
    conn = sqlite3.connect('course_recommender.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        major TEXT NOT NULL,
        year INTEGER NOT NULL,
        gpa REAL NOT NULL,
        interests TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_code TEXT UNIQUE NOT NULL,
        course_name TEXT NOT NULL,
        department TEXT NOT NULL,
        credits INTEGER NOT NULL,
        difficulty_level INTEGER NOT NULL,
        prerequisites TEXT,
        description TEXT,
        avg_rating REAL DEFAULT 0.0,
        enrollment_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id INTEGER,
        grade TEXT,
        semester TEXT,
        year INTEGER,
        rating INTEGER,
        FOREIGN KEY (student_id) REFERENCES students (student_id),
        FOREIGN KEY (course_id) REFERENCES courses (course_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id INTEGER,
        confidence_score REAL,
        reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (student_id) REFERENCES students (student_id),
        FOREIGN KEY (course_id) REFERENCES courses (course_id)
    )
    ''')
    
    # Mock data for students
    students_data = [
        ("Alice Johnson", "alice.johnson@university.edu", "Computer Science", 3, 3.8, "Machine Learning, Web Development, Data Science"),
        ("Bob Smith", "bob.smith@university.edu", "Mathematics", 2, 3.6, "Statistics, Algorithms, Cryptography"),
        ("Carol Davis", "carol.davis@university.edu", "Engineering", 4, 3.9, "AI, Robotics, Control Systems"),
        ("David Wilson", "david.wilson@university.edu", "Physics", 3, 3.4, "Quantum Mechanics, Astronomy, Programming"),
        ("Emma Brown", "emma.brown@university.edu", "Computer Science", 2, 3.7, "Software Engineering, Databases, UI/UX"),
        ("Frank Miller", "frank.miller@university.edu", "Data Science", 3, 3.5, "Analytics, Machine Learning, Statistics"),
        ("Grace Lee", "grace.lee@university.edu", "Mathematics", 4, 4.0, "Pure Mathematics, Logic, Computer Science"),
        ("Henry Taylor", "henry.taylor@university.edu", "Engineering", 2, 3.3, "Mechanical Design, Programming, CAD"),
        ("Ivy Chen", "ivy.chen@university.edu", "Computer Science", 3, 3.8, "Artificial Intelligence, Neural Networks"),
        ("Jack Wilson", "jack.wilson@university.edu", "Physics", 4, 3.6, "Theoretical Physics, Mathematics, Programming")
    ]
    
    cursor.executemany('''
    INSERT INTO students (name, email, major, year, gpa, interests)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', students_data)
    
    # Mock data for courses
    courses_data = [
        ("CS101", "Introduction to Programming", "Computer Science", 3, 2, "", "Basic programming concepts using Python"),
        ("CS201", "Data Structures", "Computer Science", 3, 3, "CS101", "Arrays, lists, trees, graphs, and algorithms"),
        ("CS301", "Machine Learning", "Computer Science", 4, 4, "CS201,MATH201", "Supervised and unsupervised learning algorithms"),
        ("CS401", "Advanced AI", "Computer Science", 4, 5, "CS301", "Deep learning, neural networks, and AI applications"),
        ("MATH101", "Calculus I", "Mathematics", 4, 3, "", "Limits, derivatives, and basic integration"),
        ("MATH201", "Statistics", "Mathematics", 3, 3, "MATH101", "Probability theory and statistical analysis"),
        ("MATH301", "Linear Algebra", "Mathematics", 3, 4, "MATH101", "Vectors, matrices, and linear transformations"),
        ("ENG201", "Engineering Mechanics", "Engineering", 4, 4, "MATH101", "Statics and dynamics in engineering systems"),
        ("ENG301", "Control Systems", "Engineering", 3, 5, "ENG201,MATH301", "Feedback control and system design"),
        ("PHYS201", "Quantum Physics", "Physics", 4, 5, "MATH101", "Quantum mechanics and atomic structure"),
        ("CS202", "Database Systems", "Computer Science", 3, 3, "CS101", "Relational databases and SQL"),
        ("CS302", "Web Development", "Computer Science", 3, 2, "CS101", "HTML, CSS, JavaScript, and web frameworks"),
        ("CS402", "Software Engineering", "Computer Science", 4, 4, "CS201", "Software development lifecycle and project management"),
        ("MATH401", "Advanced Calculus", "Mathematics", 4, 5, "MATH301", "Multivariable calculus and differential equations"),
        ("ENG401", "Robotics", "Engineering", 4, 5, "ENG301,CS201", "Robot design, control, and programming"),
        ("DS201", "Data Analytics", "Data Science", 3, 3, "MATH201", "Data visualization and statistical modeling"),
        ("DS301", "Big Data", "Data Science", 4, 4, "DS201,CS202", "Hadoop, Spark, and distributed computing"),
        ("CS203", "Computer Graphics", "Computer Science", 3, 4, "MATH301", "2D and 3D graphics programming"),
        ("CS303", "Computer Vision", "Computer Science", 4, 5, "CS301,MATH301", "Image processing and pattern recognition"),
        ("MATH302", "Discrete Mathematics", "Mathematics", 3, 3, "MATH101", "Logic, sets, and combinatorics")
    ]
    
    for course in courses_data:
        cursor.execute('''
        INSERT INTO courses (course_code, course_name, department, credits, difficulty_level, prerequisites, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', course)
        
        # Add random ratings and enrollment
        avg_rating = round(random.uniform(3.5, 5.0), 1)
        enrollment = random.randint(20, 150)
        cursor.execute('''
        UPDATE courses SET avg_rating = ?, enrollment_count = ? WHERE course_code = ?
        ''', (avg_rating, enrollment, course[0]))
    
    # Mock data for student_courses (student enrollment history)
    semesters = ["Fall", "Spring", "Summer"]
    years = [2022, 2023, 2024]
    grades = ["A", "A-", "B+", "B", "B-", "C+", "C"]
    
    # Generate random course history for each student
    for student_id in range(1, 11):  # 10 students
        # Each student has taken 8-15 courses
        num_courses = random.randint(8, 15)
        taken_courses = random.sample(range(1, 21), num_courses)  # Random courses from 20 available
        
        for course_id in taken_courses:
            grade = random.choice(grades)
            semester = random.choice(semesters)
            year = random.choice(years)
            rating = random.randint(3, 5)
            
            cursor.execute('''
            INSERT INTO student_courses (student_id, course_id, grade, semester, year, rating)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (student_id, course_id, grade, semester, year, rating))
    
    conn.commit()
    conn.close()
    print("Database created and populated with mock data successfully!")

if __name__ == "__main__":
    create_database()
