import React from "react";
import type { Recipe } from "@/features/recipes/types/recipe";
import RecipeCard from "./recipe-card";
import { Card, CardHeader } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

interface Props {
  recipes: Recipe[];
  loading?: boolean;
  limit?: number;
}

const classes = {
  container: "grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8",
  card: "flex flex-col overflow-hidden",
  skeletonImage: "h-48 w-full rounded-none",
  skeletonTitle: "h-6 w-3/4 mb-2",
  skeletonLine: "h-4 w-1/2",
};

export default function RecipeGrid({ recipes, loading = false, limit = 12 }: Props) {
  return (
    <div className={classes.container}>
      {loading
        ? Array.from({ length: limit }).map((_, i) => (
            <Card key={i} className={classes.card}>
              <Skeleton className={classes.skeletonImage} />
              <CardHeader>
                <Skeleton className={classes.skeletonTitle} />
                <Skeleton className={classes.skeletonLine} />
              </CardHeader>
            </Card>
          ))
        : recipes.map((r) => <RecipeCard key={r.id} recipe={r} />)}
    </div>
  );
}
