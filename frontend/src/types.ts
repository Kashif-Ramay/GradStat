// Type definitions for GradStat frontend

export interface PreviewData {
  columns: string[];
  rows: any[][];
  types: { [key: string]: string };
  rowCount: number;
  issues?: DataIssue[];
  recommendations?: string[];
}

export interface DataIssue {
  severity: 'error' | 'warning' | 'info';
  column?: string;
  message: string;
  count?: number;
}

export interface AnalysisOptions {
  independentVar?: string;
  dependentVar?: string;
  groupVar?: string;
  confounders?: string[];
  alpha?: number;
  testType?: string;
  nClusters?: number;
  nComponents?: number;
  dateColumn?: string;
  targetColumn?: string;
  [key: string]: any;
}

export interface JobStatusData {
  status: 'pending' | 'running' | 'done' | 'failed';
  progress: number;
  result_url?: string;
  result_meta?: ResultMeta;
  logs?: string[];
  error?: string;
}

export interface ResultMeta {
  analysis_type: string;
  summary: string;
  test_results?: any;
  plots?: PlotData[];
  interpretation?: string;
  assumptions?: AssumptionCheck[];
  recommendations?: string[];
  code_snippet?: string;
  conclusion?: string;
}

export interface PlotData {
  title: string;
  type: string;
  data: any;
  base64?: string;
}

export interface AssumptionCheck {
  name: string;
  passed: boolean;
  pValue?: number;
  statistic?: number;
  message: string;
}

export type AnalysisType =
  | 'descriptive'
  | 'group-comparison'
  | 'regression'
  | 'multiple-regression'
  | 'nonparametric'
  | 'categorical'
  | 'classification'
  | 'clustering'
  | 'pca'
  | 'time-series';
