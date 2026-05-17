import { Outlet } from "react-router-dom"

import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar"

import { AppSidebar } from "@/components/app/app-sidebar"
import React from "react"

export default function MainLayout() {
  return (
    <SidebarProvider>

      <AppSidebar />

      <SidebarInset>

        <header className="flex h-16 items-center border-b px-4">
          <SidebarTrigger />
        </header>

        <main className="flex-1 p-6">
          <Outlet />
        </main>

      </SidebarInset>

    </SidebarProvider>
  )
}
