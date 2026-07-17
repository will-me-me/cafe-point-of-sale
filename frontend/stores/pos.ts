// stores/pos.ts
import { defineStore } from "pinia";

// Updated Product interface to match API response
interface Product {
  id: string;
  _id: string;
  name: string;
  sku: string;
  barcode: string;
  product_type: string;
  category_id: string;
  brand_id: string;
  pricing: {
    cost_price: number;
    selling_price: number;
    price_tiers: {
      retail: number;
      wholesale: number;
      dealer: number;
      vip: number;
      member: number;
    };
    is_taxable: boolean;
    margin: number;
    markup: number;
  };
  inventory: {
    quantity: number;
    reserved: number;
    available: number;
    reorder_level: number;
    status: string;
    location: string;
    shelf_number: string;
  };
  has_variants: boolean;
  variants: any[];
  is_active: boolean;
  is_featured: boolean;
  tags: string[];
  image_url?: string;
  created_at: string;
  updated_at: string;
}

interface CartItem {
  id: number;
  productId: string;
  name: string;
  sku: string;
  barcode?: string;
  variant_id?: string;
  size: string;
  temp: string;
  modifier: string;
  price: number;
  quantity: number;
  unitPrice: number;
}

interface Category {
  id: string;
  name: string;
  itemCount: number;
  status: "available" | "restock";
  icon: string;
  gradient: string;
}

interface Order {
  id: string;
  items: CartItem[];
  subtotal: number;
  tax: number;
  total: number;
  date: string;
  paymentMode: string;
  paymentStatus: string;
}

