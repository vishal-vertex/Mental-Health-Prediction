import './FeatureCard.css';

export default function FeatureCard({ icon, title, description }) {
  return (
    <div className="feature-card glass-card">
      <div className="feature-card__icon">{icon}</div>
      <h3 className="feature-card__title">{title}</h3>
      <p className="feature-card__desc">{description}</p>
    </div>
  );
}
