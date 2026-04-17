import { createContext, useEffect, useState } from "react";
import { flushSync } from "react-dom";
import { toast } from "sonner";
import api from "~/lib/api";

type UserType = "seller" | "partner";

interface AuthContextType {
  token: string | null | undefined;
  user?: UserType;
  login: (
    userType: UserType,
    email: string,
    password: string,
  ) => Promise<boolean>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  token: null,
  login: async () => false,
  logout: () => {},
});

function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>();
  const [user, setUser] = useState<UserType>();
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      console.log("token from storage");

      setToken(token);
      setUser(localStorage.getItem("user") as UserType);

      api.setSecurityData(token);
    } else {
      setToken(null);
    }
  }, []);

  const login = async (
    userType: UserType,
    email: string,
    password: string,
  ): Promise<boolean> => {
    try {
      const loginUser =
        userType === "seller"
          ? api.sellers.loginSeller
          : api.partners.loginDeliveryPartner;

      const { data } = await loginUser({
        username: email,
        password,
      });

      if (data?.access_token) {
        flushSync(() => {
          setToken(data.access_token);
          setUser(userType);
        });
        api.setSecurityData(data.access_token);
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("user", userType);
        return true;
      }
      return false;
    } catch (error) {
      console.error("Login failed:", error);
      toast.error("Login failed. Please check your credentials and try again.");
      return false;
    }
  };

  const logout = async () => {
    await api.sellers.logoutSeller();
    setToken(null);
    setUser(undefined);
    api.setSecurityData(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  };

  return (
    <AuthContext.Provider value={{ token, user, login, logout }}>
      {token === undefined ? <div>Loading...</div> : children}
    </AuthContext.Provider>
  );
}

export { AuthContext, AuthProvider, type AuthContextType, type UserType };
