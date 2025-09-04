// Use environment variable if available, otherwise fall back to development vs production logic
const API_URL = import.meta.env.VITE_API_URL || (
  import.meta.env.DEV 
    ? 'http://localhost:8080/api' 
    : '/api'
);

export default API_URL; 