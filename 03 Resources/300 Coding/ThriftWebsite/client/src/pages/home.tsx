import { useState, useEffect } from "react";
import SearchBar from "@/components/search-bar";
import CategoryFilter from "@/components/category-filter";
import ListView from "@/components/list-view";
import MapView from "@/components/map-view";
import ViewToggle from "@/components/view-toggle";
import OfflineIndicator from "@/components/offline-indicator";
import { useGeolocation } from "@/hooks/use-geolocation";
import { useStores, useNearbyStores, useStoresByCategory, useSearchStores } from "@/hooks/use-stores";
import { StoreResponse } from "@shared/schema";
import { queryClient } from "@/lib/queryClient";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

type ViewMode = "list" | "map";
type SortMode = "distance" | "rating";

export default function Home() {
  // State for view and filters
  const [view, setView] = useState<ViewMode>("list");
  const [sortBy, setSortBy] = useState<SortMode>("distance");
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [allCategories, setAllCategories] = useState<string[]>([]);
  
  // Get user location
  const { coords: userLocation, loading: locationLoading, error: locationError } = useGeolocation();
  
  // Query data based on filters
  const { data: allStores, isLoading: isLoadingAllStores } = useStores();
  const { data: nearbyStores, isLoading: isLoadingNearbyStores } = useNearbyStores(
    userLocation?.lat,
    userLocation?.lng
  );
  const { data: categoryStores, isLoading: isLoadingCategoryStores } = useStoresByCategory(
    selectedCategory
  );
  const { data: searchResults, isLoading: isLoadingSearchResults } = useSearchStores(
    searchQuery
  );
  
  // Extract unique categories from all stores
  useEffect(() => {
    if (allStores) {
      const categories = new Set<string>();
      allStores.forEach(store => {
        store.categories.forEach(category => {
          categories.add(category);
        });
      });
      setAllCategories(Array.from(categories));
    }
  }, [allStores]);
  
  // Determine which stores to display based on filters
  const getFilteredStores = (): StoreResponse[] => {
    // If searching, use search results
    if (searchQuery && searchResults) {
      return searchResults;
    }
    
    // If filtering by category (not "all"), use category results
    if (selectedCategory !== "all" && categoryStores) {
      return categoryStores;
    }
    
    // If sorting by distance and we have location, use nearby stores
    if (sortBy === "distance" && nearbyStores) {
      return nearbyStores;
    }
    
    // Default to all stores
    return allStores || [];
  };
  
  // Sort stores based on sort mode
  const getSortedStores = (): StoreResponse[] => {
    const stores = getFilteredStores();
    
    if (sortBy === "distance" && nearbyStores) {
      // Already sorted by distance from API
      return stores;
    } else {
      // Sort by rating
      return [...stores].sort((a, b) => {
        const ratingA = a.rating || 0;
        const ratingB = b.rating || 0;
        return ratingB - ratingA;
      });
    }
  };
  
  const stores = getSortedStores();
  const isLoading = isLoadingAllStores || 
    isLoadingNearbyStores || 
    isLoadingCategoryStores || 
    isLoadingSearchResults;
  
  // Pull to refresh handler
  const handleRefresh = () => {
    queryClient.invalidateQueries({ queryKey: ["/api/stores"] });
    if (userLocation) {
      queryClient.invalidateQueries({ 
        queryKey: ["/api/stores/nearby", userLocation.lat, userLocation.lng] 
      });
    }
    if (selectedCategory !== "all") {
      queryClient.invalidateQueries({ 
        queryKey: ["/api/stores/category", selectedCategory] 
      });
    }
  };
  
  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="sticky top-0 z-30 bg-white dark:bg-gray-800 shadow-md">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center">
          <div className="flex items-center">
            <h1 className="text-xl font-semibold text-primary dark:text-indigo-400">Thrift SD</h1>
          </div>
        </div>
        
        {/* Search Bar */}
        <div className="container mx-auto px-4 pb-3">
          <SearchBar onSearch={setSearchQuery} initialQuery={searchQuery} />
        </div>
        
        {/* Category Filter */}
        <div className="container mx-auto px-4 pb-3">
          <CategoryFilter
            categories={allCategories}
            selectedCategory={selectedCategory}
            onSelectCategory={setSelectedCategory}
          />
        </div>
        
        {/* Sort Options */}
        <div className="container mx-auto px-4 pb-3 flex justify-between text-sm text-gray-500 dark:text-gray-400">
          <div>
            <span>{stores.length} stores found</span>
          </div>
          <div className="flex items-center space-x-2">
            <span>Sort by:</span>
            <Select 
              value={sortBy} 
              onValueChange={(value: SortMode) => setSortBy(value)}
            >
              <SelectTrigger className="bg-transparent border-none w-auto p-0">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent align="end">
                <SelectItem value="distance">Distance</SelectItem>
                <SelectItem value="rating">Rating</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </header>
      
      {/* Main Content */}
      <main className="flex-grow container mx-auto px-4 pb-24">
        {/* View Toggle */}
        <ViewToggle currentView={view} onViewChange={setView} />
        
        {/* List View */}
        {view === "list" && (
          <ListView 
            stores={stores} 
            isLoading={isLoading} 
            onRefresh={handleRefresh}
          />
        )}
        
        {/* Map View */}
        {view === "map" && (
          <MapView 
            stores={stores} 
            userLocation={userLocation}
          />
        )}
        
        {/* Offline Indicator */}
        <OfflineIndicator />
      </main>
      
      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-4 text-center text-sm text-gray-500 dark:text-gray-400">
        <div className="container mx-auto px-4">
          <p>© {new Date().getFullYear()} Thrift SD. All thrift stores in San Diego.</p>
        </div>
      </footer>
    </div>
  );
}
