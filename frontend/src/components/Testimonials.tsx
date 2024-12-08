import { motion } from 'framer-motion';
import { User } from 'lucide-react';

const testimonials = [
  {
    quote: '“Real-time detection of new tech trends has revolutionized our marketing.”',
    name: 'CTO of a Tech Startup',
    avatar: '/avatars/cto-techstartup.jpg', // Optional: Path to avatar image
  },
  {
    quote: '“The versatile formats save us significant time and boost our creativity.”',
    name: 'Content Lead of an IT Blog',
    avatar: '/avatars/content-lead-itblog.jpg', // Optional: Path to avatar image
  },
];


interface TestimonialsSectionProps {
  odd: boolean;
}

const Testimonials: React.FC<TestimonialsSectionProps> = ({ odd }) => (
  <section className={`bg-gradient-to-b ${odd ? 'from-primary-100 to-white' : 'from-white to-primary-100'} text-center py-20 min-h-screen flex items-center`}>
    <div className="max-w-6xl mx-auto px-6 py-16 ">
      <motion.h2
        className="text-3xl md:text-4xl font-bold text-center mb-12 text-primary-600"
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
      >
        What Our Customers Say
      </motion.h2>
      <div className="grid md:grid-cols-2 gap-10">
        {testimonials.map((testi, i) => (
          <motion.div
            key={i}
            className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow flex flex-col items-center text-center"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.2 * i }}
          >
            {/* Optional: Avatar */}
            {/* 
          <img
            src={testi.avatar}
            alt={`${testi.name} Avatar`}
            className="w-16 h-16 rounded-full mb-4 object-cover"
          />
          */}
            <p className="text-lg italic mb-4 text-gray-700">"{testi.quote}"</p>
            <div className="flex items-center space-x-2">
              <User className="w-6 h-6 text-accent-500" />
              <p className="font-semibold text-primary-700">{testi.name}</p>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default Testimonials;
