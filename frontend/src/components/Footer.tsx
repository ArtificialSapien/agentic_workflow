// src/components/Footer.tsx
import React from 'react';
import { Link } from 'react-router-dom';
import { Twitter, Facebook, Instagram, Linkedin } from 'lucide-react'; // Example: Use Lucide icons or another icon library

const Footer: React.FC = () => (
  <footer className="bg-primary-500 text-white py-6">
    <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between">
      {/* Copyright */}
      <p className="text-sm">
        &copy; {new Date().getFullYear()} Tech Trend AI Agent. All rights reserved.
      </p>

      {/* Links */}
      <div className="mt-4 md:mt-0">
        <Link to="/impressum" className="text-white hover:underline mx-2">
          Legal Notice
        </Link>
        |
        <Link to="/datenschutz" className="text-white hover:underline mx-2">
          Privacy Policy
        </Link>
        |
        <Link to="/kontakt" className="text-white hover:underline mx-2">
          Contact
        </Link>
      </div>

      {/* Social Media Icons (optional) */}
      <div className="mt-4 md:mt-0 flex space-x-4">
        <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" aria-label="Twitter">
          <Twitter className="w-5 h-5 text-white hover:text-accent-400 transition-colors" />
        </a>
        <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" aria-label="Facebook">
          <Facebook className="w-5 h-5 text-white hover:text-accent-400 transition-colors" />
        </a>
        <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
          <Instagram className="w-5 h-5 text-white hover:text-accent-400 transition-colors" />
        </a>
        <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
          <Linkedin className="w-5 h-5 text-white hover:text-accent-400 transition-colors" />
        </a>
      </div>
    </div>
  </footer>
);

export default Footer;
