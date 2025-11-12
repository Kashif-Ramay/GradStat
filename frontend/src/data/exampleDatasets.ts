export interface ExampleDataset {
  name: string;
  description: string;
  icon: string;
  category: string;
  recommendedAnalysis: string;
  csvData: string;
  sampleSize: number;
  variables: number;
}

export const exampleDatasets: ExampleDataset[] = [
  {
    name: "Student Performance",
    description: "Compare test scores between two teaching methods (independent samples)",
    icon: "📚",
    category: "Education",
    recommendedAnalysis: "group_comparison",
    sampleSize: 60,
    variables: 3,
    csvData: `student_id,teaching_method,test_score
1,Traditional,72
2,Traditional,68
3,Traditional,75
4,Traditional,71
5,Traditional,69
6,Traditional,73
7,Traditional,70
8,Traditional,74
9,Traditional,67
10,Traditional,72
11,Traditional,76
12,Traditional,71
13,Traditional,69
14,Traditional,73
15,Traditional,70
16,Traditional,74
17,Traditional,68
18,Traditional,72
19,Traditional,71
20,Traditional,73
21,Traditional,69
22,Traditional,75
23,Traditional,70
24,Traditional,72
25,Traditional,71
26,Traditional,74
27,Traditional,68
28,Traditional,73
29,Traditional,70
30,Traditional,72
31,Interactive,78
32,Interactive,82
33,Interactive,80
34,Interactive,79
35,Interactive,83
36,Interactive,81
37,Interactive,77
38,Interactive,80
39,Interactive,82
40,Interactive,79
41,Interactive,81
42,Interactive,78
43,Interactive,80
44,Interactive,83
45,Interactive,79
46,Interactive,81
47,Interactive,82
48,Interactive,80
49,Interactive,78
50,Interactive,81
51,Interactive,79
52,Interactive,82
53,Interactive,80
54,Interactive,83
55,Interactive,81
56,Interactive,79
57,Interactive,80
58,Interactive,82
59,Interactive,78
60,Interactive,81`
  },
  {
    name: "Blood Pressure Study",
    description: "Before and after treatment measurements (paired samples)",
    icon: "💊",
    category: "Health",
    recommendedAnalysis: "group_comparison",
    sampleSize: 40,
    variables: 3,
    csvData: `patient_id,before_treatment,after_treatment
1,145,132
2,152,138
3,148,135
4,155,140
5,150,136
6,147,133
7,153,139
8,149,134
9,151,137
10,146,131
11,154,141
12,148,135
13,150,136
14,152,138
15,147,133
16,149,134
17,151,137
18,153,139
19,146,132
20,148,134
21,150,136
22,152,138
23,147,133
24,149,135
25,151,137
26,154,140
27,148,134
28,150,136
29,152,138
30,147,133
31,149,135
32,151,137
33,153,139
34,146,132
35,148,134
36,150,136
37,152,138
38,147,133
39,149,135
40,151,137`
  },
  {
    name: "Exercise & Weight Loss",
    description: "Correlation between exercise hours and weight loss",
    icon: "🏃",
    category: "Health",
    recommendedAnalysis: "regression",
    sampleSize: 50,
    variables: 3,
    csvData: `participant_id,exercise_hours_per_week,weight_loss_kg
1,2,1.5
2,3,2.1
3,1,0.8
4,4,3.2
5,2,1.7
6,5,4.1
7,3,2.5
8,1,0.9
9,4,3.5
10,2,1.6
11,6,4.8
12,3,2.3
13,1,1.0
14,5,4.0
15,2,1.8
16,4,3.3
17,3,2.4
18,1,0.7
19,5,4.2
20,2,1.9
21,6,4.9
22,3,2.6
23,4,3.4
24,1,0.8
25,5,4.1
26,2,1.7
27,3,2.5
28,4,3.6
29,1,0.9
30,6,5.0
31,2,1.6
32,5,4.3
33,3,2.4
34,4,3.5
35,1,1.0
36,6,4.7
37,2,1.8
38,3,2.6
39,5,4.2
40,4,3.4
41,1,0.8
42,6,4.9
43,2,1.7
44,3,2.5
45,5,4.1
46,4,3.6
47,1,0.9
48,6,5.1
49,2,1.9
50,3,2.7`
  },
  {
    name: "Customer Satisfaction",
    description: "Survey responses across different service categories",
    icon: "😊",
    category: "Business",
    recommendedAnalysis: "descriptive",
    sampleSize: 100,
    variables: 4,
    csvData: `customer_id,service_quality,response_time,overall_satisfaction
1,4,5,4
2,5,4,5
3,3,3,3
4,4,4,4
5,5,5,5
6,3,4,3
7,4,3,4
8,5,5,5
9,4,4,4
10,3,3,3
11,5,4,5
12,4,5,4
13,3,3,3
14,5,5,5
15,4,4,4
16,3,4,3
17,5,5,5
18,4,3,4
19,3,3,3
20,5,4,5
21,4,5,4
22,3,3,3
23,5,5,5
24,4,4,4
25,3,4,3
26,5,5,5
27,4,3,4
28,3,3,3
29,5,4,5
30,4,5,4
31,3,3,3
32,5,5,5
33,4,4,4
34,3,4,3
35,5,5,5
36,4,3,4
37,3,3,3
38,5,4,5
39,4,5,4
40,3,3,3
41,5,5,5
42,4,4,4
43,3,4,3
44,5,5,5
45,4,3,4
46,3,3,3
47,5,4,5
48,4,5,4
49,3,3,3
50,5,5,5
51,4,4,4
52,3,4,3
53,5,5,5
54,4,3,4
55,3,3,3
56,5,4,5
57,4,5,4
58,3,3,3
59,5,5,5
60,4,4,4
61,3,4,3
62,5,5,5
63,4,3,4
64,3,3,3
65,5,4,5
66,4,5,4
67,3,3,3
68,5,5,5
69,4,4,4
70,3,4,3
71,5,5,5
72,4,3,4
73,3,3,3
74,5,4,5
75,4,5,4
76,3,3,3
77,5,5,5
78,4,4,4
79,3,4,3
80,5,5,5
81,4,3,4
82,3,3,3
83,5,4,5
84,4,5,4
85,3,3,3
86,5,5,5
87,4,4,4
88,3,4,3
89,5,5,5
90,4,3,4
91,3,3,3
92,5,4,5
93,4,5,4
94,3,3,3
95,5,5,5
96,4,4,4
97,3,4,3
98,5,5,5
99,4,3,4
100,3,3,3`
  },
  {
    name: "Product Sales",
    description: "Monthly sales data for time series analysis",
    icon: "📈",
    category: "Business",
    recommendedAnalysis: "timeseries",
    sampleSize: 24,
    variables: 2,
    csvData: `month,sales
2023-01,15000
2023-02,16500
2023-03,18000
2023-04,17500
2023-05,19000
2023-06,20500
2023-07,22000
2023-08,21500
2023-09,23000
2023-10,24500
2023-11,26000
2023-12,28000
2024-01,16000
2024-02,17500
2024-03,19000
2024-04,18500
2024-05,20000
2024-06,21500
2024-07,23000
2024-08,22500
2024-09,24000
2024-10,25500
2024-11,27000
2024-12,29000`
  }
];

// Helper function to convert CSV to File object
export const createFileFromDataset = (dataset: ExampleDataset): File => {
  const blob = new Blob([dataset.csvData], { type: 'text/csv' });
  return new File([blob], `${dataset.name.toLowerCase().replace(/\s+/g, '_')}.csv`, {
    type: 'text/csv',
  });
};
