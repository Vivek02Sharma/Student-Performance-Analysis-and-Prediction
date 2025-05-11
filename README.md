# Student Performance Analysis and Prediction System

![banner (1)](https://github.com/user-attachments/assets/e104358b-6667-483a-9015-fc064ce42507)


A comprehensive web application built with Streamlit for analyzing and predicting student academic performance using machine learning models. The system provides dashboards for professors and students, performance insights, and predictive analytics.

## Features

- **Role-Based Access**: Separate login portals for professors and students.
- **Interactive Dashboards**: Visualize academic data with charts and statistics.
- **Performance Prediction**: Predict SGPA, Percentage, and Total Marks using pre-trained ML models.
- **Data Analysis**: Explore semester-wise performance trends and course analytics.
- **MongoDB Integration**: Secure storage and retrieval of student records.
- **Automated Reporting**: Generate test reports and prediction results.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/username/student-performance-analysis.git
   ```

2. **Install Dependencies**
  ```bash
  pip install -r requirements.txt
  ```

3. **Set Up MongoDB**
  - Install MongoDB locally and start the service on `mongodb://localhost:27017`.
  - Create a database named `college_db` with collections `professors` and `students`.

4. **Run the Application**
   ```bash
   streamlit run main.py
   ```
