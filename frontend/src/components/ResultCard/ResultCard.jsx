import './ResultCard.css';
import ConfidenceBar from '../ConfidenceBar/ConfidenceBar';

export default function ResultCard({ result }) {
  const { condition, severity, treatment, confidence, prediction_time } = result;

  const bgClass =
    condition === 'Normal' ? 'bg-gradient-normal' :
    condition === 'Anxiety' ? 'bg-gradient-anxiety' :
    condition === 'Depression' ? 'bg-gradient-depression' :
    'bg-gradient-burnout';

  return (
    <div className="result-card glass-card animate-fadeInScale">
      <div className={`result-card__banner ${bgClass}`}>
        <h2 className="result-card__condition">{condition}</h2>
        <span className={`badge badge-${severity.toLowerCase()}`}>
          {severity} Severity
        </span>
      </div>

      <div className="result-card__content">
        <div className="result-card__treatment">
          <span className="result-card__label">Recommended Approach</span>
          <p className="result-card__treatment-text">{treatment}</p>
        </div>

        <ConfidenceBar confidence={confidence} />

        <div className="result-card__meta">
          <span>Analyzed in {prediction_time}</span>
        </div>
      </div>
    </div>
  );
}
