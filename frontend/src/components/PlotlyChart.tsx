import React from 'react';
import Plot from 'react-plotly.js';

interface PlotlyChartProps {
  data: any;
  title?: string;
  className?: string;
}

const PlotlyChart: React.FC<PlotlyChartProps> = ({ data, title, className = '' }) => {
  // Handle both old base64 format and new Plotly format
  if (data.type === 'plotly' && data.data) {
    const plotlyData = data.data;
    
    return (
      <div className={`bg-white rounded-lg shadow-sm border border-gray-200 p-4 ${className}`}>
        {title && (
          <h3 className="text-lg font-semibold text-gray-900 mb-3">{title}</h3>
        )}
        <Plot
          data={plotlyData.data}
          layout={{
            ...plotlyData.layout,
            autosize: true,
            margin: { l: 60, r: 40, t: 60, b: 60 }
          }}
          config={{
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ['lasso2d', 'select2d'],
            toImageButtonOptions: {
              format: 'png',
              filename: title || 'plot',
              height: 600,
              width: 800,
              scale: 2
            }
          }}
          style={{ width: '100%', height: '500px' }}
          useResizeHandler={true}
        />
      </div>
    );
  }
  
  // Fallback for old base64 image format
  if (data.base64) {
    return (
      <div className={`bg-white rounded-lg shadow-sm border border-gray-200 p-4 ${className}`}>
        {title && (
          <h3 className="text-lg font-semibold text-gray-900 mb-3">{title}</h3>
        )}
        <img
          src={`data:image/png;base64,${data.base64}`}
          alt={title || data.title || 'Plot'}
          className="w-full h-auto rounded"
        />
      </div>
    );
  }
  
  return (
    <div className={`bg-white rounded-lg shadow-sm border border-gray-200 p-4 ${className}`}>
      <p className="text-gray-500">No plot data available</p>
    </div>
  );
};

export default PlotlyChart;
