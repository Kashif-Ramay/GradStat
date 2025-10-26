import React from 'react';
import { JobStatusData } from '../types';

interface JobStatusProps {
  jobId: string;
  status: JobStatusData | null;
}

const JobStatus: React.FC<JobStatusProps> = ({ jobId, status }) => {
  const getStatusColor = () => {
    switch (status?.status) {
      case 'done':
        return 'bg-green-100 border-green-300 text-green-800';
      case 'failed':
        return 'bg-red-100 border-red-300 text-red-800';
      case 'running':
        return 'bg-blue-100 border-blue-300 text-blue-800';
      default:
        return 'bg-gray-100 border-gray-300 text-gray-800';
    }
  };

  const getStatusIcon = () => {
    switch (status?.status) {
      case 'done':
        return '✅';
      case 'failed':
        return '❌';
      case 'running':
        return '⚙️';
      default:
        return '⏳';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Analysis Status</h2>

      <div className={`p-4 rounded-lg border ${getStatusColor()}`}>
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <span className="text-2xl">{getStatusIcon()}</span>
            <div>
              <p className="font-semibold capitalize">{status?.status || 'Pending'}</p>
              <p className="text-sm opacity-75">Job ID: {jobId}</p>
            </div>
          </div>
          {status?.progress !== undefined && (
            <span className="text-2xl font-bold">{status.progress}%</span>
          )}
        </div>

        {/* Progress Bar */}
        {status?.status === 'running' && status.progress !== undefined && (
          <div className="mt-3">
            <div className="w-full bg-white bg-opacity-50 rounded-full h-2">
              <div
                className="bg-current h-2 rounded-full transition-all duration-500"
                style={{ width: `${status.progress}%` }}
              />
            </div>
          </div>
        )}

        {/* Error Message */}
        {status?.status === 'failed' && status.error && (
          <div className="mt-3 p-3 bg-white bg-opacity-50 rounded">
            <p className="text-sm font-medium">Error:</p>
            <p className="text-sm mt-1">{status.error}</p>
          </div>
        )}
      </div>

      {/* Logs */}
      {status?.logs && status.logs.length > 0 && (
        <div className="mt-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">Analysis Log</h3>
          <div className="bg-gray-900 text-green-400 p-4 rounded-lg font-mono text-xs max-h-48 overflow-y-auto">
            {status.logs.map((log, idx) => (
              <div key={idx} className="mb-1">
                {log}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default JobStatus;