export const usePosStore = defineStore("pos", {
  state: () => ({
    AllOrders: [] as Order[],
    paymentMode: "cash" as "cash" | "mpesa" | "debt",

    categories: [
      {
        id: "coffee",
        name: "Coffee",
        itemCount: 50,
        status: "available" as const,
        icon: "🍃",
        gradient: "linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%)",
      },
      {
        id: "tea",
        name: "Tea",
        itemCount: 20,
        status: "available" as const,
        icon: "🫖",
        gradient: "#f5f3ed",
      },
      {
        id: "snack",
        name: "Snack",
        itemCount: 10,
        status: "restock" as const,
        icon: "🍪",
        gradient: "#f5f3ed",
      },
    ] as Category[],

    products: [] as Product[],
    searchQuery: "",
    cart: [] as CartItem[],
    selectedCategory: "coffee" as string,
    nextCartId: 1,
  }),

  getters: {
    filteredProducts: (state) => {
      let filtered = state.products;
      console.log(filtered, "All products before filtering");

      // Filter by category
      if (state.selectedCategory) {
        // Map category names to product types or categories
        // You might need to adjust this mapping based on your data
        filtered = filtered.filter((product) => {
          // If product has category_id, try to match
          if (product.category_id) {
            // For now, just show all products since we don't have category mapping
            return true;
          }
          return true;
        });
      }

      // Filter by search query
      if (state.searchQuery) {
        const query = state.searchQuery.toLowerCase();
        filtered = filtered.filter(
          (product) =>
            product.name.toLowerCase().includes(query) ||
            product.sku.toLowerCase().includes(query) ||
            (product.barcode && product.barcode.includes(query))
        );
      }

      return filtered;
    },

    filteredCategories: (state) => {
      return state.categories.filter((category) =>
        state.products.some((product) => {
          // Check if product belongs to this category
          // This mapping needs to be adjusted based on your actual data
          return true;
        })
      );
    },

    cartItems: (state) => state.cart,

    hasCartItems: (state) => state.cart.length > 0,

    subtotal: (state) => {
      return parseFloat(
        state.cart
          .reduce((sum, item) => sum + item.unitPrice * item.quantity, 0)
          .toFixed(2)
      );
    },

    tax(state) {
      return parseFloat((this.subtotal * 0.1).toFixed(2));
    },

    total(state) {
      return parseFloat((this.subtotal + this.tax).toFixed(2));
    },
  },

  actions: {
    setCategory(category: string) {
      this.selectedCategory = category;
    },

    setSearchQuery(query: string) {
      this.searchQuery = query;
    },

    async addProduct(productData: any) {
      const authStore = useAuthStore();

      try {
        console.log("📤 Sending to backend");
        console.log(JSON.stringify(productData, null, 2));

        const response = await fetch("http://127.0.0.1:8000/products/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authStore.token}`,
          },
          body: JSON.stringify(productData),
        });

        if (!response.ok) {
          const errorText = await response.text();

          console.error("❌ Backend Error");
          console.error(errorText);

          throw new Error(`HTTP ${response.status}: ${errorText}`);
        }

        const product = await response.json();

        console.log("✅ Product created");
        console.log(product);

        await this.getAllProducts();

        return product;
      } catch (err) {
        console.error("❌ addProduct()");
        console.error(err);
        throw err;
      }
    },

    async addBrand(brandData: any) {
      const authStore = useAuthStore();

      try {
        const brand = {
          name: brandData.name,
          description: brandData.description || "",
          logo_url: brandData.logo_url || "",
          website: brandData.website || "",
          is_active:
            brandData.is_active !== undefined ? brandData.is_active : true,
        };

        console.log("📤 Sending brand data:", JSON.stringify(brand, null, 2));

        const response = await fetch("http://127.0.0.1:8000/brands/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authStore.token}`,
          },
          body: JSON.stringify(brand),
        });

        if (!response.ok) {
          const errorText = await response.text();
          console.error("❌ Brand creation failed:", errorText);
          throw new Error(
            `HTTP error! status: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        await this.getAllBrands(); // Refresh the brands list after adding a new brand
        console.log("✅ Brand added successfully:", data);
        return data;
      } catch (error) {
        console.error("❌ Error adding brand:", error);
        throw error;
      }
    },

    // Get single product by ID
    async getProductById(id: string) {
      try {
        // const authStore = useAuthStore();

        const response = await fetch(`http://127.0.0.1:8000/products/${id}`, {
          method: "GET",
          headers: {
            Accept: "application/json",
            // Authorization: `Bearer ${authStore.token}`,
          },
        });

        if (!response.ok) {
          throw new Error(await response.text());
        }

        const product = await response.json();

        console.log("✅ Product loaded", product);

        return product;
      } catch (err) {
        console.error("❌ getProductById()", err);
        throw err;
      }
    },
    // Update product
    async updateProduct(id: string, productData: any) {
      const authStore = useAuthStore();

      try {
        console.log("📤 Updating product");
        console.log(JSON.stringify(productData, null, 2));

        const response = await fetch(`http://127.0.0.1:8000/products/${id}`, {
          method: "PUT",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
            Authorization: `Bearer ${authStore.token}`,
          },
          body: JSON.stringify(productData),
        });

        if (!response.ok) {
          const error = await response.text();
          console.error("❌ Update failed:", error);
          throw new Error(error);
        }

        const updated = await response.json();

        console.log("✅ Product updated", updated);

        // Refresh cached list
        await this.getAllProducts();

        return updated;
      } catch (err) {
        console.error("❌ updateProduct()", err);
        throw err;
      }
    },

    async getAllBrands() {
      // const authStore = useAuthStore();

      try {
        const response = await fetch("http://127.0.0.1:8000/brands/", {
          method: "GET",
          headers: {
            // Authorization: `Bearer ${authStore.token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          const errorText = await response.text();
          console.error("❌ Brands fetch failed:", errorText);
          throw new Error(
            `HTTP error! status: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        console.log("✅ Brands fetched successfully:", data);

        // Store brands in state if you have a brands array
        // this.brands = data;

        return data;
      } catch (error) {
        console.error("❌ Error fetching brands:", error);
        throw error;
      }
    },
    async getAllCategories() {
      const authStore = useAuthStore();

      try {
        const response = await fetch("http://127.0.0.1:8000/categories/", {
          method: "GET",
          headers: {
            // Authorization: `Bearer ${authStore.token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          const errorText = await response.text();
          console.error("❌ Categories fetch failed:", errorText);
          throw new Error(
            `HTTP error! status: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        console.log("✅ Categories fetched successfully:", data);

        // Store categories in state if you have a categories array
        // this.categories = data;

        return data;
      } catch (error) {
        console.error("❌ Error fetching categories:", error);
        throw error;
      }
    },

    async addCategory(categoryData: any) {
      const authStore = useAuthStore();

      try {
        const category = {
          name: categoryData.name,
          parent_id: categoryData.parent_id || null,
          description: categoryData.description || "",
          image_url: categoryData.image_url || "",
          is_active:
            categoryData.is_active !== undefined
              ? categoryData.is_active
              : true,
          sort_order: categoryData.sort_order || 0,
        };

        console.log(
          "📤 Sending category data:",
          JSON.stringify(category, null, 2)
        );

        const response = await fetch("http://127.0.0.1:8000/categories/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authStore.token}`,
          },
          body: JSON.stringify(category),
        });

        if (!response.ok) {
          const errorText = await response.text();
          console.error("❌ Category creation failed:", errorText);
          throw new Error(
            `HTTP error! status: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        console.log("✅ Category added successfully:", data);
        return data;
      } catch (error) {
        console.error("❌ Error adding category:", error);
        throw error;
      }
    },

    async addSupplier(supplierData: any) {
      const authStore = useAuthStore();

      try {
        const supplier = {
          name: supplierData.name,
          code: supplierData.code || "",
          contact: {
            name: supplierData.contact_name || "",
            phone: supplierData.phone || "",
            email: supplierData.email || "",
            address: {
              street: supplierData.street || "",
              city: supplierData.city || "",
              state: supplierData.state || "",
              country: supplierData.country || "Kenya",
              postal_code: supplierData.postal_code || "",
            },
          },
          tax_id: supplierData.tax_id || "",
          website: supplierData.website || "",
          notes: supplierData.notes || "",
          is_active:
            supplierData.is_active !== undefined
              ? supplierData.is_active
              : true,
        };

        console.log(
          "📤 Sending supplier data:",
          JSON.stringify(supplier, null, 2)
        );

        const response = await fetch(
          "http://127.0.0.1:8000/api/v1/suppliers/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${authStore.token}`,
            },
            body: JSON.stringify(supplier),
          }
        );

        if (!response.ok) {
          const errorText = await response.text();
          console.error("❌ Supplier creation failed:", errorText);
          throw new Error(
            `HTTP error! status: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        console.log("✅ Supplier added successfully:", data);
        return data;
      } catch (error) {
        console.error("❌ Error adding supplier:", error);
        throw error;
      }
    },
    async getAllSuppliers() {
      // const authStore = useAuthStore();

      try {
        const response = await fetch("http://127.0.0.1:8000/suppliers/", {
          method: "GET",
          headers: {
            // Authorization: `Bearer ${authStore.token}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          const errorText = await response.text();
          console.error("❌ Suppliers fetch failed:", errorText);
          throw new Error(
            `HTTP error! status: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        console.log("✅ Suppliers fetched successfully:", data);

        // Store suppliers in state if you have a suppliers array
        // this.suppliers = data;

        return data;
      } catch (error) {
        console.error("❌ Error fetching suppliers:", error);
        throw error;
      }
    },
    async updateSupplier(supplierId: string, supplierData: any) {
      const authStore = useAuthStore();

      try {
        const supplier = {
          name: supplierData.name,
          code: supplierData.code || "",
          contact: {
            name: supplierData.contact_name || "",
            phone: supplierData.phone || "",
            email: supplierData.email || "",
            address: {
              street: supplierData.street || "",
              city: supplierData.city || "",
              state: supplierData.state || "",
              country: supplierData.country || "Kenya",
              postal_code: supplierData.postal_code || "",
            },
          },
          tax_id: supplierData.tax_id || "",
          website: supplierData.website || "",
          notes: supplierData.notes || "",
          is_active:
            supplierData.is_active !== undefined
              ? supplierData.is_active
              : true,
        };

        const response = await fetch(
          `http://127.0.0.1:8000/suppliers/${supplierId}`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${authStore.token}`,
            },
            body: JSON.stringify(supplier),
          }
        );

        if (!response.ok) {
          const errorText = await response.text();
          console.error("❌ Supplier update failed:", errorText);
          throw new Error(
            `HTTP error! status: ${response.status} - ${errorText}`
          );
        }

        const data = await response.json();
        console.log("✅ Supplier updated successfully:", data);
        return data;
      } catch (error) {
        console.error("❌ Error updating supplier:", error);
        throw error;
      }
    },

    async deleteSupplier(supplierId: string) {
      const authStore = useAuthStore();

      try {
        const response = await fetch(
          `http://127.0.0.1:8000/suppliers/${supplierId}`,
          {
            method: "DELETE",
            headers: {
              Authorization: `Bearer ${authStore.token}`,
            },
          }
        );

        if (!response.ok) {
          const errorText = await response.text();
          console.error("❌ Supplier delete failed:", errorText);
          throw new Error(
            `HTTP error! status: ${response.status} - ${errorText}`
          );
        }

        console.log("✅ Supplier deleted successfully");
        return true;
      } catch (error) {
        console.error("❌ Error deleting supplier:", error);
        throw error;
      }
    },

    async getAllOrders() {
      const authStore = useAuthStore();

      try {
        const response = await fetch("http://127.0.0.1:8000/orders/", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${authStore.token}`,
          },
        });
        const data = await response.json();
        console.log("Orders fetched:", data);
        this.AllOrders = data;
        return data;
      } catch (error) {
        console.error("Error fetching orders:", error);
      }
    },

    async getAllProducts() {
      try {
        const response = await fetch("http://127.0.0.1:8000/products/");
        const data = await response.json();
        console.log("Products fetched:", data);

        // Map API products to the store format
        this.products = data.map((product: any) => ({
          ...product,
          id: product.id || product._id,
          // Map pricing
          pricing: {
            ...product.pricing,
            selling_price: product.pricing?.selling_price || 0,
            cost_price: product.pricing?.cost_price || 0,
          },
          // Map inventory
          inventory: {
            ...product.inventory,
            quantity: product.inventory?.quantity || 0,
            available: product.inventory?.available || 0,
            status: product.inventory?.status || "in_stock",
          },
          // Use first tag as category fallback
          category: product.tags?.[0] || "coffee",
          price: product.pricing?.selling_price || 0,
          image_url: product.image_url || product.media?.images?.[0]?.url || "",
        }));

        return data;
      } catch (error) {
        console.error("Error fetching products:", error);
        this.products = [];
        return [];
      }
    },

    async saveOrder(orderData: any) {
      const authStore = useAuthStore();

      try {
        // Ensure we have the correct product IDs
        const products = this.products || [];

        const order = {
          order_type: orderData.orderType || "takeaway",
          customer_id: orderData.customerId || null,
          customer_name: orderData.customerName || "Guest",
          customer_phone: orderData.customerPhone || "",
          customer_email: orderData.customerEmail || "",
          table_number: orderData.tableNumber || null,
          branch_id: orderData.branchId || null,
          items: orderData.items.map((item: any) => {
            let productId = item.productId || item.id;
            let sku = item.sku || "";
            let barcode = item.barcode || "";
            let productName = item.name || item.product_name || "";

            if (
              productId &&
              typeof productId === "string" &&
              productId.length < 20
            ) {
              const foundProduct = products.find(
                (p) => p.sku === productId || p.id === productId
              );
              if (foundProduct) {
                productId = foundProduct.id || foundProduct._id;
                sku = foundProduct.sku || sku;
                barcode = foundProduct.barcode || barcode;
                productName = foundProduct.name || productName;
              }
            }

            return {
              product_id: productId,
              variant_id: item.variant_id || null,
              product_name: productName,
              sku: sku,
              barcode: barcode,
              quantity: item.quantity || 1,
              unit_price: item.unitPrice || item.price || 0,
              total_price:
                (item.unitPrice || item.price || 0) * (item.quantity || 1),
              cost_price: item.cost_price || null,
              discount: item.discount || 0,
              tax_amount: item.tax_amount || 0,
              weight: item.weight || null,
              batch_number: item.batch_number || null,
              serial_numbers: item.serial_numbers || [],
            };
          }),
          subtotal: orderData.subtotal || 0,
          tax: orderData.tax || 0,
          discount_total: orderData.discount_total || 0,
          total: orderData.total || 0,
          receipt_number: orderData.receiptNumber || null,
          payment_mode: orderData.paymentMode || "cash",
          // FIXED: Use 'paid' instead of 'completed'
          payment_status: orderData.paymentStatus || "paid",
          order_status: "completed", // This is correct for order_status
          notes: orderData.notes || "",
          created_at: new Date().toISOString(),
          created_by: authStore.user?.id || null,
          sales_agent: orderData.cashier || authStore.user?.name || "Cashier",
        };

        console.log("📤 Sending order data:", JSON.stringify(order, null, 2));

        const res = await fetch("http://127.0.0.1:8000/orders/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authStore.token}`,
          },
          body: JSON.stringify(order),
        });

        if (!res.ok) {
          const errorText = await res.text();
          console.error("❌ Order creation failed:", errorText);
          console.error("❌ Status:", res.status);
          console.error("❌ Status Text:", res.statusText);
          throw new Error(`HTTP error! status: ${res.status} - ${errorText}`);
        }

        const data = await res.json();
        console.log("✅ Order saved successfully:", data);
        return data;
      } catch (error) {
        console.error("❌ Error saving order:", error);
        throw error;
      }
    },

    addToCart(product: any) {
      // Find if product already in cart
      const existingItem = this.cart.find(
        (item) => item.productId === (product.id || product._id)
      );

      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        // Get price from product
        const price = product.pricing?.selling_price || product.price || 0;

        const newItem: CartItem = {
          id: this.nextCartId++,
          productId: product.id || product._id,
          name: product.name,
          sku: product.sku || "",
          barcode: product.barcode || "",
          variant_id: null,
          size: "Regular",
          temp: "Hot",
          modifier: "Standard",
          price: price,
          quantity: 1,
          unitPrice: price,
        };

        this.cart.push(newItem);
        console.log("Added to cart:", newItem);
      }
    },

    addVariantToCart(product: any, variant: any) {
      const price =
        variant.pricing?.selling_price || product.pricing?.selling_price || 0;

      const newItem: CartItem = {
        id: this.nextCartId++,
        productId: product.id || product._id,
        name: `${product.name} - ${variant.variant_name}`,
        sku: variant.sku || product.sku || "",
        barcode: variant.barcode || product.barcode || "",
        variant_id: variant.sku || variant.id,
        size: variant.attributes?.size || "Regular",
        temp: "Hot",
        modifier: variant.attributes?.flavor || "Standard",
        price: price,
        quantity: 1,
        unitPrice: price,
      };

      this.cart.push(newItem);
      console.log("Added variant to cart:", newItem);
    },

    incrementQuantity(itemId: number) {
      const item = this.cart.find((i) => i.id === itemId);
      if (item) {
        item.quantity += 1;
      }
    },

    decrementQuantity(itemId: number) {
      const item = this.cart.find((i) => i.id === itemId);
      if (item && item.quantity > 1) {
        item.quantity--;
      } else if (item && item.quantity === 1) {
        this.removeFromCart(itemId);
      }
    },

    removeFromCart(itemId: number) {
      const index = this.cart.findIndex((i) => i.id === itemId);
      if (index > -1) {
        this.cart.splice(index, 1);
      }
    },

    clearCart() {
      this.cart = [];
    },

    async updateDebtOrderStatus(orderId: string) {
      const authStore = useAuthStore();

      try {
        const response = await fetch(
          `http://127.0.0.1:8000/reports/debt/${orderId}/pay`,
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${authStore.token}`,
            },
          }
        );
        if (!response.ok) {
          const errText = await response.text();
          console.error("Server response:", errText);
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("✅ Order status updated successfully:", data);
        return data;
      } catch (error) {
        console.error("❌ Error updating order status:", error);
        throw error;
      }
    },

    async getDebtOverview() {
      const authStore = useAuthStore();
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/reports/debt/overview",
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${authStore.token}`,
            },
          }
        );

        if (!response.ok) {
          const errText = await response.text();
          console.error("Server response:", errText);
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("✅ Debt overview fetched successfully:", data);
        return data;
      } catch (error) {
        console.error("❌ Error fetching debt overview:", error);
        throw error;
      }
    },
  },

  persist: {
    storage: localStorage,
    paths: ["cart", "paymentMode"],
  },
});
