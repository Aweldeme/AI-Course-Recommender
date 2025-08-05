# AI-Driven Course Recommendation System

This project is designed to provide personalized course recommendations to students based on their academic history and interests.

## Features
- **Student Profiles:** Major, courses taken, grades, interests.
- **Course Details:** Difficulty, prerequisites, student feedback.
- **Recommendation Engine:** Advanced ML algorithms for personalized course suggestions.
- **Interactive Web UI:** Modern, responsive interface with real-time recommendations.
- **Data Visualization:** Charts and statistics powered by Chart.js.
- **RESTful API:** JSON-based API endpoints for all system interactions.

## 🛠️ Tech Stack

### **Programming Languages**
- **Python 3.x** - Backend development and ML algorithms
- **JavaScript (ES6+)** - Frontend interactivity and API calls
- **HTML5** - Web structure and semantic markup
- **CSS3** - Custom styling and responsive design

### **Frameworks & Libraries**
- **Flask** - Lightweight Python web framework for REST API
- **Flask-CORS** - Cross-Origin Resource Sharing support
- **Tailwind CSS** - Utility-first CSS framework for modern UI
- **Chart.js** - Interactive data visualization and statistics

### **Machine Learning & Data Science**
- **Scikit-learn** - ML algorithms and model training
  - TF-IDF Vectorization for content-based filtering
  - TruncatedSVD for matrix factorization
  - Cosine similarity for user/content matching
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing and array operations
- **SciPy** - Scientific computing utilities

### **Database & Storage**
- **SQLite** - Embedded relational database
- **SQL** - Database queries and data management

### **Development Tools**
- **Git** - Version control system
- **GitHub CLI** - Repository management
- **Python Virtual Environment** - Dependency isolation

## 🧠 Machine Learning Algorithms

Our recommendation system uses a **hybrid ensemble approach** combining three ML techniques:

### **1. Content-Based Filtering (40%)**
- **TF-IDF Vectorization** for text analysis
- **Cosine Similarity** for interest matching
- Analyzes course descriptions vs student interests

### **2. Collaborative Filtering (30%)**
- **Matrix Factorization** using Singular Value Decomposition (SVD)
- **User-Item Matrix** for rating predictions
- Finds similar students and their course preferences

### **3. Feature-Based Scoring (30%)**
- **GPA-Difficulty Matching** algorithm
- **Department Preference** weighting
- **Course Rating & Popularity** factors

### **Ensemble Method**
- Weighted combination of all three approaches
- Normalized scoring with edge case handling
- Excludes already completed courses

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
