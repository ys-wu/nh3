import React, { Component } from 'react';
import './App.css';
import 'antd/dist/antd.css'
import Row from 'antd/lib/row';
import Col from 'antd/lib/col';


import MainSwitch from './components/MainSwitch.jsx';
import DataTable from './components/DataTable.jsx';


class App extends Component {
  render() {
    return (
      <div className="App">
        <Row style={{paddingTop: 20}}>
          <Col style={{padding: 10}} span={8} offset={0}>
            <Row>
              <MainSwitch />
            </Row>
            <Row>
              <DataTable />
            </Row>
          </Col>
          <Col style={{padding: 10}} span={16} offset={0}>
            col-6 col-offset-6
          </Col>
        </Row>
      </div>
    );
  };
};

export default App;
