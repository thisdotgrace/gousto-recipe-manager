import React, { useState } from "react";
import useRecipes from "../hooks/useRecipes";
import RecipeGrid from "../components/recipe-grid";
import RecipesPagination from "../components/recipes-pagination";
import { RecipeSearch } from "../components/recipe-search";
import { useDebounce } from "../hooks/useDebounce";

export default function RecipesPage() {
  const LIMIT = 12;

  const [search, setSearch] = useState("");
  const debouncedSearch = useDebounce(search, 500);

  const {
    recipes,
    loading,
    error,
    currentPage,
    setCurrentPage,
    totalPages,
  } = useRecipes(1, LIMIT, debouncedSearch);


  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight dark:text-slate-50">Recipes</h1>
        <p className="text-muted-foreground dark:text-slate-400 mt-2">
          Browse our collection of delicious meals.
        </p>
        <RecipeSearch
          search={search}
          onSearch={(value) => {
            setCurrentPage(1);
            setSearch(value)
          }}
        />
      </div>

      {error && (
        <div className="p-4 mb-8 text-destructive-foreground dark:text-red-400 bg-destructive dark:bg-red-950 rounded-md">
          {error}
        </div>
      )}

      {/* Grid */}
      <RecipeGrid recipes={recipes} loading={loading} limit={LIMIT} />

      {/* Pagination */}
      {!loading && (
        <RecipesPagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={(page) => setCurrentPage(page)}
        />
      )}
    </div>
  );
}
