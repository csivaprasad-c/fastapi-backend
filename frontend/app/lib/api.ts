import { Api } from "./client";

const api = new Api({
  baseUrl: "http://localhost:8000",
  securityWorker: (token) => {
    if (token) {
      return {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
    } else {
      return {};
    }
  },
});

export default api;
