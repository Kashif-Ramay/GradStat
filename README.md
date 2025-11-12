# 📊 GradStat — Intelligent Statistical Analysis Platform

> **A comprehensive, production-ready web application designed for graduate students, researchers, and data analysts to perform sophisticated statistical analyses with guidance and confidence.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)

## ✨ What Makes GradStat Special

GradStat isn't just another statistical tool—it's an **intelligent analysis companion** that:

- 🎓 **Teaches while you analyze** with contextual help and plain-language explanations
- 🤖 **Guides test selection** with an AI-powered Test Advisor wizard
- 📈 **Creates publication-ready visualizations** with interactive Plotly charts
- ✅ **Validates data quality** automatically with 6 comprehensive checks
- 📝 **Generates APA-formatted results** ready for your research papers
- 🎨 **Offers 5 professional themes** including colorblind-accessible options
- 💡 **Provides 15+ help topics** explaining statistical concepts clearly
- 🔬 **Covers 95% of graduate research needs** with 15+ analysis types

---

## 🚀 Key Features

### 🧙 Intelligent Test Advisor
- **Smart Recommendations**: Answer simple questions, get the right statistical test
- **Auto-Detection**: Upload data once, let GradStat analyze it for you
- **Confidence Indicators**: See how confident the system is about each recommendation
- **Covers All Research Questions**: Compare groups, find relationships, predict outcomes

### 📊 Interactive Visualizations
- **8 Plot Types**: Scatter, box, line, histogram, bar, heatmap, Q-Q plots
- **5 Professional Themes**: Default, colorblind-safe, grayscale, vibrant, scientific
- **Full Interactivity**: Zoom, pan, hover for details, export to PNG
- **Publication-Ready**: High-quality output suitable for journals

### 💡 Contextual Help System
- **15+ Help Topics**: Statistical concepts explained in plain language
- **Hover Tooltips**: Get help exactly where you need it
- **Real Examples**: See how concepts apply to actual research
- **Best Practices**: Learn what to do (and what to avoid)

### ✅ Data Quality Checks
- **6 Automated Checks**: Missing data, outliers, types, sample size, distribution, correlation
- **Quality Score**: Get an overall score (0-100) for your dataset
- **Actionable Recommendations**: Specific suggestions to improve data quality
- **Visual Feedback**: Color-coded indicators (✓ pass, ⚠️ warning, ✗ fail)

### 📝 Plain-Language Interpretations
- **Auto-Generated**: Results explained in clear, jargon-free language
- **Effect Sizes**: Understand practical significance (small/medium/large)
- **APA Format**: One-click copy for research papers
- **Recommendations**: What your results mean and what to do next

### 🔬 Comprehensive Statistical Coverage
- **15+ Analysis Types**: From basic descriptives to advanced models
- **Assumption Checking**: Automated validation of statistical assumptions
- **Power Analysis**: Calculate required sample sizes
- **Post-hoc Tests**: Tukey HSD for multiple comparisons
- **Effect Sizes**: Cohen's d, eta-squared, correlation coefficients

## Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   React     │─────▶│   Express   │─────▶│   Python    │
│  Frontend   │      │   Backend   │      │   Worker    │
│ (Port 3000) │      │ (Port 3001) │      │ (Port 8001) │
└─────────────┘      └─────────────┘      └─────────────┘
```

## 🎯 Quick Start

### Prerequisites

- **Node.js 18+** - [Download](https://nodejs.org/)
- **Python 3.13+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/)

### Installation (5 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/gradstat.git
cd gradstat

# Install Python Worker dependencies
cd worker
pip install -r requirements.txt
cd ..

# Install Backend dependencies
cd backend
npm install
cd ..

# Install Frontend dependencies
cd frontend
npm install --legacy-peer-deps
cd ..
```

### Running the Application

**Open 3 terminal windows:**

#### Terminal 1: Python Worker
```bash
cd worker
python main.py
# Server runs on http://localhost:8001
```

#### Terminal 2: Backend
```bash
cd backend
node server.js
# Server runs on http://localhost:3001
```

#### Terminal 3: Frontend
```bash
cd frontend
npm start
# Opens browser at http://localhost:3000
```

### 🎉 You're Ready!

Open your browser to **http://localhost:3000** and start analyzing!

---

## 📖 Usage Guide

### 1. Upload Your Data
- Click "Choose File" and select your CSV or Excel file
- Preview your data and see automatic quality checks
- Get a quality score (0-100) with recommendations

### 2. Choose Your Analysis Path

#### Option A: Use Test Advisor (Recommended for Beginners)
1. Click "Test Advisor" button
2. Answer simple questions about your research
3. Let GradStat auto-detect data characteristics
4. Get personalized test recommendations

