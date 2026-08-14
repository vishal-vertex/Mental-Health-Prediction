import './RecommendationCard.css';

export default function RecommendationCard({ recommendations, aiSuggestion }) {
  return (
    <div className="recommendation-card glass-card animate-fadeInScale" style={{ animationDelay: '0.1s' }}>
      <div className="rec-section">
        <h3 className="rec-section__title">
          <span className="icon">✓</span> Wellness Recommendations
        </h3>
        <ul className="rec-list">
          {recommendations.map((rec, idx) => (
            <li key={idx} className="rec-list__item animate-slideInLeft" style={{ animationDelay: `${0.2 + idx * 0.1}s` }}>
              <span className="rec-list__bullet">{idx + 1}</span>
              <p>{rec}</p>
            </li>
          ))}
        </ul>
      </div>

      <div className="divider"></div>

      <div className="rec-section">
        <h3 className="rec-section__title">
          <span className="icon">✨</span> AI Personalized Suggestion
        </h3>
        <div className="ai-suggestion-box">
          <p className="ai-suggestion-text">{aiSuggestion}</p>
        </div>
      </div>
    </div>
  );
}
