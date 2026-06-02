import { useEffect, useRef, useState } from "react";
import { StoreResponse } from "@shared/schema";
import { Button } from "@/components/ui/button";
import { Loader } from "lucide-react";
import StoreDetail from "@/components/store-detail";

interface MapViewProps {
  stores: StoreResponse[];
  userLocation?: { lat: number; lng: number } | null;
}

export default function MapView({ stores, userLocation }: MapViewProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  const [mapError, setMapError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [mapboxgl, setMapboxgl] = useState<any>(null);
  const [map, setMap] = useState<any>(null);
  const [selectedStore, setSelectedStore] = useState<StoreResponse | null>(null);
  
  // Dynamically load Mapbox GL
  useEffect(() => {
    const loadMapbox = async () => {
      try {
        setIsLoading(true);
        
        // Dynamic import of mapbox-gl
        const mapboxModule = await import('mapbox-gl');
        setMapboxgl(mapboxModule.default);
        
        // Get API key from environment
        const accessToken = import.meta.env.VITE_MAPBOX_TOKEN;
        if (!accessToken) {
          setMapError("Map configuration is missing.");
          setIsLoading(false);
          return;
        }
        mapboxModule.default.accessToken = accessToken;
        
        setMapLoaded(true);
        setIsLoading(false);
      } catch (error) {
        console.error("Error loading Mapbox GL:", error);
        setMapError("Failed to load map. Please try again later.");
        setIsLoading(false);
      }
    };
    
    loadMapbox();
  }, []);
  
  // Initialize map when Mapbox is loaded and container is ready
  useEffect(() => {
    if (!mapLoaded || !mapboxgl || !mapContainerRef.current) return;
    
    // Default center to San Diego if no user location
    const center = userLocation 
      ? [userLocation.lng, userLocation.lat] 
      : [-117.1611, 32.7157]; // San Diego coordinates
    
    const newMap = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: 'mapbox://styles/mapbox/streets-v11',
      center: center,
      zoom: 12
    });
    
    // Add navigation controls
    newMap.addControl(new mapboxgl.NavigationControl(), 'top-right');
    
    // Add geolocation control if supported
    if (navigator.geolocation) {
      newMap.addControl(
        new mapboxgl.GeolocateControl({
          positionOptions: {
            enableHighAccuracy: true
          },
          trackUserLocation: true
        }),
        'top-right'
      );
    }
    
    // On map load, add markers
    newMap.on('load', () => {
      setMap(newMap);
    });
    
    return () => {
      newMap.remove();
    };
  }, [mapLoaded, mapboxgl, userLocation]);
  
  // Add markers when map and stores are available
  useEffect(() => {
    if (!map || !mapboxgl || !stores.length) return;
    
    // Remove existing markers
    const existingMarkers = document.querySelectorAll('.mapboxgl-marker');
    existingMarkers.forEach(marker => marker.remove());
    
    // Add markers for each store
    stores.forEach(store => {
      // Custom marker element
      const el = document.createElement('div');
      el.className = 'marker';
      el.style.backgroundColor = '#6366F1';
      el.style.width = '25px';
      el.style.height = '25px';
      el.style.borderRadius = '50%';
      el.style.cursor = 'pointer';
      el.style.border = '2px solid white';
      el.style.boxShadow = '0 2px 4px rgba(0,0,0,0.3)';
      
      // Add store name as tooltip
      const popup = new mapboxgl.Popup({ offset: 25 }).setText(store.name);
      
      // Create marker
      const marker = new mapboxgl.Marker(el)
        .setLngLat([store.lng, store.lat])
        .setPopup(popup)
        .addTo(map);
      
      // Add click event to show store details
      el.addEventListener('click', () => {
        setSelectedStore(store);
      });
    });
    
    // If we have many stores, fit bounds to show all markers
    if (stores.length > 1) {
      const bounds = new mapboxgl.LngLatBounds();
      stores.forEach(store => {
        bounds.extend([store.lng, store.lat]);
      });
      map.fitBounds(bounds, { padding: 50 });
    }
  }, [map, mapboxgl, stores]);
  
  // Handle map errors or loading state
  if (isLoading) {
    return (
      <div className="h-full w-full bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center text-center">
        <div className="p-6">
          <Loader className="h-8 w-8 text-gray-400 dark:text-gray-500 mb-4 animate-spin mx-auto" />
          <p className="text-gray-600 dark:text-gray-400">Loading map...</p>
        </div>
      </div>
    );
  }
  
  if (mapError) {
    return (
      <div className="h-full w-full bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center text-center">
        <div className="p-6">
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            className="h-8 w-8 text-red-500 mx-auto mb-4" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path 
              strokeLinecap="round" 
              strokeLinejoin="round" 
              strokeWidth={2} 
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" 
            />
          </svg>
          <p className="text-gray-600 dark:text-gray-400 mb-4">{mapError}</p>
          <Button onClick={() => window.location.reload()}>
            Try Again
          </Button>
        </div>
      </div>
    );
  }
  
  return (
    <>
      <div 
        ref={mapContainerRef} 
        className="h-full w-full rounded-lg overflow-hidden"
      />
      {selectedStore && (
        <div className="absolute inset-0 bg-black bg-opacity-50 z-50 flex items-end md:items-center justify-center">
          <div className="w-full md:w-auto md:max-w-md bg-white dark:bg-gray-800 rounded-t-lg md:rounded-lg overflow-auto max-h-[80vh]">
            <Button 
              variant="ghost" 
              className="absolute top-2 right-2 rounded-full w-8 h-8 p-0" 
              onClick={() => setSelectedStore(null)}
              aria-label="Close details"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                className="h-5 w-5" 
                viewBox="0 0 20 20" 
                fill="currentColor"
              >
                <path 
                  fillRule="evenodd" 
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" 
                  clipRule="evenodd" 
                />
              </svg>
            </Button>
            <StoreDetail store={selectedStore} onClose={() => setSelectedStore(null)} />
          </div>
        </div>
      )}
    </>
  );
}
