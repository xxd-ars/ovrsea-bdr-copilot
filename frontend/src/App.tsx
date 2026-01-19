import React, { useEffect, useState, useRef } from 'react';
import { Layout, Table, Button, Tag, Descriptions, Space, Typography, Modal, Form, Input, Select, message, Popconfirm, Divider } from 'antd';
import { PlusOutlined, ReloadOutlined, RobotOutlined, DeleteOutlined, EditOutlined, CloseOutlined, SendOutlined, SearchOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { Lead, LeadCreate, LeadUpdate } from './types';
import { getLeads, createLead, updateLead, deleteLead, chatAgent, resetAgent } from './api/client';

const { Header, Content } = Layout;
const { Title, Text } = Typography;
const { TextArea } = Input;

// Status options for dropdown
const STATUS_OPTIONS = [
  { value: 'New', label: 'New', color: 'blue' },
  { value: 'Qualified', label: 'Qualified', color: 'green' },
  { value: 'Disqualified', label: 'Disqualified', color: 'default' },
  { value: 'Contacted', label: 'Contacted', color: 'orange' },
  { value: 'Negotiating', label: 'Negotiating', color: 'gold' },
];

function App() {
    const [leads, setLeads] = useState<Lead[]>([]);
    const [loading, setLoading] = useState(false);
    const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [form] = Form.useForm();

    // For Detail Panel Editing
    const [isEditing, setIsEditing] = useState(false);
    const [editForm] = Form.useForm();

    // For real-time column search
    const [companySearch, setCompanySearch] = useState('');
    const [locationSearch, setLocationSearch] = useState('');
  
    // For AI Assistant
    const [aiInput, setAiInput] = useState('');
    const [chatHistory, setChatHistory] = useState<{role: 'user' | 'agent', content: string}[]>([
      { role: 'agent', content: '[SYSTEM] Initialized OVRSEA BDR Agent v1.0.0' },
      { role: 'agent', content: '[SYSTEM] Context loaded. Ready for instructions.' }
    ]);
    const [isAgentProcessing, setIsAgentProcessing] = useState(false);
    const chatEndRef = useRef<HTMLDivElement>(null);
  
    const fetchLeads = async () => {
      setLoading(true);
      try {
        const data = await getLeads();
        setLeads(data);
      } catch (error) {
        message.error('Failed to fetch leads');
      } finally {
        setLoading(false);
      }
    };
  
    useEffect(() => {
      fetchLeads();
    }, []);

    useEffect(() => {
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [chatHistory]);

    // --- Real-time filtered data ---
    const filteredLeads = leads.filter(lead => {
      const matchCompany = lead.company_name.toLowerCase().includes(companySearch.toLowerCase());
      const matchLocation = lead.location.toLowerCase().includes(locationSearch.toLowerCase());
      return matchCompany && matchLocation;
    });

    // --- Actions ---

    const handleNewSession = async () => {
      try {
        await resetAgent();
        setChatHistory([{ role: 'agent', content: '[SYSTEM] Session reset. Context cleared.' }]);
        message.success('New chat session started');
      } catch (error) {
        message.error('Failed to reset session');
      }
    };

    const handleAgentSubmit = async () => {
      if (!aiInput.trim()) return;
      
      const userMsg = aiInput;
      setAiInput('');
      setChatHistory(prev => [...prev, { role: 'user', content: userMsg }]);
      setIsAgentProcessing(true);

      try {
        const res = await chatAgent(userMsg);
        setChatHistory(prev => [...prev, { role: 'agent', content: res.response }]);
        // Refresh leads in case agent modified something
        fetchLeads();
      } catch (error) {
        setChatHistory(prev => [...prev, { role: 'agent', content: `[ERROR] Failed to communicate with agent: ${error}` }]);
      } finally {
        setIsAgentProcessing(false);
      }
    };
  
    const handleAddLead = async (values: LeadCreate) => {
      try {
        await createLead(values);
        message.success('Lead added successfully');
        setIsModalOpen(false);
        form.resetFields();
        fetchLeads();
      } catch (error) {
        message.error('Failed to add lead');
      }
    };
  
    const handleUpdateLead = async (values: LeadUpdate) => {
      if (!selectedLead) return;
      try {
        // Convert comma-separated strings back to arrays for list fields
        const processedValues: LeadUpdate = {
          ...values,
          transport_modes: typeof values.transport_modes === 'string'
            ? (values.transport_modes as string).split(',').map(s => s.trim()).filter(Boolean)
            : values.transport_modes,
          import_locations: typeof values.import_locations === 'string'
            ? (values.import_locations as string).split(',').map(s => s.trim()).filter(Boolean)
            : values.import_locations,
          export_locations: typeof values.export_locations === 'string'
            ? (values.export_locations as string).split(',').map(s => s.trim()).filter(Boolean)
            : values.export_locations,
        };
  
        const updated = await updateLead(selectedLead.id, processedValues);
        message.success('Lead updated');
        setSelectedLead(updated);
        setIsEditing(false);
        fetchLeads();
      } catch (error) {
        message.error('Failed to update lead');
      }
    };
  
    const handleDeleteLead = async (id: number) => {
      try {
        await deleteLead(id);
        message.success('Lead deleted');
        fetchLeads();
        if (selectedLead?.id === id) {
          setSelectedLead(null);
        }
      } catch (error) {
        message.error('Failed to delete lead');
      }
    };
  
    const openDetailPanel = (lead: Lead) => {
      setSelectedLead(lead);
      setIsEditing(false);
    };
  
    const closeDetailPanel = () => {
      setSelectedLead(null);
      setIsEditing(false);
    };
  
    const startEditing = () => {
      if (selectedLead) {
        editForm.setFieldsValue({
          ...selectedLead,
          // Convert arrays to comma-separated strings for editing
          transport_modes: selectedLead.transport_modes?.join(', ') || '',
          import_locations: selectedLead.import_locations?.join(', ') || '',
          export_locations: selectedLead.export_locations?.join(', ') || '',
        });
        setIsEditing(true);
      }
    };
  
    // --- UI Config ---
  
    const getStatusColor = (status: string) => {
      const found = STATUS_OPTIONS.find(s => s.value === status);
      return found?.color || 'blue';
    };
  
    const columns: ColumnsType<Lead> = [
      {
        title: 'Status',
        dataIndex: 'status',
        key: 'status',
        width: 130,
        render: (status) => <Tag color={getStatusColor(status)}>{status}</Tag>,
        filters: STATUS_OPTIONS.map(opt => ({ text: opt.label, value: opt.value })),
        onFilter: (value, record) => record.status === value,
      },
      {
        title: (
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span>Company</span>
            <Input
              placeholder="Search..."
              size="small"
              value={companySearch}
              onChange={(e) => setCompanySearch(e.target.value)}
              prefix={<SearchOutlined style={{ color: '#bfbfbf' }} />}
              allowClear
              onClick={(e) => e.stopPropagation()}
              style={{ width: 120 }}
            />
          </div>
        ),
        dataIndex: 'company_name',
        key: 'company_name',
        render: (text) => <Text strong>{text}</Text>,
      },
      {
        title: 'Industry',
        dataIndex: 'industry',
        key: 'industry',
        ellipsis: true,
        sorter: (a, b) => a.industry.localeCompare(b.industry),
      },
      {
        title: (
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span>Location</span>
            <Input
              placeholder="Search..."
              size="small"
              value={locationSearch}
              onChange={(e) => setLocationSearch(e.target.value)}
              prefix={<SearchOutlined style={{ color: '#bfbfbf' }} />}
              allowClear
              onClick={(e) => e.stopPropagation()}
              style={{ width: 120 }}
            />
          </div>
        ),
        dataIndex: 'location',
        key: 'location',
      },
      {
        title: 'Employees',
        dataIndex: 'employee_count',
        key: 'employee_count',
        width: 130,
        filters: [
          { text: '0-50', value: '0-50' },
          { text: '50-100', value: '50-100' },
          { text: '100-200', value: '100-200' },
          { text: '200-500', value: '200-500' },
          { text: '500-1000', value: '500-1000' },
          { text: '1000+', value: '1000+' },
        ],
        onFilter: (value, record) => record.employee_count === value,
      },
      {
        title: 'Action',
        key: 'action',
        width: 120,
        render: (_, record) => (
          <Space size="small">
            <Button type="primary" size="small" onClick={() => openDetailPanel(record)}>View</Button>
            <Popconfirm
              title="Delete this lead?"
              onConfirm={() => handleDeleteLead(record.id)}
              okText="Yes"
              cancelText="No"
            >
              <Button type="text" danger size="small" icon={<DeleteOutlined />} />
            </Popconfirm>
          </Space>
        ),
      },
    ];
  
    // --- Render ---
  
    return (
      <Layout style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <Header style={{
          display: 'flex',
          alignItems: 'center',
          background: '#fff',
          padding: '0 24px',
          borderBottom: '1px solid #f0f0f0',
          flexShrink: 0
        }}>
          <Title level={3} style={{ margin: 0, flex: 1 }}>🚀 Ovrsea BDR Tool</Title>
          <Space>
            <Button icon={<ReloadOutlined />} onClick={fetchLeads}>Refresh</Button>
            <Button type="primary" icon={<PlusOutlined />} onClick={() => setIsModalOpen(true)}>Add Lead</Button>
          </Space>
        </Header>
  
        {/* Main Content Area */}
        <Content style={{ display: 'flex', flexDirection: 'column', flex: 1, overflow: 'hidden' }}>
  
          {/* Top Section: List + Detail Panel */}
          <div style={{
            flex: 1,
            display: 'flex',
            overflow: 'hidden',
            borderBottom: '1px solid #f0f0f0'
          }}>
            {/* Left: Lead List Table */}
            <div style={{
              flex: selectedLead ? 1 : 1,
              overflow: 'auto',
              padding: '16px',
              minWidth: 0
            }}>
              <Table
                columns={columns}
                dataSource={filteredLeads}
                rowKey="id"
                loading={loading}
                size="middle"
                pagination={{ pageSize: 10, showSizeChanger: false }}
                scroll={{ y: 'calc(100vh - 400px)' }}
              />
            </div>
          {/* Right: Detail Panel (visible when lead selected) */}
          {selectedLead && (
            <div style={{
              width: '35%',
              minWidth: 400,
              maxWidth: 800,
              borderLeft: '1px solid #f0f0f0',
              overflow: 'auto',
              background: '#fafafa',
              flexShrink: 0
            }}>
              <div style={{ padding: '24px' }}>
                {/* Panel Header */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
                  <Title level={4} style={{ margin: 0 }}>{selectedLead.company_name}</Title>
                  <Space>
                    {!isEditing && (
                      <Button icon={<EditOutlined />} size="small" onClick={startEditing}>Edit</Button>
                    )}
                    {isEditing && (
                      <>
                        <Button size="small" onClick={() => setIsEditing(false)}>Cancel</Button>
                        <Button type="primary" size="small" onClick={() => editForm.submit()}>Save</Button>
                      </>
                    )}
                    <Button icon={<CloseOutlined />} size="small" onClick={closeDetailPanel} />
                  </Space>
                </div>

                {isEditing ? (
                  /* Edit Form Mode */
                  <Form
                    form={editForm}
                    layout="vertical"
                    onFinish={handleUpdateLead}
                    size="small"
                  >
                    <Form.Item name="company_name" label="Company Name">
                      <Input />
                    </Form.Item>
                    <Form.Item name="website_url" label="Website">
                      <Input />
                    </Form.Item>
                    <Form.Item name="industry" label="Industry">
                      <Input />
                    </Form.Item>
                    <Form.Item name="location" label="Location">
                      <Input />
                    </Form.Item>
                    <Form.Item name="employee_count" label="Employees">
                      <Input />
                    </Form.Item>
                    <Form.Item name="product" label="Product">
                      <TextArea rows={2} />
                    </Form.Item>
                    <Form.Item name="product_type" label="Product Type">
                      <Select>
                        <Select.Option value="Physical Goods">Physical Goods</Select.Option>
                        <Select.Option value="Software / Service">Software / Service</Select.Option>
                      </Select>
                    </Form.Item>
                    <Form.Item name="transport_modes" label="Transport Modes" tooltip="Comma-separated: Sea, Air, Road">
                      <Input placeholder="Sea, Air, Road" />
                    </Form.Item>
                    <Form.Item name="import_locations" label="Import Locations" tooltip="Comma-separated">
                      <Input placeholder="China, Vietnam, ..." />
                    </Form.Item>
                    <Form.Item name="export_locations" label="Export Locations" tooltip="Comma-separated">
                      <Input placeholder="USA, Europe, ..." />
                    </Form.Item>
                    <Form.Item name="status" label="Status">
                      <Select>
                        {STATUS_OPTIONS.map(opt => (
                          <Select.Option key={opt.value} value={opt.value}>{opt.label}</Select.Option>
                        ))}
                      </Select>
                    </Form.Item>
                  </Form>
                ) : (
                  /* View Mode */
                  <Descriptions column={1} size="small" bordered>
                    <Descriptions.Item label="Website">
                      <a href={selectedLead.website_url} target="_blank" rel="noopener noreferrer">
                        {selectedLead.website_url}
                      </a>
                    </Descriptions.Item>
                    <Descriptions.Item label="Industry">{selectedLead.industry}</Descriptions.Item>
                    <Descriptions.Item label="Location">{selectedLead.location}</Descriptions.Item>
                    <Descriptions.Item label="Employees">{selectedLead.employee_count}</Descriptions.Item>
                    <Descriptions.Item label="Product">{selectedLead.product || '-'}</Descriptions.Item>
                    <Descriptions.Item label="Product Type">
                      <Tag color={selectedLead.product_type === 'Physical Goods' ? 'green' : 'purple'}>
                        {selectedLead.product_type || 'N/A'}
                      </Tag>
                    </Descriptions.Item>
                    <Descriptions.Item label="Transport">
                      {selectedLead.transport_modes?.length > 0
                        ? selectedLead.transport_modes.map(m => <Tag key={m}>{m}</Tag>)
                        : '-'
                      }
                    </Descriptions.Item>
                    <Descriptions.Item label="Import From">
                      {selectedLead.import_locations?.join(', ') || '-'}
                    </Descriptions.Item>
                    <Descriptions.Item label="Export To">
                      {selectedLead.export_locations?.join(', ') || '-'}
                    </Descriptions.Item>
                    <Descriptions.Item label="Status">
                      <Tag color={getStatusColor(selectedLead.status)}>{selectedLead.status}</Tag>
                    </Descriptions.Item>
                  </Descriptions>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Bottom Section: AI Agent Workspace (Light Theme with History Sidebar) */}
        <div style={{
          height: '55vh',
          background: '#fff',
          borderTop: '1px solid #d9d9d9',
          display: 'flex',
          flexShrink: 0,
        }}>
          {/* Sidebar: Chat History */}
          <div style={{
            width: 250,
            background: '#f8f9fa',
            borderRight: '1px solid #f0f0f0',
            display: 'flex',
            flexDirection: 'column',
            flexShrink: 0
          }}>
            <div style={{ padding: '12px 16px', borderBottom: '1px solid #eee', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Text strong size="small" style={{ color: '#555' }}>SESSIONS</Text>
              <Button size="small" icon={<PlusOutlined />} onClick={handleNewSession}>New</Button>
            </div>
            <div style={{ flex: 1, overflowY: 'auto', padding: '8px' }}>
              <div style={{ 
                padding: '8px 12px', 
                background: '#e6f7ff', 
                borderRadius: 4, 
                cursor: 'pointer', 
                marginBottom: 4,
                border: '1px solid #91d5ff'
              }}>
                <Text strong style={{ fontSize: '12px' }}>Current Investigation</Text><br/>
                <Text type="secondary" style={{ fontSize: '10px' }}>Just now</Text>
              </div>
              <div style={{ padding: '8px 12px', borderRadius: 4, cursor: 'not-allowed', opacity: 0.6 }}>
                <Text style={{ fontSize: '12px' }}>Previous Outreach</Text><br/>
                <Text type="secondary" style={{ fontSize: '10px' }}>2 hours ago</Text>
              </div>
            </div>
          </div>

          {/* Main Chat Area */}
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', background: '#fff' }}>
            {/* Minimalist Terminal Header */}
            <div style={{
              padding: '8px 24px',
              borderBottom: '1px solid #f0f0f0',
              display: 'flex',
              alignItems: 'center',
              background: '#fff',
              fontSize: '12px'
            }}>
              <RobotOutlined style={{ fontSize: 14, marginRight: 8, color: '#1890ff' }} />
              <Text type="secondary" strong>AGENT WORKSPACE</Text>
              <Divider type="vertical" />
              <Text type="secondary">ID: session_8829</Text>
            </div>

            {/* Content: Left-aligned Raw Text (CLI style) */}
            <div style={{
              flex: 1,
              overflowY: 'auto',
              padding: '20px 32px',
              fontFamily: 'Menlo, Monaco, "Courier New", monospace',
              fontSize: '13px',
              lineHeight: 1.6,
              color: '#333'
            }}>
              {chatHistory.map((msg, idx) => (
                <div key={idx} style={{ marginBottom: 12 }}>
                  {msg.role === 'agent' ? (
                    <div style={{ whiteSpace: 'pre-wrap' }}>
                      <span style={{ color: '#1890ff', marginRight: 8 }}>[AGENT]</span> 
                      {msg.content}
                    </div>
                  ) : (
                    <div>
                      <span style={{ color: '#52c41a', marginRight: 8, fontWeight: 'bold' }}>❯</span> 
                      <span style={{ fontWeight: 600 }}>{msg.content}</span>
                    </div>
                  )}
                </div>
              ))}
              {isAgentProcessing && (
                <div style={{ color: '#888', fontStyle: 'italic' }}>
                  <span style={{ color: '#1890ff', marginRight: 8 }}>[AGENT]</span> 
                  Thinking...
                </div>
              )}
              <div ref={chatEndRef} />
            </div>

            {/* Input Area: Ergonomic & Clean */}
            <div style={{
              padding: '16px 32px',
              background: '#fff',
              borderTop: '1px solid #f0f0f0'
            }}>
              <div style={{ display: 'flex', gap: 12, alignItems: 'flex-start' }}>
                <span style={{ color: '#1890ff', fontSize: '18px', fontWeight: 'bold', paddingTop: 4 }}>❯</span>
                <TextArea
                  value={aiInput}
                  onChange={(e) => setAiInput(e.target.value)}
                  placeholder="Ask the agent to qualify leads, search info, or draft emails..."
                  autoSize={{ minRows: 1, maxRows: 4 }}
                  style={{ 
                    flex: 1, 
                    border: 'none', 
                    boxShadow: 'none', 
                    padding: '8px 0',
                    fontSize: '15px',
                    fontFamily: 'inherit',
                    resize: 'none'
                  }}
                  onPressEnter={(e) => {
                    if (!e.shiftKey) {
                      e.preventDefault();
                      handleAgentSubmit();
                    }
                  }}
                  disabled={isAgentProcessing}
                />
                <Button
                  type="primary"
                  icon={<SendOutlined />}
                  style={{ height: 40, padding: '0 24px', borderRadius: 6 }}
                  disabled={!aiInput.trim() || isAgentProcessing}
                  onClick={handleAgentSubmit}
                  loading={isAgentProcessing}
                >
                  Run
                </Button>
              </div>
            </div>
          </div>
        </div>
      </Content>

      {/* Add Lead Modal */}
      <Modal
        title="Add New Lead"
        open={isModalOpen}
        onCancel={() => { setIsModalOpen(false); form.resetFields(); }}
        onOk={() => form.submit()}
        okText="Add Lead"
      >
        <Form form={form} layout="vertical" onFinish={handleAddLead}>
          <Form.Item
            name="company_name"
            label="Company Name"
            rules={[{ required: true, message: 'Please enter company name' }]}
          >
            <Input placeholder="e.g., Sézane" />
          </Form.Item>
          <Form.Item
            name="website_url"
            label="Website URL"
            rules={[{ required: true, message: 'Please enter website URL' }]}
          >
            <Input placeholder="https://www.example.com" />
          </Form.Item>
          <Form.Item name="industry" label="Industry">
            <Input placeholder="e.g., Fashion & Apparel" />
          </Form.Item>
          <Form.Item name="location" label="Location">
            <Input placeholder="e.g., Paris, France" />
          </Form.Item>
          <Form.Item name="employee_count" label="Employee Count">
             <Select placeholder="Select size">
                <Select.Option value="0-50">0-50</Select.Option>
                <Select.Option value="50-100">50-100</Select.Option>
                <Select.Option value="100-200">100-200</Select.Option>
                <Select.Option value="200-500">200-500</Select.Option>
                <Select.Option value="500-1000">500-1000</Select.Option>
                <Select.Option value="1000+">1000+</Select.Option>
             </Select>
          </Form.Item>
        </Form>
      </Modal>
    </Layout>
  );
}

export default App;
