/**
 * 🧠 AI Model State Slice
 */

import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  currentProvider: 'nvidia',
  currentModel: null,
  providers: [],
  metrics: null,
  loading: false,
  error: null,
};

const aiModelSlice = createSlice({
  name: 'aiModel',
  initialState,
  reducers: {
    setProvider: (state, action) => {
      state.currentProvider = action.payload;
    },
    setModel: (state, action) => {
      state.currentModel = action.payload;
    },
    setProviders: (state, action) => {
      state.providers = action.payload;
    },
    setMetrics: (state, action) => {
      state.metrics = action.payload;
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
  setProvider,
  setModel,
  setProviders,
  setMetrics,
  setLoading,
  setError,
} = aiModelSlice.actions;

export default aiModelSlice.reducer;