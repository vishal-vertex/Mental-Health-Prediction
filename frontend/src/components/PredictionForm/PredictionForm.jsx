import './PredictionForm.css';
import InputCard from '../InputCard/InputCard';
import { VALID_GENDERS, VALID_OCCUPATIONS } from '../../utils/validators';

export default function PredictionForm({ formData, updateField, errors, onSubmit, loading }) {
  const handleChange = (e) => {
    updateField(e.target.name, e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit();
  };

  const renderField = (name, label, type, options, placeholder, min, max, step) => {
    const isError = !!errors[name];

    return (
      <div className="form-group" key={name}>
        <label className="form-label" htmlFor={name}>{label}</label>
        {options ? (
          <select
            id={name}
            name={name}
            className={`form-select ${isError ? 'error' : ''}`}
            value={formData[name]}
            onChange={handleChange}
            disabled={loading}
          >
            <option value="">{placeholder || 'Select an option'}</option>
            {options.map((opt) => (
              <option key={opt} value={opt}>{opt}</option>
            ))}
          </select>
        ) : (
          <input
            id={name}
            name={name}
            type={type}
            className={`form-input ${isError ? 'error' : ''}`}
            value={formData[name]}
            onChange={handleChange}
            placeholder={placeholder}
            min={min}
            max={max}
            step={step}
            disabled={loading}
          />
        )}
        {isError && <span className="form-error">⚠ {errors[name]}</span>}
      </div>
    );
  };

  return (
    <form className="prediction-form" onSubmit={handleSubmit} noValidate>
      <div className="grid-3">
        {/* Personal Details */}
        <InputCard title="Personal Profile" icon="👤">
          {renderField('age', 'Age', 'number', null, 'e.g., 25', 1, 120, 1)}
          {renderField('gender', 'Gender', 'select', VALID_GENDERS, 'Select gender')}
          {renderField('occupation', 'Occupation', 'select', VALID_OCCUPATIONS, 'Select occupation')}
        </InputCard>

        {/* Lifestyle & Habits */}
        <InputCard title="Lifestyle & Habits" icon="🌙">
          {renderField('sleep_hours', 'Sleep (hours/night)', 'number', null, 'e.g., 7.5', 0, 24, 0.1)}
          {renderField('sleep_quality', 'Sleep Quality (1-10)', 'number', null, '1=Poor, 10=Excellent', 1, 10, 0.1)}
          {renderField('social_media_hours', 'Social Media (hrs/day)', 'number', null, 'e.g., 3', 0, 24, 0.1)}
          {renderField('physical_activity_days', 'Exercise (days/week)', 'number', null, '0-7', 0, 7, 1)}
        </InputCard>

        {/* Academic / Work */}
        <InputCard title="Work & Academic" icon="💼">
          {renderField('academic_work_pressure', 'Work Pressure (1-10)', 'number', null, '1=Low, 10=High', 1, 10, 0.1)}
          {renderField('work_life_balance', 'Work-Life Balance (1-10)', 'number', null, '1=Poor, 10=Excellent', 1, 10, 0.1)}
          {renderField('concentration_level', 'Concentration (1-10)', 'number', null, '1=Poor, 10=Excellent', 1, 10, 0.1)}
        </InputCard>
      </div>

      <div className="grid-2" style={{ marginTop: 'var(--space-lg)' }}>
        {/* Mental Health Indicators */}
        <InputCard title="Mental Well-being" icon="🧠">
          {renderField('stress_level', 'Stress Level (1-10)', 'number', null, '1=Low, 10=High', 1, 10, 0.1)}
          {renderField('anxiety_score', 'Anxiety Score (1-10)', 'number', null, '1=Low, 10=High', 1, 10, 0.1)}
          {renderField('depression_score', 'Depression Score (1-10)', 'number', null, '1=Low, 10=High', 1, 10, 0.1)}
        </InputCard>

        {/* Social & Emotional */}
        <InputCard title="Social & Emotional" icon="❤️">
          {renderField('mood_score', 'Overall Mood (1-10)', 'number', null, '1=Poor, 10=Excellent', 1, 10, 0.1)}
          {renderField('social_support', 'Social Support (1-10)', 'number', null, '1=None, 10=Strong', 1, 10, 0.1)}
        </InputCard>
      </div>

      <div className="form-actions flex-center" style={{ marginTop: 'var(--space-2xl)' }}>
        <button
          type="submit"
          className="btn btn-primary btn-lg"
          disabled={loading}
          style={{ width: '100%', maxWidth: '400px' }}
        >
          {loading ? 'Analyzing Profile...' : 'Generate Assessment'}
        </button>
      </div>
    </form>
  );
}
