
import { Button } from "@/components/ui/button"
import { ButtonGroup } from "@/components/ui/button-group"
import { Field, FieldLabel } from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import React from "react"

export function RecipeSearch({ search, onSearch }: { search: string; onSearch: (value: string) => void }) {
  return (
    <Field className="mt-4">
      <ButtonGroup>
        <Input
          id="input-button-group"
          placeholder="Type to search..."
          value={search}
          onChange={(e) => onSearch(e.target.value)}
        />
        <Button variant="outline">Search</Button>
      </ButtonGroup>
    </Field>
  )
}
