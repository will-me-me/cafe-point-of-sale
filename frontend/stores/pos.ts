import { defineStore } from "pinia";

interface Product {
  id: number;
  name: string;
  price: number;
  category: "coffee" | "tea" | "snack";
}

interface CartItem {
  id: number;
  productId: number;
  name: string;
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
interface Oders {
  id: number;
  items: CartItem[];
  subtotal: number;
  tax: number;
  total: number;
  date: string;
}

export const usePosStore = defineStore("pos", {
  state: () => ({
    AllOrders: [] as Oders[],

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

    products: [
      // { id: 1, name: "Espresso", price: 4.2, category: "coffee" as const },
      // { id: 2, name: "Cappuchino", price: 3.3, category: "coffee" as const },
      // { id: 3, name: "Latte", price: 4.0, category: "coffee" as const },
      // { id: 4, name: "Americano", price: 4.0, category: "coffee" as const },
      // { id: 5, name: "Mocha", price: 4.0, category: "coffee" as const },
      // {
      //   id: 6,
      //   name: "Iced Coffee Milk",
      //   price: 3.8,
      //   category: "coffee" as const,
      // },
      // { id: 7, name: "Cold Brew", price: 4.0, category: "coffee" as const },
      // { id: 8, name: "Flat White", price: 3.8, category: "coffee" as const },
      // { id: 9, name: "Caramel Mac", price: 4.0, category: "coffee" as const },
      // {
      //   id: 10,
      //   name: "Salted Caramel",
      //   price: 4.2,
      //   category: "coffee" as const,
      // },
      // {
      //   id: 11,
      //   name: "Hazelnut Latte",
      //   price: 4.0,
      //   category: "coffee" as const,
      // },
      // { id: 12, name: "Pour Over", price: 4.0, category: "coffee" as const },
      // { id: 13, name: "Green Tea", price: 3.5, category: "tea" as const },
      // { id: 14, name: "Black Tea", price: 3.5, category: "tea" as const },
      // { id: 15, name: "Chamomile", price: 3.8, category: "tea" as const },
      // { id: 16, name: "Earl Grey", price: 3.5, category: "tea" as const },
      // { id: 17, name: "Matcha Latte", price: 4.5, category: "tea" as const },
      // { id: 18, name: "Croissant", price: 3.5, category: "snack" as const },
      // { id: 19, name: "Muffin", price: 3.0, category: "snack" as const },
      // { id: 20, name: "Cookie", price: 2.5, category: "snack" as const },
      // { id: 21, name: "Brownie", price: 3.5, category: "snack" as const },
      // { id: 22, name: "Bagel", price: 2.0, category: "snack" as const },
      // { id: 23, name: "Scone", price: 3.0, category: "snack" as const },
      // { id: 24, name: "Donut", price: 2.5, category: "snack" as const },
      // { id: 25, name: "Pancake", price: 4.0, category: "snack" as const },
    ] as Product[],

    cart: [] as CartItem[],
    selectedCategory: "coffee" as string,
    nextCartId: 1,
  }),

  getters: {
    filteredProducts: (state) => {
      return state.products.filter(
        (product) => product.category === state.selectedCategory
      );
    },

    filteredCategories: (state) => {
      return state.categories.filter((category) =>
        state.products.some((product) => product.category === category.id)
      );
    },

    cartItems: (state) => state.cart,

    hasCartItems: (state) => state.cart.length > 0,

    subtotal: (state) => {
      // FIXED: Use unitPrice * quantity
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

    async addProduct(formData) {
      try {
        const res = await fetch("http://127.0.0.1:8000/products/", {
          method: "POST",
          body: formData,
        });

        if (!res.ok) {
          const errText = await res.text();
          console.error("Server response:", errText);
          throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();
        console.log("✅ Product added successfully:", data);
        return data;
      } catch (error) {
        console.error("❌ Error adding product:", error);
        throw error;
      }
    },
    async getAllOrders() {
      try {
        const response = await fetch("http://127.0.0.1:8000/orders/");
        const data = await response.json();
        console.log(data);
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
        console.log(data);
        this.products = data;
        return data;
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    },

    async saveOrder(orderData: any) {
      try {
        const order = {
          receiptNumber: orderData.receiptNumber,
          orderType: orderData.orderType,
          customerName: orderData.customerName,
          tableNumber: orderData.tableNumber,
          items: JSON.parse(JSON.stringify(orderData.items)),
          subtotal: orderData.subtotal,
          tax: orderData.tax,
          total: orderData.total,
        };

        const res = await fetch("http://127.0.0.1:8000/orders/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(order),
        });

        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();
        console.log("✅ Order saved successfully:", data);
        return data;
      } catch (error) {
        console.error("❌ Error saving order:", error);
        throw error;
      }
    },

    addToCart(product: Product) {
      const existingItem = this.cart.find(
        (item) => item.productId === product.id
      );

      if (existingItem) {
        // FIXED: Only increment quantity
        existingItem.quantity += 1;
        console.log("Updated existing item:", existingItem);
      } else {
        const newItem: CartItem = {
          id: this.nextCartId++,
          productId: product.id,
          name: product.name,
          size: "SB.4.2",
          temp: "Medium",
          modifier: "Less Sugar",
          price: product.price,
          quantity: 1,
          unitPrice: product.price,
        };
        console.log("Adding new item to cart:", newItem);
        this.cart.push(newItem);
      }
    },

    incrementQuantity(itemId: number) {
      const item = this.cart.find((i) => i.id === itemId);
      if (item) {
        item.quantity += 1;
        // FIXED: No price modification needed
      }
    },
    removeFromCart(itemId: number) {
      const index = this.cart.findIndex((i) => i.id === itemId);
      if (index > -1) {
        this.cart.splice(index, 1);
      }
    },

    decrementQuantity(itemId: number) {
      const item = this.cart.find((i) => i.id === itemId);
      if (item && item.quantity > 1) {
        item.quantity--;
        // FIXED: No price modification needed
      } else if (item && item.quantity === 1) {
        this.removeFromCart(itemId);
      }
    },

    clearCart() {
      this.cart = [];
    },
  },

  persist: true, // Enable persistence using pinia-plugin-persistedstate
});
