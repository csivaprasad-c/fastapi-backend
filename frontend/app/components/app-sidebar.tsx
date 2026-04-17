import * as React from "react";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "~/components/ui/sidebar";
import { GalleryVerticalEndIcon } from "lucide-react";
import { AuthContext } from "~/contexts/AuthContext";

export function AppSidebar({
  currentRoute,
  ...props
}: { currentRoute: string } & React.ComponentProps<typeof Sidebar>) {
  const { user } = React.useContext(AuthContext);
  const menuItems = [
    { title: "Dashboard", url: "/dashboard" },
    { title: "Account", url: "/account" },
  ];

  return (
    <Sidebar variant="floating" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="#">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                  <GalleryVerticalEndIcon className="size-4" />
                </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-medium">FastShip</span>
                  <span className="">DMS</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarMenu className="gap-1">
            {menuItems.map((item) => (
              <SidebarMenuItem key={item.title}>
                <SidebarMenuButton asChild>
                  <a href={item.url}>{item.title}</a>
                </SidebarMenuButton>
                {/* {item.items?.length ? (
                  <SidebarMenuSub className="ml-0 border-l-0 px-1.5">
                    {item.items.map((item) => (
                      <SidebarMenuSubItem key={item.title}>
                        <SidebarMenuSubButton asChild isActive={item.isActive}>
                          <a href={item.url}>{item.title}</a>
                        </SidebarMenuSubButton>
                      </SidebarMenuSubItem>
                    ))}
                  </SidebarMenuSub>
                ) : null} */}
              </SidebarMenuItem>
            ))}
            {user === "seller" && (
              <SidebarMenuItem>
                <SidebarMenuButton
                  asChild
                  isActive={currentRoute === "Submit Shipment"}
                >
                  <a href="/seller/submit-shipment">Submit Shipment</a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            )}
            {user === "partner" && (
              <SidebarMenuItem>
                <SidebarMenuButton
                  asChild
                  isActive={currentRoute === "Update Shipment"}
                >
                  <a href="/partner/update-shipment">Update Shipment</a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            )}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
