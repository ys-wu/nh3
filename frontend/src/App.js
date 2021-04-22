import React, { Component } from 'react';
import './App.css';

import Row from 'antd/lib/row';
import Col from 'antd/lib/col';


class App extends Component {
  render() {
    return (
      <Row>
        <Col span={6} offset={1}>
          col_1
        </Col>
        <Col span={14}>
          col_2
        </Col>
      </Row>
    );
  };
};

export default App;
