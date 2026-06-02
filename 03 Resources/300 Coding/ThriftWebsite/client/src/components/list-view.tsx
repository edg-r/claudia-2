import { useRef, useEffect, useState } from "react";
import { FixedSizeList as List } from "react-window";
import AutoSizer from "react-virtualized-auto-sizer";
import StoreCard from "@/components/store-card";
import { StoreResponse } from "@shared/schema";
import { Skeleton } from "@/components/ui/skeleton";
import { useIsMobile } from "@/hooks/use-mobile";

interface ListViewProps {
  stores: StoreResponse[];
  isLoading: boolean;
  onRefresh?: () => void;
}

function StoreCardSkeleton() {
  return (
    <div className="mb-4 p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-100 dark:border-gray-700">
      <div className="flex justify-between items-start">
        <div className="flex-grow">
          <Skeleton className="h-6 w-3/4 rounded mb-2" />
          <Skeleton className="h-4 w-24 rounded mb-2" />
          <Skeleton className="h-4 w-full rounded mb-2" />
          <div className="flex gap-1 mt-2">
            <Skeleton className="h-6 w-16 rounded-full" />
            <Skeleton className="h-6 w-16 rounded-full" />
          </div>
        </div>
        <Skeleton className="h-6 w-12 rounded-full" />
      </div>
    </div>
  );
}

export default function ListView({ stores, isLoading, onRefresh }: ListViewProps) {
  const isMobile = useIsMobile();
  const listRef = useRef<List>(null);
  
  // Pull to refresh functionality
  const startY = useRef<number | null>(null);
  const pullThreshold = 100; // Pixels to pull down to trigger refresh
  const containerRef = useRef<HTMLDivElement>(null);
  const refreshIndicatorRef = useRef<HTMLDivElement>(null);
  const [isPulling, setIsPulling] = useState(false);
  
  useEffect(() => {
    const handleTouchStart = (e: TouchEvent) => {
      if (containerRef.current && containerRef.current.scrollTop === 0) {
        startY.current = e.touches[0].clientY;
      }
    };
    
    const handleTouchMove = (e: TouchEvent) => {
      if (startY.current !== null) {
        const currentY = e.touches[0].clientY;
        const diff = currentY - startY.current;
        
        if (diff > 0) {
          e.preventDefault(); // Prevent default scroll
          setIsPulling(true);
          
          if (refreshIndicatorRef.current) {
            const height = Math.min(diff * 0.5, 100); // Cap at 100px
            refreshIndicatorRef.current.style.height = `${height}px`;
          }
        }
      }
    };
    
    const handleTouchEnd = () => {
      if (startY.current !== null && refreshIndicatorRef.current) {
        const height = parseInt(refreshIndicatorRef.current.style.height || '0');
        
        if (height > pullThreshold && onRefresh) {
          onRefresh();
        }
        
        // Reset
        refreshIndicatorRef.current.style.height = '0';
        startY.current = null;
        setIsPulling(false);
      }
    };
    
    const container = containerRef.current;
    if (isMobile && container && onRefresh) {
      container.addEventListener('touchstart', handleTouchStart, { passive: false });
      container.addEventListener('touchmove', handleTouchMove, { passive: false });
      container.addEventListener('touchend', handleTouchEnd);
      
      return () => {
        container.removeEventListener('touchstart', handleTouchStart);
        container.removeEventListener('touchmove', handleTouchMove);
        container.removeEventListener('touchend', handleTouchEnd);
      };
    }
  }, [isMobile, onRefresh]);
  
  // If loading, show skeleton cards
  if (isLoading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <StoreCardSkeleton key={i} />
        ))}
      </div>
    );
  }
  
  // Render each store as an item in the virtualized list
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => {
    const store = stores[index];
    return (
      <div style={style}>
        <StoreCard
          place_id={store.place_id}
          name={store.name}
          address={store.address}
          rating={store.rating}
          user_ratings_total={store.user_ratings_total}
          categories={store.categories}
          distance={store.distance}
        />
      </div>
    );
  };
  
  // Either use virtualized list for efficiency or regular map
  return (
    <div 
      className="virtualized-list-container"
      ref={containerRef}
    >
      {/* Pull to refresh indicator (only on mobile) */}
      {isMobile && onRefresh && (
        <div
          ref={refreshIndicatorRef}
          className="pull-refresh-indicator flex items-center justify-center overflow-hidden"
          aria-live="polite"
          style={{ height: 0 }}
        >
          <div className="flex items-center">
            <svg 
              className={`animate-spin -ml-1 mr-2 h-5 w-5 text-primary ${isPulling ? 'opacity-100' : 'opacity-0'}`} 
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24"
            >
              <circle 
                className="opacity-25" 
                cx="12" 
                cy="12" 
                r="10" 
                stroke="currentColor" 
                strokeWidth="4"
              ></circle>
              <path 
                className="opacity-75" 
                fill="currentColor" 
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            <span>{isPulling ? "Release to refresh..." : "Refreshing..."}</span>
          </div>
        </div>
      )}
      
      {stores.length === 0 ? (
        <div className="flex flex-col items-center justify-center h-64">
          <p className="text-gray-500 dark:text-gray-400">No stores found</p>
        </div>
      ) : (
        <AutoSizer>
          {({ height, width }) => (
            <List
              ref={listRef}
              height={height}
              width={width}
              itemCount={stores.length}
              itemSize={150}
            >
              {Row}
            </List>
          )}
        </AutoSizer>
      )}
    </div>
  );
}
