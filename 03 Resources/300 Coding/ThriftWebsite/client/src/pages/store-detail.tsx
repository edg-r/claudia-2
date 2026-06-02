import { useRoute } from "wouter";
import { useStoreDetail } from "@/hooks/use-stores";
import StoreDetail from "@/components/store-detail";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Loader } from "lucide-react";
import { useEffect } from "react";

export default function StoreDetailPage() {
  const [match, params] = useRoute<{ placeId: string }>("/store/:placeId");
  const { data: store, isLoading, error } = useStoreDetail(params?.placeId || "");
  
  // Set page title and meta tags for SEO
  useEffect(() => {
    if (store) {
      document.title = `${store.name} | Thrift SD`;
      
      // Add meta description
      let metaDescription = document.querySelector('meta[name="description"]');
      if (!metaDescription) {
        metaDescription = document.createElement('meta');
        metaDescription.setAttribute('name', 'description');
        document.head.appendChild(metaDescription);
      }
      metaDescription.setAttribute('content', `Discover ${store.name} in San Diego. ${store.categories.join(', ')} thrift store.`);
      
      // Add JSON-LD schema for LocalBusiness
      const schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": store.name,
        "address": {
          "@type": "PostalAddress",
          "streetAddress": store.address
        },
        "telephone": store.phone,
        "url": store.website,
        "geo": {
          "@type": "GeoCoordinates",
          "latitude": store.lat,
          "longitude": store.lng
        },
        "aggregateRating": store.rating ? {
          "@type": "AggregateRating",
          "ratingValue": store.rating,
          "reviewCount": store.user_ratings_total
        } : undefined
      };
      
      let scriptSchema = document.querySelector('#jsonld-schema');
      if (!scriptSchema) {
        scriptSchema = document.createElement('script');
        scriptSchema.id = 'jsonld-schema';
        scriptSchema.type = 'application/ld+json';
        document.head.appendChild(scriptSchema);
      }
      scriptSchema.textContent = JSON.stringify(schema);
      
      return () => {
        // Clean up on unmount
        if (scriptSchema) {
          document.head.removeChild(scriptSchema);
        }
      };
    }
  }, [store]);
  
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <header className="sticky top-0 z-30 bg-white dark:bg-gray-800 shadow-md">
        <div className="container mx-auto px-4 py-3 flex items-center">
          <Button
            variant="ghost"
            size="sm"
            className="mr-2"
            onClick={() => window.history.back()}
          >
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <h1 className="text-xl font-semibold text-primary dark:text-indigo-400 truncate">
            {isLoading ? "Loading..." : store?.name || "Store Details"}
          </h1>
        </div>
      </header>
      
      <main className="container mx-auto px-4 py-6">
        {isLoading ? (
          <div className="flex flex-col items-center justify-center py-20">
            <Loader className="h-8 w-8 text-primary animate-spin mb-4" />
            <p className="text-gray-500 dark:text-gray-400">Loading store information...</p>
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-lg mb-4">
              <p>Failed to load store details.</p>
            </div>
            <Button onClick={() => window.history.back()}>
              Go Back
            </Button>
          </div>
        ) : store ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
            <StoreDetail store={store} />
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400 p-4 rounded-lg mb-4">
              <p>Store not found.</p>
            </div>
            <Button onClick={() => window.history.back()}>
              Go Back
            </Button>
          </div>
        )}
      </main>
      
      <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 py-4 text-center text-sm text-gray-500 dark:text-gray-400 mt-auto">
        <div className="container mx-auto px-4">
          <p>© {new Date().getFullYear()} Thrift SD. All thrift stores in San Diego.</p>
        </div>
      </footer>
    </div>
  );
}
