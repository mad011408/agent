/**
 * 🗃️ Redux Store Configuration
 */

import { configureStore } from '@reduxjs/toolkit';
import aiModelReducer from './slices/aiModelSlice';
import agentReducer from './slices/agentSlice';

export const store = configureStore({
  reducer: {
    aiModel: aiModelReducer,
    agent: agentReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});

export default store;