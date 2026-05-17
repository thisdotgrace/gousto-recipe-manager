export interface Recipe {
  id: string | number;
  title: string;
  slug: string;
  image_url?: string;
  time?: number;
  prep_time?: number;
  calories?: number;
  rating?: {
    average: number;
    count: number;
  };
  cuisine?: string;
}

export interface RecipesResponse {
  total: number;
  offset: number;
  limit: number;
  data: Recipe[];
}
