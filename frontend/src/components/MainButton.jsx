import React, { useState } from 'react';
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
      if (service === true && data['data']['Status'] !== 'Servicing') {
        apiPost(urlStatus, { status: 'Servicing' });
      } else if (service === false) {
        if (start === true && data['data']['Status'] !== 'Sampling') {
          apiPost(urlCommand, { command: 'start' });
        } else if (start === false && data['data']['Status'] !== 'Idle') {
          apiPost(urlCommand, { command: 'stop' });
        };
      };
    };
  }, 5000);

  const onStart = () => {
    setStart(true);
  };

  const onStop = () => {
    setStart(false);
  };

  const onService = e => {
    setService(e.target.checked);
  };

  const StatusTag = data => {
    if (data && (data['data'] !== null)) {
      if (data['data']['Status'] === 'Servicing') {
        return <Tag icon={<MinusCircleOutlined />} color="default">Servicing</Tag>
      } else if (data['data']['Status'] === 'Idle') {
        return <Tag icon={<CheckCircleOutlined />} color="success">Idle</Tag>
      } else if (data['data']['Status'] === 'Sampling') {
        return <Tag icon={<SyncOutlined spin />} color="processing">Sampling</Tag>
      } else if (data['data']['Status'] === 'GasZero') {
        return <Tag icon={<SyncOutlined spin />} color="processing">GasZero</Tag>
      } else if (data['data']['Status'] === 'Sampling') {
        return <Tag icon={<SyncOutlined spin />} color="processing">LiqSpan</Tag>
      };
    };
    return null;
  };

  return (
    <div>
      <Button onClick={onStart}>Start</Button>
      <Button onClick={onStop}>Stop</Button>
      <Checkbox onChange={onService}>Service</Checkbox>
      <StatusTag data={data}/>
    </div>
  );
};
