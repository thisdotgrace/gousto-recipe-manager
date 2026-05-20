import { API_BASE_URL } from '../../../api/client';
import type { RecipesResponse } from '@/features/recipes/types/recipe';

export async function getRecipes(offset: number, limit: number): Promise<RecipesResponse> {
  const res = await fetch(`${API_BASE_URL}/recipes?limit=${limit}&offset=${offset}`);
  if (!res.ok) {
    throw new Error('Failed to fetch recipes');
  }
  return res.json();
}

export async function searchRecipes(
  query: string,
  offset = 0,
  limit = 12
) {
  const res = await fetch(`${API_BASE_URL}/recipes/search?q=${encodeURIComponent(query)}&limit=${limit}&offset=${offset}`);

  if (!res.ok) {
    throw new Error('Failed to search recipes');
  }

  return res.json();
}
