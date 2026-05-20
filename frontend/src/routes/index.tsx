import {
  createBrowserRouter,
} from "react-router-dom"

import MainLayout from "@/layouts/main-layout"

import HomePage from "@/pages/home"
import RecipesPage from "@/features/recipes/pages/recipes"
import React from "react"

export const router = createBrowserRouter([
  {
    path: "/",
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: "recipes",
        element: <RecipesPage />,
      },
    ],
  },
])
