import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

interface CallToActionSectionProps {
  odd: boolean;
}

const CallToAction: React.FC<CallToActionSectionProps> = ({ odd }) => (
  <section
    className={`bg-gradient-to-b ${
      odd ? 'from-primary-100 to-white' : 'from-white to-primary-100'
    } text-center min-h-screen flex flex-col justify-center items-center py-10`}
  >
    <div className="max-w-6xl mx-auto px-6 text-center">
      <motion.h2
        className="text-4xl md:text-6xl font-bold mb-4 text-transparent bg-gradient-rainbow bg-clip-text animate-gradient-x"
        initial={{ opacity: 0, scale: 0.8 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true }}
        transition={{ duration: 0.5 }}
      >
        Ready to shape the future?
      </motion.h2>
      <p className="text-xl md:text-2xl lg:text-3xl mb-8">
        Start your free demo now and discover the potential.
      </p>
      <Link
        to="/demo"
        className="inline-block bg-limegreen text-darkgray px-8 py-4 rounded-md text-lg font-bold hover:bg-lightblue hover:text-white transition-all"
      >
        Try for Free
      </Link>
    </div>
  </section>
);

export default CallToAction;
