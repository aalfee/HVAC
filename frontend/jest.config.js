module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx'],
  testMatch: ['**/__tests__/**/*.(test|spec).(ts|tsx|js)'],
  setupFilesAfterEnv: ['@testing-library/jest-dom'],
};
