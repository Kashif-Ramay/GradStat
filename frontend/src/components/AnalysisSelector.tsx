import React from 'react';
import { AnalysisOptions } from '../types';
import HelpTooltip from './HelpTooltip';

interface AnalysisSelectorProps {
  analysisType: string;
  onAnalysisTypeChange: (type: string) => void;
  options: AnalysisOptions;
  onOptionsChange: (options: AnalysisOptions) => void;
  columns: string[];
  columnTypes: { [key: string]: string };
  onAnalyze: () => void;
  loading: boolean;
}

const AnalysisSelector: React.FC<AnalysisSelectorProps> = ({
  analysisType,
  onAnalysisTypeChange,
  options,
  onOptionsChange,
  columns,
  columnTypes,
  onAnalyze,
  loading,
}) => {
  const numericColumns = columns.filter(
    (col) => columnTypes[col] === 'float64' || columnTypes[col] === 'int64' || columnTypes[col] === 'numeric'
  );
  const categoricalColumns = columns.filter(
    (col) => columnTypes[col] === 'object' || columnTypes[col] === 'category' || columnTypes[col] === 'string'
  );

  // Helper to identify likely binary columns (for event indicators)
  const isBinaryColumn = (col: string): boolean => {
    const colType = columnTypes[col];
    // Binary columns are typically int64 with values 0 and 1
    return colType === 'int64' || colType === 'bool';
  };

  // Helper to check if event column is likely wrong
  const isEventColumnValid = (col: string): boolean => {
    if (!col) return true; // Not selected yet
    const colType = columnTypes[col];
    // Event column should be numeric (int or bool), not categorical
    return colType === 'int64' || colType === 'float64' || colType === 'bool' || colType === 'numeric';
  };

  const updateOption = (key: string, value: any) => {
    const newOptions = { ...options, [key]: value };
    console.log('Updating options:', key, '=', value);
    console.log('New options object:', newOptions);
    onOptionsChange(newOptions);
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Configure Analysis</h2>

      {/* Analysis Type Selection - Hide for power analysis */}
      {analysisType !== 'power' && (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Analysis Type
          </label>
          <select
            value={analysisType}
            onChange={(e) => onAnalysisTypeChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="descriptive">Descriptive Statistics</option>
            <option value="group-comparison">Group Comparison (t-test/ANOVA)</option>
            <option value="ancova">ANCOVA (ANOVA with Covariates)</option>
            <option value="repeated-measures">Repeated Measures ANOVA</option>
            <option value="posthoc-tukey">Post-hoc Tests (Tukey HSD)</option>
            <option value="correlation">Correlation Analysis</option>
            <option value="regression">Simple Linear Regression</option>
            <option value="multiple-regression">Multiple Regression</option>
            <option value="logistic-regression">Logistic Regression (Classification)</option>
            <option value="survival">Survival Analysis (Kaplan-Meier, Cox)</option>
            <option value="nonparametric">Non-Parametric Tests</option>
            <option value="categorical">Categorical Analysis (Chi-square)</option>
            <option value="clustering">Clustering</option>
            <option value="pca">PCA / Dimensionality Reduction</option>
            <option value="time-series">Time Series Analysis</option>
          </select>
        </div>
      )}

      {/* Analysis-specific options */}
      {analysisType === 'power' ? (
        /* Power Analysis Options - Always shown in Power Analysis mode */
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Test Type
            </label>
            <select
              value={options.powerAnalysisType || 't-test'}
              onChange={(e) => updateOption('powerAnalysisType', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="t-test">Independent t-test (2 groups)</option>
              <option value="anova">ANOVA (3+ groups)</option>
              <option value="correlation">Correlation</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              What to Calculate
            </label>
            <select
              value={options.calculate || 'sample_size'}
              onChange={(e) => updateOption('calculate', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="sample_size">Required Sample Size</option>
              <option value="power">Statistical Power</option>
              <option value="effect_size">Detectable Effect Size</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Effect Size
            </label>
            <input
              type="number"
              step="0.1"
              min="0.1"
              max="2.0"
              value={options.effectSize || 0.5}
              onChange={(e) => updateOption('effectSize', parseFloat(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-xs text-gray-500 mt-1">
              {options.powerAnalysisType === 'correlation' 
                ? 'Correlation (r): Small=0.1, Medium=0.3, Large=0.5'
                : options.powerAnalysisType === 'anova'
                ? "Cohen's f: Small=0.1, Medium=0.25, Large=0.4"
                : "Cohen's d: Small=0.2, Medium=0.5, Large=0.8"}
            </p>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Significance Level (α)
            </label>
            <select
              value={options.alpha || 0.05}
              onChange={(e) => updateOption('alpha', parseFloat(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="0.10">0.10 (10%)</option>
              <option value="0.05">0.05 (5%) - Standard</option>
              <option value="0.01">0.01 (1%)</option>
            </select>
          </div>

          {options.calculate !== 'power' && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Desired Power (1 - β)
              </label>
              <select
                value={(options.power || 0.8).toFixed(2)}
                onChange={(e) => {
                  console.log('Power changed to:', e.target.value);
                  updateOption('power', parseFloat(e.target.value));
                }}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="0.70">0.70 (70%)</option>
                <option value="0.80">0.80 (80%) - Standard</option>
                <option value="0.90">0.90 (90%) - High</option>
                <option value="0.95">0.95 (95%) - Very High</option>
              </select>
            </div>
          )}

          {options.calculate !== 'sample_size' && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sample Size per Group
              </label>
              <input
                type="number"
                min="10"
                max="1000"
                value={options.sampleSize || 30}
                onChange={(e) => updateOption('sampleSize', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
          )}

          {options.powerAnalysisType === 'anova' && (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Groups
              </label>
              <input
                type="number"
                min="2"
                max="10"
                value={options.nGroups || 3}
                onChange={(e) => updateOption('nGroups', parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
          )}

          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg mb-4">
            <p className="text-sm text-blue-800">
              💡 <strong>Power Analysis</strong> helps you determine the required sample size for your study, 
              or assess the statistical power of your existing data. No dataset upload needed!
            </p>
          </div>
        </>
      ) : null}

      {analysisType === 'group-comparison' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Group Variable (Independent)
            </label>
            <select
              value={options.groupVar || ''}
              onChange={(e) => updateOption('groupVar', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {categoricalColumns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Outcome Variable (Dependent)
            </label>
            <select
              value={options.dependentVar || ''}
              onChange={(e) => updateOption('dependentVar', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {numericColumns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>
        </>
      )}

      {analysisType === 'ancova' && (
        <>
          <div className="mb-4">
            <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
              Group Variable
              <HelpTooltip contentId="group-variable" position="top" className="ml-2" />
            </label>
            <select
              value={options.groupVar || ''}
              onChange={(e) => updateOption('groupVar', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {categoricalColumns.map((col) => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
          </div>
          <div className="mb-4">
            <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
              Dependent Variable
              <HelpTooltip contentId="dependent-variable" position="top" className="ml-2" />
            </label>
            <select
              value={options.dependentVar || ''}
              onChange={(e) => updateOption('dependentVar', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {numericColumns.map((col) => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Covariates (Ctrl/Cmd+Click for multiple)
            </label>
            <select
              multiple
              value={options.covariates || []}
              onChange={(e) => updateOption('covariates', Array.from(e.target.selectedOptions, option => option.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 h-32"
            >
              {numericColumns.map((col) => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
          </div>
        </>
      )}

      {analysisType === 'repeated-measures' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Subject ID Column
            </label>
            <select
              value={options.subjectVar || ''}
              onChange={(e) => updateOption('subjectVar', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {columns.map((col) => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Time/Condition Variable
            </label>
            <select
              value={options.timeVar || ''}
              onChange={(e) => updateOption('timeVar', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {categoricalColumns.map((col) => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dependent Variable
            </label>
            <select
              value={options.dependentVar || ''}
              onChange={(e) => updateOption('dependentVar', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {numericColumns.map((col) => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
          </div>
        </>
      )}

      {analysisType === 'posthoc-tukey' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Group Variable
            </label>
            <select
              value={options.groupVar || ''}
              onChange={(e) => updateOption('groupVar', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {categoricalColumns.map((col) => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dependent Variable
            </label>
            <select
              value={options.dependentVar || ''}
              onChange={(e) => updateOption('dependentVar', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {numericColumns.map((col) => (
                <option key={col} value={col}>{col}</option>
              ))}
            </select>
          </div>
        </>
      )}

      {analysisType === 'correlation' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Correlation Method
            </label>
            <select
              value={options.correlationMethod || 'pearson'}
              onChange={(e) => updateOption('correlationMethod', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="pearson">Pearson (linear relationships)</option>
              <option value="spearman">Spearman (monotonic relationships)</option>
              <option value="kendall">Kendall's Tau (ordinal data)</option>
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Pearson for linear, Spearman for non-linear but monotonic, Kendall for small samples
            </p>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Variables to Correlate - Hold Ctrl/Cmd to select multiple
            </label>
            <select
              multiple
              value={options.variables || []}
              onChange={(e) => {
                const selected = Array.from(e.target.selectedOptions, option => option.value);
                updateOption('variables', selected);
              }}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 min-h-[150px]"
            >
              {numericColumns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Selected: {(options.variables || []).length} variable(s) - Select 2+ variables
            </p>
          </div>
        </>
      )}

      {analysisType === 'regression' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dependent Variable (Y)
            </label>
            <select
              value={options.dependentVar || ''}
              onChange={(e) => updateOption('dependentVar', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {numericColumns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Independent Variable (X)
            </label>
            <select
              value={options.independentVar || ''}
              onChange={(e) => updateOption('independentVar', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {numericColumns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>
        </>
      )}

      {analysisType === 'multiple-regression' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dependent Variable (Y)
            </label>
            <select
              value={options.dependentVar || ''}
              onChange={(e) => updateOption('dependentVar', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {numericColumns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Independent Variables (X) - Hold Ctrl/Cmd to select multiple
            </label>
            <select
              multiple
              value={options.independentVars || []}
              onChange={(e) => {
                const selected = Array.from(e.target.selectedOptions, option => option.value);
                updateOption('independentVars', selected);
              }}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 min-h-[120px]"
            >
              {numericColumns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Selected: {(options.independentVars || []).length} variable(s)
            </p>
          </div>
        </>
      )}

      {analysisType === 'logistic-regression' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Variable (Binary Outcome)
            </label>
            <select
              value={options.targetColumn || ''}
              onChange={(e) => updateOption('targetColumn', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {columns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Must be binary (0/1 or two categories)
            </p>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Predictor Variables - Hold Ctrl/Cmd to select multiple
            </label>
            <select
              multiple
              value={options.predictorColumns || []}
              onChange={(e) => {
                const selected = Array.from(e.target.selectedOptions, option => option.value);
                updateOption('predictorColumns', selected);
              }}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 min-h-[120px]"
            >
              {numericColumns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Selected: {(options.predictorColumns || []).length} variable(s)
            </p>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Test Size (Train/Test Split)
            </label>
            <select
              value={options.testSize || 0.3}
              onChange={(e) => updateOption('testSize', parseFloat(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="0.2">20% Test, 80% Train</option>
              <option value="0.25">25% Test, 75% Train</option>
              <option value="0.3">30% Test, 70% Train (Default)</option>
              <option value="0.4">40% Test, 60% Train</option>
            </select>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Random State (Seed)
            </label>
            <input
              type="number"
              value={options.randomState || 42}
              onChange={(e) => updateOption('randomState', parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="42"
            />
            <p className="text-xs text-gray-500 mt-1">
              For reproducible results (default: 42)
            </p>
          </div>

          <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg mb-4">
            <p className="text-sm text-purple-800">
              🎯 <strong>Logistic Regression</strong> predicts binary outcomes with ROC curve, 
              confusion matrix, and classification metrics (AUC, precision, recall, F1-score).
            </p>
          </div>
        </>
      )}

      {analysisType === 'survival' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Duration Column (Time to Event)
            </label>
            <select
              value={options.durationColumn || ''}
              onChange={(e) => updateOption('durationColumn', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {numericColumns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Time until event or censoring
            </p>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Event Column (Status Indicator)
            </label>
            <select
              value={options.eventColumn || ''}
              onChange={(e) => updateOption('eventColumn', e.target.value)}
              className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 ${
                options.eventColumn && !isEventColumnValid(options.eventColumn)
                  ? 'border-red-500 bg-red-50'
                  : 'border-gray-300'
              }`}
            >
              <option value="">Select column...</option>
              {numericColumns.map((col) => (
                <option key={col} value={col}>
                  {col} {isBinaryColumn(col) ? '✓ (binary)' : ''}
                </option>
              ))}
            </select>
            {options.eventColumn && !isEventColumnValid(options.eventColumn) && (
              <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-xs text-red-700">
                ⚠️ <strong>Warning:</strong> Column '{options.eventColumn}' appears to be categorical (text). 
                Event column must contain numeric values (0 or 1). Please select a different column.
              </div>
            )}
            <p className="text-xs text-gray-500 mt-1">
              Must contain binary values: 1 = event occurred, 0 = censored
            </p>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Group Column (Optional - for comparison)
            </label>
            <select
              value={options.groupColumn || ''}
              onChange={(e) => updateOption('groupColumn', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">None (overall survival)</option>
              {columns.filter(col => col !== options.durationColumn && col !== options.eventColumn).map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Compare survival curves between groups (e.g., treatment, stage)
            </p>
          </div>

          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Covariates (Optional - for Cox regression)
            </label>
            <select
              multiple
              value={options.covariates || []}
              onChange={(e) => {
                const selected = Array.from(e.target.selectedOptions, option => option.value);
                updateOption('covariates', selected);
              }}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 min-h-[100px]"
            >
              {numericColumns
                .filter(col => 
                  col !== options.durationColumn && 
                  col !== options.eventColumn && 
                  col !== options.groupColumn
                )
                .map((col) => (
                  <option key={col} value={col}>
                    {col}
                  </option>
                ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Selected: {(options.covariates || []).length} covariate(s) - Hold Ctrl/Cmd to select multiple
            </p>
          </div>

          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg mb-4">
            <p className="text-sm text-blue-900 font-semibold mb-2">
              📋 Column Requirements:
            </p>
            <ul className="text-xs text-blue-800 space-y-1 ml-4">
              <li><strong>Duration:</strong> Numeric (time values)</li>
              <li><strong>Event:</strong> Binary numeric (0 or 1 only)</li>
              <li><strong>Group:</strong> Any type (for comparing groups)</li>
              <li><strong>Covariates:</strong> Numeric (for Cox regression)</li>
            </ul>
          </div>

          <div className="p-4 bg-green-50 border border-green-200 rounded-lg mb-4">
            <p className="text-sm text-green-800">
              ⏱️ <strong>Survival Analysis</strong> analyzes time-to-event data with Kaplan-Meier curves, 
              Log-Rank test for group comparisons, and Cox proportional hazards regression for multivariate analysis.
            </p>
          </div>
        </>
      )}

      {analysisType === 'nonparametric' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Test Type
            </label>
            <select
              value={options.testType || 'mann-whitney'}
              onChange={(e) => updateOption('testType', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="mann-whitney">Mann-Whitney U (2 groups)</option>
              <option value="kruskal-wallis">Kruskal-Wallis (3+ groups)</option>
              <option value="wilcoxon">Wilcoxon Signed-Rank (paired)</option>
            </select>
          </div>
          {(options.testType === 'mann-whitney' || options.testType === 'kruskal-wallis' || !options.testType) && (
            <>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Group Variable
                </label>
                <select
                  value={options.groupVar || ''}
                  onChange={(e) => updateOption('groupVar', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select column...</option>
                  {categoricalColumns.map((col) => (
                    <option key={col} value={col}>
                      {col}
                    </option>
                  ))}
                </select>
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Outcome Variable
                </label>
                <select
                  value={options.dependentVar || ''}
                  onChange={(e) => updateOption('dependentVar', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select column...</option>
                  {numericColumns.map((col) => (
                    <option key={col} value={col}>
                      {col}
                    </option>
                  ))}
                </select>
              </div>
            </>
          )}
          {options.testType === 'wilcoxon' && (
            <>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Variable 1 (Pre)
                </label>
                <select
                  value={options.variable1 || ''}
                  onChange={(e) => updateOption('variable1', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select column...</option>
                  {numericColumns.map((col) => (
                    <option key={col} value={col}>
                      {col}
                    </option>
                  ))}
                </select>
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Variable 2 (Post)
                </label>
                <select
                  value={options.variable2 || ''}
                  onChange={(e) => updateOption('variable2', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select column...</option>
                  {numericColumns.map((col) => (
                    <option key={col} value={col}>
                      {col}
                    </option>
                  ))}
                </select>
              </div>
            </>
          )}
        </>
      )}

      {analysisType === 'categorical' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Variable 1
            </label>
            <select
              value={options.variable1 || ''}
              onChange={(e) => updateOption('variable1', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {categoricalColumns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Variable 2
            </label>
            <select
              value={options.variable2 || ''}
              onChange={(e) => updateOption('variable2', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select column...</option>
              {categoricalColumns.map((col) => (
                <option key={col} value={col}>
                  {col}
                </option>
              ))}
            </select>
          </div>
        </>
      )}

      {analysisType === 'clustering' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Clustering Method
            </label>
            <select
              value={options.method || 'kmeans'}
              onChange={(e) => updateOption('method', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="kmeans">K-Means Clustering</option>
              <option value="hierarchical">Hierarchical Clustering</option>
            </select>
            <p className="text-xs text-gray-500 mt-1">
              {options.method === 'hierarchical' 
                ? 'Creates a tree-like structure (dendrogram) showing cluster relationships' 
                : 'Partitions data into k distinct clusters based on distance'}
            </p>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Clusters
            </label>
            <input
              type="number"
              min="2"
              max="10"
              value={options.nClusters || 3}
              onChange={(e) => updateOption('nClusters', parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="mb-4">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={options.showElbow !== false}
                onChange={(e) => updateOption('showElbow', e.target.checked)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm text-gray-700">Show elbow method & silhouette analysis</span>
            </label>
            <p className="text-xs text-gray-500 mt-1 ml-6">
              Helps determine the optimal number of clusters
            </p>
          </div>
        </>
      )}

      {analysisType === 'pca' && (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Number of Components
          </label>
          <input
            type="number"
            min="2"
            max="10"
            value={options.nComponents || 2}
            onChange={(e) => updateOption('nComponents', parseInt(e.target.value))}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
      )}

      {analysisType === 'time-series' && (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Date/Time Column
          </label>
          <select
            value={options.dateColumn || ''}
            onChange={(e) => updateOption('dateColumn', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select column...</option>
            {columns.map((col) => (
              <option key={col} value={col}>
                {col}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Common Options */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Significance Level (α)
        </label>
        <select
          value={options.alpha || 0.05}
          onChange={(e) => updateOption('alpha', parseFloat(e.target.value))}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value={0.01}>0.01 (99% confidence)</option>
          <option value={0.05}>0.05 (95% confidence)</option>
          <option value={0.10}>0.10 (90% confidence)</option>
        </select>
      </div>

      {/* Validation Warning for Survival Analysis */}
      {analysisType === 'survival' && options.eventColumn && !isEventColumnValid(options.eventColumn) && (
        <div className="mb-4 p-4 bg-red-50 border-2 border-red-300 rounded-lg">
          <p className="text-sm text-red-800 font-semibold mb-2">
            ⚠️ Cannot Run Analysis - Invalid Column Selection
          </p>
          <p className="text-xs text-red-700">
            The Event Column must contain numeric values (0 or 1). 
            Column '{options.eventColumn}' appears to be categorical. 
            Please select a numeric column with binary values.
          </p>
        </div>
      )}

      {/* Run Analysis Button */}
      <button
        onClick={onAnalyze}
        disabled={loading || (analysisType === 'survival' && options.eventColumn && !isEventColumnValid(options.eventColumn))}
        className="w-full px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-semibold"
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Running Analysis...
          </span>
        ) : (
          '🚀 Run Analysis'
        )}
      </button>

      {/* Info Box */}
      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-xs text-blue-800">
          <strong>Note:</strong> The analysis will automatically check assumptions, generate
          visualizations, and provide plain-language interpretations.
        </p>
      </div>
    </div>
  );
};

export default AnalysisSelector;
