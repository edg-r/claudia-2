import { useState, useEffect } from "react";

interface GeolocationState {
  coords: { lat: number; lng: number } | null;
  loading: boolean;
  error: string | null;
}

export function useGeolocation() {
  const [state, setState] = useState<GeolocationState>({
    coords: null,
    loading: true,
    error: null,
  });
  
  useEffect(() => {
    if (!navigator.geolocation) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: "Geolocation is not supported by your browser"
      }));
      return;
    }
    
    const successHandler = (position: GeolocationPosition) => {
      setState({
        coords: {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        },
        loading: false,
        error: null
      });
    };
    
    const errorHandler = (error: GeolocationPositionError) => {
      setState({
        coords: null,
        loading: false,
        error: error.message
      });
    };
    
    navigator.geolocation.getCurrentPosition(successHandler, errorHandler, {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0
    });
    
    return () => {
      // Cleanup
    };
  }, []);
  
  return state;
}
