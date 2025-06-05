
import { useContext } from 'react';
import { MamaBearContext } from '../contexts/MamaBearContext';

export const useMamaBear = () => {
  const context = useContext(MamaBearContext);
  if (context === undefined) {
    throw new Error('useMamaBear must be used within a MamaBearProvider');
  }
  return context;
};