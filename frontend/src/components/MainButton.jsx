import React, { useState } from 'react';
import Row from 'antd/lib/row'
import Button from 'antd/lib/button';
import Checkbox from 'antd/lib/checkbox';
import Tag from 'antd/lib/tag';
import {
  CheckCircleOutlined,
  SyncOutlined,
  MinusCircleOutlined,
} from '@ant-design/icons';

import url from '../conf.js';
import apiPost from '../helpers/apiPost.js';
import useInterval from '../hooks/useInterval.jsx';


export default function MainButon({ data }) {
  const urlCommand = url + 'command';
  const urlStatus = url + 'status';
  const [start, setStart] = useState(null);
  const [service, setService] = useState(false);

  useInterval(() => {
    if (data && (data['data'] !== null)) {
      const status = data['data']['Status'];
      if (service === true) {
        if (status !== 'Servicing') {
          apiPost(urlStatus, { status: 'Servicing' });
        }
      } else {
        if (start === true) {
          if (!['Sampling', 'GasZero', 'LiqSpan'].includes(status)) {
            apiPost(urlCommand, { command: 'start' });
          };
        } else if (start === false) {
          if (status !== 'Idle') {
            apiPost(urlCommand, { command: 'stop' });
          };
        } else {
          if (status === 'Servicing') {
            apiPost(urlCommand, { command: 'stop' });
          };
        };
      };
    };
  }, 2000);

  const onStart = () => {
    setStart(true);
  };

  const onStop = () => {
    setStart(false);
  };

  const onService = e => {
    setService(e.target.checked);
  };

  return (
    <div>
      <Row>
        <div style={{ marginLeft: 10 }}>
          {
            !data['data']['Status'] ? null :
            data['data']['Status'] === 'Servicing' ?
              <Tag icon={<MinusCircleOutlined />} color="default">Servicing</Tag> :
            data['data']['Status'] === 'Idle' ?
              <Tag icon={<CheckCircleOutlined />} color="success">Idle</Tag> :
            data['data']['Status'] === 'Sampling' ?
              <Tag icon={<SyncOutlined spin />} color="processing">Sampling</Tag> :
            data['data']['Status'] === 'GasZero' ?
              <Tag icon={<SyncOutlined spin />} color="processing">GasZero</Tag> :
            data['data']['Status'] === 'LiqSpan' ?
              <Tag icon={<SyncOutlined spin />} color="processing">LiqSpan</Tag> :
            null
          }
        </div>
        <Checkbox tyle={{ margin: 10 }} onChange={onService}>Service</Checkbox>
      </Row>
      <Row>
        <Button style={{ margin: 10 }} onClick={onStart}>Start</Button>
        <Button style={{ margin: 10 }} onClick={onStop}>Stop</Button>
      </Row>
    </div>
  );
};
