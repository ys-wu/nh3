import { useState } from 'react';

import url from '../conf.js';
import useInterval from '../hooks/useInterval.jsx';
import apiGet from '../helpers/apiGet.js';


export default function DataTable() {
  const urlData = url + 'data';
  const [data, setData] = useState(null);

  const dataProcessor = data => {
    setData(data);
    return data['status'];
  };

  useInterval(() => {
    apiGet(urlData, dataProcessor);
    setTimeout(() => {}, 100);
  }, 500);
  
  return 'data table';
};
