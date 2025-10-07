/**
 * 🤖 Agent State Slice
 */

import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  agents: [],
  activeAgents: [],
  selectedAgent: null,
  tasks: [],
  loading: false,
  error: null,
};

const agentSlice = createSlice({
  name: 'agent',
  initialState,
  reducers: {
    setAgents: (state, action) => {
      state.agents = action.payload;
    },
    setActiveAgents: (state, action) => {
      state.activeAgents = action.payload;
    },
    setSelectedAgent: (state, action) => {
      state.selectedAgent = action.payload;
    },
    addAgent: (state, action) => {
      state.agents.push(action.payload);
    },
    removeAgent: (state, action) => {
      state.agents = state.agents.filter(
        (agent) => agent.id !== action.payload
      );
    },
    setTasks: (state, action) => {
      state.tasks = action.payload;
    },
    addTask: (state, action) => {
      state.tasks.push(action.payload);
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
    },
  },
});

export const {
  setAgents,
  setActiveAgents,
  setSelectedAgent,
  addAgent,
  removeAgent,
  setTasks,
  addTask,
  setLoading,
  setError,
} = agentSlice.actions;

export default agentSlice.reducer;