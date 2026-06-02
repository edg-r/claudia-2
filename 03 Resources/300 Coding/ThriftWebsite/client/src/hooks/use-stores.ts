import { useQuery } from "@tanstack/react-query";
import { StoreResponse } from "@shared/schema";

export function useStores() {
  return useQuery<StoreResponse[]>({
    queryKey: ["/api/stores"],
    staleTime: 60 * 1000, // 1 minute
  });
}

export function useNearbyStores(lat?: number, lng?: number, radius?: number) {
  return useQuery<(StoreResponse & { distance: number })[]>({
    queryKey: ["/api/stores/nearby", lat, lng, radius],
    enabled: !!lat && !!lng,
    staleTime: 60 * 1000, // 1 minute
  });
}

export function useStoresByCategory(category: string) {
  return useQuery<StoreResponse[]>({
    queryKey: ["/api/stores/category", category],
    enabled: !!category && category !== "all",
    staleTime: 60 * 1000, // 1 minute
  });
}

export function useSearchStores(query: string) {
  return useQuery<StoreResponse[]>({
    queryKey: ["/api/stores/search", query],
    enabled: !!query && query.length > 2, // Only search when query is at least 3 chars
    staleTime: 60 * 1000, // 1 minute
  });
}

export function useStoreDetail(placeId: string) {
  return useQuery<StoreResponse>({
    queryKey: [`/api/stores/${placeId}`],
    enabled: !!placeId,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}
