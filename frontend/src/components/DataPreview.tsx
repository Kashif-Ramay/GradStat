import React from 'react';
import { PreviewData } from '../types';

interface DataPreviewProps {
  preview: PreviewData;
}

const DataPreview: React.FC<DataPreviewProps> = ({ preview }) => {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Data Preview</h2>
        <span className="text-sm text-gray-600">
          {preview.rowCount} rows × {preview.columns.length} columns
        </span>
      </div>

      {/* Data Quality Issues */}
      {preview.issues && preview.issues.length > 0 && (
        <div className="mb-4 space-y-2">
          {preview.issues.map((issue, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-lg border ${
                issue.severity === 'error'
                  ? 'bg-red-50 border-red-200'
                  : issue.severity === 'warning'
                  ? 'bg-yellow-50 border-yellow-200'
                  : 'bg-blue-50 border-blue-200'
              }`}
            >
              <div className="flex items-start gap-2">
                <span className="text-sm font-medium">
                  {issue.severity === 'error' ? '❌' : issue.severity === 'warning' ? '⚠️' : 'ℹ️'}
                </span>
                <div className="flex-1">
                  {issue.column && (
                    <span className="text-sm font-medium">{issue.column}: </span>
                  )}
                  <span className="text-sm">{issue.message}</span>
                  {issue.count && (
                    <span className="text-sm text-gray-600"> ({issue.count} occurrences)</span>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Column Types */}
      <div className="mb-4 flex flex-wrap gap-2">
        {preview.columns.map((col) => (
          <div
            key={col}
            className="inline-flex items-center gap-2 px-3 py-1 bg-gray-100 rounded-full text-sm"
          >
            <span className="font-medium">{col}</span>
            <span className="text-gray-600">
              ({preview.types[col] || 'unknown'})
            </span>
          </div>
        ))}
      </div>

      {/* Data Table */}
      <div className="overflow-x-auto border rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                #
              </th>
              {preview.columns.map((col) => (
                <th
                  key={col}
                  className="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {preview.rows.slice(0, 10).map((row, rowIdx) => (
              <tr key={rowIdx} className="hover:bg-gray-50">
                <td className="px-3 py-2 text-sm text-gray-500">{rowIdx + 1}</td>
                {row.map((cell, cellIdx) => (
                  <td key={cellIdx} className="px-3 py-2 text-sm text-gray-900">
                    {cell === null || cell === undefined || cell === '' ? (
                      <span className="text-gray-400 italic">null</span>
                    ) : (
                      String(cell)
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {preview.rowCount > 10 && (
        <p className="mt-2 text-sm text-gray-500 text-center">
          Showing first 10 of {preview.rowCount} rows
        </p>
      )}

      {/* Recommendations */}
      {preview.recommendations && preview.recommendations.length > 0 && (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <h3 className="text-sm font-semibold text-blue-900 mb-2">Recommendations</h3>
          <ul className="space-y-1">
            {preview.recommendations.map((rec, idx) => (
              <li key={idx} className="text-sm text-blue-800 flex items-start gap-2">
                <span>•</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DataPreview;
