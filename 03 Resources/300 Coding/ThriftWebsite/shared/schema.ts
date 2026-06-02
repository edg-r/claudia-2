import { pgTable, text, serial, integer, boolean, doublePrecision, timestamp, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;

// Thrift store schema
export const stores = pgTable("stores", {
  id: serial("id").primaryKey(),
  place_id: text("place_id").notNull().unique(),
  name: text("name").notNull(),
  address: text("address").notNull(),
  phone: text("phone"),
  website: text("website"),
  rating: doublePrecision("rating"),
  user_ratings_total: integer("user_ratings_total"),
  lat: doublePrecision("lat").notNull(),
  lng: doublePrecision("lng").notNull(),
  categories: text("categories").array(),
  last_updated: timestamp("last_updated").defaultNow(),
});

export const reviews = pgTable("reviews", {
  id: serial("id").primaryKey(),
  store_id: integer("store_id").references(() => stores.id).notNull(),
  author: text("author").notNull(),
  rating: integer("rating").notNull(),
  text: text("text").notNull(),
  time: timestamp("time").defaultNow(),
});

// Create schemas for inserts
export const insertStoreSchema = createInsertSchema(stores).omit({
  id: true,
  last_updated: true,
});

export const insertReviewSchema = createInsertSchema(reviews).omit({
  id: true,
});

// Create types
export type Store = typeof stores.$inferSelect;
export type InsertStore = z.infer<typeof insertStoreSchema>;
export type Review = typeof reviews.$inferSelect;
export type InsertReview = z.infer<typeof insertReviewSchema>;

// Create a view schema for client consumption that includes all fields
export const storeResponseSchema = z.object({
  place_id: z.string(),
  name: z.string(),
  address: z.string(),
  phone: z.string().nullable(),
  website: z.string().nullable(),
  rating: z.number().optional(),
  user_ratings_total: z.number().optional(),
  lat: z.number(),
  lng: z.number(),
  categories: z.array(z.string()),
  distance: z.number().optional(),
  reviews: z.array(z.object({
    author: z.string(),
    rating: z.number(),
    text: z.string(),
    time: z.number()
  })).optional()
});

export type StoreResponse = z.infer<typeof storeResponseSchema>;
