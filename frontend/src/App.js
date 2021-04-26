import React, { useState } from 'react';
import './App.css';
import 'antd/dist/antd.css'
import Row from 'antd/lib/row';
import Col from 'antd/lib/col';

import url from './conf.js';
import apiGet from './helpers/apiGet.js';
import useInterval from './hooks/useInterval.jsx';
import MainButton from './components/MainButton.jsx';
import DataTable from './components/DataTable.jsx';
import TimeSeriesPlot from './components/TimeSeriesPlot.jsx';


export default function App () {

  const urlData = url + 'data';
  const [data, setData] = useState(null);
  const [dataArr, setDataArr] = useState([]);

  const updateArr = rawData => {
    const { dttm, data } = rawData;
    const { NH3, NH4 } = data;
    const newDataArr = [...dataArr];
    newDataArr.push({
      dttm: dttm,
      NH3: NH3,
      NH4: NH4,
    });
    while ((Date.parse(dttm) - Date.parse(newDataArr[0]['dttm'])) >= 60 * 60 * 1000) {
      newDataArr.shift();
    };
    setDataArr(newDataArr);
  };

  const dataProcessor = data => {
    if (data) {
      if (data['data'] !== null) {
        setData(data);
        updateArr(data);
        return data['data']['Status'];
      } else {
        return 'get empty data';
      };
    };  
    return 'cannot get data';
  };

  useInterval(() => {
    apiGet(urlData, dataProcessor);
    setTimeout(() => {}, 100);
  }, 500);

  return (
    <div className="App">
      {
        !data ? null :
          <Row style={{padding: 10}}>
            <Col xs={24} lg={12}>
              <Row>
                <MainButton data={data} />
              </Row>
              <Row>
                <DataTable data={data} />
              </Row>
            </Col>
            {
              dataArr.length > 0 ?
                <Col xs={24} lg={12}>
                  <TimeSeriesPlot dataArr={dataArr} />
                </Col> :
                null
            }
          </Row>
      }
    </div>
  );
};
