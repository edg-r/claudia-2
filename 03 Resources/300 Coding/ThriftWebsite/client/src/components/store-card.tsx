import { Link } from "wouter";
import { Card, CardContent } from "@/components/ui/card";
import StarRating from "@/components/star-rating";

interface StoreCardProps {
  place_id: string;
  name: string;
  address: string;
  rating?: number;
  user_ratings_total?: number;
  categories: string[];
  distance?: number;
}

export default function StoreCard({
  place_id,
  name,
  address,
  rating,
  user_ratings_total,
  categories,
  distance,
}: StoreCardProps) {
  return (
    <Card className="mb-4 border border-gray-100 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <Link href={`/store/${place_id}`}>
          <div className="flex justify-between items-start cursor-pointer">
            <div className="flex-grow">
              <h2 className="text-lg font-medium text-gray-800 dark:text-gray-200">{name}</h2>
              <div className="flex items-center mt-1">
                {rating ? (
                  <>
                    <StarRating rating={rating} className="mr-2" />
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {rating.toFixed(1)} ({user_ratings_total})
                    </span>
                  </>
                ) : (
                  <span className="text-sm text-gray-400 dark:text-gray-500">No ratings yet</span>
                )}
              </div>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{address}</p>

              <div className="flex flex-wrap gap-1 mt-2">
                {categories.map((category) => (
                  <span 
                    key={category}
                    className="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-full"
                  >
                    {category}
                  </span>
                ))}
              </div>
            </div>
            {distance !== undefined && (
              <div className="flex flex-col items-end">
                <span className="inline-block px-2 py-1 bg-primary/10 dark:bg-indigo-900/30 text-primary dark:text-indigo-400 text-xs font-medium rounded-full">
                  {distance < 1 
                    ? `${(distance * 5280).toFixed(0)} ft` 
                    : `${distance.toFixed(1)} mi`}
                </span>
              </div>
            )}
          </div>
        </Link>
      </CardContent>
    </Card>
  );
}