#### Option B: Select Analysis Directly
1. Choose analysis type from dropdown
2. Select variables (dependent, independent, groups)
3. Adjust options (alpha level, test type, etc.)
4. Click "Analyze"

### 3. Explore Results
- **Visualizations**: Interactive Plotly charts (zoom, pan, hover)
- **Test Results**: Statistical tests with p-values and effect sizes
- **Interpretation**: Plain-language explanation of what results mean
- **APA Format**: Copy-paste ready citations for your paper
- **Assumptions**: See which assumptions were met/violated
- **Recommendations**: What to do next

### 4. Export & Share
- Download results as ZIP (HTML report, plots, data)
- Copy APA-formatted results
- Share interactive visualizations

---

## 💡 Example Workflows

### Comparing Two Groups
```
Research Question: Does treatment improve outcomes?

1. Upload data with columns: [subject_id, group, outcome]
2. Use Test Advisor → "Compare Groups"
3. Auto-detect: 2 groups, continuous outcome
4. Get recommendation: Independent t-test
5. View results: t-statistic, p-value, Cohen's d
6. Copy APA format: "t(28) = 3.45, p = .002, d = 0.92"
```

### Finding Relationships
```
Research Question: Is age related to blood pressure?

1. Upload data with columns: [age, blood_pressure]
2. Select "Correlation Analysis"
3. Choose Pearson correlation
4. View results: r = 0.65, p < .001
5. See interpretation: "Strong positive correlation"
```

### Predicting Outcomes
```
Research Question: Can we predict sales from advertising?

1. Upload data with columns: [sales, tv_ads, radio_ads, social_ads]
2. Select "Multiple Linear Regression"
3. Choose outcome: sales, predictors: all ad types
4. View results: R² = 0.78, VIF scores, coefficients
5. Check assumptions: Residual plots, Q-Q plot
```

## API Endpoints

- `POST /api/validate` - Validate and preview uploaded dataset
- `POST /api/analyze` - Start an analysis job
- `GET /api/job-status?id=<job_id>` - Check job status
- `GET /api/report?id=<job_id>` - Download analysis report

See `openapi.yaml` for full API specification.

## 📚 Analysis Types Supported

### Descriptive Statistics
- Summary statistics (mean, median, SD, IQR)
- Distribution analysis with visualizations
- Outlier detection and handling
- Frequency tables and cross-tabulations

### Group Comparisons
- **Parametric**: Independent t-test, Paired t-test, One-way ANOVA, Repeated Measures ANOVA, ANCOVA
- **Non-parametric**: Mann-Whitney U, Wilcoxon Signed-Rank, Kruskal-Wallis H
- **Post-hoc Tests**: Tukey HSD, Bonferroni, Holm
- **Effect Sizes**: Cohen's d, eta-squared, partial eta-squared

### Regression Analysis
- **Simple Linear Regression**: One predictor, one outcome
- **Multiple Linear Regression**: Multiple predictors with VIF for multicollinearity
- **Logistic Regression**: Binary outcomes with ROC curves and confusion matrix
- **Assumption Checking**: Normality, linearity, homoscedasticity

### Correlation Analysis
- **Pearson**: Linear relationships (parametric)
- **Spearman**: Monotonic relationships (non-parametric)
- **Kendall**: Small samples with tied ranks
- **Correlation Matrices**: Heatmaps with significance stars

### Categorical Analysis
- **Chi-square Test**: Independence testing for categorical variables
- **Fisher's Exact Test**: Small sample sizes
- **Automatic Selection**: System chooses appropriate test

### Advanced Analyses
- **PCA**: Dimensionality reduction and visualization
- **Clustering**: K-means, hierarchical, DBSCAN
- **Time Series**: Trend analysis, seasonal decomposition
- **Survival Analysis**: Kaplan-Meier curves, log-rank tests

### Power Analysis
- **Sample Size Calculation**: Determine required n for desired power
- **Power Calculation**: Evaluate power for given sample size
- **Effect Size Detection**: Find detectable effect with current n
- **Test Types**: t-test, ANOVA, correlation

## 🧪 Testing

### Automated Tests
```bash
# Worker tests (Python)
cd worker
pytest

# Test Plotly visualizations
python test_plotly_viz.py

# Backend tests (Node.js)
cd backend
npm test
```

### Manual Testing Checklist
- [ ] Upload CSV and Excel files
- [ ] Run Test Advisor wizard
- [ ] Perform each analysis type
- [ ] Check interactive visualizations
- [ ] Test help tooltips
- [ ] Copy APA format
- [ ] Download results ZIP
- [ ] Test with different browsers

---

## 🎓 Educational Features

