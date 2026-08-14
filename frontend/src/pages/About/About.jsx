import { useEffect, useState } from 'react';
import StatisticsCard from '../../components/StatisticsCard/StatisticsCard';
import { getModelInfo } from '../../services/api';
import './About.css';

export default function About() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    async function fetchMetrics() {
      try {
        const data = await getModelInfo();
        setMetrics(data);
      } catch (err) {
        console.error('Failed to load metrics:', err);
      }
    }
    fetchMetrics();
  }, []);

  return (
    <main className="page-about animate-fadeIn">
      <div className="container">
        <header className="page-header text-center">
          <span className="section-label">Our Technology</span>
          <h1 className="section-title">Behind the Intelligence</h1>
          <p className="section-subtitle mx-auto">
            MindAI utilizes three independent Random Forest models trained on diverse clinical datasets to ensure highly accurate, unbiased predictions.
          </p>
        </header>

        <section className="about-content">
          <div className="about-text glass-card">
            <h2 className="gradient-text">How It Works</h2>
            <p>
              When you submit your assessment, our system processes 15 distinct data points spanning your lifestyle choices, academic/work pressures, and emotional states. The data is securely passed to three separate Machine Learning pipelines:
            </p>
            <ul>
              <li><strong>Model 1:</strong> Identifies potential mental health conditions (Anxiety, Depression, Burnout, or Normal).</li>
              <li><strong>Model 2:</strong> Evaluates the severity level (Mild, Moderate, Severe).</li>
              <li><strong>Model 3:</strong> Determines the most effective recommended treatment pathway.</li>
            </ul>
            <p>
              Finally, we integrate with Google's Gemini AI to synthesize these outputs into an empathetic, highly personalized wellness plan.
            </p>
          </div>
        </section>

        {metrics && (
          <section className="about-metrics">
            <h2 className="section-title text-center" style={{ marginBottom: 'var(--space-2xl)' }}>
              Model <span className="gradient-text">Performance</span>
            </h2>
            <div className="grid-3">
              <StatisticsCard title="Condition Prediction" metrics={metrics.condition} />
              <StatisticsCard title="Severity Evaluation" metrics={metrics.severity} />
              <StatisticsCard title="Treatment Suggestion" metrics={metrics.treatment} />
            </div>
          </section>
        )}
      </div>
    </main>
  );
}
