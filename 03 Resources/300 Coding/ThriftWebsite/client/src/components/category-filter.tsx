import { cn } from "@/lib/utils";

interface CategoryProps {
  categories: string[];
  selectedCategory: string;
  onSelectCategory: (category: string) => void;
}

export default function CategoryFilter({ 
  categories,
  selectedCategory,
  onSelectCategory 
}: CategoryProps) {
  return (
    <div className="overflow-x-auto hide-scrollbar">
      <div className="flex space-x-2 pb-1">
        <button
          className={cn(
            "flex-shrink-0 px-3 py-1 rounded-full text-sm",
            selectedCategory === "all"
              ? "bg-primary text-white dark:bg-indigo-600"
              : "bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600"
          )}
          onClick={() => onSelectCategory("all")}
        >
          All
        </button>
        
        {categories.map((category) => (
          <button
            key={category}
            className={cn(
              "flex-shrink-0 px-3 py-1 rounded-full text-sm",
              selectedCategory === category
                ? "bg-primary text-white dark:bg-indigo-600"
                : "bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600"
            )}
            onClick={() => onSelectCategory(category)}
          >
            {category}
          </button>
        ))}
      </div>
    </div>
  );
}
