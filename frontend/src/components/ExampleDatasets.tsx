import React, { useState } from 'react';
import { exampleDatasets, createFileFromDataset, ExampleDataset } from '../data/exampleDatasets';
import { analytics } from '../utils/analytics';

interface ExampleDatasetsProps {
  onSelectDataset: (file: File, analysisType: string) => void;
}

const ExampleDatasets: React.FC<ExampleDatasetsProps> = ({ onSelectDataset }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const categories = ['All', ...Array.from(new Set(exampleDatasets.map(d => d.category)))];

  const filteredDatasets = selectedCategory === 'All'
    ? exampleDatasets
    : exampleDatasets.filter(d => d.category === selectedCategory);

  const handleSelectDataset = (dataset: ExampleDataset) => {
    const file = createFileFromDataset(dataset);
    analytics.exampleDatasetUsed(dataset.name);
    onSelectDataset(file, dataset.recommendedAnalysis);
    setIsOpen(false);
  };

  return (
    <>
      {/* Trigger Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 text-white rounded-lg hover:from-green-700 hover:to-emerald-700 transition-all shadow-md hover:shadow-lg"
      >
        <span className="text-xl">✨</span>
        <span className="font-semibold">Try Example Data</span>
      </button>

      {/* Modal */}
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
            {/* Header */}
            <div className="bg-gradient-to-r from-green-600 to-emerald-600 text-white p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-2xl font-bold mb-2">Example Datasets</h2>
                  <p className="text-green-100">Try GradStat with ready-to-use sample data</p>
                </div>
                <button
                  onClick={() => setIsOpen(false)}
                  className="text-white hover:text-green-100 transition-colors"
                >
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Category Filter */}
            <div className="p-6 border-b border-gray-200">
              <div className="flex flex-wrap gap-2">
                {categories.map((category) => (
                  <button
                    key={category}
                    onClick={() => setSelectedCategory(category)}
                    className={`px-4 py-2 rounded-lg font-medium transition-all ${
                      selectedCategory === category
                        ? 'bg-gradient-to-r from-green-600 to-emerald-600 text-white shadow-md'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {category}
                  </button>
                ))}
              </div>
            </div>

            {/* Datasets Grid */}
            <div className="p-6 overflow-y-auto max-h-[60vh]">
              <div className="grid md:grid-cols-2 gap-4">
                {filteredDatasets.map((dataset) => (
                  <div
                    key={dataset.name}
                    className="border-2 border-gray-200 rounded-xl p-4 hover:border-green-400 hover:shadow-lg transition-all cursor-pointer group"
                    onClick={() => handleSelectDataset(dataset)}
                  >
                    <div className="flex items-start gap-3">
                      <div className="text-4xl group-hover:scale-110 transition-transform">
                        {dataset.icon}
                      </div>
                      <div className="flex-1">
                        <h3 className="font-bold text-gray-900 mb-1 group-hover:text-green-600 transition-colors">
                          {dataset.name}
                        </h3>
                        <p className="text-sm text-gray-600 mb-3">{dataset.description}</p>
                        
                        <div className="flex flex-wrap gap-2 text-xs">
                          <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full">
                            {dataset.category}
                          </span>
                          <span className="px-2 py-1 bg-purple-100 text-purple-700 rounded-full">
                            {dataset.sampleSize} rows
                          </span>
                          <span className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded-full">
                            {dataset.variables} variables
                          </span>
                        </div>

                        <div className="mt-3 flex items-center gap-2 text-sm text-green-600 font-medium group-hover:gap-3 transition-all">
                          <span>Try this dataset</span>
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                          </svg>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Footer */}
            <div className="p-6 bg-gray-50 border-t border-gray-200">
              <p className="text-sm text-gray-600 text-center">
                💡 <strong>Tip:</strong> These datasets are perfect for learning and testing. Your own data will work the same way!
              </p>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ExampleDatasets;
