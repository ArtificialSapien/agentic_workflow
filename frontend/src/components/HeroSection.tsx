// src/components/HeroSection.tsx
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

interface HeroSectionProps {
  odd: boolean;
}

const HeroSection: React.FC<HeroSectionProps> = ({ odd }) => (
  <section className={`bg-gradient-to-b ${odd ? 'from-primary-100 to-white' : 'from-white to-primary-100'} text-center py-20 min-h-screen flex items-center`}>
    <div className="max-w-6xl mx-auto px-6">
      <motion.h1
        className="text-4xl md:text-6xl font-bold mb-4 text-transparent bg-gradient-rainbow bg-clip-text animate-gradient-x"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        Be the first to tell the future.
      </motion.h1>
      <motion.p
        className="text-xl md:text-2xl font-light leading-relaxed mb-8 text-gray-800"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1, delay: 0.5 }}
      >
        Our{' '}
        <span className="text-accent-400 font-semibold">
          Tech Trend AI Agent
        </span>{' '}
        identifies emerging technologies before they go mainstream and transforms them into
        engaging content for your audience – from social media posts to videos and memes.
      </motion.p>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1, delay: 1 }}
      >
        <Link
          to="#"
          onClick={(e) => {
            e.preventDefault();
            const section = document.getElementById('content-generator-section');
            if (section) {
              section.scrollIntoView({ behavior: 'smooth' });
            }
          }}
          className="inline-block bg-accent-500 text-white px-8 py-3 rounded-md text-lg font-semibold hover:bg-accent-600 transition-all shadow-accent-glow focus:outline-none focus:ring-2 focus:ring-accent-400"
          aria-label="Try it for free now"
        >
          Try it for free now
        </Link>
      </motion.div>
    </div>
  </section>
);

export default HeroSection;
