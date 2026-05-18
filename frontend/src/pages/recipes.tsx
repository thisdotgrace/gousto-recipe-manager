import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getRecipes } from "@/api/recipe";
import type { Recipe } from "@/types/recipe";
import {
  Card,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { Star, Clock, Flame } from "lucide-react";

function titleCase(value?: string) {
  if (!value) return "";

  return value
    .replace(/[-_]+/g, " ")
    .split(" ")
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export default function RecipesPage() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Pagination state
  const [currentPage, setCurrentPage] = useState(1);
  const [totalItems, setTotalItems] = useState(0);

  const LIMIT = 12;

  useEffect(() => {
    const fetchRecipes = async () => {
      setLoading(true);
      setError(null);

      const offset = (currentPage - 1) * LIMIT;

      try {
        const data = await getRecipes(offset, LIMIT);
        setRecipes(data.data);
        setTotalItems(data.total);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchRecipes();
  }, [currentPage]);

  const totalPages = Math.ceil(totalItems / LIMIT);

  return (
    <div className="container mx-auto py-8 px-4">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight dark:text-slate-50">Recipes</h1>
        <p className="text-muted-foreground dark:text-slate-400 mt-2">
          Browse our collection of delicious meals.
        </p>
      </div>

      {error && (
        <div className="p-4 mb-8 text-destructive-foreground dark:text-red-400 bg-destructive dark:bg-red-950 rounded-md">
          {error}
        </div>
      )}

      {/* Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
        {loading
          ? Array.from({ length: LIMIT }).map((_, i) => (
              <Card key={i} className="flex flex-col overflow-hidden dark:bg-slate-900 dark:border-slate-700">
                <Skeleton className="h-48 w-full rounded-none dark:bg-slate-800" />
                <CardHeader>
                  <Skeleton className="h-6 w-3/4 mb-2 dark:bg-slate-800" />
                  <Skeleton className="h-4 w-1/2 dark:bg-slate-800" />
                </CardHeader>
              </Card>
            ))
          : recipes.map((recipe) => (
              <Link to={`https://www.gousto.co.uk/cookbook/recipes/${recipe.slug}`} key={recipe.id} className="group">
                <Card className="flex flex-col h-full overflow-hidden transition-all hover:shadow-md dark:bg-slate-900 dark:border-slate-700 relative">
                  <div className="aspect-[4/3] overflow-hidden bg-muted dark:bg-slate-800 relative">
                    <div className="absolute top-2 left-2 z-10 flex gap-2 flex-wrap">
                      {recipe.calories && (
                        <Badge variant="secondary" className="flex items-center gap-1 bg-background/80 dark:bg-slate-900/80 dark:text-slate-50 backdrop-blur-sm border-0 font-medium">
                          <Flame className="w-3 h-3 text-orange-500" />
                          {recipe.calories} kcal
                        </Badge>
                      )}
                      {recipe.prep_time && (
                        <Badge variant="secondary" className="flex items-center gap-1 bg-background/80 dark:bg-slate-900/80 dark:text-slate-50 backdrop-blur-sm border-0 font-medium">
                          <Clock className="w-3 h-3 text-blue-500" />
                          {recipe.prep_time} mins
                        </Badge>
                      )}
                    </div>
                    <div className="absolute bottom-2 left-2 z-10">
                      <Badge variant="secondary" className="bg-background/80 dark:bg-slate-900/80 dark:text-slate-50 backdrop-blur-sm border-0 font-medium capitalize">
                        {titleCase(recipe.cuisine) || "Mixed"}
                      </Badge>
                    </div>
                    {recipe.image_url ? (
                      <img
                        src={recipe.image_url}
                        alt={recipe.title}
                        className="object-cover w-full h-full transition-transform group-hover:scale-105"
                      />
                    ) : (
                      <div className="flex items-center justify-center w-full h-full text-muted-foreground dark:text-slate-400 bg-secondary dark:bg-slate-800">
                        No image
                      </div>
                    )}
                  </div>
                  <CardHeader className="p-4 pb-2 flex-grow">
                    <CardTitle className="line-clamp-2 text-lg leading-tight dark:text-slate-50">
                      {recipe.title}
                    </CardTitle>

                    {recipe.rating && (
                      <div className="flex items-center gap-1 text-sm text-muted-foreground dark:text-slate-400 mt-2">
                        <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                        <span className="font-medium text-foreground dark:text-slate-50">{recipe.rating.average}</span>
                        <span className="dark:text-slate-400">({recipe.rating.count} reviews)</span>
                      </div>
                    )}
                  </CardHeader>

                  <div className="px-4 pb-4 pt-1 flex flex-wrap gap-2">
                    {(recipe.categories || []).map((category) => (
                      <Badge key={category} variant="outline" className="text-[11px] font-medium capitalize dark:border-slate-700 dark:text-slate-300">
                        {titleCase(category)}
                      </Badge>
                    ))}
                    {(recipe.themes || []).map((theme) => (
                      <Badge key={theme} variant="secondary" className="text-[11px] font-medium capitalize dark:bg-slate-800 dark:text-slate-300">
                        {titleCase(theme)}
                      </Badge>
                    ))}
                  </div>
                </Card>
              </Link>
            ))}
      </div>

      {/* Pagination */}
      {!loading && totalPages > 1 && (
        <Pagination>
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  if (currentPage > 1) setCurrentPage(p => p - 1);
                }}
                className={currentPage === 1 ? "pointer-events-none opacity-50" : "cursor-pointer"}
              />
            </PaginationItem>

            {/* Dynamic Page Links with Ellipsis */}
            {(() => {
              const pages = [];
              const maxVisiblePages = 5;

              if (totalPages <= maxVisiblePages) {
                // Show all pages if total is small
                for (let i = 1; i <= totalPages; i++) pages.push(i);
              } else {
                // Always show first, last, current, and pages around current
                if (currentPage <= 3) {
                  pages.push(1, 2, 3, 4, 'ellipsis', totalPages);
                } else if (currentPage >= totalPages - 2) {
                  pages.push(1, 'ellipsis', totalPages - 3, totalPages - 2, totalPages - 1, totalPages);
                } else {
                  pages.push(1, 'ellipsis', currentPage - 1, currentPage, currentPage + 1, 'ellipsis', totalPages);
                }
              }

              return pages.map((page, index) => {
                if (page === 'ellipsis') {
                  return (
                    <PaginationItem key={`ellipsis-${index}`}>
                      <PaginationEllipsis />
                    </PaginationItem>
                  );
                }

                return (
                  <PaginationItem key={page}>
                    <PaginationLink
                      href="#"
                      isActive={currentPage === page}
                      onClick={(e) => {
                        e.preventDefault();
                        setCurrentPage(page as number);
                      }}
                    >
                      {page}
                    </PaginationLink>
                  </PaginationItem>
                );
              });
            })()}

            <PaginationItem>
              <PaginationNext
                href="#"
                onClick={(e) => {
                  e.preventDefault();
                  if (currentPage < totalPages) setCurrentPage(p => p + 1);
                }}
                className={currentPage >= totalPages ? "pointer-events-none opacity-50" : "cursor-pointer"}
              />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      )}
    </div>
  );
}
