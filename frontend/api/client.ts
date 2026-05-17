export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

// frontend/src/api/recipe.ts
import { API_BASE_URL } from './client';
import type { RecipesResponse } from '@/types/recipe';

export async function getRecipes(offset: number, limit: number): Promise<RecipesResponse> {
  const res = await fetch(`${API_BASE_URL}/recipes?offset=${offset}&limit=${limit}`);
  if (!res.ok) {
    throw new Error('Failed to fetch recipes');
  }
  return res.json();
}
