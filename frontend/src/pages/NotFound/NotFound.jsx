import { NavLink } from 'react-router-dom';
import './NotFound.css';

export default function NotFound() {
  return (
    <main className="page-404 flex-center">
      <div className="text-center animate-fadeInScale">
        <h1 className="error-code gradient-text">404</h1>
        <h2 className="error-title">Page Not Found</h2>
        <p className="error-desc">
          The page you are looking for doesn't exist or has been moved.
        </p>
        <NavLink to="/" className="btn btn-primary mt-4">
          Return Home
        </NavLink>
      </div>
    </main>
  );
}
