import ReactGA from 'react-ga4';

// Initialize Google Analytics
export const initGA = () => {
  const measurementId = process.env.REACT_APP_GA_MEASUREMENT_ID;
  
  if (measurementId) {
    ReactGA.initialize(measurementId);
    console.log('Google Analytics initialized');
  } else {
    console.log('Google Analytics not configured (no measurement ID)');
  }
};

// Track page views
export const trackPageView = (path: string) => {
  ReactGA.send({ hitType: 'pageview', page: path });
};

// Track events
export const trackEvent = (category: string, action: string, label?: string, value?: number) => {
  ReactGA.event({
    category,
    action,
    label,
    value,
  });
};

// Specific event trackers
export const analytics = {
  // File upload
  fileUploaded: (fileType: string, fileSize: number) => {
    trackEvent('File', 'Upload', fileType, fileSize);
  },

  // Analysis
  analysisStarted: (analysisType: string) => {
    trackEvent('Analysis', 'Started', analysisType);
  },

  analysisCompleted: (analysisType: string, duration: number) => {
    trackEvent('Analysis', 'Completed', analysisType, duration);
  },

  analysisFailed: (analysisType: string, error: string) => {
    trackEvent('Analysis', 'Failed', `${analysisType}: ${error}`);
  },

  // Test Advisor
  testAdvisorOpened: () => {
    trackEvent('Test Advisor', 'Opened');
  },

  testAdvisorWizardCompleted: (recommendedTest: string) => {
    trackEvent('Test Advisor', 'Wizard Completed', recommendedTest);
  },

  testAdvisorAIUsed: (feature: string) => {
    trackEvent('Test Advisor', 'AI Used', feature);
  },

  autoDetectUsed: (questionType: string) => {
    trackEvent('Test Advisor', 'Auto Detect', questionType);
  },

  // Downloads
  reportDownloaded: (analysisType: string) => {
    trackEvent('Download', 'Report', analysisType);
  },

  // AI Features
  aiInterpretationViewed: (analysisType: string) => {
    trackEvent('AI', 'Interpretation Viewed', analysisType);
  },

  aiQuestionAsked: (questionLength: number) => {
    trackEvent('AI', 'Question Asked', undefined, questionLength);
  },

  aiWhatIfUsed: (scenario: string) => {
    trackEvent('AI', 'What-If Analysis', scenario);
  },

  // Navigation
  homePageViewed: () => {
    trackEvent('Navigation', 'Home Page Viewed');
  },

  getStartedClicked: () => {
    trackEvent('Navigation', 'Get Started Clicked');
  },

  // Feedback
  feedbackSubmitted: (rating: number, hasComment: boolean) => {
    trackEvent('Feedback', 'Submitted', hasComment ? 'With Comment' : 'Rating Only', rating);
  },

  // Social Sharing
  socialShare: (platform: string, content: string) => {
    trackEvent('Social', 'Share', `${platform}: ${content}`);
  },

  // Example Datasets
  exampleDatasetUsed: (datasetName: string) => {
    trackEvent('Example', 'Dataset Used', datasetName);
  },

  // Errors
  errorOccurred: (errorType: string, errorMessage: string) => {
    trackEvent('Error', errorType, errorMessage);
  },
};
