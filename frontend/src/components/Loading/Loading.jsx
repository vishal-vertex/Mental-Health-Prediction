import './Loading.css';

export default function Loading({ text = 'Analyzing data...' }) {
  return (
    <div className="loading-container animate-fadeIn">
      <div className="loading-spinner"></div>
      <p className="loading-text gradient-text">{text}</p>
    </div>
  );
}
