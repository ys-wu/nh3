import React from 'react';
import Row from 'antd/lib/row';
import Col from 'antd/lib/col'
import Table from 'antd/lib/table';


export default function DataTable({ data }) {

  const measureColumns = [
    {
      title: 'Data',
      dataIndex: 'data',
      key: 'data',
    },
    {
      title: 'Value',
      dataIndex: 'value',
      key: 'value',
    },
  ];

  const measureData = Object.entries(data['data'])
    .map(([key, value]) => ({
      key: key,
      data: key,
      value: value,
    }));

  const statusColumns = [
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: 'Value',
      dataIndex: 'value',
      key: 'value',
    },
  ];

  const statusData = Object.entries(data['status'])
    .map(([key, value]) => ({
      key: key,
      status: key,
      value: value,
    }));

  return (
    <div>
      <Row style={{ marginLeft: 20 }}>
        <h3>{ data['dttm'] + ' (UTC)' }</h3>
      </Row>
      <Row>
        <Col style={{ padding: 10 }} span={12} offset={0}>
          <Table
            pagination={false}
            columns={measureColumns}
            dataSource={measureData}
          />
        </Col>
        <Col style={{ padding: 10 }} span={12} offset={0}>
          <Table
            pagination={false}
            columns={statusColumns}
            dataSource={statusData}
          />
        </Col>
      </Row>
    </div>
  );
};
