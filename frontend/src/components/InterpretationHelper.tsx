import React, { useState } from 'react';

interface InterpretationHelperProps {
  testResults: any;
}

// Helper function to format p-values properly
const formatPValue = (p: number | undefined): string => {
  if (p === undefined || p === null) {
    return 'N/A';
  }
  if (p < 0.001) {
    return '< 0.001';
  } else if (p < 0.01) {
    return p.toFixed(3);
  } else {
    return p.toFixed(4);
  }
};

const InterpretationHelper: React.FC<InterpretationHelperProps> = ({
  testResults
}) => {
  const [copied, setCopied] = useState(false);

  // Generate plain-language interpretation
  const generateInterpretation = (): string => {
    if (!testResults) return '';

    const { p_value, significant, alpha = 0.05 } = testResults;

    let interpretation = '';

    // Statistical significance (only if p_value exists)
    if (p_value !== undefined && p_value !== null) {
      if (significant) {
        interpretation += `✓ **Statistically Significant Result**\n\n`;
        interpretation += `The analysis shows a statistically significant effect (p = ${formatPValue(p_value)} < ${alpha}). `;
        interpretation += `This means the observed difference or relationship is unlikely to have occurred by chance alone.\n\n`;
      } else {
        interpretation += `✗ **Not Statistically Significant**\n\n`;
        interpretation += `The analysis did not find a statistically significant effect (p = ${formatPValue(p_value)} ≥ ${alpha}). `;
        interpretation += `This means we cannot confidently conclude there is a real effect beyond chance variation.\n\n`;
      }
    }

    // Effect size interpretation
    if (testResults.cohens_d !== undefined) {
      const d = Math.abs(testResults.cohens_d);
      let magnitude = '';
      if (d < 0.2) magnitude = 'negligible';
      else if (d < 0.5) magnitude = 'small';
      else if (d < 0.8) magnitude = 'medium';
      else magnitude = 'large';

      interpretation += `**Effect Size:** Cohen's d = ${testResults.cohens_d.toFixed(3)} (${magnitude})\n`;
      interpretation += `This indicates a ${magnitude} practical difference between groups. `;
      
      if (magnitude === 'large') {
        interpretation += `The effect is substantial and likely meaningful in practice.\n\n`;
      } else if (magnitude === 'medium') {
        interpretation += `The effect is moderate and may be practically important.\n\n`;
      } else if (magnitude === 'small') {
        interpretation += `The effect is small but may still be important depending on context.\n\n`;
      } else {
        interpretation += `The effect is very small and may not be practically meaningful.\n\n`;
      }
    }

    if (testResults.partial_eta_squared !== undefined) {
      const eta = testResults.partial_eta_squared;
      let magnitude = '';
      if (eta < 0.01) magnitude = 'negligible';
      else if (eta < 0.06) magnitude = 'small';
      else if (eta < 0.14) magnitude = 'medium';
      else magnitude = 'large';

      interpretation += `**Effect Size:** ηp² = ${eta.toFixed(3)} (${magnitude})\n`;
      interpretation += `This means the factor explains ${(eta * 100).toFixed(1)}% of the variance in the outcome. `;
      
      if (magnitude === 'large') {
        interpretation += `This is a substantial effect.\n\n`;
      } else if (magnitude === 'medium') {
        interpretation += `This is a moderate effect.\n\n`;
      } else {
        interpretation += `This is a small effect.\n\n`;
      }
    }

    // Correlation interpretation
    if (testResults.correlation !== undefined) {
      const r = Math.abs(testResults.correlation);
      let strength = '';
      if (r < 0.1) strength = 'negligible';
      else if (r < 0.3) strength = 'weak';
      else if (r < 0.5) strength = 'moderate';
      else if (r < 0.7) strength = 'strong';
      else strength = 'very strong';

      const direction = testResults.correlation > 0 ? 'positive' : 'negative';
      
      interpretation += `**Correlation:** r = ${testResults.correlation.toFixed(3)} (${strength} ${direction})\n`;
      interpretation += `This indicates a ${strength} ${direction} relationship. `;
      
      if (direction === 'positive') {
        interpretation += `As one variable increases, the other tends to increase.\n\n`;
      } else {
        interpretation += `As one variable increases, the other tends to decrease.\n\n`;
      }
      
      interpretation += `⚠️ Remember: Correlation does not imply causation!\n\n`;
    }

    // Recommendations
    interpretation += `**What This Means:**\n`;
    if (significant) {
      interpretation += `• The results provide evidence for a real effect\n`;
      interpretation += `• Consider the practical significance (effect size)\n`;
      interpretation += `• Report both statistical and practical significance\n`;
      interpretation += `• Consider replication to confirm findings\n`;
    } else {
      interpretation += `• Lack of significance doesn't prove no effect exists\n`;
      interpretation += `• Consider if sample size was adequate (power analysis)\n`;
      interpretation += `• Check if effect size suggests practical importance\n`;
      interpretation += `• Avoid concluding "no difference" from non-significant results\n`;
    }

    return interpretation;
  };

  // Generate APA format
  const generateAPA = (): string => {
    if (!testResults) return '';

    let apa = '';

    // t-test
    if (testResults.test === 'Independent t-test' || testResults.test === 'Paired t-test') {
      const t = testResults.t_statistic?.toFixed(2);
      const df = testResults.df;
      const p = testResults.p_value;
      const d = testResults.cohens_d?.toFixed(2);
      
      apa = `${testResults.test === 'Paired t-test' ? 'A paired-samples' : 'An independent-samples'} t-test was conducted. `;
      apa += `Results showed ${testResults.significant ? 'a significant' : 'no significant'} difference, `;
      apa += `t(${df}) = ${t}, p ${p < 0.001 ? '< .001' : `= ${p.toFixed(3)}`}`;
      if (d) apa += `, d = ${d}`;
      apa += `.`;
    }

    // ANOVA
    if (testResults.test === 'One-way ANOVA') {
      const f = testResults.F_statistic?.toFixed(2);
      const df1 = testResults.df_between;
      const df2 = testResults.df_within;
      const p = testResults.p_value;
      const eta = testResults.eta_squared?.toFixed(3);
      
      apa = `A one-way ANOVA was conducted. `;
      apa += `Results showed ${testResults.significant ? 'a significant' : 'no significant'} effect, `;
      apa += `F(${df1}, ${df2}) = ${f}, p ${p < 0.001 ? '< .001' : `= ${p.toFixed(3)}`}`;
      if (eta) apa += `, η² = ${eta}`;
      apa += `.`;
    }

    // Correlation
    if (testResults.correlation !== undefined) {
      const r = testResults.correlation?.toFixed(3);
      const p = testResults.p_value;
      const n = testResults.n;
      
      apa = `A ${testResults.method || 'Pearson'} correlation was computed. `;
      apa += `Results showed ${testResults.significant ? 'a significant' : 'no significant'} correlation, `;
      apa += `r(${n - 2}) = ${r}, p ${p < 0.001 ? '< .001' : `= ${p.toFixed(3)}`}`;
      apa += `.`;
    }

    return apa;
  };

  const interpretation = generateInterpretation();
  const apaFormat = generateAPA();

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  if (!testResults) return null;

  return (
    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg border border-purple-200 p-6 mb-6">
      <div className="flex items-center mb-4">
        <span className="text-3xl mr-3">📝</span>
        <h3 className="text-lg font-semibold text-gray-900">
          Plain-Language Interpretation
        </h3>
      </div>

      {/* Interpretation Text */}
      <div className="bg-white rounded-lg p-4 mb-4 text-sm text-gray-700 whitespace-pre-line">
        {interpretation.split('\n').map((line, idx) => {
          if (line.startsWith('**') && line.endsWith('**')) {
            return (
              <p key={idx} className="font-semibold text-gray-900 mt-3 mb-1">
                {line.replace(/\*\*/g, '')}
              </p>
            );
          }
          if (line.startsWith('✓')) {
            return (
              <p key={idx} className="text-green-700 font-medium mb-2">
                {line}
              </p>
            );
          }
          if (line.startsWith('✗')) {
            return (
              <p key={idx} className="text-orange-700 font-medium mb-2">
                {line}
              </p>
            );
          }
          if (line.startsWith('⚠️')) {
            return (
              <p key={idx} className="text-amber-700 font-medium mb-2">
                {line}
              </p>
            );
          }
          if (line.startsWith('•')) {
            return (
              <p key={idx} className="ml-4 mb-1">
                {line}
              </p>
            );
          }
          return line ? <p key={idx} className="mb-2">{line}</p> : <br key={idx} />;
        })}
      </div>

      {/* APA Format */}
      {apaFormat && (
        <div className="bg-white rounded-lg p-4 mb-4">
          <p className="text-xs font-semibold text-gray-700 mb-2">📄 APA Format:</p>
          <p className="text-sm text-gray-700 italic">{apaFormat}</p>
        </div>
      )}

      {/* Copy Buttons */}
      <div className="flex gap-2">
        <button
          onClick={() => copyToClipboard(interpretation)}
          className="flex-1 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium"
        >
          {copied ? '✓ Copied!' : '📋 Copy Plain Text'}
        </button>
        {apaFormat && (
          <button
            onClick={() => copyToClipboard(apaFormat)}
            className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-sm font-medium"
          >
            {copied ? '✓ Copied!' : '📄 Copy APA Format'}
          </button>
        )}
      </div>

      {/* Educational Note */}
      <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-xs text-blue-800">
          <span className="font-semibold">💡 Tip:</span> Always consider both statistical significance (p-value) 
          and practical significance (effect size) when interpreting results. A statistically significant result 
          may not always be practically meaningful, and vice versa.
        </p>
      </div>
    </div>
  );
};

export default InterpretationHelper;
