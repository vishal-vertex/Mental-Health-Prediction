import './StatisticsCard.css';

export default function StatisticsCard({ title, metrics }) {
  return (
    <div className="stat-card glass-card">
      <h3 className="stat-card__title">{title}</h3>
      <div className="stat-card__grid">
        <div className="stat-item">
          <span className="stat-item__label">Accuracy</span>
          <span className="stat-item__value gradient-text">{metrics.accuracy}%</span>
        </div>
        <div className="stat-item">
          <span className="stat-item__label">F1 Score</span>
          <span className="stat-item__value">{metrics.f1_score}%</span>
        </div>
        <div className="stat-item">
          <span className="stat-item__label">Precision</span>
          <span className="stat-item__value">{metrics.precision}%</span>
        </div>
        <div className="stat-item">
          <span className="stat-item__label">Recall</span>
          <span className="stat-item__value">{metrics.recall}%</span>
        </div>
      </div>
    </div>
  );
}
