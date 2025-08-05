from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
import sqlite3
from scipy.sparse import hstack


def connect_db():
    """Connect to the SQLite database and return the connection."""
    return sqlite3.connect('course_recommender.db')


def get_course_recommendations(student_id, num_recommendations=5):
    """Get advanced course recommendations using multiple ML techniques."""
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch student data including interests, GPA, and major
    cursor.execute('SELECT interests, gpa, major FROM students WHERE student_id = ?', (student_id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        return pd.DataFrame()
    
    student_interests, student_gpa, student_major = student

    # Fetch all courses with comprehensive data
    sql = '''
    SELECT course_id, course_name, description, difficulty_level, credits, 
           avg_rating, enrollment_count, department FROM courses
    '''
    all_courses_df = pd.read_sql(sql, conn)
    
    # Get courses already taken by the student to exclude them
    taken_courses_sql = '''
    SELECT course_id FROM student_courses WHERE student_id = ?
    '''
    taken_courses = pd.read_sql(taken_courses_sql, conn, params=(student_id,))
    taken_course_ids = taken_courses['course_id'].tolist() if not taken_courses.empty else []
    
    # Filter out already taken courses
    available_courses = all_courses_df[~all_courses_df['course_id'].isin(taken_course_ids)].reset_index(drop=True)
    
    if available_courses.empty:
        conn.close()
        return available_courses

    # Content-based filtering using TF-IDF
    tfidf = TfidfVectorizer(stop_words='english', max_features=1000)
    all_descriptions = pd.concat([available_courses['description'], pd.Series([student_interests])], ignore_index=True)
    tfidf_matrix = tfidf.fit_transform(all_descriptions)
    
    # Compute cosine similarity for content-based recommendations
    content_similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    
    # Collaborative filtering using matrix factorization
    try:
        # Create user-item matrix for collaborative filtering
        user_courses_sql = '''
        SELECT student_id, course_id, rating FROM student_courses
        '''
        user_courses = pd.read_sql(user_courses_sql, conn)
        
        if not user_courses.empty:
            # Create pivot table
            user_item_matrix = user_courses.pivot_table(index='student_id', columns='course_id', values='rating', fill_value=0)
            
            # Apply SVD for matrix factorization
            svd = TruncatedSVD(n_components=min(50, user_item_matrix.shape[1]-1), random_state=42)
            user_factors = svd.fit_transform(user_item_matrix)
            
            # Get current student's latent factors
            if student_id in user_item_matrix.index:
                student_idx = user_item_matrix.index.get_loc(student_id)
                student_factors = user_factors[student_idx].reshape(1, -1)
                
                # Compute similarity with other users
                user_similarity = cosine_similarity(student_factors, user_factors).flatten()
                
                # Find similar users
                similar_users = np.argsort(user_similarity)[::-1][1:6]  # Top 5 similar users
                
                # Get collaborative filtering scores
                collab_scores = np.zeros(len(available_courses))
                for course_idx, course_id in enumerate(available_courses['course_id']):
                    if course_id in user_item_matrix.columns:
                        course_ratings = user_item_matrix.loc[user_item_matrix.index[similar_users], course_id]
                        collab_scores[course_idx] = np.mean(course_ratings[course_ratings > 0])
            else:
                collab_scores = np.zeros(len(available_courses))
        else:
            collab_scores = np.zeros(len(available_courses))
    except:
        collab_scores = np.zeros(len(available_courses))
    
    # Feature-based scoring
    feature_scores = np.zeros(len(available_courses))
    for idx, course in available_courses.iterrows():
        score = 0
        
        # GPA-based difficulty matching
        if student_gpa >= 3.5 and course['difficulty_level'] >= 4:
            score += 0.3
        elif student_gpa >= 3.0 and course['difficulty_level'] >= 3:
            score += 0.2
        elif student_gpa < 3.0 and course['difficulty_level'] <= 2:
            score += 0.2
        
        # Department matching (prefer courses in same field)
        if student_major.lower() in course['department'].lower():
            score += 0.4
        
        # Rating and popularity boost
        score += (course['avg_rating'] / 5.0) * 0.2
        score += min(course['enrollment_count'] / 100.0, 0.1)
        
        feature_scores[idx] = score
    
    # Normalize all score types (with proper handling of edge cases)
    def safe_normalize(scores):
        if len(scores) == 0:
            return scores
        min_val = np.min(scores)
        max_val = np.max(scores)
        if max_val - min_val == 0:
            return np.ones_like(scores) / len(scores)
        return (scores - min_val) / (max_val - min_val)
    
    content_similarity = safe_normalize(content_similarity)
    collab_scores = safe_normalize(collab_scores)
    feature_scores = safe_normalize(feature_scores)
    
    # Ensemble scoring: combine different recommendation approaches
    final_scores = (0.4 * content_similarity + 0.3 * collab_scores + 0.3 * feature_scores)
    
    # Get top recommendations
    top_indices = np.argsort(final_scores)[::-1][:num_recommendations]
    recommended_courses = available_courses.iloc[top_indices].copy()
    
    # Add recommendation scores for transparency
    recommended_courses['recommendation_score'] = final_scores[top_indices]
    
    conn.close()
    return recommended_courses


if __name__ == "__main__":
    student_id = 1  # Example student ID
    recommendations = get_course_recommendations(student_id)
    print("Recommended Courses:")
    for idx, row in recommendations.iterrows():
        print(f"Course Name: {row['course_name']}, Description: {row['description']}")
