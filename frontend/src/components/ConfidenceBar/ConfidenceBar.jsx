import { useEffect, useState } from 'react';
import './ConfidenceBar.css';

export default function ConfidenceBar({ confidence }) {
  const [width, setWidth] = useState(0);

  useEffect(() => {
    // Small delay to trigger the CSS animation
    const timer = setTimeout(() => setWidth(confidence), 100);
    return () => clearTimeout(timer);
  }, [confidence]);

  // Determine color based on threshold
  let colorClass = 'confidence-bar__fill--high';
  if (confidence < 70) colorClass = 'confidence-bar__fill--medium';
  if (confidence < 40) colorClass = 'confidence-bar__fill--low';

  return (
    <div className="confidence-wrapper">
      <div className="confidence-header">
        <span className="confidence-label">Prediction Confidence</span>
        <span className="confidence-value">{confidence}%</span>
      </div>
      <div className="confidence-track">
        <div
          className={`confidence-bar__fill ${colorClass}`}
          style={{ width: `${width}%` }}
        />
      </div>
      <p className="confidence-info">
        Our AI model is {confidence}% confident in this assessment based on the provided inputs.
      </p>
    </div>
  );
}
