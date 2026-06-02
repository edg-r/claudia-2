import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { z, ZodError } from "zod";
import { fromZodError } from "zod-validation-error";
import rateLimit from "express-rate-limit";

// Rate limiter
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
});

export async function registerRoutes(app: Express): Promise<Server> {
  // Apply rate limiter to all API routes
  app.use("/api", apiLimiter);

  // Get all stores
  app.get("/api/stores", async (req, res) => {
    try {
      const stores = await storage.getStores();
      res.json(stores);
    } catch (error) {
      console.error("Error fetching stores:", error);
      res.status(500).json({ message: "Failed to fetch stores" });
    }
  });

  // Get a store by place_id
  app.get("/api/stores/:placeId", async (req, res) => {
    try {
      const { placeId } = req.params;
      
      const store = await storage.getStoreByPlaceId(placeId);
      if (!store) {
        return res.status(404).json({ message: "Store not found" });
      }
      
      // Get reviews
      const storeReviews = await storage.getReviewsByStoreId(store.id);
      
      // Format the response with reviews
      const response = {
        ...store,
        reviews: storeReviews.map(review => ({
          author: review.author,
          rating: review.rating,
          text: review.text,
          time: review.time ? Math.floor(review.time.getTime() / 1000) : null
        }))
      };
      
      res.json(response);
    } catch (error) {
      console.error("Error fetching store:", error);
      res.status(500).json({ message: "Failed to fetch store" });
    }
  });

  // Search stores by query
  app.get("/api/stores/search/:query", async (req, res) => {
    try {
      const { query } = req.params;
      const stores = await storage.searchStores(query);
      res.json(stores);
    } catch (error) {
      console.error("Error searching stores:", error);
      res.status(500).json({ message: "Failed to search stores" });
    }
  });

  // Get stores by category
  app.get("/api/stores/category/:category", async (req, res) => {
    try {
      const { category } = req.params;
      const stores = await storage.getStoresByCategory(category);
      res.json(stores);
    } catch (error) {
      console.error("Error fetching stores by category:", error);
      res.status(500).json({ message: "Failed to fetch stores by category" });
    }
  });

  // Get nearby stores
  app.get("/api/stores/nearby/:lat/:lng", async (req, res) => {
    try {
      const latParam = z.coerce.number().safeParse(req.params.lat);
      const lngParam = z.coerce.number().safeParse(req.params.lng);
      const radiusParam = z.coerce.number().optional().safeParse(req.query.radius);
      
      if (!latParam.success || !lngParam.success) {
        return res.status(400).json({ message: "Invalid coordinates" });
      }
      
      const lat = latParam.data;
      const lng = lngParam.data;
      const radius = radiusParam.success ? radiusParam.data : undefined;
      
      const stores = await storage.getNearbyStores(lat, lng, radius);
      res.json(stores);
    } catch (error) {
      console.error("Error fetching nearby stores:", error);
      res.status(500).json({ message: "Failed to fetch nearby stores" });
    }
  });

  // Create a store
  app.post("/api/stores", async (req, res) => {
    try {
      const storeData = req.body;
      const store = await storage.createStore(storeData);
      res.status(201).json(store);
    } catch (error) {
      console.error("Error creating store:", error);
      if (error instanceof ZodError) {
        return res.status(400).json({ 
          message: "Invalid store data", 
          errors: fromZodError(error).message 
        });
      }
      res.status(500).json({ message: "Failed to create store" });
    }
  });

  // Update a store
  app.put("/api/stores/:placeId", async (req, res) => {
    try {
      const { placeId } = req.params;
      const storeData = req.body;
      
      const updatedStore = await storage.updateStore(placeId, storeData);
      if (!updatedStore) {
        return res.status(404).json({ message: "Store not found" });
      }
      
      res.json(updatedStore);
    } catch (error) {
      console.error("Error updating store:", error);
      if (error instanceof ZodError) {
        return res.status(400).json({ 
          message: "Invalid store data", 
          errors: fromZodError(error).message 
        });
      }
      res.status(500).json({ message: "Failed to update store" });
    }
  });

  // Add a review to a store
  app.post("/api/stores/:placeId/reviews", async (req, res) => {
    try {
      const { placeId } = req.params;
      const reviewData = req.body;
      
      // Get store id from place_id
      const store = await storage.getStoreByPlaceId(placeId);
      if (!store) {
        return res.status(404).json({ message: "Store not found" });
      }
      
      // Add store id to review data
      const review = await storage.addReview({
        ...reviewData,
        store_id: store.id
      });
      
      res.status(201).json(review);
    } catch (error) {
      console.error("Error adding review:", error);
      if (error instanceof ZodError) {
        return res.status(400).json({ 
          message: "Invalid review data", 
          errors: fromZodError(error).message 
        });
      }
      res.status(500).json({ message: "Failed to add review" });
    }
  });

  const httpServer = createServer(app);
  return httpServer;
}
