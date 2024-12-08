import { motion } from 'framer-motion';
import { Bolt, Clock, PaintBucket } from 'lucide-react';

const features = [
  {
    title: 'Real-Time Trend Analysis',
    description: 'Detects the latest tech topics in seconds and provides you with insights before others discover them.',
    icon: <Bolt className="w-12 h-12 text-accent-500" />,
  },
  {
    title: 'Versatile Content Formats',
    description: 'From LinkedIn posts to blog articles, memes, and videos – all automatically generated.',
    icon: <PaintBucket className="w-12 h-12 text-accent-500" />,
  },
  {
    title: 'Save Time & Costs',
    description: 'Automated research, preparation, and formatting – drastically reduce your workload.',
    icon: <Clock className="w-12 h-12 text-accent-500" />,
  },
];

interface FeatureSectionProps {
  odd: boolean;
}

const Features: React.FC<FeatureSectionProps> = ({ odd }) => (
  <section className={`bg-gradient-to-b ${odd ? 'from-primary-100 to-white' : 'from-white to-primary-100'} text-center py-20 min-h-screen flex items-center`}>
    <div className="max-w-6xl mx-auto px-6 ">
    <motion.h2
      className="text-3xl md:text-4xl font-bold text-center mb-12 text-primary-600"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5 }}
    >
      Why Choose Our Agent?
    </motion.h2>
    <div className="grid md:grid-cols-3 gap-10">
      {features.map((feature, i) => (
        <motion.div
          key={i}
          className="p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow flex flex-col items-center text-center"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.2 * i }}
        >
          <div className="mb-4">{feature.icon}</div>
          <h3 className="text-2xl font-semibold mb-2 text-primary-700">{feature.title}</h3>
          <p className="text-lg text-darkgray">{feature.description}</p>
        </motion.div>
      ))}
    </div>
    </div>
  </section>
);

export default Features;
