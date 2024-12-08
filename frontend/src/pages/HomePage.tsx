
import React from 'react';
import HeroSection from '@/components/HeroSection';
import Features from '@/components/Features';
import UseCases from '@/components/UseCases';
import Testimonials from '@/components/Testimonials';
import CallToAction from '@/components/CallToAction';
import ChatbotButton from '@/components/ChatbotButton';
import ContentGeneratorSection from '@/components/ContentGenerator/ContentGeneratorSection'; // Import der ContentGeneratorSection

const Home: React.FC = () => (
  <main>
    <HeroSection odd={true} />
    <Features odd={false} />
    <UseCases odd={true} />
    <Testimonials odd={false} />
    <CallToAction odd={true} />
    <ContentGeneratorSection odd={false}  /> 
    {/* Floating Chatbot-Button */}
    <ChatbotButton />
  </main>
);

export default Home;