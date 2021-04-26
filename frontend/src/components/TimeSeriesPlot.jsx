import React from 'react';
import Plot from 'react-plotly.js';


export default function TimeSeriesPlot ({ dataArr }) {

  const x = dataArr.map(v => v['dttm']);
  const y1 = dataArr.map(v => v['NH3']);
  const y2 = dataArr.map(v => v['NH4']);

  const dataNH3 = [
    {
      x: x,
      y: y1,
    },
    { type: 'scatter' },
  ];

  const dataNH4 = [
    {
      x: x,
      y: y2,
    },
    {type: 'scatter'},
  ];

  return (
    <div>
      <Plot
        data={dataNH3}
        layout={{
          yaxis: {
            title: 'NH4 (ppt[g])',
          },
        }}
      />
      <Plot
        data={dataNH4}
        layout={{
          yaxis: {
            title: 'NH4+ (ppb[aq])',
          },
        }}
      />
    </div>
  );
};
