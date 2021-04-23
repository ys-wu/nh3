import React, { useState, useEffect } from 'react';
import Switch from 'antd/lib/switch';


export default function MainSwitch() {
  const [running, setRunningg] = useState(true);

  useEffect(() => {
    if (running) {
      
    } else {

    };
  }, [useEffect])

  

  const onChangeRunning = checked => {
    setRunningg(checked);
  };

  return <Switch style={{ margin: 5 }} onChange={onChangeRunning} />
};
