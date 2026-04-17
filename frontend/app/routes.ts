import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/home.tsx"),
  route("/seller/login", "routes/seller/login.tsx"),
  route("/seller/forgot-password", "routes/seller/forgot-password.tsx"),
  route("/seller/submit-shipment", "routes/seller/submit-shipment.tsx"),
  route("/partner/login", "routes/partner/login.tsx"),
  route("/partner/forgot-password", "routes/partner/forgot-password.tsx"),
  route("/dashboard", "routes/dashboard.tsx"),
  route("/account", "routes/account.tsx"),
] satisfies RouteConfig;
