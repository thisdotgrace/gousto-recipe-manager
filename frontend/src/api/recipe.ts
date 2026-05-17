import { API_BASE_URL } from './client';
import type { RecipesResponse } from '@/types/recipe';

export async function getRecipes(offset: number, limit: number): Promise<RecipesResponse> {
  const res = await fetch(`${API_BASE_URL}/recipes?limit=${limit}&offset=${offset}`);
  if (!res.ok) {
    throw new Error('Failed to fetch recipes');
  }
  return res.json();
}
