# GradStat Quick Start Guide

Get up and running with GradStat in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- 4GB RAM available
- Modern web browser

## Installation

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/your-org/gradstat.git
cd gradstat

# Start all services
docker-compose up -d

# Wait for services to start (about 30 seconds)
# Check status
docker-compose ps
```

Access the application at **http://localhost:3000**

### Option 2: Local Development

**Frontend:**
```bash
cd frontend
npm install
npm start
```

**Backend (in new terminal):**
```bash
cd backend
npm install
cp .env.example .env
npm start
```

**Worker (in new terminal):**
```bash
cd worker
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Your First Analysis

### 1. Upload Data

1. Open http://localhost:3000
2. Click "Upload Data" or drag & drop a CSV/Excel file
3. Use the example dataset: `example-data/sample_dataset.csv`
4. Click "Validate & Preview Data"

### 2. Configure Analysis

**For Descriptive Statistics:**
- Select "Descriptive Statistics" from dropdown
- Click "Run Analysis"

**For Group Comparison:**
- Select "Group Comparison"
- Group Variable: `group`
- Outcome Variable: `exam_score`
- Click "Run Analysis"

**For Regression:**
- Select "Regression Analysis"
- Dependent Variable: `exam_score`
- Independent Variable: `study_hours`
- Click "Run Analysis"

### 3. View Results

- Wait for analysis to complete (usually 10-30 seconds)
- View summary, interpretation, and visualizations
- Check assumption tests
- Download full report (ZIP file with HTML, notebook, and images)

## Example Analyses

### Descriptive Statistics

```
Dataset: sample_dataset.csv
Analysis: Descriptive Statistics
Purpose: Get overview of all variables
```

### Compare Two Groups

```
Dataset: sample_dataset.csv
Analysis: Group Comparison
Independent Variable: group (Control vs Treatment)
Dependent Variable: exam_score
Question: Do treatment and control groups differ in exam scores?
```

### Predict Outcome

```
Dataset: sample_dataset.csv
Analysis: Regression
Independent Variable: study_hours
Dependent Variable: exam_score
Question: Does study time predict exam performance?
```

### Find Patterns

```
Dataset: sample_dataset.csv
Analysis: Clustering
Number of Clusters: 3
Purpose: Group students by similar characteristics
```

## Understanding Results

### Summary
Plain-language overview of what was analyzed

### Interpretation
Statistical findings explained in accessible language

### Assumption Checks
- ✅ Green: Assumption met
- ⚠️ Yellow: Assumption violated (consider alternative methods)

### Test Results
Detailed statistical output (p-values, effect sizes, confidence intervals)

### Visualizations
- Histograms: Distribution of variables
- Boxplots: Compare groups
- Scatter plots: Relationships between variables
- Residual plots: Check regression assumptions

### Reproducible Code
Python code snippet to replicate the analysis

## Tips

1. **Data Quality**: Clean your data before analysis (remove duplicates, handle missing values)
2. **Sample Size**: Aim for n ≥ 30 for most analyses
3. **Assumptions**: Pay attention to assumption checks
4. **Effect Sizes**: Report effect sizes, not just p-values
5. **Visualization**: Use plots to understand your data

## Common Issues

### Upload Fails
- Check file format (CSV or Excel only)
- Ensure file size < 50MB
- Verify file is not corrupted

### Analysis Stuck
- Check Docker containers are running: `docker-compose ps`
- View logs: `docker-compose logs worker`
- Restart services: `docker-compose restart`

### Results Not Showing
- Wait for job to complete (check status indicator)
- Refresh the page
- Check browser console for errors

## Next Steps

- Read the full [README.md](README.md) for detailed features
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Review [OpenAPI specification](openapi.yaml) for API details

## Support

- 📖 Documentation: See README.md
- 🐛 Report bugs: GitHub Issues
- 💡 Feature requests: GitHub Issues
- 📧 Contact: support@gradstat.example.com

## Stopping the Application

```bash
# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

Happy analyzing! 📊
