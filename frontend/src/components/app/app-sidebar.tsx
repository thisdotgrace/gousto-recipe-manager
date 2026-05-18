import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

import { Home, BookOpen, Settings } from "lucide-react"
import React from "react"
import { Link } from "react-router-dom"

const items = [
  {
    title: "Home",
    url: "/",
    icon: Home,
  },
  {
    title: "Recipes",
    url: "/recipes",
    icon: BookOpen,
  },
  {
    title: "Settings",
    url: "/settings",
    icon: Settings,
  },
]

export function AppSidebar() {
  return (
    <Sidebar collapsible="icon" className="dark:bg-slate-900 dark:border-slate-700">
      <SidebarContent className="dark:bg-slate-900">
        <SidebarGroup className="dark:border-slate-700">
          <SidebarGroupLabel className="dark:text-slate-400">Gousto Manager</SidebarGroupLabel>

          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild className="dark:hover:bg-slate-800 dark:text-slate-300">
                    <Link to={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>

        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
