import './Footer.css';
import { NavLink } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer__container">
        <div className="footer__info">
          <NavLink to="/" className="footer__logo">
            <span className="footer__logo-icon">🧠</span>
            <span className="footer__logo-text">Mind<span className="gradient-text">AI</span></span>
          </NavLink>
          <p className="footer__desc">
            An advanced AI-powered system for preliminary mental health assessment and personalised wellness recommendations.
          </p>
        </div>
        <div className="footer__links">
          <h4 className="footer__heading">Quick Links</h4>
          <nav aria-label="Footer Navigation">
            <NavLink to="/">Home</NavLink>
            <NavLink to="/predict">Predict</NavLink>
            <NavLink to="/about">About System</NavLink>
          </nav>
        </div>
      </div>
      <div className="footer__bottom">
        
      </div>
    </footer>
  );
}
