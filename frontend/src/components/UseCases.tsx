import { motion } from 'framer-motion';
import { Rocket, BarChart2, Video } from 'lucide-react';

const useCases = [
  {
    title: 'Startups',
    description: 'Stay one step ahead of established players.',
    icon: <Rocket className="w-12 h-12 text-accent-500" />,
  },
  {
    title: 'Agencies',
    description: 'Create complete campaigns for your clients in minutes.',
    icon: <BarChart2 className="w-12 h-12 text-accent-500" />,
  },
  {
    title: 'Creators & Influencers',
    description: 'Leverage new trends for maximum reach and engagement.',
    icon: <Video className="w-12 h-12 text-accent-500" />,
  },
];

interface UseCasesSectionProps {
  odd: boolean;
}

const UseCases: React.FC<UseCasesSectionProps> = ({ odd }) => (
  <section className={`bg-gradient-to-b ${odd ? 'from-primary-100 to-white' : 'from-white to-primary-100'} text-center py-20 min-h-screen flex items-center`}>
    <div className="max-w-6xl mx-auto px-6 py-16 bg-lightblue-100 text-center rounded-md my-10">
    <motion.h2
      className="text-3xl md:text-4xl font-bold text-primary-600 mb-12"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
    >
      Who is our agent designed for?
    </motion.h2>
    <div className="grid md:grid-cols-3 gap-10">
      {useCases.map((uc, i) => (
        <motion.div
          key={i}
          className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow flex flex-col items-center text-center"
          initial={{ opacity: 0, x: -30 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.1 * i }}
        >
          <div className="mb-4">{uc.icon}</div>
          <h3 className="text-2xl font-semibold mb-2 text-primary-700">{uc.title}</h3>
          <p className="text-lg text-darkgray">{uc.description}</p>
        </motion.div>
      ))}
    </div>
    </div>
  </section>
);

export default UseCases;
