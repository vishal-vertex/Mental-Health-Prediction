/**
 * Field-level validation rules for the prediction form.
 */

export const VALID_GENDERS = ['Female', 'Male', 'Non-binary'];
export const VALID_OCCUPATIONS = [
  'Student',
  'Working Professional',
  'Both (Part-time work + Study)',
];

const required = (value) => {
  if (value === '' || value === null || value === undefined) {
    return 'This field is required.';
  }
  return null;
};

const inRange = (value, min, max, label = 'Value') => {
  const num = parseFloat(value);
  if (isNaN(num)) return `${label} must be a number.`;
  if (num < min || num > max) return `${label} must be between ${min} and ${max}.`;
  return null;
};

const FIELD_VALIDATORS = {
  age: (v) => required(v) || inRange(v, 1, 120, 'Age'),
  gender: (v) => {
    if (!VALID_GENDERS.includes(v)) return 'Please select a valid gender.';
    return null;
  },
  occupation: (v) => {
    if (!VALID_OCCUPATIONS.includes(v)) return 'Please select a valid occupation.';
    return null;
  },
  sleep_hours:              (v) => required(v) || inRange(v, 0, 24,  'Sleep hours'),
  sleep_quality:            (v) => required(v) || inRange(v, 1, 10,  'Sleep quality'),
  social_media_hours:       (v) => required(v) || inRange(v, 0, 24,  'Social media hours'),
  academic_work_pressure:   (v) => required(v) || inRange(v, 0, 10,  'Academic/work pressure'),
  physical_activity_days:   (v) => required(v) || inRange(v, 0, 7,   'Physical activity days'),
  stress_level:             (v) => required(v) || inRange(v, 0, 10,  'Stress level'),
  anxiety_score:            (v) => required(v) || inRange(v, 0, 10,  'Anxiety score'),
  depression_score:         (v) => required(v) || inRange(v, 0, 10,  'Depression score'),
  work_life_balance:        (v) => required(v) || inRange(v, 0, 10,  'Work-life balance'),
  mood_score:               (v) => required(v) || inRange(v, 0, 10,  'Mood score'),
  concentration_level:      (v) => required(v) || inRange(v, 0, 10,  'Concentration level'),
  social_support:           (v) => required(v) || inRange(v, 0, 10,  'Social support'),
};

/**
 * Validate a single field.
 * @param {string} fieldName
 * @param {*} value
 * @returns {string|null} error message or null
 */
export const validateField = (fieldName, value) => {
  const validator = FIELD_VALIDATORS[fieldName];
  if (!validator) return null;
  return validator(value);
};

/**
 * Validate the entire form object.
 * @param {Object} formData
 * @returns {{ isValid: boolean, errors: Object }}
 */
export const validateForm = (formData) => {
  const errors = {};
  let isValid = true;

  Object.keys(FIELD_VALIDATORS).forEach((field) => {
    const error = FIELD_VALIDATORS[field](formData[field]);
    if (error) {
      errors[field] = error;
      isValid = false;
    }
  });

  return { isValid, errors };
};
