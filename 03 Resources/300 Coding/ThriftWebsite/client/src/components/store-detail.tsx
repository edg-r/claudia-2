import { useState } from "react";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import StarRating from "@/components/star-rating";
import { StoreResponse } from "@shared/schema";
import { Phone, Navigation, Globe, Share2 } from "lucide-react";
import { formatDistanceToNow } from "date-fns";

interface StoreDetailProps {
  store: StoreResponse;
  onClose?: () => void;
}

export default function StoreDetail({ store, onClose }: StoreDetailProps) {
  const [showAllReviews, setShowAllReviews] = useState(false);
  
  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: `${store.name} | Thrift SD`,
          text: `Check out ${store.name} on Thrift SD`,
          url: window.location.href,
        });
      } catch (error) {
        console.error('Error sharing:', error);
      }
    } else {
      // Fallback for browsers that don't support Web Share API
      navigator.clipboard.writeText(window.location.href);
      alert('Link copied to clipboard!');
    }
  };
  
  // Format reviews to show only first 5 by default
  const reviews = store.reviews || [];
  const displayedReviews = showAllReviews ? reviews : reviews.slice(0, 5);
  
  return (
    <div className="p-6">
      <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-200 mb-2">{store.name}</h2>
      <div className="flex items-center mb-4">
        {store.rating ? (
          <>
            <StarRating rating={store.rating} className="mr-2" />
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {store.rating.toFixed(1)} ({store.user_ratings_total} reviews)
            </span>
          </>
        ) : (
          <span className="text-sm text-gray-400 dark:text-gray-500">No ratings yet</span>
        )}
      </div>

      <div className="grid grid-cols-2 gap-2 mb-6">
        {store.phone ? (
          <a 
            href={`tel:${store.phone}`}
            className="flex items-center justify-center py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors"
          >
            <Phone className="mr-2 h-4 w-4" />
            <span>Call</span>
          </a>
        ) : (
          <Button variant="outline" disabled className="opacity-50">
            <Phone className="mr-2 h-4 w-4" />
            <span>No Phone</span>
          </Button>
        )}
        
        <a
          href={`https://maps.google.com/?q=${store.lat},${store.lng}`}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-center py-2 bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
        >
          <Navigation className="mr-2 h-4 w-4" />
          <span>Directions</span>
        </a>
      </div>

      <Separator className="my-4" />
      
      <h3 className="text-lg font-medium text-gray-800 dark:text-gray-200 mb-2">Information</h3>
      <div className="space-y-2 text-sm">
        <p className="flex items-start">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500 dark:text-gray-400 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span className="text-gray-600 dark:text-gray-300">{store.address}</span>
        </p>
        
        {store.phone && (
          <p className="flex items-start">
            <Phone className="h-5 w-5 text-gray-500 dark:text-gray-400 mr-2 flex-shrink-0" />
            <span className="text-gray-600 dark:text-gray-300">{store.phone}</span>
          </p>
        )}
        
        {store.website && (
          <p className="flex items-start">
            <Globe className="h-5 w-5 text-gray-500 dark:text-gray-400 mr-2 flex-shrink-0" />
            <a
              href={store.website}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary dark:text-indigo-400 hover:underline"
            >
              {store.website.replace(/(^\w+:|^)\/\//, '').replace(/\/$/, '')}
            </a>
          </p>
        )}
      </div>

      <Separator className="my-4" />
      
      <h3 className="text-lg font-medium text-gray-800 dark:text-gray-200 mb-2">Categories</h3>
      <div className="flex flex-wrap gap-2">
        {store.categories.map((category) => (
          <span
            key={category}
            className="px-3 py-1 bg-gray-100 dark:bg-gray-700 rounded-full text-sm"
          >
            {category}
          </span>
        ))}
      </div>

      {reviews.length > 0 && (
        <>
          <Separator className="my-4" />
          
          <h3 className="text-lg font-medium text-gray-800 dark:text-gray-200 mb-2">Reviews</h3>
          
          {displayedReviews.map((review, index) => (
            <div key={index} className="mb-4">
              <div className="flex justify-between">
                <span className="font-medium">{review.author}</span>
                <StarRating rating={review.rating} />
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{review.text}</p>
              <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                {formatDistanceToNow(new Date(review.time * 1000), { addSuffix: true })}
              </p>
            </div>
          ))}
          
          {reviews.length > 5 && (
            <Button
              variant="ghost"
              className="w-full py-2 text-sm text-primary dark:text-indigo-400 font-medium"
              onClick={() => setShowAllReviews(!showAllReviews)}
            >
              {showAllReviews ? "Show less reviews" : "Show more reviews"}
            </Button>
          )}
        </>
      )}

      <Separator className="my-4" />
      
      <Button
        variant="ghost"
        className="flex items-center justify-center w-full py-2 text-sm text-gray-600 dark:text-gray-400"
        onClick={handleShare}
      >
        <Share2 className="h-4 w-4 mr-2" />
        <span>Share this store</span>
      </Button>
    </div>
  );
}
