import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import RoutesComponent from '@/router/Routes';
import QueryProvider from '@/providers/QueryProvider';

const App: React.FC = () => {
  return (
    <QueryProvider>
      <Router>
        <RoutesComponent />
      </Router>
    </QueryProvider>
  );
};

export default App;