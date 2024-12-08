// frontend/src/router/Routes.tsx

import React, { Suspense, lazy } from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from '@/components/Layout';

const HomePage = lazy(() => import('@/pages/HomePage'));
const FeaturesPage = lazy(() => import('@/pages/FeaturesPage'));
const TeamPage = lazy(() => import('@/pages/TeamPage'));
const NotFoundPage = lazy(() => import('@/pages/NotFoundPage')); 

const RoutesComponent: React.FC = () => (
  <Suspense fallback={<div className="mt-20 text-center">Loading...</div>}>
    <Routes>
      <Route path="/" element={<Layout><HomePage /></Layout>} />
      <Route path="/features" element={<Layout><FeaturesPage /></Layout>} />
      <Route path="/team" element={<Layout><TeamPage /></Layout>} />
      <Route path="*" element={<Layout><NotFoundPage /></Layout>} /> 
    </Routes>
  </Suspense>
);

export default RoutesComponent;