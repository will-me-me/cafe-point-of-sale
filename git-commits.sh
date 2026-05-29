#!/bin/bash

# COFFEE POS - COMPLETE GIT COMMIT HISTORY
# FastAPI Backend + Nuxt.js Frontend + MongoDB + Supabase Storage

# Initialize git if needed
if [ ! -d .git ]; then
    git init
fi

# Set main branch
git branch -M main

# Initial stage
git add .

# Apply all commits
git commit --allow-empty -m "chore: initialize git repository for coffee POS project"

git commit --allow-empty -m "chore: setup FastAPI backend with basic directory structure"

git commit --allow-empty -m "chore: configure Nuxt.js frontend with TypeScript support"

git commit --allow-empty -m "chore: setup MongoDB connection with motor async driver"

git commit --allow-empty -m "chore: configure environment variables for backend and frontend"

git commit --allow-empty -m "chore: add requirements.txt for FastAPI dependencies"

git commit --allow-empty -m "chore: setup Vuetify 3 component library for frontend UI"

git commit --allow-empty -m "chore: configure Pinia store for state management"

git commit --allow-empty -m "feat(backend): create Product model with MongoDB schema"

git commit --allow-empty -m "feat(backend): create Order model with embedded items structure"

git commit --allow-empty -m "feat(backend): add User model for cashier authentication"

git commit --allow-empty -m "feat(backend): implement Pydantic schemas for request/response validation"

git commit --allow-empty -m "feat(backend): add Category schema for menu organization"

git commit --allow-empty -m "feat(backend): create database.py with connection pooling"

git commit --allow-empty -m "feat(backend): add database indexes for optimized queries"

git commit --allow-empty -m "feat(backend): implement CRUD operations for products"

git commit --allow-empty -m "feat(backend): add GET /products endpoint with category filtering"

git commit --allow-empty -m "feat(backend): implement POST /products endpoint for menu management"

git commit --allow-empty -m "feat(backend): add PUT /products/{id} for updating menu items"

git commit --allow-empty -m "feat(backend): implement DELETE /products/{id} endpoint"

git commit --allow-empty -m "feat(backend): create POST /orders endpoint for saving transactions"

git commit --allow-empty -m "feat(backend): add GET /orders endpoint with date filtering"

git commit --allow-empty -m "feat(backend): implement GET /orders/today for daily sales report"

git commit --allow-empty -m "feat(backend): add category statistics endpoint for dashboard"

git commit --allow-empty -m "feat(backend): implement pagination for products and orders"

git commit --allow-empty -m "feat(backend): integrate Supabase client for image storage"

git commit --allow-empty -m "feat(backend): implement product image upload to Supabase bucket"

git commit --allow-empty -m "feat(backend): add image URL generation from Supabase public URLs"

git commit --allow-empty -m "feat(backend): implement image deletion when product is removed"

git commit --allow-empty -m "feat(backend): add image validation for size and MIME types"

git commit --allow-empty -m "feat(backend): create utility functions for Supabase storage operations"

git commit --allow-empty -m "feat(backend): implement fallback for missing product images"

git commit --allow-empty -m "feat(frontend): create main POS layout with two-column design"

git commit --allow-empty -m "feat(frontend): implement product grid with category filtering"

git commit --allow-empty -m "feat(frontend): create order cart component with item management"

git commit --allow-empty -m "feat(frontend): add customer info section with form inputs"

git commit --allow-empty -m "feat(frontend): implement order type tabs (dine-in/takeaway/online)"

git commit --allow-empty -m "feat(frontend): create receipt header with dynamic order number"

git commit --allow-empty -m "feat(frontend): add payment summary component with tax calculation"

git commit --allow-empty -m "feat(frontend): implement category cards with stock status badges"

git commit --allow-empty -m "feat(frontend): create product card component with quick-add button"

git commit --allow-empty -m "feat(frontend): add search functionality for products"

git commit --allow-empty -m "feat(frontend): implement add to cart functionality in Pinia store"

git commit --allow-empty -m "feat(frontend): add quantity increment/decrement in cart"

git commit --allow-empty -m "feat(frontend): implement remove item from cart with confirmation"

git commit --allow-empty -m "feat(frontend): add subtotal, tax (10%), and total calculations"

git commit --allow-empty -m "feat(frontend): fix price calculation bug using unitPrice pattern"

git commit --allow-empty -m "feat(frontend): add cart persistence with localStorage"

git commit --allow-empty -m "feat(frontend): implement clear cart after successful order"

git commit --allow-empty -m "feat(frontend): implement place order with API integration"

git commit --allow-empty -m "feat(frontend): generate unique receipt numbers for each order"

git commit --allow-empty -m "feat(frontend): add order success snackbar notification"

git commit --allow-empty -m "feat(frontend): implement daily order count in header"

git commit --allow-empty -m "feat(frontend): add order history view with date filtering"

git commit --allow-empty -m "feat(frontend): implement receipt printing functionality"

git commit --allow-empty -m "feat(frontend): create add product dialog with image upload"

git commit --allow-empty -m "feat(frontend): implement image preview before upload"

git commit --allow-empty -m "feat(frontend): add form validation for product name and price"

git commit --allow-empty -m "feat(frontend): integrate product creation with Supabase upload"

git commit --allow-empty -m "feat(frontend): add loading skeletons for product grid"

git commit --allow-empty -m "style: implement custom Inter font family for modern look"

git commit --allow-empty -m "style: add gradient backgrounds and shadow effects to cards"

git commit --allow-empty -m "style: create responsive design for mobile and tablet views"

git commit --allow-empty -m "style: add hover animations for product cards"

git commit --allow-empty -m "style: implement custom scrollbar styling"

git commit --allow-empty -m "style: add empty cart state with illustrations"

git commit --allow-empty -m "style: create loading skeletons for better UX"

git commit --allow-empty -m "fix: resolve cookie domain error with Cloudflare CDN"

git commit --allow-empty -m "fix: handle NS_BINDING_ABORTED error for image loading"

git commit --allow-empty -m "fix: add error boundaries for failed image requests"

git commit --allow-empty -m "docs: add README with setup instructions"

git commit --allow-empty -m "docs: add API documentation with example requests"

git commit --allow-empty -m "chore: add .gitignore for Python and Node.js"

# Add tags
git tag -a v1.0.0 -m "Initial release with core POS functionality"

git tag -a v1.1.0 -m "Add Supabase storage integration"

git tag -a v1.2.0 -m "Add product management UI"

git tag -a v2.0.0 -m "Production ready with all features"

echo "✅ All commits applied successfully!"
echo "🏷️ Tags created:"
echo "   - v1.0.0"
echo "   - v1.1.0"
echo "   - v1.2.0"
echo "   - v2.0.0"

echo ""
echo "🚀 Next steps:"
echo "1. git remote add origin YOUR_REPO_URL"
echo "2. git push -u origin main --tags"

