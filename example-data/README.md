# Example Datasets

This directory contains sample datasets for testing GradStat.

## sample_dataset.csv

A synthetic dataset simulating a study comparing two groups of students.

**Variables:**
- `student_id`: Unique identifier
- `age`: Student age (21-25)
- `gender`: Male/Female
- `study_hours`: Weekly study hours
- `exam_score`: Final exam score (0-100)
- `group`: Control or Treatment group
- `satisfaction`: Satisfaction rating (1-5)
- `gpa`: Grade point average (0-4.0)

**Suggested Analyses:**

1. **Descriptive Statistics**: Get overview of all variables
2. **Group Comparison**: Compare exam scores between Control and Treatment groups
   - Independent variable: `group`
   - Dependent variable: `exam_score`
3. **Regression**: Predict exam score from study hours
   - Independent variable: `study_hours`
   - Dependent variable: `exam_score`
4. **Clustering**: Group students by characteristics
   - Use numeric variables: `age`, `study_hours`, `exam_score`, `gpa`
5. **PCA**: Reduce dimensionality of student characteristics

## Usage

1. Upload the CSV file through the GradStat web interface
2. Select your desired analysis type
3. Configure variables according to your research question
4. Run the analysis and download the report
