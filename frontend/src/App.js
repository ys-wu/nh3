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


export default function App () {

  const urlData = url + 'data';
  const [data, setData] = useState(null);

  const dataProcessor = data => {
    setData(data);
    return data['data']['Status'];
  };

  useInterval(() => {
    apiGet(urlData, dataProcessor);
    setTimeout(() => {}, 100);
  }, 2000);

  return (
    <div className="App">
      <Row style={{paddingTop: 20}}>
        <Col style={{padding: 10}} span={8} offset={0}>
          <Row>
            <MainButton data={data}/>
          </Row>
          <Row>
            <DataTable />
          </Row>
        </Col>
        <Col style={{padding: 10}} span={16} offset={0}>
          <h1>Plots</h1>
        </Col>
      </Row>
    </div>
  );
};