### For Students
- **Learn by Doing**: Understand statistics through guided analysis
- **Contextual Help**: 15+ help topics explain concepts clearly
- **Plain Language**: No jargon without explanation
- **Best Practices**: Learn what professional researchers do
- **Mistake Prevention**: Warnings for common errors

### For Instructors
- **Teaching Tool**: Demonstrate statistical concepts interactively
- **Reproducible**: Students can share exact analysis steps
- **Quality Checks**: Teach data validation importance
- **Interpretation**: Show how to explain results properly

---

## 🚀 Deployment

### Local Development (Recommended)
See "Quick Start" section above for running locally.

### Docker Compose (Coming Soon)
```bash
docker-compose up --build
```

### Cloud Deployment Options

#### Heroku
```bash
# Deploy worker
cd worker
heroku create gradstat-worker
git push heroku main

# Deploy backend
cd backend
heroku create gradstat-backend
git push heroku main

# Deploy frontend
cd frontend
npm run build
# Deploy to Netlify/Vercel
```

#### AWS
- **Frontend**: S3 + CloudFront
- **Backend**: Elastic Beanstalk or ECS
- **Worker**: Lambda or ECS

#### Vercel/Netlify (Frontend Only)
```bash
cd frontend
npm run build
# Connect to Vercel/Netlify via GitHub
```

---

## 🔒 Security Considerations

### Data Privacy
- ✅ No data stored permanently
- ✅ Files deleted after analysis
- ✅ Ephemeral sessions
- ✅ No user tracking

### Security Features
- ✅ File upload validation (size, type)
- ✅ Input sanitization
- ✅ Rate limiting on API endpoints
- ✅ CORS protection
- ✅ Error handling without data leakage

### Production Recommendations
- [ ] Enable HTTPS/SSL
- [ ] Add authentication (JWT)
- [ ] Implement file virus scanning
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Add CAPTCHA for public deployments

---

## 📊 Project Statistics

- **Lines of Code**: ~11,000
- **Components**: 15+ React components
- **Analysis Functions**: 20+ Python functions
- **Help Topics**: 15+ comprehensive guides
- **Test Coverage**: All major features tested
- **Development Time**: 6 months
- **Contributors**: Open for contributions!

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Areas for Contribution
- 🐛 **Bug Reports**: Found an issue? Open a GitHub issue
- ✨ **New Features**: Suggest new analysis types or features
- 📚 **Documentation**: Improve guides and help content
- 🌍 **Translations**: Help make GradStat multilingual
- 🎨 **UI/UX**: Improve design and user experience
- 🧪 **Testing**: Add test cases and improve coverage

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit (`git commit -m 'Add amazing feature'`)
6. Push (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style
- **Frontend**: ESLint + Prettier (React/TypeScript)
- **Backend**: ESLint (Node.js)
- **Worker**: Black + Flake8 (Python)

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

**TL;DR**: You can use, modify, and distribute this software freely. Just include the original license and copyright notice.

---

## 🙏 Acknowledgments

### Technologies Used
- **Frontend**: React, TypeScript, TailwindCSS, Plotly.js
- **Backend**: Node.js, Express, Multer
- **Worker**: Python, FastAPI, Pandas, NumPy, SciPy, Statsmodels, Scikit-learn
- **Visualization**: Plotly, Matplotlib, Seaborn

### Inspiration
Built with ❤️ for graduate students and researchers who want to:
- Understand statistics, not just run tests
- Create publication-ready results
- Learn best practices
- Save time on analysis

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/gradstat/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/gradstat/discussions)
- **Email**: support@gradstat.com (coming soon)

---

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] Multi-language support (Spanish, French, Chinese)
- [ ] Bayesian statistics
- [ ] Mixed-effects models
- [ ] Meta-analysis tools
- [ ] Collaborative analysis (multiple users)
- [ ] API for programmatic access
- [ ] Mobile-responsive design improvements
- [ ] Dark mode

### Version 1.5 (In Progress)
- [x] Interactive Plotly visualizations
- [x] Contextual help system
- [x] Plain-language interpretations
- [x] APA format generation
- [x] Test Advisor wizard
- [x] Data quality checks
- [ ] More help tooltips throughout UI
- [ ] Video tutorials

---

## 📄 License & Copyright

**Copyright (c) 2024-2025 Kashif Ramay. All rights reserved.**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### What This Means:
- ✅ Free to use for research and education
- ✅ Free to modify and distribute
- ✅ Free for commercial use
- ✅ Attribution required
- ❌ No warranty provided

---

<div align="center">

**⭐ If GradStat helps your research, please star this repository! ⭐**

Made with 🧠 and ☕ by researchers, for researchers.

**Copyright (c) 2024-2025 Kashif Ramay**

</div>
