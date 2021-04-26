import React, { useState } from 'react';
import Button from 'antd/lib/button';

import url from '../conf.js';
import apiPost from '../helpers/apiPost.js';
import useInterval from '../hooks/useInterval.jsx';


export default function MainButon({ data }) {
  const urlCommand = url + 'command';
  const [start, setStart] = useState(false);


  useInterval(() => {
    if (data && (data['data'] !== null)) {
      if (
        (start === true) &&
        (!['Sampling', 'Servicing'].includes(data['data']['Status']))
      ) {
        apiPost(urlCommand, { command: 'start' });
      } else if (
        (start === false) &&
        (!['Idle', 'Servicing'].includes(data['data']['Status']))
      ) {
        apiPost(urlCommand, { command: 'stop' });
      };
    };
  }, 5000);

  const onStart = () => {
    setStart(true);
  };

  const onStop = () => {
    setStart(false);
  };

  return (
    <div>
      <Button onClick={onStart}>Start</Button>
      <Button onClick={onStop}>Stop</Button>
    </div>
  );
};
