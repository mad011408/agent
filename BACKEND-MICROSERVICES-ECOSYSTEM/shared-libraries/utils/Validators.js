/**
 * ✅ Validators
 * Data validation utilities
 */

/**
 * Email validation
 */
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

/**
 * Password strength validation
 */
export const isStrongPassword = (password) => {
  // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/;
  return passwordRegex.test(password);
};

/**
 * Username validation
 */
export const isValidUsername = (username) => {
  // 3-20 characters, alphanumeric and underscore only
  const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
  return usernameRegex.test(username);
};

/**
 * URL validation
 */
export const isValidUrl = (url) => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

/**
 * UUID validation
 */
export const isValidUUID = (uuid) => {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  return uuidRegex.test(uuid);
};

/**
 * Phone number validation (basic)
 */
export const isValidPhone = (phone) => {
  const phoneRegex = /^\+?[\d\s\-()]+$/;
  return phoneRegex.test(phone) && phone.replace(/\D/g, '').length >= 10;
};

/**
 * JSON validation
 */
export const isValidJSON = (str) => {
  try {
    JSON.parse(str);
    return true;
  } catch {
    return false;
  }
};

/**
 * Date validation
 */
export const isValidDate = (dateString) => {
  const date = new Date(dateString);
  return date instanceof Date && !isNaN(date);
};

/**
 * Number range validation
 */
export const isInRange = (value, min, max) => {
  const num = Number(value);
  return !isNaN(num) && num >= min && num <= max;
};

/**
 * Array validation
 */
export const isNonEmptyArray = (arr) => {
  return Array.isArray(arr) && arr.length > 0;
};

/**
 * Object validation
 */
export const isNonEmptyObject = (obj) => {
  return obj && typeof obj === 'object' && Object.keys(obj).length > 0;
};

/**
 * Sanitize string (remove HTML tags)
 */
export const sanitizeString = (str) => {
  return str.replace(/<[^>]*>/g, '');
};

/**
 * Validate required fields
 */
export const validateRequired = (obj, requiredFields) => {
  const missing = [];
  
  for (const field of requiredFields) {
    if (!obj[field]) {
      missing.push(field);
    }
  }
  
  return {
    isValid: missing.length === 0,
    missing
  };
};

export default {
  isValidEmail,
  isStrongPassword,
  isValidUsername,
  isValidUrl,
  isValidUUID,
  isValidPhone,
  isValidJSON,
  isValidDate,
  isInRange,
  isNonEmptyArray,
  isNonEmptyObject,
  sanitizeString,
  validateRequired
};