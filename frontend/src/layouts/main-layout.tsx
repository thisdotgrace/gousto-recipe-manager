import { Outlet } from "react-router-dom"

import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"

import { AppSidebar } from "@/components/app/app-sidebar"
import { ThemeToggle } from "@/components/app/theme-toggle"
import React from "react"

export default function MainLayout() {
  return (
    <SidebarProvider>

      <AppSidebar />

      <SidebarInset className="dark:bg-slate-950">

        <header className="flex h-16 items-center justify-between border-b px-4 dark:border-slate-700 dark:bg-slate-900">
          <SidebarTrigger />
          <ThemeToggle />
        </header>

        <main className="flex-1 p-6 dark:bg-slate-950 min-h-screen">
          <Outlet />
        </main>

      </SidebarInset>

    </SidebarProvider>
  )
}
