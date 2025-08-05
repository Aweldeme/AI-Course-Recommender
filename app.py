from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd
from recommendation_engine import get_course_recommendations

app = Flask(__name__)
CORS(app)

def connect_db():
    """Connect to the SQLite database and return the connection."""
    return sqlite3.connect('course_recommender.db')

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/students')
def get_students():
    """Get all students"""
    conn = connect_db()
    students = pd.read_sql('SELECT * FROM students', conn)
    conn.close()
    return jsonify(students.to_dict('records'))

@app.route('/api/courses')
def get_courses():
    """Get all courses"""
    conn = connect_db()
    courses = pd.read_sql('SELECT * FROM courses', conn)
    conn.close()
    return jsonify(courses.to_dict('records'))

@app.route('/api/student/<int:student_id>')
def get_student(student_id):
    """Get a specific student"""
    conn = connect_db()
    student = pd.read_sql('SELECT * FROM students WHERE student_id = ?', conn, params=(student_id,))
    conn.close()
    if not student.empty:
        return jsonify(student.iloc[0].to_dict())
    return jsonify({"error": "Student not found"}), 404

@app.route('/api/student/<int:student_id>/courses')
def get_student_courses(student_id):
    """Get courses taken by a student"""
    conn = connect_db()
    query = '''
    SELECT c.course_code, c.course_name, c.department, sc.grade, sc.semester, sc.year, sc.rating
    FROM student_courses sc
    JOIN courses c ON sc.course_id = c.course_id
    WHERE sc.student_id = ?
    ORDER BY sc.year DESC, sc.semester
    '''
    courses = pd.read_sql(query, conn, params=(student_id,))
    conn.close()
    return jsonify(courses.to_dict('records'))

@app.route('/api/recommend/<int:student_id>')
def recommend_courses(student_id):
    """Get course recommendations for a student"""
    try:
        recommendations = get_course_recommendations(student_id, num_recommendations=6)
        
        # Get additional course details
        conn = connect_db()
        course_ids = recommendations['course_id'].tolist()
        placeholders = ','.join(['?' for _ in course_ids])
        query = f'''
        SELECT course_id, course_code, course_name, department, credits, 
               difficulty_level, prerequisites, description, avg_rating, enrollment_count
        FROM courses
        WHERE course_id IN ({placeholders})
        '''
        detailed_courses = pd.read_sql(query, conn, params=course_ids)
        conn.close()
        
        return jsonify(detailed_courses.to_dict('records'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/course/<int:course_id>')
def get_course(course_id):
    """Get detailed information about a course"""
    conn = connect_db()
    course = pd.read_sql('SELECT * FROM courses WHERE course_id = ?', conn, params=(course_id,))
    conn.close()
    if not course.empty:
        return jsonify(course.iloc[0].to_dict())
    return jsonify({"error": "Course not found"}), 404

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    conn = connect_db()
    
    # Count students by major
    students_by_major = pd.read_sql('SELECT major, COUNT(*) as count FROM students GROUP BY major', conn)
    
    # Count courses by department
    courses_by_dept = pd.read_sql('SELECT department, COUNT(*) as count FROM courses GROUP BY department', conn)
    
    # Average GPA by major
    avg_gpa_by_major = pd.read_sql('SELECT major, AVG(gpa) as avg_gpa FROM students GROUP BY major', conn)
    
    # Top rated courses
    top_courses = pd.read_sql('SELECT course_name, avg_rating FROM courses ORDER BY avg_rating DESC LIMIT 5', conn)
    
    conn.close()
    
    return jsonify({
        'students_by_major': students_by_major.to_dict('records'),
        'courses_by_dept': courses_by_dept.to_dict('records'),
        'avg_gpa_by_major': avg_gpa_by_major.to_dict('records'),
        'top_courses': top_courses.to_dict('records')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
