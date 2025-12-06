import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: false, // No login yet
});

export default api;



// import axios from "axios";

// const isDevelopment = import.meta.env.MODE === "development";

// const baseURL = isDevelopment
//   ? import.meta.env.VITE_API_BASE_URL_LOCAL
//   : import.meta.env.VITE_API_BASE_URL_DEPLOY;


// const api = axios.create({
//   baseURL: "http://127.0.0.1:8000/api/",
//   withCredentials: false,  // No login yet
// });

// export default api;
