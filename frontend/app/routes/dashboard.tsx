import { useQuery } from "@tanstack/react-query";
import { useContext } from "react";
import { Navigate } from "react-router";
import { AppSidebar } from "~/components/app-sidebar";
import ShipmentCard from "~/components/shipment-card";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "~/components/ui/breadcrumb";
import { Separator } from "~/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "~/components/ui/sidebar";
import { Spinner } from "~/components/ui/spinner";
import { AuthContext } from "~/contexts/AuthContext";
import api from "~/lib/api";
import { ShipmentStatus } from "~/lib/client";
import { getShipmentsCountWithStatus } from "~/lib/utils";

export default function DashboardPage() {
  const { token, user } = useContext(AuthContext);

  if (!token) {
    console.log("token is null");
    return (
      <Navigate
        to={user === "partner" ? "/partner/login" : "/seller/login"}
        replace
      />
    );
  }

  const { isLoading, isError, data } = useQuery({
    queryKey: ["shipments"],
    queryFn: async () => {
      const userApi = user === "seller" ? api.sellers : api.partners;
      const { data } = await userApi.getShipments();
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
      <AppSidebar currentRoute="Dashboard" />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center gap-2 px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator
            orientation="vertical"
            className="mr-2 data-vertical:h-4 data-vertical:self-auto"
          />
          <h2>Dashboard</h2>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
          {isLoading || !data ? (
            <Spinner />
          ) : (
            <>
              <div className="grid auto-rows-min gap-4 md:grid-cols-4">
                <NumberLabel value={data.length} label={"Total Shipments"} />
                <NumberLabel
                  value={getShipmentsCountWithStatus(
                    data,
                    ShipmentStatus.Placed,
                  )}
                  label={"Placed"}
                />
                <NumberLabel
                  value={getShipmentsCountWithStatus(
                    data,
                    ShipmentStatus.InTransit,
                  )}
                  label={"In Transit"}
                />
                <NumberLabel
                  value={getShipmentsCountWithStatus(
                    data,
                    ShipmentStatus.Delivered,
                  )}
                  label={"Delivered"}
                />
              </div>
              <div className="grid auto-rows-min gap-4 md:grid-cols-4">
                {data.map((shipment) => (
                  <ShipmentCard shipment={shipment}></ShipmentCard>
                ))}
              </div>
            </>
          )}
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}

function NumberLabel({ value, label }: { value: number; label: string }) {
  return (
    <div className="flex flex-col gap-2 rounded-xl border border-gray-200 p-4">
      <h1 className="text-4xl font-bold">{value}</h1>
      <p className="text-gray-500">{label}</p>
    </div>
  );
}
