import React, { useState } from 'react';
import Switch from 'antd/lib/switch';


export default function MainSwitch() {
  const [running, setRunningg] = useState(false);

  const onChangeRunning = checked => {
    setRunningg(checked);
  };

  return <Switch style={{ margin: 5 }} onChange={onChangeRunning} />
};
