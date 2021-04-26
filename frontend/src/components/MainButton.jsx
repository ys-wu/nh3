import React, { useState, useEffect } from 'react';
import Button from 'antd/lib/button';

import url from '../conf.js';
import apiPost from '../helpers/apiPost.js';


export default function MainButon() {
  const urlCommand = url + 'command';
  const [start, setStart] = useState(true);

  useEffect(() => {
    if (start) {
      apiPost(urlCommand, {command: 'start'});
    } else {
      apiPost(urlCommand, {command: 'stop'});
    };
  }, [start])

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
