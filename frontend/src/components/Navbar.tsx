import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Menu, X, Brain } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navLinks = [
    { path: '/', label: 'Home' },
    { path: '/features', label: 'Features' },
    { path: '/team', label: 'Team' },
  ];

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleNavigateAndScroll = () => {
    navigate('/'); // Navigate to the homepage
    setTimeout(() => {
      const section = document.getElementById('content-generator-section');
      if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
      }
    }, 0); // Timeout to ensure the page is fully loaded
  };

  return (
    <>
      {/* Mobile Menu Overlay */}
      <div
        className={`fixed inset-0 bg-black/50 backdrop-blur-sm z-40 md:hidden ${
          isMobileMenuOpen ? 'block' : 'hidden'
        }`}
        onClick={() => setIsMobileMenuOpen(false)}
        aria-hidden={!isMobileMenuOpen}
      />

      {/* Main Navbar */}
      <nav
        className={`fixed top-0 w-full z-50 px-4 transition-all duration-300 ${
          isScrolled ? 'bg-white shadow-accent-light py-3' : 'bg-white shadow-accent-dark py-6'
        }`}
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between relative">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-rainbow rounded-xl flex items-center justify-center">
              <Brain className="w-6 h-6 text-white" aria-hidden="true" />
            </div>
            <span
              className={`font-bold text-3xl inline-block ${
                isScrolled
                  ? 'text-transparent bg-gradient-rainbow bg-clip-text animate-gradient-x'
                  : 'text-primary-600'
              }`}
            >
              Artificial Sapien
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`text-gray-700 hover:text-primary-600 transition-colors ${
                  location.pathname === link.path ? 'text-primary-600 font-medium' : ''
                }`}
              >
                {link.label}
              </Link>
            ))}
            <button
              onClick={handleNavigateAndScroll}
              className="bg-accent-500 text-white px-6 py-2 rounded-xl hover:bg-accent-600 transition-colors shadow-accent-glow focus:outline-none focus:ring-2 focus:ring-accent-400"
              aria-label="Navigate to Content Generator"
            >
              Content Generator
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden focus:outline-none focus:ring-2 focus:ring-accent-400 rounded"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            aria-label={isMobileMenuOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={isMobileMenuOpen}
          >
            {isMobileMenuOpen ? (
              <X className="w-6 h-6 text-primary-600" aria-hidden="true" />
            ) : (
              <Menu className="w-6 h-6 text-primary-600" aria-hidden="true" />
            )}
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div
        className={`fixed top-20 right-4 left-4 bg-white rounded-2xl shadow-accent-glow z-50 md:hidden transform transition-transform duration-200 ${
          isMobileMenuOpen ? 'translate-y-0' : '-translate-y-full'
        }`}
      >
        <div className="p-6 space-y-4">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={`block px-4 py-2 rounded-lg hover:bg-primary-50 transition-colors ${
                location.pathname === link.path ? 'text-primary-600 bg-primary-50' : 'text-gray-700'
              }`}
              onClick={() => setIsMobileMenuOpen(false)}
            >
              {link.label}
            </Link>
          ))}
          <button
            onClick={handleNavigateAndScroll}
            className="w-full bg-accent-500 text-white px-6 py-2 rounded-xl hover:bg-accent-600 transition-colors shadow-accent-glow focus:outline-none focus:ring-2 focus:ring-accent-400"
            aria-label="Navigate to Content Generator"
          >
            Content Generator
          </button>
        </div>
      </div>
    </>
  );
};

export default Navbar;
