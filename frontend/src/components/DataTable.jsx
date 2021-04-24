import { useState } from 'react';

import url from '../conf.js';
import useInterval from '../hooks/useInterval';


export default function DataTable() {

  const urlData = url + 'data';

  const [data, setData] = useState(null);

  const fetchData = () => {
    fetch(urlData)
      .then(res => res.json())
      .then(setData)
  };

  useInterval(() => {
    fetchData();
    setTimeout(() => {}, 100);
    console.log(data);
  }, 500);
  
  return 'data table';
};
