import React, { useEffect, useState } from 'react';
import Tabs from 'antd/lib/tabs';
import Plot from 'react-plotly.js';

const { TabPane } = Tabs;


export default function TimeSeriesPlot ({ dataArr }) {

  const x = dataArr.map(v => v['dttm']);
  const y1 = dataArr.map(v => v['NH3']);
  const y2 = dataArr.map(v => v['NH4']);

  return (
    <div>
      <Tabs defaultActiveKey="2">
        <TabPane tab="NH3[g] Time Series" key="1">
          <Plot
            data={[
              {
                x: x,
                y: y1,
              },
              { type: 'scatter' },
            ]}
            layout={{
              width: 500,
              height: 400,
              yaxis: {
                title: 'NH4 (ppt[g])',
              },
            }}
          />
        </TabPane>
        <TabPane tab="NH4+[aq] Time Series" key="2">
          <Plot
            data={[
              {
                x: x,
                y: y2,
              },
              { type: 'scatter' },
            ]}
            layout={{
              width: 500,
              height: 400,
              yaxis: {
                title: 'NH4+ (ppb[aq])',
              },
            }}
          />
        </TabPane>
      </Tabs>
    </div>
  );
};
