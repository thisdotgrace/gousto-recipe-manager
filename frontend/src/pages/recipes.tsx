import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getRecipes } from "@/api/recipe";
import type { Recipe } from "@/types/recipe";
import {
  Card,
  CardContent,
  CardDescription,
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
        <h1 className="text-3xl font-bold tracking-tight">Recipes</h1>
        <p className="text-muted-foreground mt-2">
          Browse our collection of delicious meals.
        </p>
      </div>

      {error && (
        <div className="p-4 mb-8 text-destructive-foreground bg-destructive rounded-md">
          {error}
        </div>
      )}

      {/* Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
        {loading
          ? Array.from({ length: LIMIT }).map((_, i) => (
              <Card key={i} className="flex flex-col overflow-hidden">
                <Skeleton className="h-48 w-full rounded-none" />
                <CardHeader>
                  <Skeleton className="h-6 w-3/4 mb-2" />
                  <Skeleton className="h-4 w-1/2" />
                </CardHeader>
              </Card>
            ))
          : recipes.map((recipe) => (
              <Link to={`/recipes/${recipe.slug}`} key={recipe.id} className="group">
                <Card className="flex flex-col h-full overflow-hidden transition-all hover:shadow-md relative">
                  <div className="aspect-[4/3] overflow-hidden bg-muted relative">
                    <div className="absolute top-2 left-2 z-10 flex gap-2">
                      {recipe.calories && (
                        <Badge variant="secondary" className="flex items-center gap-1 bg-background/80 backdrop-blur-sm border-0 font-medium">
                          <Flame className="w-3 h-3 text-orange-500" />
                          {recipe.calories} kcal
                        </Badge>
                      )}
                      {recipe.prep_time && (
                        <Badge variant="secondary" className="flex items-center gap-1 bg-background/80 backdrop-blur-sm border-0 font-medium">
                          <Clock className="w-3 h-3 text-blue-500" />
                          {recipe.prep_time} mins
                        </Badge>
                      )}
                    </div>
                    {recipe.image_url ? (
                      <img
                        src={recipe.image_url}
                        alt={recipe.title}
                        className="object-cover w-full h-full transition-transform group-hover:scale-105"
                      />
                    ) : (
                      <div className="flex items-center justify-center w-full h-full text-muted-foreground bg-secondary">
                        No image
                      </div>
                    )}
                  </div>
                  <CardHeader className="p-4 flex-grow">
                    <div className="flex items-start justify-between gap-2 mb-1">
                      <CardTitle className="line-clamp-2 text-lg leading-tight">
                        {recipe.title}
                      </CardTitle>
                    </div>
                    <CardDescription className="flex items-center justify-between mt-auto pt-2">
                      <span className="font-medium text-primary">
                        {recipe.cuisine || "Mixed"}
                      </span>
                      {recipe.rating && (
                        <div className="flex items-center gap-1 text-sm text-muted-foreground">
                          <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                          <span className="font-medium text-foreground">{recipe.rating.average}</span>
                          <span>({recipe.rating.count})</span>
                        </div>
                      )}
                    </CardDescription>
                  </CardHeader>
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
