import { NavLink } from 'react-router-dom';
import FeatureCard from '../../components/FeatureCard/FeatureCard';

export default function Home() {
  return (
    <main className="page-home animate-fadeIn">
      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <div className="hero__content">
            <h1 className="section-title">
              Predictive Mental Health <span className="gradient-text">Insights</span>
            </h1>
            <p className="hero__subtitle section-subtitle">
              Leverage advanced machine learning to assess your current mental well-being across 15 crucial lifestyle and emotional metrics. Confidential, fast, and personalized.
            </p>
            <div className="hero__actions flex">
              <NavLink to="/predict" className="btn btn-primary btn-lg">
                Start Assessment
              </NavLink>
              <NavLink to="/about" className="btn btn-secondary btn-lg">
                How It Works
              </NavLink>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="section bg-secondary">
        <div className="container">
          <h2 className="section-title" style={{ textAlign: 'center', marginBottom: 'var(--space-3xl)' }}>
            Why Choose <span className="gradient-text">MindAI?</span>
          </h2>
          <div className="grid-3">
            <FeatureCard
              icon="⚡"
              title="Instant Analysis"
              description="Our Random Forest models analyze your input instantly to provide immediate, actionable insights into your mental health state."
            />
            <FeatureCard
              icon="🔒"
              title="Private & Secure"
              description="Your data is processed confidentially. We don't store your personal assessment data on our servers."
            />
            <FeatureCard
              icon="✨"
              title="AI Wellness Companion"
              description="Receive highly personalized, empathetic wellness recommendations powered by Google's Gemini AI."
            />
          </div>
        </div>
      </section>
    </main>
  );
}
