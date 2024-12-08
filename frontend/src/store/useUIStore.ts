import {create } from 'zustand';

interface UIState {
  isDarkMode: boolean;
  toggleDarkMode: () => void;
}

const useUIStore = create<UIState>((set) => ({
  isDarkMode: false,
  toggleDarkMode: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
}));

export default useUIStore;