import React from 'react';
import Plot from 'react-plotly.js';


export default function TimeSeriesPlot ({ dataArr }) {

  const x = dataArr.map(v => v['dttm']);
  const y1 = dataArr.map(v => v['NH3']);
  const y2 = dataArr.map(v => v['NH4']);

  const dataNH4 = [
    {
      x: x,
      y: y2,
      // marker: { color: 'red' },
    },
    {type: 'scatter'},
  ];

  return (
    <div>
      <Plot
        data={dataNH4}
        layout={{
          yaxis: {
            title: 'NH4+ (ppb[aq])'
          },
        }}
      />
    </div>
  );
};
