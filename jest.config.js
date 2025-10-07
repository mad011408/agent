/**
 * Jest Configuration
 * Testing framework configuration
 */

export default {
  // Test environment
  testEnvironment: 'node',
  
  // Setup files
  setupFilesAfterEnv: ['<rootDir>/test-setup.js'],
  
  // Test match patterns
  testMatch: [
    '**/TESTING-SUITE/unit-tests/**/*.test.js',
    '**/TESTING-SUITE/integration-tests/**/*.test.js'
  ],
  
  // Coverage
  collectCoverageFrom: [
    'BACKEND-MICROSERVICES-ECOSYSTEM/**/*.js',
    'FRONTEND-ECOSYSTEM/**/*.{js,jsx}',
    '!**/node_modules/**',
    '!**/dist/**',
    '!**/coverage/**'
  ],
  
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    }
  },
  
  // Module paths
  moduleDirectories: ['node_modules', '<rootDir>'],
  
  // Transform
  transform: {
    '^.+\\.jsx?$': 'babel-jest'
  },
  
  // Ignore patterns
  testPathIgnorePatterns: [
    '/node_modules/',
    '/dist/',
    '/build/'
  ],
  
  // Verbose output
  verbose: true,
  
  // Timeout
  testTimeout: 10000
};