import { useQuery } from "@tanstack/react-query";
import { useContext } from "react";
import { Navigate } from "react-router";
import { AuthContext } from "~/contexts/AuthContext";
import api from "~/lib/api";
import {
  SidebarProvider,
  SidebarInset,
  SidebarTrigger,
} from "~/components/ui/sidebar";
import { AppSidebar } from "~/components/app-sidebar";
import { Separator } from "~/components/ui/separator";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "~/components/ui/breadcrumb";
import { Spinner } from "~/components/ui/spinner";
import { Label } from "~/components/ui/label";
import { Input } from "~/components/ui/input";
import { Button } from "~/components/ui/button";

export default function AccountPage() {
  const { token, user, logout } = useContext(AuthContext);
  if (!token) {
    return (
      <Navigate to={user === "seller" ? "/seller/login" : "/partner/login"} />
    );
  }

  const { isLoading, isError, data } = useQuery({
    queryKey: ["account"],
    queryFn: async () => {
      const getUserProfile =
        user === "seller"
          ? api.sellers.getSellerProfile
          : api.partners.getDeliveryPartnerProfile;
      const { data } = await getUserProfile();
      return data;
    },
  });

  if (isError) {
    return (
      <div className="flex h-screen items-center justify-center">
        <h1 className="text-2xl font-bold">Error Loading Shipments</h1>
      </div>
    );
  }

  return (
    <SidebarProvider
      style={
        {
          "--sidebar-width": "19rem",
        } as React.CSSProperties
      }
    >
      <AppSidebar currentRoute="Account" />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator
            orientation="vertical"
            className="mr-2 data-vertical:h-4 data-vertical:self-auto"
          />
          <h2>Account</h2>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
          {isLoading || !data ? (
            <Spinner />
          ) : (
            <div className="flex flex-col gap-4 max-w-100">
              <Label htmlFor="name">Name</Label>
              <Input id="name" value={data?.name ?? "..."} readOnly />
              <Label htmlFor="email">Email</Label>
              <Input id="name" value={data?.email ?? "..."} readOnly />
              <Button className="w-min ml-auto" onClick={logout}>
                Log Out
              </Button>
            </div>
          )}
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
