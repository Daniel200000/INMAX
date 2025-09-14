import React from 'react';
import './Footer.css';

const Footer: React.FC = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h4>INMAX AVISADORES</h4>
          <p>Sistema de gestión de campañas publicitarias</p>
        </div>
        
        <div className="footer-section">
          <h4>Enlaces Rápidos</h4>
          <ul>
            <li><a href="/">Dashboard</a></li>
            <li><a href="/campaigns">Campañas</a></li>
            <li><a href="/campaigns/create">Crear Campaña</a></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h4>Síguenos</h4>
          <div className="social-links">
            <a href="https://facebook.com/inmaxavisadores" target="_blank" rel="noopener noreferrer" className="social-link">
              <i className="fab fa-facebook"></i>
              Facebook
            </a>
            <a href="https://twitter.com/inmaxavisadores" target="_blank" rel="noopener noreferrer" className="social-link">
              <i className="fab fa-twitter"></i>
              Twitter
            </a>
            <a href="https://instagram.com/inmaxavisadores" target="_blank" rel="noopener noreferrer" className="social-link">
              <i className="fab fa-instagram"></i>
              Instagram
            </a>
            <a href="https://linkedin.com/company/inmaxavisadores" target="_blank" rel="noopener noreferrer" className="social-link">
              <i className="fab fa-linkedin"></i>
              LinkedIn
            </a>
          </div>
        </div>
        
        <div className="footer-section">
          <h4>Contacto</h4>
          <p>Email: info@inmaxavisadores.com</p>
          <p>Teléfono: +1 (555) 123-4567</p>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; 2024 INMAX AVISADORES. Todos los derechos reservados.</p>
      </div>
    </footer>
  );
};

export default Footer;
