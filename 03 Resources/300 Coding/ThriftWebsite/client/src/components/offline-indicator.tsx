import { useEffect, useState } from "react";
import { Wifi, WifiOff } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function OfflineIndicator() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const { toast } = useToast();
  
  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      toast({
        title: "You're back online",
        description: "Connected to the network",
        variant: "default",
      });
    };
    
    const handleOffline = () => {
      setIsOnline(false);
      toast({
        title: "You're offline",
        description: "Some features may be unavailable",
        variant: "destructive",
      });
    };
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [toast]);
  
  if (isOnline) return null;
  
  return (
    <div 
      className="fixed bottom-24 left-1/2 transform -translate-x-1/2 bg-destructive text-destructive-foreground px-4 py-2 rounded-lg shadow-lg z-40"
      aria-live="assertive"
    >
      <div className="flex items-center">
        <WifiOff className="h-5 w-5 mr-2" />
        <span>You're offline. Some features may be unavailable.</span>
      </div>
    </div>
  );
}
