import React from 'react';
import { analytics } from '../utils/analytics';

interface SocialShareProps {
  analysisType?: string;
  resultSummary?: string;
}

const SocialShare: React.FC<SocialShareProps> = ({ analysisType, resultSummary }) => {
  const appUrl = 'https://gradstat-frontend.onrender.com';
  
  const defaultText = `I just used GradStat for statistical analysis! 📊 ${analysisType ? `Performed ${analysisType} analysis` : 'Check it out'} - it's free and AI-powered! 🤖`;
  
  const shareText = resultSummary || defaultText;

  const handleShare = (platform: string, url: string) => {
    analytics.socialShare(platform, analysisType || 'general');
    window.open(url, '_blank', 'width=600,height=400');
  };

  const shareLinks = {
    twitter: `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(appUrl)}`,
    linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(appUrl)}`,
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(appUrl)}`,
    email: `mailto:?subject=${encodeURIComponent('Check out GradStat!')}&body=${encodeURIComponent(`${shareText}\n\n${appUrl}`)}`,
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(`${shareText}\n\n${appUrl}`);
    analytics.socialShare('clipboard', analysisType || 'general');
    alert('✅ Copied to clipboard!');
  };

  return (
    <div className="bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-blue-200 rounded-xl p-6">
      <div className="flex items-center gap-3 mb-4">
        <span className="text-3xl">🎉</span>
        <div>
          <h3 className="font-bold text-gray-900 text-lg">Love GradStat?</h3>
          <p className="text-sm text-gray-600">Share it with your research community!</p>
        </div>
      </div>

      <div className="flex flex-wrap gap-3">
        {/* Twitter */}
        <button
          onClick={() => handleShare('Twitter', shareLinks.twitter)}
          className="flex items-center gap-2 px-4 py-2 bg-[#1DA1F2] hover:bg-[#1a8cd8] text-white rounded-lg transition-colors shadow-md hover:shadow-lg"
        >
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
          </svg>
          <span className="font-semibold">Twitter</span>
        </button>

        {/* LinkedIn */}
        <button
          onClick={() => handleShare('LinkedIn', shareLinks.linkedin)}
          className="flex items-center gap-2 px-4 py-2 bg-[#0077B5] hover:bg-[#006399] text-white rounded-lg transition-colors shadow-md hover:shadow-lg"
        >
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
          </svg>
          <span className="font-semibold">LinkedIn</span>
        </button>

        {/* Facebook */}
        <button
          onClick={() => handleShare('Facebook', shareLinks.facebook)}
          className="flex items-center gap-2 px-4 py-2 bg-[#1877F2] hover:bg-[#166fe5] text-white rounded-lg transition-colors shadow-md hover:shadow-lg"
        >
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
          </svg>
          <span className="font-semibold">Facebook</span>
        </button>

        {/* Email */}
        <button
          onClick={() => handleShare('Email', shareLinks.email)}
          className="flex items-center gap-2 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors shadow-md hover:shadow-lg"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
          <span className="font-semibold">Email</span>
        </button>

        {/* Copy Link */}
        <button
          onClick={copyToClipboard}
          className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white rounded-lg transition-colors shadow-md hover:shadow-lg"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          <span className="font-semibold">Copy Link</span>
        </button>
      </div>

      <p className="text-xs text-gray-500 mt-4 text-center">
        Help us grow by sharing GradStat with researchers who need statistical analysis! 🚀
      </p>
    </div>
  );
};

export default SocialShare;
