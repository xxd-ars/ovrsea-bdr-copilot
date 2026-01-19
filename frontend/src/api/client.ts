import axios from 'axios';
import { Lead, LeadCreate, LeadUpdate } from '../types';

const API_URL = 'http://localhost:8000';

export const getLeads = async (): Promise<Lead[]> => {
  const response = await axios.get(`${API_URL}/leads`);
  return response.data;
};

export const createLead = async (lead: LeadCreate): Promise<Lead> => {
  const response = await axios.post(`${API_URL}/leads`, lead);
  return response.data;
};

export const updateLead = async (id: number, lead: LeadUpdate): Promise<Lead> => {
  const response = await axios.patch(`${API_URL}/leads/${id}`, lead);
  return response.data;
};

export const deleteLead = async (id: number): Promise<void> => {
  await axios.delete(`${API_URL}/leads/${id}`);
};
