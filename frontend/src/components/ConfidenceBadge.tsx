import React from 'react';

interface ConfidenceBadgeProps {
  confidence: 'high' | 'medium' | 'low';
  explanation?: string;
  size?: 'sm' | 'md' | 'lg';
}

const ConfidenceBadge: React.FC<ConfidenceBadgeProps> = ({ 
  confidence, 
  explanation,
  size = 'md' 
}) => {
  const getStyles = () => {
    const baseStyles = 'inline-flex items-center gap-1 rounded-full font-semibold';
    
    const sizeStyles = {
      sm: 'px-2 py-0.5 text-xs',
      md: 'px-3 py-1 text-sm',
      lg: 'px-4 py-1.5 text-base'
    };

    const confidenceStyles = {
      high: 'bg-green-100 text-green-800 border border-green-300',
      medium: 'bg-yellow-100 text-yellow-800 border border-yellow-300',
      low: 'bg-red-100 text-red-800 border border-red-300'
    };

    return `${baseStyles} ${sizeStyles[size]} ${confidenceStyles[confidence]}`;
  };

  const getIcon = () => {
    switch (confidence) {
      case 'high':
        return '🟢';
      case 'medium':
        return '🟡';
      case 'low':
        return '🔴';
    }
  };

  const getLabel = () => {
    switch (confidence) {
      case 'high':
        return 'High Confidence';
      case 'medium':
        return 'Medium Confidence';
      case 'low':
        return 'Low Confidence';
    }
  };

  const badge = (
    <span className={getStyles()}>
      <span>{getIcon()}</span>
      <span>{getLabel()}</span>
    </span>
  );

  if (explanation) {
    return (
      <div className="group relative inline-block">
        {badge}
        <div className="invisible group-hover:visible absolute z-10 w-64 p-2 mt-2 text-sm bg-gray-900 text-white rounded-lg shadow-lg -left-24">
          {explanation}
          <div className="absolute -top-1 left-28 w-2 h-2 bg-gray-900 transform rotate-45"></div>
        </div>
      </div>
    );
  }

  return badge;
};

export default ConfidenceBadge;
