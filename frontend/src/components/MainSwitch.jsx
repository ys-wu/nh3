import React, { useState, useEffect } from 'react';
import Switch from 'antd/lib/switch';

import url from '../conf.js';
import apiPost from '../helpers/apiPost.js';


export default function MainSwitch() {
  const urlCommand = url + 'command';
  const [start, setStart] = useState(true);

  useEffect(() => {
    if (start) {
      apiPost(urlCommand, {command: 'start'});
    } else {
      apiPost(urlCommand, {command: 'stop'});
    };
  }, [start])

  const onChangeStart = checked => {
    setStart(checked);
  };

  return <Switch style={{ margin: 5 }} onChange={onChangeStart} />
};
