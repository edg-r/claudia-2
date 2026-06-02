import { Button } from "@/components/ui/button";
import { MapPin, List } from "lucide-react";
import { cn } from "@/lib/utils";

type View = "list" | "map";

interface ViewToggleProps {
  currentView: View;
  onViewChange: (view: View) => void;
}

export default function ViewToggle({ currentView, onViewChange }: ViewToggleProps) {
  return (
    <div className="fixed bottom-5 right-5 z-20">
      <div className="bg-white dark:bg-gray-800 rounded-full shadow-lg">
        <Button
          aria-label="List View"
          className={cn(
            "px-4 py-3 rounded-l-full",
            currentView === "list"
              ? "bg-primary text-white"
              : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300"
          )}
          onClick={() => onViewChange("list")}
        >
          <List className="h-5 w-5" />
        </Button>
        <Button
          aria-label="Map View"
          className={cn(
            "px-4 py-3 rounded-r-full",
            currentView === "map"
              ? "bg-primary text-white"
              : "bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300"
          )}
          onClick={() => onViewChange("map")}
        >
          <MapPin className="h-5 w-5" />
        </Button>
      </div>
    </div>
  );
}
