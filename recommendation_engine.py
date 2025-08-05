from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import pandas as pd
import sqlite3


def connect_db():
    """Connect to the SQLite database and return the connection."""
    return sqlite3.connect('course_recommender.db')


def get_course_recommendations(student_id, num_recommendations=5):
    """Get course recommendations for a student based on other students' course feedback."""
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch student courses and interests
    cursor.execute('SELECT interests FROM students WHERE student_id = ?', (student_id,))
    student_interests = cursor.fetchone()[0]

    # Fetch all courses with their descriptions and IDs
    sql = '''
    SELECT course_id, course_name, description FROM courses
    '''
    all_courses_df = pd.read_sql(sql, conn)

    # Vectorize the course descriptions and student interests
    tfidf = TfidfVectorizer(stop_words='english')
    all_descriptions = pd.concat([all_courses_df['description'], pd.Series([student_interests])], ignore_index=True)
    tfidf_matrix = tfidf.fit_transform(all_descriptions)

    # Compute similarity between student interests and course descriptions
    cosine_sim = linear_kernel(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Get indices of most similar courses
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sim_scores[:num_recommendations]]

    # Return course recommendations
    recommended_courses = all_courses_df.iloc[top_indices]
    conn.close()
    return recommended_courses


if __name__ == "__main__":
    student_id = 1  # Example student ID
    recommendations = get_course_recommendations(student_id)
    print("Recommended Courses:")
    for idx, row in recommendations.iterrows():
        print(f"Course Name: {row['course_name']}, Description: {row['description']}")
