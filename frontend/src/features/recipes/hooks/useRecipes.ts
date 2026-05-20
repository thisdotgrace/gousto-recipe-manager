import { useCallback, useEffect, useState } from "react";
import { getRecipes, searchRecipes } from "@/features/recipes/api/recipe";
import type { Recipe } from "@/features/recipes/types/recipe";

export default function useRecipes(
  initialPage = 1,
  limit = 12,
  search = ""
) {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [currentPage, setCurrentPage] = useState(initialPage);
  const [totalItems, setTotalItems] = useState(0);

  const fetchPage = useCallback(
    async (page: number) => {
      setLoading(true);
      setError(null);

      const offset = (page - 1) * limit;

      try {

        const data = search.trim()
          ? await searchRecipes(search, offset, limit)
          : await getRecipes(offset, limit);

        setRecipes(data.data);
        setTotalItems(data.total);

      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    },
    [limit, search]
  );

  useEffect(() => {
    void fetchPage(currentPage);
  }, [currentPage, fetchPage]);

  const totalPages = Math.max(1, Math.ceil(totalItems / limit));

  return {
    recipes,
    loading,
    error,
    currentPage,
    setCurrentPage,
    totalItems,
    totalPages,
  } as const;
}
