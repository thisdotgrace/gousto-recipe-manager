import React from "react";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Star, Clock, Flame } from "lucide-react";
import type { Recipe } from "@/features/recipes/types/recipe";
import { titleCase } from "@/features/recipes/utils";

interface Props {
  recipe: Recipe;
}

const classes = {
  link: "group",
  card: "flex flex-col h-full overflow-hidden transition-all hover:shadow-md relative",
  imageWrapper: "aspect-[4/3] overflow-hidden bg-muted dark:bg-slate-800 relative",
  topBadges: "absolute top-2 left-2 z-10 flex gap-2 flex-wrap",
  pillBadge: "flex items-center gap-1 bg-background/80 backdrop-blur-sm border-0 font-medium",
  cuisineWrapper: "absolute bottom-2 left-2 z-10",
  cuisineBadge: "bg-background/80 backdrop-blur-sm border-0 font-medium capitalize",
  image: "object-cover w-full h-full transition-transform group-hover:scale-105",
  noImage: "flex items-center justify-center w-full h-full text-muted-foreground bg-secondary",
  header: "p-4 pb-2 flex-grow",
  title: "line-clamp-2 text-lg leading-tight",
  rating: "flex items-center gap-1 text-sm text-muted-foreground mt-2",
  star: "w-4 h-4 fill-yellow-400 text-yellow-400",
  ratingValue: "font-medium text-foreground",
  tags: "px-4 pb-4 pt-1 flex flex-wrap gap-2",
  categoryBadge: "text-[11px] font-medium capitalize",
  themeBadge: "text-[11px] font-medium capitalize",
};

export default function RecipeCard({ recipe }: Props) {
  const { slug, image_url, title, calories, prep_time, cuisine, rating, categories, themes } = recipe;
  const url = `https://www.gousto.co.uk/cookbook/recipes/${slug}`;

  return (
    <a href={url} target="_blank" rel="noreferrer" className={classes.link}>
      <Card className={classes.card}>
        <div className={classes.imageWrapper}>
          <div className={classes.topBadges}>
            {calories && (
              <Badge variant="secondary" className={classes.pillBadge}>
                <Flame className="w-3 h-3 text-orange-500" />
                {calories} kcal
              </Badge>
            )}
            {prep_time && (
              <Badge variant="secondary" className={classes.pillBadge}>
                <Clock className="w-3 h-3 text-blue-500" />
                {prep_time} mins
              </Badge>
            )}
          </div>

          <div className={classes.cuisineWrapper}>
            <Badge variant="secondary" className={classes.cuisineBadge}>
              {titleCase(cuisine) || "Mixed"}
            </Badge>
          </div>

          {image_url ? (
            <img src={image_url} alt={title} className={classes.image} />
          ) : (
            <div className={classes.noImage}>No image</div>
          )}
        </div>

        <CardHeader className={classes.header}>
          <CardTitle className={classes.title}>{title}</CardTitle>

          {rating && (
            <div className={classes.rating}>
              <Star className={classes.star} />
              <span className={classes.ratingValue}>{rating.average}</span>
              <span>({rating.count} reviews)</span>
            </div>
          )}
        </CardHeader>

        <div className={classes.tags}>
          {(categories || []).map((c: string) => (
            <Badge key={c} variant="outline" className={classes.categoryBadge}>
              {titleCase(c)}
            </Badge>
          ))}
          {(themes || []).map((t: string) => (
            <Badge key={t} variant="secondary" className={classes.themeBadge}>
              {titleCase(t)}
            </Badge>
          ))}
        </div>
      </Card>
    </a>
  );
}
