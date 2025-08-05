# AI-Driven Course Recommendation System

This project is designed to provide personalized course recommendations to students based on their academic history and interests.

## Features
- **Student Profiles:** Major, courses taken, grades, interests.
- **Course Details:** Difficulty, prerequisites, student feedback.
- **Recommendation Engine:** Uses machine learning to suggest courses.

## Technologies
- **Backend:** Python, SQLite.
- **Machine Learning:** Scikit-learn, Pandas.
- **Web:** Flask (for serving API), possibly extendable with JavaScript/CSS for UI.

## Setup and Usage
1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd AI-Course-Recommender
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Database**
   - Create the database and populate it with mock data by running:
     ```bash
     python database_setup.py
     ```

4. **Run the Recommendation Engine**
   - To test the recommendation engine, execute:
     ```bash
     python recommendation_engine.py
     ```
   - Modify `student_id` in `recommendation_engine.py` to recommend courses for different students.

## Future Enhancements
- **Web UI:** Implement a user-friendly interface with JavaScript/CSS.
- **Advanced Algorithms:** Integrate more sophisticated recommendation algorithms.
