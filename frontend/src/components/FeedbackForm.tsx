import React, { useState } from 'react';
import { analytics } from '../utils/analytics';

interface FeedbackFormProps {
  analysisType?: string;
  onClose?: () => void;
}

const FeedbackForm: React.FC<FeedbackFormProps> = ({ analysisType, onClose }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [rating, setRating] = useState<number>(0);
  const [comment, setComment] = useState('');
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Track in analytics
      analytics.feedbackSubmitted(rating, comment.length > 0);

      // Here you could send to a backend or Google Forms
      // For now, we'll just log it
      console.log('Feedback submitted:', {
        rating,
        comment,
        email,
        analysisType,
        timestamp: new Date().toISOString(),
      });

      setSubmitted(true);
      setTimeout(() => {
        setIsOpen(false);
        setSubmitted(false);
        setRating(0);
        setComment('');
        setEmail('');
        if (onClose) onClose();
      }, 2000);
    } catch (error) {
      console.error('Error submitting feedback:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-full shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-200 flex items-center gap-2 z-50"
      >
        <span className="text-xl">💬</span>
        <span className="font-semibold">Feedback</span>
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 bg-white rounded-2xl shadow-2xl p-6 w-96 z-50 border-2 border-gray-200">
      {submitted ? (
        <div className="text-center py-8">
          <div className="text-6xl mb-4">🎉</div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">Thank You!</h3>
          <p className="text-gray-600">Your feedback helps us improve GradStat.</p>
        </div>
      ) : (
        <>
          {/* Header */}
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-bold text-gray-900">How was your experience?</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {/* Star Rating */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Rate your experience
              </label>
              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRating(star)}
                    className="text-3xl transition-transform hover:scale-110"
                  >
                    {star <= rating ? '⭐' : '☆'}
                  </button>
                ))}
              </div>
            </div>

            {/* Comment */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tell us more (optional)
              </label>
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="What did you like? What could be better?"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                rows={3}
              />
            </div>

            {/* Email */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email (optional - for updates)
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={rating === 0 || loading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all"
            >
              {loading ? '⏳ Sending...' : '📤 Send Feedback'}
            </button>
          </form>
        </>
      )}
    </div>
  );
};

export default FeedbackForm;
