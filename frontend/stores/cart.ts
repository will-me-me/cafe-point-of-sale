import { defineStore } from "pinia";

export const useCartStore = defineStore("cart", {
  state: () => ({
    items: [] as { id: number; name: string; price: number; qty: number }[],
  }),
  getters: {
    subtotal: (state) =>
      state.items.reduce((acc, item) => acc + item.price * item.qty, 0),
    tax: (state) =>
      state.items.reduce((acc, item) => acc + item.price * item.qty * 0.1, 0),
    total(): number {
      return this.subtotal + this.tax;
    },
  },
  actions: {
    addItem(product: { id: number; name: string; price: number }) {
      const existing = this.items.find((i) => i.id === product.id);
      console.log(
        "Adding item:",
        existing
          ? { ...existing, qty: existing.qty + 1 }
          : { ...product, qty: 1 }
      );
      if (existing) {
        existing.qty += 1;
      } else {
        this.items.push({ ...product, qty: 1 });
      }
    },
    removeItem(id: number) {
      this.items = this.items.filter((i) => i.id !== id);
    },
  },
});
