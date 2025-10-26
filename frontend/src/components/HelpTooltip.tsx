import React, { useState } from 'react';
import { getHelpContent } from '../utils/helpContent';

interface HelpTooltipProps {
  contentId: string;
  position?: 'top' | 'bottom' | 'left' | 'right';
  className?: string;
}

const HelpTooltip: React.FC<HelpTooltipProps> = ({ 
  contentId, 
  position = 'top',
  className = '' 
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const content = getHelpContent(contentId);

  if (!content) {
    return null;
  }

  const positionClasses = {
    top: 'bottom-full left-1/2 transform -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 transform -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 transform -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 transform -translate-y-1/2 ml-2'
  };

  return (
    <div className={`relative inline-block ${className}`}>
      {/* Help Icon */}
      <button
        type="button"
        onMouseEnter={() => setIsOpen(true)}
        onMouseLeave={() => setIsOpen(false)}
        onClick={() => setIsOpen(!isOpen)}
        className="inline-flex items-center justify-center w-5 h-5 text-gray-400 hover:text-blue-600 transition-colors cursor-help"
        aria-label="Help"
      >
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </button>

      {/* Tooltip */}
      {isOpen && (
        <div
          className={`absolute z-50 ${positionClasses[position]} w-80`}
          onMouseEnter={() => setIsOpen(true)}
          onMouseLeave={() => setIsOpen(false)}
        >
          <div className="bg-white rounded-lg shadow-xl border border-gray-200 p-4">
            {/* Title */}
            <div className="flex items-start mb-2">
              <span className="text-2xl mr-2">💡</span>
              <h3 className="text-sm font-semibold text-gray-900 flex-1">
                {content.title}
              </h3>
            </div>

            {/* Short Description */}
            <p className="text-sm text-gray-700 mb-3">
              {content.shortDescription}
            </p>

            {/* Full Description */}
            <div className="text-xs text-gray-600 mb-3 whitespace-pre-line">
              {content.fullDescription}
            </div>

            {/* Examples */}
            {content.examples && content.examples.length > 0 && (
              <div className="mb-3">
                <p className="text-xs font-semibold text-gray-700 mb-1">Examples:</p>
                <ul className="text-xs text-gray-600 space-y-1">
                  {content.examples.map((example, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-blue-500 mr-1">•</span>
                      <span>{example}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Tips */}
            {content.tips && content.tips.length > 0 && (
              <div className="mb-3">
                <p className="text-xs font-semibold text-gray-700 mb-1">💡 Tips:</p>
                <ul className="text-xs text-gray-600 space-y-1">
                  {content.tips.map((tip, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-green-500 mr-1">✓</span>
                      <span>{tip}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Learn More Link */}
            {content.learnMoreUrl && (
              <a
                href={content.learnMoreUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-blue-600 hover:text-blue-800 font-medium inline-flex items-center"
              >
                Learn More
                <svg
                  className="w-3 h-3 ml-1"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                  />
                </svg>
              </a>
            )}
          </div>

          {/* Arrow */}
          <div
            className={`absolute w-3 h-3 bg-white border transform rotate-45 ${
              position === 'top'
                ? 'bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2 border-t-0 border-l-0 border-gray-200'
                : position === 'bottom'
                ? 'top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 border-b-0 border-r-0 border-gray-200'
                : position === 'left'
                ? 'right-0 top-1/2 translate-x-1/2 -translate-y-1/2 border-t-0 border-r-0 border-gray-200'
                : 'left-0 top-1/2 -translate-x-1/2 -translate-y-1/2 border-b-0 border-l-0 border-gray-200'
            }`}
          />
        </div>
      )}
    </div>
  );
};

export default HelpTooltip;
