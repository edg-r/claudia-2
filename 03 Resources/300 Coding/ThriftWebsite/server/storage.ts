import { stores, reviews, type Store, type InsertStore, type Review, type InsertReview, type User, type InsertUser, users } from "@shared/schema";
import { db } from "./db";
import { eq, and, ilike, desc, asc, sql } from "drizzle-orm";
import { z } from "zod";

export interface IStorage {
  // User methods
  getUser(id: number): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  
  // Store methods
  getStores(): Promise<Store[]>;
  getStoreById(id: number): Promise<Store | undefined>;
  getStoreByPlaceId(placeId: string): Promise<Store | undefined>;
  createStore(store: InsertStore): Promise<Store>;
  updateStore(placeId: string, store: Partial<InsertStore>): Promise<Store | undefined>;
  searchStores(query: string): Promise<Store[]>;
  getStoresByCategory(category: string): Promise<Store[]>;
  getNearbyStores(lat: number, lng: number, radius?: number): Promise<(Store & { distance: number })[]>;
  
  // Review methods
  getReviewsByStoreId(storeId: number): Promise<Review[]>;
  addReview(review: InsertReview): Promise<Review>;
}

export class DatabaseStorage implements IStorage {
  // User methods
  async getUser(id: number): Promise<User | undefined> {
    const [user] = await db.select().from(users).where(eq(users.id, id));
    return user;
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    const [user] = await db.select().from(users).where(eq(users.username, username));
    return user;
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const [user] = await db.insert(users).values(insertUser).returning();
    return user;
  }
  
  // Store methods
  async getStores(): Promise<Store[]> {
    return db.select().from(stores).orderBy(desc(stores.rating));
  }
  
  async getStoreById(id: number): Promise<Store | undefined> {
    const [store] = await db.select().from(stores).where(eq(stores.id, id));
    return store;
  }
  
  async getStoreByPlaceId(placeId: string): Promise<Store | undefined> {
    const [store] = await db.select().from(stores).where(eq(stores.place_id, placeId));
    return store;
  }
  
  async createStore(store: InsertStore): Promise<Store> {
    const [newStore] = await db.insert(stores).values(store).returning();
    return newStore;
  }
  
  async updateStore(placeId: string, storeData: Partial<InsertStore>): Promise<Store | undefined> {
    const [updatedStore] = await db
      .update(stores)
      .set({ ...storeData, last_updated: new Date() })
      .where(eq(stores.place_id, placeId))
      .returning();
    return updatedStore;
  }
  
  async searchStores(query: string): Promise<Store[]> {
    return db
      .select()
      .from(stores)
      .where(ilike(stores.name, `%${query}%`))
      .orderBy(desc(stores.rating));
  }
  
  async getStoresByCategory(category: string): Promise<Store[]> {
    // Using SQL 'ANY' to check if the category exists in the array
    return db
      .select()
      .from(stores)
      .where(sql`${category} = ANY(${stores.categories})`)
      .orderBy(desc(stores.rating));
  }
  
  async getNearbyStores(lat: number, lng: number, radius: number = 50): Promise<(Store & { distance: number })[]> {
    // Calculate distance using Haversine formula
    const distanceCalc = sql`
      (
        6371 * acos(
          cos(radians(${lat})) 
          * cos(radians(${stores.lat})) 
          * cos(radians(${stores.lng}) - radians(${lng})) 
          + sin(radians(${lat})) 
          * sin(radians(${stores.lat}))
        )
      ) as distance
    `;
    
    const result = await db
      .select({
        id: stores.id,
        place_id: stores.place_id,
        name: stores.name,
        address: stores.address,
        phone: stores.phone,
        website: stores.website,
        rating: stores.rating,
        user_ratings_total: stores.user_ratings_total,
        lat: stores.lat,
        lng: stores.lng,
        categories: stores.categories,
        last_updated: stores.last_updated,
        distance: distanceCalc,
      })
      .from(stores)
      .having(sql`distance <= ${radius}`)
      .orderBy(asc(sql`distance`), desc(stores.rating));
      
    return result;
  }
  
  // Review methods
  async getReviewsByStoreId(storeId: number): Promise<Review[]> {
    return db
      .select()
      .from(reviews)
      .where(eq(reviews.store_id, storeId))
      .orderBy(desc(reviews.time));
  }
  
  async addReview(review: InsertReview): Promise<Review> {
    const [newReview] = await db.insert(reviews).values(review).returning();
    return newReview;
  }
}

export const storage = new DatabaseStorage();
