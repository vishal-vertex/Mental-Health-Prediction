import './InputCard.css';

export default function InputCard({ title, icon, children }) {
  return (
    <div className="input-card glass-card">
      <div className="input-card__header">
        <span className="input-card__icon">{icon}</span>
        <h3 className="input-card__title">{title}</h3>
      </div>
      <div className="input-card__body">
        {children}
      </div>
    </div>
  );
}
