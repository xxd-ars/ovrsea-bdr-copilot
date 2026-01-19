import axios from 'axios';
import { Lead, LeadCreate, LeadUpdate } from '../types';

const API_URL = 'http://localhost:8000'; // Default FastAPI port

export const getLeads = async (): Promise<Lead[]> => {
  const response = await axios.get(`${API_URL}/leads`);
  return response.data;
};

export const getLead = async (id: number): Promise<Lead> => {
  const response = await axios.get(`${API_URL}/leads/${id}`);
  return response.data;
};

export const createLead = async (data: LeadCreate): Promise<Lead> => {
  const response = await axios.post(`${API_URL}/leads`, data);
  return response.data;
};

export const updateLead = async (id: number, data: LeadUpdate): Promise<Lead> => {
  const response = await axios.patch(`${API_URL}/leads/${id}`, data);
  return response.data;
};

export const deleteLead = async (id: number): Promise<void> => {
  await axios.delete(`${API_URL}/leads/${id}`);
};

// Agent Chat API
export const chatAgent = async (message: string): Promise<{ response: string }> => {
  const response = await axios.post(`${API_URL}/api/agent/chat`, { message });
  return response.data;
};

export const resetAgent = async (): Promise<void> => {
  await axios.post(`${API_URL}/api/agent/reset`);
};