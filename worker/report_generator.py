"""
Report generation utilities for GradStat
"""

import os
import json
import base64
import zipfile
from pathlib import Path
from datetime import datetime
import nbformat as nbf
from jinja2 import Template
import pandas as pd

def generate_report_package(results: dict, df: pd.DataFrame, opts: dict) -> str:
    """Generate a ZIP package with report, notebook, and results"""
    
    # Create temporary directory for report files
    import tempfile
    temp_dir = tempfile.mkdtemp()
    
    # Generate HTML report
    html_content = generate_html_report(results, opts)
    html_path = os.path.join(temp_dir, 'report.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Generate Jupyter notebook
    notebook = generate_jupyter_notebook(results, opts)
    notebook_path = os.path.join(temp_dir, 'analysis.ipynb')
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(notebook, f)
    
    # Save results JSON
    results_path = os.path.join(temp_dir, 'results.json')
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Save plots as separate images
    images_dir = os.path.join(temp_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    if 'plots' in results:
        for i, plot in enumerate(results['plots']):
            if 'base64' in plot:
                img_data = base64.b64decode(plot['base64'])
                img_path = os.path.join(images_dir, f'plot_{i+1}.png')
                with open(img_path, 'wb') as f:
                    f.write(img_data)
    
    # Create ZIP file
    zip_path = os.path.join(temp_dir, 'report.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(html_path, 'report.html')
        zipf.write(notebook_path, 'analysis.ipynb')
        zipf.write(results_path, 'results.json')
        
        # Add images
        for root, dirs, files in os.walk(images_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.join('images', file)
                zipf.write(file_path, arcname)
    
    # Read ZIP and convert to base64
    with open(zip_path, 'rb') as f:
        zip_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)
    
    return zip_base64

def generate_html_report(results: dict, opts: dict) -> str:
    """Generate HTML report from results"""
    
    template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GradStat Analysis Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .section {
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 { margin: 0; font-size: 2em; }
        h2 { color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
        h3 { color: #555; }
        .summary {
            background: #e3f2fd;
            padding: 15px;
            border-left: 4px solid #2196f3;
            margin: 15px 0;
        }
        .assumption {
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .assumption.passed {
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
        }
        .assumption.failed {
            background: #fff3e0;
            border-left: 4px solid #ff9800;
        }
        .plot {
            margin: 20px 0;
            text-align: center;
        }
        .plot img {
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        pre {
            background: #263238;
            color: #aed581;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #f5f5f5;
            font-weight: 600;
        }
        .recommendations {
            background: #f3e5f5;
            padding: 15px;
            border-left: 4px solid #9c27b0;
            margin: 15px 0;
        }
        .recommendations ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .footer {
            text-align: center;
            color: #666;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 GradStat Analysis Report</h1>
        <p>Generated on {{ timestamp }}</p>
        <p><strong>Analysis Type:</strong> {{ analysis_type }}</p>
    </div>

    <div class="section">
        <h2>Summary</h2>
        <div class="summary">
            {{ summary }}
        </div>
    </div>

    {% if interpretation %}
    <div class="section">
        <h2>Interpretation</h2>
        <p>{{ interpretation }}</p>
    </div>
    {% endif %}

    {% if assumptions %}
    <div class="section">
        <h2>Assumption Checks</h2>
        {% for assumption in assumptions %}
        <div class="assumption {{ 'passed' if assumption.passed else 'failed' }}">
            <strong>{{ '✅' if assumption.passed else '⚠️' }} {{ assumption.name }}</strong>
            <p>{{ assumption.message }}</p>
            {% if assumption.pValue %}
            <small>p-value: {{ "%.4f"|format(assumption.pValue) }}</small>
            {% endif %}
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% if test_results %}
    <div class="section">
        <h2>Statistical Results</h2>
        <pre>{{ test_results_json }}</pre>
    </div>
    {% endif %}

    {% if plots %}
    <div class="section">
        <h2>Visualizations</h2>
        {% for plot in plots %}
        <div class="plot">
            <h3>{{ plot.title }}</h3>
            <img src="data:image/png;base64,{{ plot.base64 }}" alt="{{ plot.title }}">
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% if code_snippet %}
    <div class="section">
        <h2>Reproducible Code</h2>
        <pre>{{ code_snippet }}</pre>
    </div>
    {% endif %}

    {% if recommendations %}
    <div class="section">
        <h2>Recommendations</h2>
        <div class="recommendations">
            <ul>
            {% for rec in recommendations %}
                <li>{{ rec }}</li>
            {% endfor %}
            </ul>
        </div>
    </div>
    {% endif %}

    {% if conclusion %}
    <div class="section">
        <h2>📝 Conclusion</h2>
        <div class="summary" style="background: #fff9e6; border-left: 4px solid #ffc107;">
            <p style="font-size: 1.05em; line-height: 1.8;">{{ conclusion }}</p>
        </div>
    </div>
    {% endif %}

    <div class="footer">
        <p>Generated by GradStat v0.1.0</p>
        <p>Automated Statistical Analysis Platform for Graduate Research</p>
    </div>
</body>
</html>
    """)
    
    return template.render(
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        analysis_type=results.get('analysis_type', 'Unknown').title(),
        summary=results.get('summary', ''),
        interpretation=results.get('interpretation', ''),
        assumptions=results.get('assumptions', []),
        test_results=results.get('test_results'),
        test_results_json=json.dumps(results.get('test_results', {}), indent=2, default=str),
        plots=results.get('plots', []),
        code_snippet=results.get('code_snippet', ''),
        recommendations=results.get('recommendations', []),
        conclusion=results.get('conclusion', '')
    )

def generate_jupyter_notebook(results: dict, opts: dict) -> nbf.NotebookNode:
    """Generate Jupyter notebook with analysis code"""
    
    nb = nbf.v4.new_notebook()
    
    # Title cell
    nb.cells.append(nbf.v4.new_markdown_cell(f"""# GradStat Analysis Report
    
**Analysis Type:** {results.get('analysis_type', 'Unknown')}  
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary

{results.get('summary', '')}
"""))
    
    # Import cell
    nb.cells.append(nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

# Set plotting style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
"""))
    
    # Data loading cell
    nb.cells.append(nbf.v4.new_code_cell("""# Load your data
df = pd.read_csv('your_data.csv')
df.head()
"""))
    
    # Analysis code
    if results.get('code_snippet'):
        nb.cells.append(nbf.v4.new_markdown_cell("## Analysis Code"))
        nb.cells.append(nbf.v4.new_code_cell(results['code_snippet']))
    
    # Results
    if results.get('test_results'):
        nb.cells.append(nbf.v4.new_markdown_cell("## Results"))
        nb.cells.append(nbf.v4.new_code_cell(f"""# Statistical results
results = {json.dumps(results['test_results'], indent=2, default=str)}
print(results)
"""))
    
    # Interpretation
    if results.get('interpretation'):
        nb.cells.append(nbf.v4.new_markdown_cell(f"""## Interpretation

{results['interpretation']}
"""))
    
    # Recommendations
    if results.get('recommendations'):
        recs = '\n'.join([f"- {r}" for r in results['recommendations']])
        nb.cells.append(nbf.v4.new_markdown_cell(f"""## Next Steps

{recs}
"""))
    
    return nb
