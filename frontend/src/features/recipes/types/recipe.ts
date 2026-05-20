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
  macros?: {
    energy_kcal?: number;
    protein_g?: number;
    fat_g?: number;
    saturates_g?: number;
    carbs_g?: number;
    sugars_g?: number;
    fibre_g?: number;
    salt_g?: number;
  };
  ingredients?: string[];
  categories?: string[];
  themes?: string[];
}

export interface RecipesResponse {
  total: number;
  offset: number;
  limit: number;
  data: Recipe[];
}
