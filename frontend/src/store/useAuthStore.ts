import { create } from 'zustand';

const ALLOW_GUEST = import.meta.env.VITE_ALLOW_GUEST === 'true';

interface AuthState {
  isGuest: boolean;
  guestUsed: boolean;
  allowGuest: boolean;
  setGuest: (isGuest: boolean) => void;
  useGuestOnce: () => void;
}

const useAuthStore = create<AuthState>((set) => ({
  isGuest: false,
  guestUsed: JSON.parse(localStorage.getItem('guestUsed') || 'false'),
  allowGuest: ALLOW_GUEST,
  setGuest: (isGuest) => set({ isGuest }),
  useGuestOnce: () => {
    set({ guestUsed: true });
    localStorage.setItem('guestUsed', 'true');
  },
}));

export default useAuthStore;