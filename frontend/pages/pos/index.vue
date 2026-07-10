<!-- pages/pos/index.vue -->
<template>
  <div class="pos-container">
    <!-- Left Section -->
    <div class="left-section">
      <!-- Header - Fixed -->
      <div class="header" v-if="headerLoading">
        <v-skeleton-loader type="heading" class="mb-2" width="40%" />
        <v-skeleton-loader type="text" width="60%" class="mb-1" />
        <v-skeleton-loader type="text" width="50%" />
      </div>
      <div class="header" v-else>
        <div class="logo-section">
          <div class="logo-icon">🍔</div>
          <div class="logo-text">BABADEACON</div>
          <div class="logo-badge">COFFEE</div>
        </div>
        <div class="header-right">
          <div class="stats-group">
            <div class="stat-item">
              <span class="stat-label">Today</span>
              <span class="stat-value">{{ today }}</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-label">Orders</span>
              <span class="stat-value highlight">{{ TodaysTotalOrders }}</span>
            </div>
          </div>

          <!-- Toggle Switch: Product View / Scanner -->
          <v-btn
            variant="text"
            class="scan-toggle-btn"
            @click="toggleView"
            :color="isScannerMode ? '#2D6A4F' : '#6B7280'"
          >
            <v-icon>{{
              isScannerMode ? "mdi-barcode" : "mdi-view-grid"
            }}</v-icon>
            <span class="toggle-label">{{
              isScannerMode ? "Products" : "Scanner"
            }}</span>
            <v-switch
              v-model="isScannerMode"
              color="#2D6A4F"
              hide-details
              density="compact"
              class="mode-switch"
            />
          </v-btn>

          <v-btn variant="text" class="report-btn">
            <span>Report</span>
            <v-icon end size="18">mdi-file-document-outline</v-icon>
          </v-btn>

          <!-- Clickable Cart Badge -->
          <div class="cart-badge-wrapper" @click="showCartDialog = true">
            <v-badge
              color="#E07A5F"
              :content="store.cart.length"
              offset-x="8"
              offset-y="8"
              v-if="store.hasCartItems"
            >
              <v-btn icon variant="text" size="small" class="cart-btn">
                <v-icon size="22">mdi-cart-outline</v-icon>
              </v-btn>
            </v-badge>
            <v-btn v-else icon variant="text" size="small" class="cart-btn">
              <v-icon size="22">mdi-cart-outline</v-icon>
            </v-btn>
          </div>
        </div>
      </div>

      <!-- Scanner Mode -->
      <div v-if="isScannerMode" class="scanner-mode">
        <div class="scanner-header">
          <div class="scanner-icon">
            <v-icon size="48" color="#2D6A4F">mdi-barcode-scan</v-icon>
          </div>
          <h2 class="scanner-title">Barcode Scanner</h2>
          <p class="scanner-subtitle">Scan a barcode to add product to cart</p>
        </div>

        <div class="scanner-input-area">
          <div class="scanner-input-wrapper">
            <v-icon class="scanner-input-icon">mdi-barcode</v-icon>
            <input
              ref="barcodeInput"
              v-model="scannerBarcode"
              type="text"
              placeholder="Scan or enter barcode..."
              class="scanner-input"
              @keyup.enter="processBarcode"
              @input="autoProcessBarcode"
              autofocus
            />
            <v-btn
              color="#2D6A4F"
              size="small"
              class="scanner-scan-btn"
              @click="processBarcode"
            >
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
          </div>
          <div class="scanner-hint">
            <v-icon size="14">mdi-information</v-icon>
            Press Enter or wait 500ms after scanning
          </div>
        </div>

        <!-- Scanner Results -->
        <div v-if="scannerResult" class="scanner-result">
          <div class="result-header">
            <div class="result-icon">
              <v-icon size="32" color="#2D6A4F">mdi-check-circle</v-icon>
            </div>
            <div>
              <div class="result-title">Product Found</div>
              <div class="result-barcode">
                Barcode: {{ scannerResult.barcode }}
              </div>
            </div>
          </div>
          <div class="result-product">
            <div class="result-product-info">
              <div class="result-product-name">{{ scannerResult.name }}</div>
              <div class="result-product-sku">SKU: {{ scannerResult.sku }}</div>
              <div class="result-product-price">
                KSh {{ getItemPrice(scannerResult) }}
              </div>
            </div>
            <v-btn
              color="#2D6A4F"
              size="large"
              class="result-add-btn"
              @click="addScannedProduct"
            >
              <v-icon start>mdi-plus</v-icon>
              Add to Cart
            </v-btn>
          </div>
          <div v-if="scannerResult.has_variants" class="result-variants">
            <div class="variant-select-label">Select Variant:</div>
            <div class="variant-select-grid">
              <v-btn
                v-for="variant in scannerResult.variants"
                :key="variant.sku || variant.id"
                size="small"
                variant="outlined"
                class="variant-select-btn"
                :class="{ active: selectedVariant === variant }"
                @click="selectedVariant = variant"
              >
                {{ variant.variant_name }}
                <span class="variant-price"
                  >KSh
                  {{
                    variant.pricing?.selling_price ||
                    getItemPrice(scannerResult)
                  }}</span
                >
              </v-btn>
            </div>
          </div>
        </div>

        <!-- No Result -->
        <div
          v-else-if="scannerBarcode && !scannerLoading"
          class="scanner-no-result"
        >
          <v-icon size="48" color="#E07A5F">mdi-barcode-off</v-icon>
          <h3>Product Not Found</h3>
          <p>
            No product found with barcode: <strong>{{ scannerBarcode }}</strong>
          </p>
          <v-btn
            color="#2D6A4F"
            variant="outlined"
            size="small"
            @click="clearScanner"
          >
            Clear
          </v-btn>
        </div>

        <!-- Scanner Loading -->
        <div v-if="scannerLoading" class="scanner-loading">
          <v-progress-circular indeterminate color="#2D6A4F" size="48" />
          <p>Searching for product...</p>
        </div>

        <!-- Recent Scans -->
        <div v-if="recentScans.length > 0" class="recent-scans">
          <div class="recent-scans-header">
            <span>Recent Scans</span>
            <v-btn
              variant="text"
              size="small"
              color="#6B7280"
              @click="clearRecentScans"
            >
              Clear
            </v-btn>
          </div>
          <div
            v-for="scan in recentScans"
            :key="scan.id"
            class="recent-scan-item"
            @click="addRecentScan(scan)"
          >
            <div class="recent-scan-info">
              <div class="recent-scan-name">{{ scan.name }}</div>
              <div class="recent-scan-barcode">{{ scan.barcode }}</div>
            </div>
            <div class="recent-scan-price">KSh {{ getItemPrice(scan) }}</div>
          </div>
        </div>
      </div>

      <!-- Product View Mode -->
      <template v-else>
        <!-- Search - Fixed -->
        <div class="search-section" v-if="searchLoading">
          <v-skeleton-loader type="text" class="mr-3" width="80%" />
          <v-skeleton-loader type="button" width="80px" />
        </div>
        <div v-else class="search-section">
          <div class="search-container">
            <v-icon class="search-icon">mdi-magnify</v-icon>
            <v-text-field
              v-model="searchQuery"
              variant="plain"
              placeholder="Search products..."
              hide-details
              density="comfortable"
              class="search-field"
              @update:model-value="handleSearch"
            />
            <v-btn
              class="filter-btn"
              variant="text"
              size="small"
              @click="showFilters = !showFilters"
            >
              <v-icon>mdi-tune-variant</v-icon>
            </v-btn>
          </div>
        </div>

        <!-- Filters - Fixed -->
        <div v-if="showFilters" class="filters-section">
          <div class="filter-group">
            <v-select
              v-model="selectedCategory"
              :items="categoryFilterOptions"
              label="Category"
              variant="outlined"
              density="compact"
              hide-details
              class="filter-select"
              @update:model-value="applyFilters"
            />
            <v-select
              v-model="stockFilter"
              :items="stockFilterOptions"
              label="Stock Status"
              variant="outlined"
              density="compact"
              hide-details
              class="filter-select"
              @update:model-value="applyFilters"
            />
            <v-btn
              color="#2D6A4F"
              variant="tonal"
              size="small"
              @click="resetFilters"
            >
              Reset
            </v-btn>
          </div>
        </div>

        <!-- Category Cards - Fixed -->
        <!-- <div class="category-cards-wrapper">
          <div class="category-cards">
            <v-card
              v-for="category in store.filteredCategories"
              :key="category.id"
              :class="[
                'category-card',
                { active: store.selectedCategory === category.id },
              ]"
              :style="
                category.id === 'coffee'
                  ? 'background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%);'
                  : 'background: white;'
              "
              @click="store.setCategory(category.id)"
              elevation="0"
            >
              <div class="category-icon-large">{{ category.icon }}</div>
              <div class="category-content">
                <div class="category-title">{{ category.name }}</div>
                <div class="category-count">
                  {{ getCategoryItemCount(category.id) }} items
                </div>
              </div>
              <v-chip
                :class="[
                  'status-chip',
                  category.status === 'restock'
                    ? 'restock-chip'
                    : 'available-chip',
                ]"
                size="x-small"
              >
                {{
                  category.status === "available"
                    ? "In Stock"
                    : "Restock Needed"
                }}
              </v-chip>
            </v-card>
          </div>
        </div> -->

        <!-- Products Grid - Scrollable -->
        <div class="products-scroll-wrapper">
          <div v-if="loading" class="product-grid">
            <v-skeleton-loader
              v-for="n in 8"
              :key="n"
              type="card"
              class="product-card-skeleton"
            />
          </div>

          <!-- Products with Variants as Individual Items -->
          <div v-else class="product-grid">
            <div
              v-for="item in displayItems"
              :key="item.id || item.sku"
              class="product-card"
              @click="handleItemClick(item)"
            >
              <div class="product-image-wrapper">
                <v-img :src="item.image_url || ''" class="product-image" cover>
                  <template v-slot:placeholder>
                    <div class="image-placeholder">
                      {{ getProductIcon(item) }}
                    </div>
                  </template>
                </v-img>
                <div class="product-badges">
                  <div v-if="item.is_variant" class="variant-badge-small">
                    <v-icon size="12">mdi-swap-horizontal</v-icon>
                    Variant
                  </div>
                  <div
                    v-if="item.has_variants && !item.is_variant"
                    class="has-variants-badge"
                  >
                    <v-icon size="12">mdi-swap-horizontal</v-icon>
                    {{ item.variants?.length || 0 }} variants
                  </div>
                </div>
                <v-btn
                  icon
                  class="quick-add-btn"
                  size="small"
                  @click.stop="handleItemClick(item)"
                >
                  <v-icon size="18">mdi-plus</v-icon>
                </v-btn>
              </div>
              <div class="product-info">
                <div class="product-name">
                  {{ item.display_name || item.name }}
                </div>
                <div class="product-sku" v-if="item.sku">
                  SKU: {{ item.sku }}
                </div>
                <div class="product-price">KSh {{ getItemPrice(item) }}</div>
                <div class="product-stock" :class="getStockClass(item)">
                  {{ getStockStatus(item) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- Right Section - Cart (Desktop) -->
    <div class="right-section" v-if="rightSectionLoading">
      <v-card class="pa-4 mb-4" elevation="0">
        <v-skeleton-loader type="heading" class="mb-3" />
        <v-skeleton-loader type="text" class="mb-2" width="70%" />
        <v-skeleton-loader type="text" class="mb-2" width="60%" />
        <v-skeleton-loader type="text" width="80%" />
      </v-card>
      <v-card class="pa-4" elevation="0">
        <v-skeleton-loader
          type="image"
          class="mb-3"
          width="100%"
          height="150"
        />
        <v-skeleton-loader type="text" class="mb-2" width="90%" />
        <v-skeleton-loader type="text" class="mb-2" width="70%" />
      </v-card>
    </div>
    <div class="right-section" v-else>
      <div class="order-header">
        <div class="receipt-info">
          <div class="receipt-badge">RECEIPT</div>
          <div class="receipt-number">{{ receiptNumber }}</div>
        </div>
        <div class="order-actions">
          <v-btn
            icon
            variant="text"
            size="small"
            class="action-btn"
            @click="reprintReceipt(store.AllOrders[0])"
          >
            <v-icon size="20">mdi-printer-outline</v-icon>
          </v-btn>
          <v-btn icon variant="text" size="small" class="action-btn">
            <v-icon size="20">mdi-format-list-bulleted</v-icon>
          </v-btn>
        </div>
      </div>

      <!-- Order Type -->
      <!-- <div class="order-type-tabs">
        <v-btn
          :class="['order-type-btn', { active: orderType === 'dine-in' }]"
          @click="orderType = 'dine-in'"
          variant="text"
        >
          <v-icon start size="18" v-if="orderType === 'dine-in'"
            >mdi-seat</v-icon
          >
          Dine In
        </v-btn>
        <v-btn
          :class="['order-type-btn', { active: orderType === 'take-away' }]"
          @click="orderType = 'take-away'"
          variant="text"
        >
          <v-icon start size="18" v-if="orderType === 'take-away'"
            >mdi-food-takeout-box</v-icon
          >
          Take Away
        </v-btn>
        <v-btn
          :class="['order-type-btn', { active: orderType === 'order-online' }]"
          @click="orderType = 'order-online'"
          variant="text"
        >
          <v-icon start size="18" v-if="orderType === 'order-online'"
            >mdi-cellphone</v-icon
          >
          Order Online
        </v-btn>
      </div> -->

      <!-- Customer Info -->
      <!-- <div class="customer-section">
        <div class="input-group">
          <label>Customer</label>
          <v-text-field
            v-model="customerName"
            variant="outlined"
            density="comfortable"
            placeholder="Customer name"
            hide-details
            class="custom-input"
          />
        </div>
        <div class="input-group">
          <label>Table / Takeaway #</label>
          <v-select
            v-model="tableNumber"
            :items="[
              'Table B12',
              'Table B11',
              'Table B13',
              'Takeaway #1',
              'Takeaway #2',
            ]"
            variant="outlined"
            density="comfortable"
            hide-details
            class="custom-select"
          />
        </div>
      </div> -->

      <!-- Order List -->
      <!-- {{ store.hasCartItems }} || {{ store.cartItems.length }} -->
      <div v-if="store.hasCartItems" class="order-list-section">
        <div class="order-list-header">
          <span>Current Order</span>
          <span class="item-count">{{ store.cartItems.length }} items</span>
        </div>
        <div class="order-items">
          <div
            v-for="item in store.cartItems"
            :key="item.id"
            class="order-item"
          >
            <div class="item-info">
              <div class="item-name-row">
                <span class="item-name">{{ item.name }}</span>
                <v-btn
                  icon
                  size="x-small"
                  variant="text"
                  class="remove-item-btn"
                  @click="store.removeFromCart(item.id)"
                >
                  <v-icon size="14">mdi-close</v-icon>
                </v-btn>
              </div>
              <div class="item-meta">
                <span class="item-size">{{ item.size || "Regular" }}</span>
                <span class="item-temp">{{ item.temp || "Hot" }}</span>
              </div>
              <div class="item-modifier" v-if="item.modifier">
                <v-icon size="12">mdi-cube-outline</v-icon>
                {{ item.modifier }}
              </div>
            </div>
            <div class="item-price">
              KSh {{ (item.unitPrice * item.quantity).toFixed(2) }}
            </div>
            <div class="item-quantity">
              <v-btn
                icon
                size="x-small"
                variant="text"
                class="qty-btn"
                @click="store.decrementQuantity(item.id)"
              >
                <v-icon size="12">mdi-minus</v-icon>
              </v-btn>
              <span class="quantity">{{ item.quantity }}</span>
              <v-btn
                icon
                size="x-small"
                variant="text"
                class="qty-btn"
                @click="store.incrementQuantity(item.id)"
              >
                <v-icon size="12">mdi-plus</v-icon>
              </v-btn>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty cart -->
      <div v-else class="empty-cart">
        <div class="empty-cart-icon">🛒</div>
        <div class="empty-cart-text">No items yet</div>
        <div class="empty-cart-subtext">
          Start by adding items from the menu
        </div>
      </div>

      <!-- Payment Mode Section -->
      <div class="payment-mode-section" v-if="store.hasCartItems">
        <div class="payment-mode-header">
          <v-icon class="header-icon">mdi-credit-card</v-icon>
          <span>Payment Method</span>
        </div>
        <div class="payment-mode-options">
          <div
            v-for="mode in paymentModes"
            :key="mode.value"
            :class="[
              'payment-mode-card',
              { active: store.paymentMode === mode.value },
            ]"
            @click="store.paymentMode = mode.value"
          >
            <v-icon
              :color="store.paymentMode === mode.value ? '#2D6A4F' : '#6B7280'"
              size="24"
            >
              {{ mode.icon }}
            </v-icon>
            <div class="mode-info">
              <div class="mode-name">{{ mode.title }}</div>
              <div class="mode-desc">{{ mode.description }}</div>
            </div>
            <v-icon
              v-if="store.paymentMode === mode.value"
              class="check-icon"
              size="20"
              color="#2D6A4F"
            >
              mdi-check-circle
            </v-icon>
          </div>
        </div>
      </div>

      <!-- Cash Payment Input -->
      <transition name="slide-fade">
        <div
          v-if="store.hasCartItems && store.paymentMode === 'cash'"
          class="cash-payment-section"
        >
          <div class="cash-payment-header">
            <v-icon>mdi-cash-multiple</v-icon>
            <span>Cash Payment</span>
          </div>
          <div class="cash-input-group">
            <label>Amount Received</label>
            <div class="currency-input">
              <span class="currency-symbol">KSH</span>
              <input
                type="number"
                v-model.number="cashAmount"
                placeholder="0.00"
                @input="calculateChange"
                class="cash-input-field"
              />
            </div>
          </div>
          <div v-if="cashAmount >= store.total" class="change-display">
            <div class="change-label">Change Due</div>
            <div class="change-amount">KSH {{ changeAmount.toFixed(2) }}</div>
          </div>
          <div
            v-else-if="cashAmount > 0 && cashAmount < store.total"
            class="insufficient-warning"
          >
            <v-icon size="20" color="#E07A5F">mdi-alert-circle</v-icon>
            <span
              >Insufficient amount. Please enter KSH
              {{ (store.total - cashAmount).toFixed(2) }} more.</span
            >
          </div>
        </div>
      </transition>

      <!-- Payment Section -->
      <div v-if="store.hasCartItems" class="payment-section">
        <div class="payment-header">Payment Summary</div>
        <div class="payment-details">
          <div class="payment-row">
            <span>Subtotal</span>
            <span>KSh {{ store.subtotal.toFixed(2) }}</span>
          </div>
          <div class="payment-row">
            <span>Tax (10%)</span>
            <span>KSh {{ store.tax.toFixed(2) }}</span>
          </div>
          <div class="payment-row total-row">
            <span>Total</span>
            <span class="total-amount">KSh {{ store.total.toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <!-- Place Order Button -->
      <v-btn
        v-if="store.hasCartItems"
        class="place-order-btn"
        block
        size="large"
        @click="placeOrder"
      >
        <span>Place Order</span>
        <span class="order-total">KSh {{ store.total.toFixed(2) }}</span>
        <v-icon end>mdi-arrow-right</v-icon>
      </v-btn>
    </div>

    <!-- Cart Dialog (Mobile/Clickable) -->
    <v-dialog
      v-model="showCartDialog"
      fullscreen
      transition="dialog-bottom-transition"
      class="cart-dialog"
    >
      <v-card class="cart-dialog-card">
        <div class="cart-dialog-header">
          <div class="cart-dialog-title">
            <v-icon size="28" color="#2D6A4F">mdi-cart</v-icon>
            <span>Your Order</span>
            <span class="cart-dialog-count"
              >{{ store.cartItems.length }} items</span
            >
          </div>
          <v-btn icon variant="text" @click="showCartDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <v-divider />

        <div class="cart-dialog-body">
          <!-- Order Type -->
          <!-- <div class="order-type-tabs dialog-tabs">
            <v-btn
              :class="['order-type-btn', { active: orderType === 'dine-in' }]"
              @click="orderType = 'dine-in'"
              variant="text"
              size="small"
            >
              Dine In
            </v-btn>
            <v-btn
              :class="['order-type-btn', { active: orderType === 'take-away' }]"
              @click="orderType = 'take-away'"
              variant="text"
              size="small"
            >
              Take Away
            </v-btn>
            <v-btn
              :class="[
                'order-type-btn',
                { active: orderType === 'order-online' },
              ]"
              @click="orderType = 'order-online'"
              variant="text"
              size="small"
            >
              Online
            </v-btn>
          </div> -->

          <!-- Customer Info -->
          <!-- <div class="customer-section dialog-customer">
            <div class="input-group">
              <label>Customer</label>
              <v-text-field
                v-model="customerName"
                variant="outlined"
                density="compact"
                placeholder="Customer name"
                hide-details
              />
            </div>
            <div class="input-group">
              <label>Table / Takeaway #</label>
              <v-select
                v-model="tableNumber"
                :items="[
                  'Table B12',
                  'Table B11',
                  'Table B13',
                  'Takeaway #1',
                  'Takeaway #2',
                ]"
                variant="outlined"
                density="compact"
                hide-details
              />
            </div>
          </div> -->

          <!-- Cart Items -->
          <div v-if="store.hasCartItems" class="cart-dialog-items">
            <div
              v-for="item in store.cartItems"
              :key="item.id"
              class="cart-dialog-item"
            >
              <div class="item-dialog-info">
                <div class="item-dialog-name">
                  {{ item.name }}
                  <v-btn
                    icon
                    size="x-small"
                    variant="text"
                    class="remove-item-btn-dialog"
                    @click="store.removeFromCart(item.id)"
                  >
                    <v-icon size="14">mdi-close</v-icon>
                  </v-btn>
                </div>
                <div class="item-dialog-meta">
                  <span>{{ item.size || "Regular" }}</span>
                  <span>{{ item.temp || "Hot" }}</span>
                </div>
              </div>
              <div class="item-dialog-right">
                <div class="item-dialog-price">
                  KSh {{ (item.unitPrice * item.quantity).toFixed(2) }}
                </div>
                <div class="item-dialog-quantity">
                  <v-btn
                    icon
                    size="x-small"
                    variant="text"
                    @click="store.decrementQuantity(item.id)"
                  >
                    <v-icon size="12">mdi-minus</v-icon>
                  </v-btn>
                  <span>{{ item.quantity }}</span>
                  <v-btn
                    icon
                    size="x-small"
                    variant="text"
                    @click="store.incrementQuantity(item.id)"
                  >
                    <v-icon size="12">mdi-plus</v-icon>
                  </v-btn>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty Cart -->
          <div v-else class="empty-cart-dialog">
            <v-icon size="64" color="#9CA3AF">mdi-cart-outline</v-icon>
            <h3>Your cart is empty</h3>
            <p>Start adding items from the menu</p>
          </div>

          <!-- Payment Mode -->
          <div
            v-if="store.hasCartItems"
            class="payment-mode-section dialog-payment"
          >
            <div class="payment-mode-header">
              <v-icon class="header-icon">mdi-credit-card</v-icon>
              <span>Payment Method</span>
            </div>
            <div class="payment-mode-options dialog-payment-options">
              <div
                v-for="mode in paymentModes"
                :key="mode.value"
                :class="[
                  'payment-mode-card',
                  { active: store.paymentMode === mode.value },
                ]"
                @click="store.paymentMode = mode.value"
              >
                <v-icon
                  :color="
                    store.paymentMode === mode.value ? '#2D6A4F' : '#6B7280'
                  "
                  size="20"
                >
                  {{ mode.icon }}
                </v-icon>
                <span class="mode-name-dialog">{{ mode.title }}</span>
                <v-icon
                  v-if="store.paymentMode === mode.value"
                  class="check-icon"
                  size="16"
                  color="#2D6A4F"
                >
                  mdi-check-circle
                </v-icon>
              </div>
            </div>
          </div>

          <!-- Cash Input Dialog -->
          <transition name="slide-fade">
            <div
              v-if="store.hasCartItems && store.paymentMode === 'cash'"
              class="cash-payment-section dialog-cash"
            >
              <div class="cash-payment-header">
                <v-icon>mdi-cash-multiple</v-icon>
                <span>Cash Payment</span>
              </div>
              <div class="cash-input-group">
                <label>Amount Received</label>
                <div class="currency-input">
                  <span class="currency-symbol">KSH</span>
                  <input
                    type="number"
                    v-model.number="cashAmount"
                    placeholder="0.00"
                    @input="calculateChange"
                    class="cash-input-field"
                  />
                </div>
              </div>
              <div v-if="cashAmount >= store.total" class="change-display">
                <div class="change-label">Change Due</div>
                <div class="change-amount">
                  KSH {{ changeAmount.toFixed(2) }}
                </div>
              </div>
              <div
                v-else-if="cashAmount > 0 && cashAmount < store.total"
                class="insufficient-warning"
              >
                <v-icon size="20" color="#E07A5F">mdi-alert-circle</v-icon>
                <span
                  >Insufficient amount. Please enter KSH
                  {{ (store.total - cashAmount).toFixed(2) }} more.</span
                >
              </div>
            </div>
          </transition>
        </div>

        <!-- Payment Summary & Place Order -->
        <div class="cart-dialog-footer" v-if="store.hasCartItems">
          <div class="dialog-payment-summary">
            <div class="dialog-summary-row">
              <span>Subtotal</span>
              <span>KSh {{ store.subtotal.toFixed(2) }}</span>
            </div>
            <div class="dialog-summary-row">
              <span>Tax (10%)</span>
              <span>KSh {{ store.tax.toFixed(2) }}</span>
            </div>
            <div class="dialog-summary-row total">
              <span>Total</span>
              <span>KSh {{ store.total.toFixed(2) }}</span>
            </div>
          </div>
          <v-btn
            class="place-order-btn dialog-place-order"
            block
            size="large"
            @click="placeOrder"
          >
            <span>Place Order</span>
            <span class="order-total">KSh {{ store.total.toFixed(2) }}</span>
            <v-icon end>mdi-arrow-right</v-icon>
          </v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- FAB for adding products -->
    <v-fab
      icon="mdi-plus"
      color="#E07A5F"
      location="bottom start"
      size="large"
      app
      @click="showFABMenu = true"
      class="fab-add-product"
      v-if="authStore.isAdmin"
    />

    <!-- FAB Menu -->
    <v-speed-dial
      v-model="showFABMenu"
      direction="top"
      transition="slide-y-reverse-transition"
      location="bottom start"
      class="fab-menu"
      v-if="authStore.isAdmin"
    >
      <template v-slot:activator>
        <v-btn v-model="showFABMenu" color="#E07A5F" size="large" icon>
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </template>
      <v-btn
        key="1"
        color="#2D6A4F"
        size="small"
        icon
        @click="openAddProductDialog"
      >
        <v-icon>mdi-coffee</v-icon>
        <v-tooltip activator="parent" location="top">Add Product</v-tooltip>
      </v-btn>
      <v-btn
        key="2"
        color="#E07A5F"
        size="small"
        icon
        @click="openExpenseDialog"
      >
        <v-icon>mdi-cash-minus</v-icon>
        <v-tooltip activator="parent" location="top">Record Expense</v-tooltip>
      </v-btn>
    </v-speed-dial>

    <!-- Expense Tracker Dialog -->
    <ExpenseTracker
      v-model="showExpenseDialog"
      @expense-recorded="handleExpenseRecorded"
    />

    <!-- Add Product Dialog -->
    <v-dialog v-model="dialog" max-width="550" transition="dialog-transition">
      <v-card class="product-dialog">
        <v-card-title class="dialog-title">
          Add New Product
          <v-btn
            icon
            variant="text"
            @click="dialog = false"
            class="close-dialog-btn"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="isValid" class="product-form">
            <v-text-field
              v-model="product.name"
              label="Product Name"
              :rules="[rules.required]"
              variant="outlined"
              density="comfortable"
            />
            <v-text-field
              v-model="product.price"
              label="Price"
              type="number"
              :rules="[rules.required, rules.positive]"
              variant="outlined"
              density="comfortable"
              prefix="ksh"
            />
            <v-select
              v-model="product.category"
              :items="categoryOptions"
              label="Category"
              :rules="[rules.required]"
              variant="outlined"
              density="comfortable"
            />
            <v-file-input
              v-model="product.file"
              label="Product Image"
              accept="image/*"
              :rules="[rules.required]"
              variant="outlined"
              density="comfortable"
              prepend-icon=""
              prepend-inner-icon="mdi-image"
            />
            <div v-if="imagePreview" class="image-preview">
              <img :src="imagePreview" alt="Preview" class="preview-img" />
            </div>
          </v-form>
        </v-card-text>
        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="dialog = false" class="cancel-btn"
            >Cancel</v-btn
          >
          <v-btn
            color="#1B4332"
            :disabled="!isValid"
            @click="submitProduct"
            class="save-btn"
          >
            Save Product
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- M-Pesa Payment Dialog -->
    <v-dialog
      v-model="showMpesaDialog"
      max-width="450"
      transition="dialog-transition"
    >
      <v-card class="mpesa-dialog">
        <div class="dialog-header">
          <div class="header-content">
            <div class="mpesa-logo">
              <v-icon size="32" color="#2D6A4F">mdi-cellphone</v-icon>
              <span>M-Pesa Payment</span>
            </div>
          </div>
          <v-btn icon variant="text" @click="closeMpesaDialog">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <div class="dialog-body">
          <div class="amount-display">
            <div class="amount-label">Amount to Pay</div>
            <div class="amount-value">KSH {{ store.total.toFixed(2) }}</div>
          </div>

          <div class="input-group">
            <label>M-Pesa Phone Number</label>
            <div class="phone-input">
              <span class="country-code">+254</span>
              <input
                type="tel"
                v-model="mpesaPhone"
                placeholder="712345678"
                maxlength="9"
                class="phone-field"
                @input="validatePhoneNumber"
              />
            </div>
            <div class="input-hint">
              Enter the M-Pesa registered phone number
            </div>
          </div>

          <div class="payment-instructions">
            <div class="instruction-item">
              <div class="instruction-step">1</div>
              <div class="instruction-text">
                Check your phone for STK Push prompt
              </div>
            </div>
            <div class="instruction-item">
              <div class="instruction-step">2</div>
              <div class="instruction-text">
                Enter your M-Pesa PIN to confirm payment
              </div>
            </div>
            <div class="instruction-item">
              <div class="instruction-step">3</div>
              <div class="instruction-text">Wait for confirmation message</div>
            </div>
          </div>
        </div>

        <div class="dialog-actions">
          <v-btn variant="outlined" @click="closeMpesaDialog">Cancel</v-btn>
          <v-btn
            color="#2D6A4F"
            :disabled="!isValidPhone || isProcessing"
            :loading="isProcessing"
            @click="processMpesaPayment"
          >
            <v-icon start>mdi-check</v-icon>
            Pay with M-Pesa
          </v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- Debt Confirmation Dialog -->
    <v-dialog
      v-model="showDebtDialog"
      max-width="400"
      transition="dialog-transition"
    >
      <v-card class="debt-dialog">
        <div class="debt-icon">
          <v-icon size="64" color="#E07A5F">mdi-account-cash</v-icon>
        </div>
        <h3>Confirm Debt Order</h3>
        <p>
          This order will be recorded as debt for customer
          <strong>{{ customerName || "Guest" }}</strong>
        </p>
        <div class="debt-amount">
          Total Amount: KSH {{ store.total.toFixed(2) }}
        </div>
        <div class="debt-warning">
          <v-icon size="18" color="#E07A5F">mdi-alert</v-icon>
          <span
            >This amount will be added to customer's outstanding balance</span
          >
        </div>
        <div class="dialog-actions">
          <v-btn variant="text" @click="showDebtDialog = false">Cancel</v-btn>
          <v-btn color="#E07A5F" @click="processDebtPayment">
            Confirm Debt Order
          </v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- Cash Payment Confirmation Dialog -->
    <v-dialog
      v-model="showCashConfirmDialog"
      max-width="400"
      transition="dialog-transition"
    >
      <v-card class="cash-confirm-dialog">
        <div class="confirm-icon">
          <v-icon size="64" color="#2D6A4F">mdi-cash-check</v-icon>
        </div>
        <h3>Confirm Cash Payment</h3>
        <div class="payment-breakdown">
          <div class="breakdown-row">
            <span>Total Amount:</span>
            <span>KSH {{ store.total.toFixed(2) }}</span>
          </div>
          <div class="breakdown-row">
            <span>Amount Received:</span>
            <span>KSH {{ cashAmount.toFixed(2) }}</span>
          </div>
          <div class="breakdown-row change">
            <span>Change Due:</span>
            <span>KSH {{ changeAmount.toFixed(2) }}</span>
          </div>
        </div>
        <div class="dialog-actions">
          <v-btn variant="text" @click="showCashConfirmDialog = false"
            >Cancel</v-btn
          >
          <v-btn color="#2D6A4F" @click="processCashPayment">
            Confirm Payment
          </v-btn>
        </div>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :timeout="3000"
      :color="snackbar.color"
      location="top"
      class="custom-snackbar"
    >
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn variant="text" icon="mdi-close" @click="snackbar.show = false" />
      </template>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from "vue";
import { usePosStore } from "~/stores/pos";
import { useAuthStore } from "~/stores/auth";
import { useReceipt } from "~/composables/useReceipt";
import ExpenseTracker from "~/components/ExpenseTracker.vue";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const receipt = useReceipt();
const authStore = useAuthStore();
const store = usePosStore();

// State
const isScannerMode = ref(false);
const scannerBarcode = ref("");
const scannerLoading = ref(false);
const scannerResult = ref(null);
const selectedVariant = ref(null);
const recentScans = ref([]);
const barcodeInput = ref(null);
const showCartDialog = ref(false);
let scannerTimeout = null;

const searchQuery = ref("");
const orderType = ref("dine-in");
const customerName = ref("");
const tableNumber = ref("Table B12");
const receiptNumber = ref("");
const TodaysTotalOrders = ref(0);
const loading = ref(true);
const rightSectionLoading = ref(true);
const headerLoading = ref(true);
const searchLoading = ref(true);
const showFABMenu = ref(false);
const showExpenseDialog = ref(false);
const showFilters = ref(false);
const selectedCategory = ref("");
const stockFilter = ref("");
const dialog = ref(false);
const isValid = ref(false);
const form = ref(null);
const imagePreview = ref("");
const product = ref({
  name: "",
  price: "",
  category: "",
  file: null,
});
const cashAmount = ref(0);
const changeAmount = ref(0);
const showMpesaDialog = ref(false);
const mpesaPhone = ref("");
const isProcessing = ref(false);
const showDebtDialog = ref(false);
const showCashConfirmDialog = ref(false);

const snackbar = ref({
  show: false,
  text: "",
  color: "success",
});

const rules = {
  required: (v: any) => !!v || "This field is required",
  positive: (v: number) => v > 0 || "Price must be positive",
};

const categoryOptions = [
  { title: "Coffee", value: "coffee" },
  { title: "Snack", value: "snack" },
  { title: "Tea", value: "tea" },
];

const paymentModes = [
  {
    value: "cash",
    title: "Cash",
    icon: "mdi-cash",
    description: "Pay with cash",
  },
  {
    value: "mpesa",
    title: "M-Pesa",
    icon: "mdi-cellphone",
    description: "Mobile money payment",
  },
  {
    value: "debt",
    title: "Debt",
    icon: "mdi-account-cash",
    description: "Pay later / Credit",
  },
];

const isValidPhone = computed(() => {
  return /^[0-9]{9}$/.test(mpesaPhone.value);
});

// Computed
const displayItems = computed(() => {
  let items: any[] = [];
  let filteredProducts = store.filteredProducts;

  if (selectedCategory.value) {
    filteredProducts = filteredProducts.filter(
      (p) =>
        p.category_id === selectedCategory.value ||
        p.tags?.includes(selectedCategory.value)
    );
  }

  if (stockFilter.value) {
    filteredProducts = filteredProducts.filter((p) => {
      const stock = getProductStock(p);
      const reorder = p.inventory?.reorder_level || 10;
      if (stockFilter.value === "in_stock") return stock > reorder;
      if (stockFilter.value === "low_stock")
        return stock <= reorder && stock > 0;
      if (stockFilter.value === "out_of_stock") return stock <= 0;
      return true;
    });
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filteredProducts = filteredProducts.filter(
      (p) =>
        p.name?.toLowerCase().includes(query) ||
        p.sku?.toLowerCase().includes(query) ||
        p.barcode?.includes(query)
    );
  }

  filteredProducts.forEach((product) => {
    if (
      product.has_variants &&
      product.variants &&
      product.variants.length > 0
    ) {
      product.variants.forEach((variant: any) => {
        const variantName = variant.variant_name || variant.name || "";
        const variantSku = variant.sku || "";
        if (searchQuery.value) {
          const query = searchQuery.value.toLowerCase();
          const matches =
            variantName.toLowerCase().includes(query) ||
            variantSku.toLowerCase().includes(query);
          if (!matches) return;
        }

        items.push({
          ...variant,
          id: variant.id || variant.sku,
          _id: product._id || product.id,
          parent_product_id: product.id || product._id,
          name: product.name,
          display_name: `${product.name} - ${variant.variant_name}`,
          sku: variant.sku || product.sku,
          barcode: variant.barcode || product.barcode,
          pricing: variant.pricing || product.pricing,
          inventory: variant.inventory || product.inventory,
          image_url:
            variant.image_url ||
            product.image_url ||
            product.media?.images?.[0]?.url,
          is_variant: true,
          variant_data: variant,
          tags: product.tags || [],
        });
      });
    } else {
      items.push({
        ...product,
        id: product.id || product._id,
        display_name: product.name,
        is_variant: false,
        has_variants: product.has_variants || false,
      });
    }
  });

  return items;
});

const categoryFilterOptions = computed(() => {
  const cats = new Set();
  store.products.forEach((p) => {
    if (p.category_id) cats.add(p.category_id);
    if (p.tags) p.tags.forEach((t) => cats.add(t));
  });
  return Array.from(cats).map((c) => ({
    title: typeof c === "string" ? c.charAt(0).toUpperCase() + c.slice(1) : c,
    value: c,
  }));
});

const stockFilterOptions = [
  { title: "All Stock", value: "" },
  { title: "In Stock", value: "in_stock" },
  { title: "Low Stock", value: "low_stock" },
  { title: "Out of Stock", value: "out_of_stock" },
];

// Helper Methods
const getCategoryItemCount = (categoryId: string) => {
  return store.products.filter(
    (p) => p.category_id === categoryId || p.tags?.includes(categoryId)
  ).length;
};

const getProductStock = (item: any) => {
  return item.inventory?.available || item.inventory?.quantity || 0;
};

const getItemPrice = (item: any) => {
  return item.pricing?.selling_price || item.price || 0;
};

const getStockStatus = (item: any) => {
  const quantity = getProductStock(item);
  const reorder = item.inventory?.reorder_level || 10;
  if (quantity <= 0) return "Out of Stock";
  if (quantity <= reorder) return "Low Stock";
  return "In Stock";
};

const getStockClass = (item: any) => {
  const quantity = getProductStock(item);
  const reorder = item.inventory?.reorder_level || 10;
  if (quantity <= 0) return "out-of-stock";
  if (quantity <= reorder) return "low-stock";
  return "in-stock";
};

const getProductIcon = (item: any) => {
  const icons: Record<string, string> = {
    coffee: "☕",
    tea: "🫖",
    snack: "🍪",
    rice: "🍚",
    beans: "🫘",
    oil: "🫒",
    flour: "🌾",
    bread: "🍞",
    soap: "🧼",
    dairy: "🥛",
    juice: "🧃",
  };

  const tag = item.tags?.[0]?.toLowerCase() || "";
  for (const [key, icon] of Object.entries(icons)) {
    if (tag.includes(key)) {
      return icon;
    }
  }
  return "📦";
};

// Scanner Methods
const toggleView = () => {
  isScannerMode.value = !isScannerMode.value;
  if (isScannerMode.value) {
    nextTick(() => {
      barcodeInput.value?.focus();
    });
  }
};

const autoProcessBarcode = () => {
  clearTimeout(scannerTimeout);
  scannerTimeout = setTimeout(() => {
    if (scannerBarcode.value.length > 0) {
      processBarcode();
    }
  }, 500);
};

const processBarcode = async () => {
  if (!scannerBarcode.value || scannerBarcode.value.length < 3) {
    return;
  }

  scannerLoading.value = true;
  scannerResult.value = null;
  selectedVariant.value = null;

  try {
    const product = await findProductByBarcode(scannerBarcode.value);
    if (product) {
      scannerResult.value = product;
      addToRecentScans(product);
    } else {
      scannerResult.value = null;
    }
  } catch (error) {
    console.error("Error scanning barcode:", error);
    scannerResult.value = null;
  } finally {
    scannerLoading.value = false;
    if (scannerResult.value) {
      scannerBarcode.value = "";
    }
    nextTick(() => {
      barcodeInput.value?.focus();
    });
  }
};

const findProductByBarcode = async (barcode: string) => {
  let product = store.products.find(
    (p) => p.barcode === barcode || p.sku === barcode
  );

  if (product) {
    return product;
  }

  for (const p of store.products) {
    if (p.variants) {
      const variant = p.variants.find(
        (v) => v.barcode === barcode || v.sku === barcode
      );
      if (variant) {
        return {
          ...p,
          selected_variant: variant,
        };
      }
    }
  }

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/products/barcode/${barcode}`
    );
    if (response.ok) {
      const data = await response.json();
      return data;
    }
  } catch (error) {
    console.error("API error:", error);
  }

  return null;
};

const addScannedProduct = () => {
  if (!scannerResult.value) return;

  const productToAdd = scannerResult.value;

  if (productToAdd.has_variants && selectedVariant.value) {
    store.addVariantToCart(productToAdd, selectedVariant.value);
    snackbar.value = {
      show: true,
      text: `${productToAdd.name} - ${selectedVariant.value.variant_name} added to cart!`,
      color: "success",
    };
  } else if (productToAdd.has_variants && productToAdd.variants?.length > 0) {
    const defaultVariant =
      productToAdd.variants.find((v) => v.is_default) ||
      productToAdd.variants[0];
    if (defaultVariant) {
      store.addVariantToCart(productToAdd, defaultVariant);
      snackbar.value = {
        show: true,
        text: `${productToAdd.name} - ${defaultVariant.variant_name} added to cart!`,
        color: "success",
      };
    }
  } else {
    store.addToCart(productToAdd);
    snackbar.value = {
      show: true,
      text: `${productToAdd.name} added to cart!`,
      color: "success",
    };
  }

  clearScanner();
};

const clearScanner = () => {
  scannerResult.value = null;
  scannerBarcode.value = "";
  selectedVariant.value = null;
  nextTick(() => {
    barcodeInput.value?.focus();
  });
};

const addToRecentScans = (product: any) => {
  recentScans.value = recentScans.value.filter(
    (item) => item.id !== product.id && item.barcode !== product.barcode
  );
  recentScans.value.unshift({
    id: product.id || product._id,
    name: product.name,
    barcode: product.barcode || product.sku,
    ...product,
  });
  if (recentScans.value.length > 10) {
    recentScans.value = recentScans.value.slice(0, 10);
  }
  localStorage.setItem("recentScans", JSON.stringify(recentScans.value));
};

const addRecentScan = (scan: any) => {
  scannerResult.value = scan;
  scannerBarcode.value = scan.barcode || scan.sku;
  if (scan.variants && scan.variants.length > 0) {
    selectedVariant.value =
      scan.variants.find((v) => v.is_default) || scan.variants[0];
  }
};

const clearRecentScans = () => {
  recentScans.value = [];
  localStorage.removeItem("recentScans");
};

const loadRecentScans = () => {
  try {
    const saved = localStorage.getItem("recentScans");
    if (saved) {
      recentScans.value = JSON.parse(saved);
    }
  } catch (error) {
    console.error("Error loading recent scans:", error);
  }
};

// Handle item click
const handleItemClick = (item: any) => {
  if (item.is_variant) {
    store.addVariantToCart(
      {
        id: item.parent_product_id || item._id,
        name: item.name,
        sku: item.sku,
        pricing: item.pricing,
        inventory: item.inventory,
        image_url: item.image_url,
        tags: item.tags,
      },
      {
        id: item.id,
        sku: item.sku,
        variant_name: item.variant_name || item.display_name,
        pricing: item.pricing,
        inventory: item.inventory,
        attributes: item.attributes || {},
        barcode: item.barcode,
      }
    );

    snackbar.value = {
      show: true,
      text: `${item.display_name} added to cart!`,
      color: "success",
    };
  } else if (item.has_variants && item.variants && item.variants.length > 0) {
    showVariantSelection(item);
  } else {
    store.addToCart(item);
    snackbar.value = {
      show: true,
      text: `${item.name} added to cart!`,
      color: "success",
    };
  }
};

const showVariantSelection = (product: any) => {
  const variantNames = product.variants.map(
    (v: any) =>
      `${v.variant_name} - KSh ${
        v.pricing?.selling_price || getItemPrice(product)
      }`
  );

  const message = `Select variant for ${product.name}:\n\n${variantNames
    .map((n: string, i: number) => `${i + 1}. ${n}`)
    .join("\n")}`;
  const choice = prompt(message);

  if (choice) {
    const index = parseInt(choice) - 1;
    if (index >= 0 && index < product.variants.length) {
      const variant = product.variants[index];
      store.addVariantToCart(product, variant);
      snackbar.value = {
        show: true,
        text: `${product.name} - ${variant.variant_name} added to cart!`,
        color: "success",
      };
    }
  }
};

// Search and filters
const handleSearch = () => {
  store.setSearchQuery(searchQuery.value);
};

const applyFilters = () => {
  // Filters applied via computed properties
};

const resetFilters = () => {
  selectedCategory.value = "";
  stockFilter.value = "";
  searchQuery.value = "";
  store.setSearchQuery("");
};

// Cash payment
const calculateChange = () => {
  if (cashAmount.value >= store.total) {
    changeAmount.value = cashAmount.value - store.total;
  } else {
    changeAmount.value = 0;
  }
};

// Place order
const placeOrder = async () => {
  if (!store.hasCartItems) return;

  if (store.paymentMode === "mpesa") {
    showMpesaDialog.value = true;
  } else if (store.paymentMode === "cash") {
    if (cashAmount.value < store.total) {
      snackbar.value = {
        show: true,
        text: `Please enter amount of KSH ${store.total.toFixed(2)} or more`,
        color: "error",
      };
      return;
    }
    showCashConfirmDialog.value = true;
  } else if (store.paymentMode === "debt") {
    showDebtDialog.value = true;
  }
};

// Complete order - FIXED: Properly clears cart
const completeOrder = async (orderData: any) => {
  try {
    orderData.cashier = authStore.user?.name || "Cashier";

    if (orderData.paymentMode === "debt") {
      orderData.paymentStatus = "pending";
    } else {
      orderData.paymentStatus = "paid";
    }

    await store.saveOrder(orderData);
    const orders = await store.getAllOrders();

    const todaysDateString = new Date().toLocaleDateString();
    TodaysTotalOrders.value = orders.reduce((count, order) => {
      const orderDate = new Date(order.created_at).toLocaleDateString();
      return count + (orderDate === todaysDateString ? 1 : 0);
    }, 0);

    try {
      await receipt.printReceipt(orderData, true);
    } catch (printError) {
      console.error("Print failed:", printError);
    }

    receipt.downloadReceipt(orderData);

    // CLEAR CART - This is critical
    store.clearCart();

    // Reset payment-related state
    receiptNumber.value = generateUniqueReceipt();
    store.paymentMode = "cash";
    cashAmount.value = 0;
    changeAmount.value = 0;
    showCartDialog.value = false;

    snackbar.value = {
      show: true,
      text: "Order placed successfully!",
      color: "success",
    };
  } catch (error) {
    console.error("Error completing order:", error);
    snackbar.value = {
      show: true,
      text: "Failed to complete order",
      color: "error",
    };
  }
};

// Process payments
const processMpesaPayment = async () => {
  if (!isValidPhone.value) return;

  isProcessing.value = true;
  setTimeout(async () => {
    isProcessing.value = false;
    closeMpesaDialog();

    const orderData = {
      receiptNumber: receiptNumber.value,
      orderType: orderType.value,
      customerName: customerName.value || authStore.user?.name || "Guest",
      tableNumber: tableNumber.value,
      items: store.cartItems,
      subtotal: store.subtotal,
      tax: store.tax,
      total: store.total,
      paymentMode: "mpesa",
      mpesaNumber: mpesaPhone.value,
      paymentStatus: "paid",
    };

    await completeOrder(orderData);
    snackbar.value = {
      show: true,
      text: `M-Pesa payment of KSH ${orderData.total.toFixed(2)} received`,
      color: "success",
    };
  }, 2000);
};

const closeMpesaDialog = () => {
  showMpesaDialog.value = false;
  mpesaPhone.value = "";
  isProcessing.value = false;
};

const processCashPayment = async () => {
  if (cashAmount.value < store.total) return;

  showCashConfirmDialog.value = false;
  const orderData = {
    receiptNumber: receiptNumber.value,
    orderType: orderType.value,
    customerName: customerName.value || authStore.user?.name || "Guest",
    tableNumber: tableNumber.value,
    items: store.cartItems,
    subtotal: store.subtotal,
    tax: store.tax,
    total: store.total,
    paymentMode: "cash",
    amountReceived: cashAmount.value,
    changeDue: changeAmount.value,
    paymentStatus: "paid",
  };

  await completeOrder(orderData);
  snackbar.value = {
    show: true,
    text: `Cash payment of KSH ${orderData.total.toFixed(
      2
    )} received. Change: KSH ${changeAmount.value.toFixed(2)}`,
    color: "success",
  };

  cashAmount.value = 0;
  changeAmount.value = 0;
};

const processDebtPayment = async () => {
  showDebtDialog.value = false;
  const orderData = {
    receiptNumber: receiptNumber.value,
    orderType: orderType.value,
    customerName: customerName.value || authStore.user?.name || "Guest",
    tableNumber: tableNumber.value,
    items: store.cartItems,
    subtotal: store.subtotal,
    tax: store.tax,
    total: store.total,
    paymentMode: "debt",
    paymentStatus: "pending",
    dueDate: new Date(Date.now() + 7 * 86400000).toISOString(),
  };

  await completeOrder(orderData);
  snackbar.value = {
    show: true,
    text: `Debt order recorded. Payment due in 7 days. Total: KSH ${orderData.total.toFixed(
      2
    )}`,
    color: "warning",
  };
};

const reprintReceipt = (order: any) => {
  if (order) {
    receipt.printReceipt(order);
    snackbar.value = {
      show: true,
      text: "Receipt reprinted successfully!",
      color: "success",
    };
  }
};

// FAB actions
const openAddProductDialog = () => {
  dialog.value = true;
  showFABMenu.value = false;
};

const openExpenseDialog = () => {
  showFABMenu.value = false;
  showExpenseDialog.value = true;
};

const handleExpenseRecorded = () => {
  // Refresh data if needed
};

// Product dialog
watch(
  () => product.value.file,
  async (file) => {
    if (!file) {
      imagePreview.value = "";
      return;
    }
    const base64 = await processFormImage(file);
    imagePreview.value = base64;
  }
);

const processFormImage = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
};

const submitProduct = async () => {
  const { valid } = await form.value.validate();
  if (!valid) return;

  try {
    const formData = new FormData();
    formData.append("name", product.value.name);
    formData.append("price", product.value.price);
    formData.append("category", product.value.category);
    formData.append("image", product.value.file);

    await store.addProduct(formData);
    await store.getAllProducts();
    dialog.value = false;
    form.value.reset();
    product.value.file = null;
    imagePreview.value = "";

    snackbar.value = {
      show: true,
      text: "Product added successfully!",
      color: "success",
    };
  } catch (error) {
    console.error("Error adding product:", error);
    snackbar.value = {
      show: true,
      text: "Failed to add product",
      color: "error",
    };
  }
};

// Receipt generation
const usedReceipts = new Set<string>();

function generateUniqueReceipt() {
  let receipt: string;
  do {
    receipt = `RCP-${Math.floor(10000 + Math.random() * 90000)}`;
  } while (usedReceipts.has(receipt));
  usedReceipts.add(receipt);
  return receipt;
}

receiptNumber.value = generateUniqueReceipt();

const today = new Date().toLocaleDateString(undefined, {
  weekday: "short",
  day: "numeric",
  month: "short",
});

// Validate phone number
const validatePhoneNumber = () => {
  mpesaPhone.value = mpesaPhone.value.replace(/[^0-9]/g, "").slice(0, 9);
};

// Watch for search
watch(searchQuery, (newQuery) => {
  store.setSearchQuery(newQuery);
});

// Lifecycle
onMounted(async () => {
  if (!authStore.checkAuth()) {
    await navigateTo("/login");
    return;
  }

  loadRecentScans();

  if (authStore.user) {
    customerName.value = authStore.user.name;
  }

  try {
    loading.value = true;
    headerLoading.value = true;
    rightSectionLoading.value = true;
    searchLoading.value = true;

    const [_, orders] = await Promise.all([
      store.getAllProducts(),
      store.getAllOrders(),
    ]);

    const todayString = new Date().toLocaleDateString();
    TodaysTotalOrders.value = orders.reduce((count, order) => {
      const orderDate = new Date(order.created_at).toLocaleDateString();
      return count + (orderDate === todayString ? 1 : 0);
    }, 0);
  } catch (error) {
    console.error("Error loading data:", error);
    snackbar.value = {
      show: true,
      text: "Failed to load data",
      color: "error",
    };
  } finally {
    loading.value = false;
    rightSectionLoading.value = false;
    headerLoading.value = false;
    searchLoading.value = false;
  }
});
</script>

<style scoped>
/* ========== POS CONTAINER ========== */
.pos-container {
  display: flex;
  gap: 0;
  min-height: calc(100vh - 64px);
  background: #f8f6f2;
}

.left-section {
  flex: 1;
  padding: 0 32px 28px 32px;
  background: #f8f6f2;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 64px);
}

.right-section {
  width: 420px;
  background: white;
  padding: 28px 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.05);
  border-radius: 32px 0 0 32px;
  height: calc(100vh - 64px);
  overflow-y: auto;
  flex-shrink: 0;
}

/* ========== HEADER - FIXED ========== */
.header {
  position: sticky;
  top: 0;
  z-index: 30;
  background: #f8f6f2;
  padding: 20px 0 16px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 28px;
}

.logo-text {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-badge {
  font-size: 12px;
  font-weight: 600;
  color: #e07a5f;
  background: rgba(224, 122, 95, 0.1);
  padding: 4px 8px;
  border-radius: 20px;
  letter-spacing: 0.5px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 24px;
}

.stats-group {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 16px;
  background: white;
  border-radius: 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.stat-label {
  font-size: 11px;
  font-weight: 500;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.stat-value.highlight {
  color: #e07a5f;
  font-size: 16px;
}

.stat-divider {
  width: 1px;
  height: 24px;
  background: #e5e0d5;
}

.report-btn {
  text-transform: none;
  font-weight: 500;
  color: #666;
  background: white;
  border-radius: 40px;
  padding: 0 16px;
}

.cart-badge-wrapper {
  margin: 0 -8px;
}

.cart-btn {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

/* ========== SEARCH - FIXED ========== */
.search-section {
  position: sticky;
  top: 80px;
  z-index: 29;
  background: #f8f6f2;
  padding-bottom: 12px;
  flex-shrink: 0;
}

.search-container {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 60px;
  padding: 0 8px 0 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  transition: all 0.2s ease;
}

.search-container:focus-within {
  box-shadow: 0 4px 16px rgba(27, 67, 50, 0.12);
}

.search-icon {
  color: #999;
  font-size: 20px;
}

.search-field {
  flex: 1;
}

.search-field :deep(.v-field) {
  --v-field-padding-start: 8px;
}

.filter-btn {
  color: #666;
  background: #f5f3ed;
  margin: 6px;
  border-radius: 40px;
}

/* ========== FILTERS - FIXED ========== */
.filters-section {
  position: sticky;
  top: 138px;
  z-index: 28;
  background: #f8f6f2;
  padding: 8px 0 12px 0;
  flex-shrink: 0;
}

.filters-section .filter-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}

.filter-select {
  min-width: 150px;
}

/* ========== CATEGORY CARDS - FIXED ========== */
.category-cards-wrapper {
  position: sticky;
  top: 208px;
  z-index: 27;
  background: #f8f6f2;
  padding: 4px 0 16px 0;
  flex-shrink: 0;
}

.category-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.category-card {
  padding: 16px 14px;
  position: relative;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 16px !important;
  border: 1px solid #e5e0d5;
}

.category-card:hover {
  transform: translateY(-2px);
}

.category-card.active {
  border-color: #1b4332;
  box-shadow: 0 8px 20px rgba(27, 67, 50, 0.15);
}

.category-icon-large {
  font-size: 28px;
  margin-bottom: 8px;
}

.category-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.category-title {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 2px;
  color: #1b4332;
}

.category-card:not([style*="linear-gradient"]) .category-title {
  color: #1b4332;
}

.category-card[style*="linear-gradient"] .category-title {
  color: white;
}

.category-count {
  font-size: 11px;
  color: #888;
}

.category-card[style*="linear-gradient"] .category-count {
  color: rgba(255, 255, 255, 0.8);
}

.status-chip {
  position: absolute;
  top: 12px;
  right: 12px;
  font-weight: 500;
}

.available-chip {
  background: #e8f5e9 !important;
  color: #2e7d32 !important;
}

.restock-chip {
  background: #ffebee !important;
  color: #c62828 !important;
}

/* ========== PRODUCTS - SCROLLABLE ========== */
.products-scroll-wrapper {
  flex: 1;
  overflow-y: auto;
  padding-top: 4px;
  padding-bottom: 20px;
}

.products-scroll-wrapper::-webkit-scrollbar {
  width: 6px;
}

.products-scroll-wrapper::-webkit-scrollbar-track {
  background: #e5e0d5;
  border-radius: 10px;
}

.products-scroll-wrapper::-webkit-scrollbar-thumb {
  background: #1b4332;
  border-radius: 10px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.product-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid #e5e0d5;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
  border-color: #1b4332;
}

.product-image-wrapper {
  position: relative;
  height: 100px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image {
  transform: scale(1.05);
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  background: #f5f3ed;
}

.quick-add-btn {
  position: absolute;
  bottom: 6px;
  right: 6px;
  background: white;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
}

.quick-add-btn:hover {
  background: #1b4332;
  color: white;
  transform: scale(1.05);
}

.product-badges {
  position: absolute;
  top: 6px;
  left: 6px;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.variant-badge-small,
.has-variants-badge {
  font-size: 8px;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 3px;
}

.variant-badge-small {
  background: rgba(45, 106, 79, 0.9);
  color: white;
}

.has-variants-badge {
  background: rgba(224, 122, 95, 0.9);
  color: white;
}

.product-info {
  padding: 10px;
  text-align: center;
}

.product-name {
  font-size: 13px;
  font-weight: 600;
  color: #333;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-sku {
  font-size: 9px;
  color: #999;
  margin-bottom: 2px;
}

.product-price {
  font-size: 14px;
  font-weight: 700;
  color: #e07a5f;
}

.product-stock {
  font-size: 10px;
  font-weight: 600;
  margin-top: 2px;
}

.product-stock.in-stock {
  color: #2d6a4f;
}

.product-stock.low-stock {
  color: #f4a261;
}

.product-stock.out-of-stock {
  color: #e07a5f;
}

/* ========== RIGHT SECTION COMPONENTS ========== */
.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.receipt-info {
  display: flex;
  flex-direction: column;
}

.receipt-badge {
  font-size: 11px;
  font-weight: 600;
  color: #e07a5f;
  letter-spacing: 1px;
}

.receipt-number {
  font-size: 20px;
  font-weight: 800;
  color: #1b4332;
  letter-spacing: -0.5px;
}

.order-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: #f5f3ed;
}

.order-type-tabs {
  display: flex;
  gap: 12px;
  background: #f5f3ed;
  padding: 4px;
  border-radius: 60px;
}

.order-type-btn {
  flex: 1;
  text-transform: none;
  font-weight: 600;
  font-size: 13px;
  border-radius: 40px !important;
  padding: 8px 0;
  color: #666;
  transition: all 0.2s ease;
}

.order-type-btn.active {
  background: #1b4332;
  color: white;
}

.customer-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #f8f6f2;
  padding: 16px;
  border-radius: 20px;
}

.input-group label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  color: #666;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.custom-input :deep(.v-field),
.custom-select :deep(.v-field) {
  border-radius: 12px;
}

.order-list-section {
  flex: 1;
  overflow-y: auto;
  max-height: 260px;
}

.order-list-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 16px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.item-count {
  font-size: 12px;
  font-weight: 500;
  color: #999;
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: #f8f6f2;
  border-radius: 16px;
  transition: all 0.2s ease;
}

.order-item:hover {
  background: #f0ede5;
}

.item-info {
  flex: 1;
}

.item-name-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.item-name {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.remove-item-btn {
  opacity: 0.5;
  transition: opacity 0.2s ease;
}

.remove-item-btn:hover {
  opacity: 1;
}

.item-meta {
  display: flex;
  gap: 12px;
  font-size: 11px;
  color: #999;
  margin-bottom: 2px;
}

.item-modifier {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #888;
}

.item-price {
  font-size: 14px;
  font-weight: 700;
  color: #1b4332;
  min-width: 60px;
  text-align: right;
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 4px;
  background: white;
  padding: 2px 6px;
  border-radius: 40px;
}

.qty-btn {
  background: transparent;
}

.quantity {
  font-size: 13px;
  font-weight: 600;
  min-width: 20px;
  text-align: center;
  color: #1b4332;
}

.empty-cart {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 20px;
}

.empty-cart-icon {
  font-size: 56px;
  margin-bottom: 12px;
  opacity: 0.4;
}

.empty-cart-text {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

.empty-cart-subtext {
  font-size: 12px;
  color: #999;
}

/* ========== PAYMENT SECTION ========== */
.payment-section {
  background: #f8f6f2;
  border-radius: 20px;
  padding: 16px 20px;
}

.payment-header {
  font-size: 12px;
  font-weight: 600;
  color: #666;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.payment-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.payment-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #666;
}

.total-row {
  font-size: 17px;
  font-weight: 800;
  color: #1b4332;
  padding-top: 10px;
  border-top: 2px solid #e5e0d5;
  margin-top: 4px;
}

.total-amount {
  color: #e07a5f;
}

.place-order-btn {
  background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 100%) !important;
  color: white !important;
  text-transform: none;
  font-weight: 700;
  font-size: 15px;
  border-radius: 60px !important;
  display: flex;
  justify-content: space-between;
  padding: 6px 20px !important;
  flex: 0 0 auto !important;
  width: 100%;
}

.order-total {
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 10px;
  border-radius: 40px;
  font-size: 13px;
}

/* ========== PAYMENT MODE SECTION ========== */
.payment-mode-section {
  background: #f8f6f2;
  border-radius: 20px;
  padding: 16px 20px;
}

.payment-mode-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #666;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.header-icon {
  color: #2d6a4f;
}

.payment-mode-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.payment-mode-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  background: white;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  position: relative;
}

.payment-mode-card:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.payment-mode-card.active {
  border-color: #2d6a4f;
  background: #f0f9f4;
}

.mode-info {
  flex: 1;
}

.mode-name {
  font-weight: 600;
  color: #1b4332;
  margin-bottom: 1px;
}

.mode-desc {
  font-size: 11px;
  color: #6b7280;
}

.check-icon {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.payment-mode-card.active .check-icon {
  opacity: 1;
}

/* ========== CASH PAYMENT SECTION ========== */
.cash-payment-section {
  background: linear-gradient(135deg, #f8f6f2, #fff);
  border-radius: 20px;
  padding: 16px 20px;
  border: 1px solid #e5e0d5;
}

.cash-payment-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #1b4332;
  margin-bottom: 12px;
  padding-bottom: 6px;
  border-bottom: 2px solid #e07a5f20;
}

.cash-input-group label {
  display: block;
  font-size: 11px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 6px;
}

.currency-input {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 12px;
  border: 2px solid #e5e0d5;
  transition: all 0.3s ease;
}

.currency-input:focus-within {
  border-color: #2d6a4f;
  box-shadow: 0 0 0 3px rgba(45, 106, 79, 0.1);
}

.currency-symbol {
  padding: 10px 14px;
  background: #f8f6f2;
  border-radius: 10px 0 0 10px;
  font-weight: 700;
  color: #1b4332;
  font-size: 13px;
}

.cash-input-field {
  flex: 1;
  padding: 10px 14px;
  border: none;
  outline: none;
  font-size: 15px;
  font-weight: 500;
  background: transparent;
  border-radius: 0 12px 12px 0;
}

.cash-input-field::-webkit-outer-spin-button,
.cash-input-field::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.change-display {
  background: linear-gradient(135deg, #2d6a4f, #1b4332);
  border-radius: 14px;
  padding: 12px;
  text-align: center;
  margin-top: 8px;
}

.change-label {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2px;
}

.change-amount {
  font-size: 24px;
  font-weight: 800;
  color: white;
}

.insufficient-warning {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px;
  background: #fee2e2;
  border-radius: 12px;
  margin-top: 10px;
  font-size: 12px;
  color: #e07a5f;
}

/* ========== FAB ========== */
.fab-menu {
  position: fixed;
  bottom: 28px;
  left: 28px;
  z-index: 100;
}

.fab-add-product {
  position: fixed;
  bottom: 28px;
  left: 28px;
  z-index: 100;
}

/* ========== DIALOG STYLES ========== */
.product-dialog {
  border-radius: 28px !important;
}

.dialog-title {
  font-size: 20px;
  font-weight: 700;
  color: #1b4332;
  padding: 24px 24px 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-dialog-btn {
  color: #999;
}

.product-form {
  padding: 8px 0;
}

.image-preview {
  margin-top: 16px;
  text-align: center;
}

.preview-img {
  max-width: 100%;
  max-height: 150px;
  border-radius: 12px;
  object-fit: cover;
}

.dialog-actions {
  padding: 16px 24px 24px 24px;
  gap: 12px;
}

.cancel-btn {
  text-transform: none;
  font-weight: 500;
  color: #666;
}

.save-btn {
  text-transform: none;
  font-weight: 600;
  color: white !important;
  background: #1b4332 !important;
  border-radius: 40px !important;
  padding: 0 24px !important;
}

/* ========== SNACKBAR ========== */
.custom-snackbar :deep(.v-snackbar__content) {
  font-weight: 500;
  border-radius: 60px;
}

/* ========== SKELETON LOADERS ========== */
.product-card-skeleton {
  border-radius: 16px !important;
}

/* ========== SCANNER MODE ========== */
.scanner-mode {
  padding: 12px 0 20px 0;
  flex: 1;
  overflow-y: auto;
}

.scanner-header {
  text-align: center;
  margin-bottom: 24px;
}

.scanner-icon {
  margin-bottom: 8px;
}

.scanner-title {
  font-size: 22px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 2px;
}

.scanner-subtitle {
  color: #6b7280;
  font-size: 13px;
}

.scanner-input-area {
  margin-bottom: 20px;
}

.scanner-input-wrapper {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 60px;
  padding: 2px 2px 2px 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  border: 2px solid #e5e7eb;
  transition: all 0.3s ease;
}

.scanner-input-wrapper:focus-within {
  border-color: #2d6a4f;
  box-shadow: 0 4px 16px rgba(45, 106, 79, 0.12);
}

.scanner-input-icon {
  color: #9ca3af;
}

.scanner-input {
  flex: 1;
  border: none;
  padding: 12px 10px;
  font-size: 15px;
  outline: none;
  background: transparent;
  font-family: monospace;
  letter-spacing: 1px;
}

.scanner-scan-btn {
  border-radius: 40px !important;
  padding: 6px 14px !important;
  min-width: 70px;
}

.scanner-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 6px;
  font-size: 11px;
  color: #6b7280;
}

.scanner-result {
  background: white;
  border-radius: 16px;
  padding: 16px 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  border: 2px solid #2d6a4f;
  margin-bottom: 20px;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f3f4f6;
}

.result-title {
  font-weight: 600;
  color: #2d6a4f;
}

.result-barcode {
  font-size: 11px;
  color: #6b7280;
}

.result-product {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.result-product-info {
  flex: 1;
}

.result-product-name {
  font-size: 16px;
  font-weight: 700;
  color: #1b4332;
}

.result-product-sku {
  font-size: 11px;
  color: #6b7280;
}

.result-product-price {
  font-size: 18px;
  font-weight: 800;
  color: #e07a5f;
}

.result-add-btn {
  border-radius: 40px !important;
  padding: 0 20px !important;
  min-width: 120px;
}

.result-variants {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f3f4f6;
}

.variant-select-label {
  font-size: 12px;
  font-weight: 600;
  color: #1b4332;
  margin-bottom: 6px;
}

.variant-select-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.variant-select-btn {
  border-radius: 40px !important;
  text-transform: none;
  font-size: 11px;
  padding: 2px 14px !important;
}

.variant-select-btn.active {
  background: #2d6a4f !important;
  color: white !important;
  border-color: #2d6a4f !important;
}

.variant-price {
  font-weight: 600;
  margin-left: 4px;
}

.scanner-no-result {
  text-align: center;
  padding: 30px 16px;
}

.scanner-no-result h3 {
  margin-top: 10px;
  color: #1b4332;
}

.scanner-no-result p {
  color: #6b7280;
  margin: 6px 0 12px;
}

.scanner-loading {
  text-align: center;
  padding: 30px 16px;
}

.scanner-loading p {
  margin-top: 10px;
  color: #6b7280;
}

.recent-scans {
  margin-top: 12px;
}

.recent-scans-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.recent-scans-header span {
  font-size: 12px;
  font-weight: 600;
  color: #1b4332;
}

.recent-scan-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: #f8f6f2;
  border-radius: 12px;
  margin-bottom: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.recent-scan-item:hover {
  background: #f0ede5;
  transform: translateX(4px);
}

.recent-scan-name {
  font-weight: 500;
  color: #1b4332;
}

.recent-scan-barcode {
  font-size: 10px;
  color: #6b7280;
}

.recent-scan-price {
  font-weight: 600;
  color: #e07a5f;
}

/* ========== TOGGLE BUTTON ========== */
.scan-toggle-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 2px 10px !important;
  border-radius: 40px !important;
  background: #f8f6f2 !important;
}

.toggle-label {
  font-size: 11px;
  font-weight: 500;
}

.mode-switch {
  margin: 0 -6px 0 2px;
}

.mode-switch :deep(.v-switch__track) {
  width: 32px;
  height: 18px;
}

/* ========== CART DIALOG ========== */
.cart-dialog-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 0 !important;
}

.cart-dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  background: white;
  position: sticky;
  top: 0;
  z-index: 10;
}

.cart-dialog-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}

.cart-dialog-count {
  font-size: 12px;
  font-weight: 500;
  color: #6b7280;
}

.cart-dialog-body {
  flex: 1;
  overflow-y: auto;
  padding: 14px 18px;
  background: #f8f6f2;
}

.dialog-tabs {
  background: white;
  padding: 4px;
  border-radius: 60px;
  margin-bottom: 14px;
}

.dialog-customer {
  background: white;
  padding: 14px;
  border-radius: 14px;
  margin-bottom: 14px;
}

.cart-dialog-items {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 14px;
}

.cart-dialog-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: white;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.cart-dialog-item:hover {
  background: #f0ede5;
}

.item-dialog-info {
  flex: 1;
}

.item-dialog-name {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  color: #1b4332;
}

.remove-item-btn-dialog {
  opacity: 0.5;
  transition: opacity 0.2s ease;
}

.remove-item-btn-dialog:hover {
  opacity: 1;
}

.item-dialog-meta {
  display: flex;
  gap: 10px;
  font-size: 10px;
  color: #999;
}

.item-dialog-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.item-dialog-price {
  font-weight: 700;
  color: #1b4332;
  min-width: 60px;
  text-align: right;
}

.item-dialog-quantity {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #f8f6f2;
  padding: 2px 6px;
  border-radius: 40px;
}

.item-dialog-quantity span {
  font-size: 13px;
  font-weight: 600;
  min-width: 20px;
  text-align: center;
  color: #1b4332;
}

.empty-cart-dialog {
  text-align: center;
  padding: 40px 16px;
}

.empty-cart-dialog h3 {
  margin-top: 10px;
  color: #1b4332;
}

.empty-cart-dialog p {
  color: #6b7280;
}

.dialog-payment {
  background: white;
  padding: 14px;
  border-radius: 14px;
  margin-bottom: 14px;
}

.dialog-payment-options {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.dialog-payment-options .payment-mode-card {
  flex: 1;
  min-width: 70px;
  padding: 8px 10px;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 2px;
}

.mode-name-dialog {
  font-size: 11px;
  font-weight: 600;
  color: #1b4332;
}

.dialog-cash {
  background: white;
  padding: 14px;
  border-radius: 14px;
  margin-bottom: 14px;
}

.cart-dialog-footer {
  padding: 14px 18px;
  background: white;
  border-top: 1px solid #e5e7eb;
  position: sticky;
  bottom: 0;
}

.dialog-payment-summary {
  margin-bottom: 10px;
}

.dialog-summary-row {
  display: flex;
  justify-content: space-between;
  padding: 3px 0;
  font-size: 13px;
  color: #6b7280;
}

.dialog-summary-row.total {
  font-size: 17px;
  font-weight: 800;
  color: #1b4332;
  border-top: 2px solid #e5e7eb;
  padding-top: 6px;
  margin-top: 2px;
}

.dialog-summary-row.total span:last-child {
  color: #e07a5f;
}

.dialog-place-order {
  border-radius: 40px !important;
  height: 48px !important;
}

/* ========== M-PESA DIALOG ========== */
.mpesa-dialog {
  border-radius: 32px !important;
  overflow: hidden;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px 0;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.mpesa-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}

.dialog-body {
  padding: 20px 24px;
}

.amount-display {
  background: linear-gradient(135deg, #f0f9f4, #e8f5e9);
  border-radius: 20px;
  padding: 16px;
  text-align: center;
  margin-bottom: 20px;
}

.amount-label {
  font-size: 11px;
  color: #6b7280;
  margin-bottom: 6px;
}

.amount-value {
  font-size: 28px;
  font-weight: 800;
  color: #2d6a4f;
}

.phone-input {
  display: flex;
  align-items: center;
  border: 2px solid #e5e0d5;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.phone-input:focus-within {
  border-color: #2d6a4f;
  box-shadow: 0 0 0 3px rgba(45, 106, 79, 0.1);
}

.country-code {
  padding: 10px 14px;
  background: #f8f6f2;
  font-weight: 600;
  color: #1b4332;
}

.phone-field {
  flex: 1;
  padding: 10px 14px;
  border: none;
  outline: none;
  font-size: 15px;
}

.input-hint {
  font-size: 10px;
  color: #9ca3af;
  margin-top: 6px;
}

.payment-instructions {
  margin-top: 20px;
  padding: 14px;
  background: #f8f6f2;
  border-radius: 14px;
}

.instruction-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
}

.instruction-step {
  width: 24px;
  height: 24px;
  background: #2d6a4f;
  color: white;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
}

.instruction-text {
  font-size: 12px;
  color: #374151;
}

/* ========== DEBT DIALOG ========== */
.debt-dialog {
  text-align: center;
  padding: 28px;
  border-radius: 32px !important;
}

.debt-icon {
  margin-bottom: 16px;
}

.debt-dialog h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 10px;
}

.debt-dialog p {
  color: #6b7280;
  margin-bottom: 14px;
}

.debt-amount {
  font-size: 22px;
  font-weight: 800;
  color: #e07a5f;
  margin: 12px 0;
}

.debt-warning {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px;
  background: #fff3e0;
  border-radius: 12px;
  font-size: 11px;
  color: #e07a5f;
  margin: 12px 0;
}

/* ========== CASH CONFIRM DIALOG ========== */
.cash-confirm-dialog {
  text-align: center;
  padding: 28px;
  border-radius: 32px !important;
}

.confirm-icon {
  margin-bottom: 16px;
}

.cash-confirm-dialog h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 16px;
}

.payment-breakdown {
  background: #f8f6f2;
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 16px;
}

.breakdown-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  font-size: 13px;
}

.breakdown-row.change {
  border-top: 1px solid #e5e0d5;
  margin-top: 6px;
  padding-top: 10px;
  font-weight: 700;
  font-size: 15px;
  color: #2d6a4f;
}

/* ========== ANIMATIONS ========== */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

/* ========== RESPONSIVE BREAKPOINTS ========== */
@media (max-width: 1200px) {
  .product-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 1024px) {
  .right-section {
    width: 360px;
    padding: 24px 20px;
  }
}

@media (max-width: 900px) {
  .pos-container {
    flex-direction: column;
    height: auto;
    min-height: calc(100vh - 64px);
  }

  .left-section {
    height: auto;
    min-height: calc(100vh - 64px);
    padding: 0 20px 20px 20px;
  }

  .right-section {
    width: 100%;
    height: auto;
    max-height: 600px;
    border-radius: 32px 32px 0 0;
  }

  .product-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 768px) {
  .left-section {
    padding: 0 16px 16px 16px;
  }

  .product-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .category-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }

  .category-cards-wrapper {
    top: 190px;
  }

  .filters-section {
    top: 126px;
  }

  .search-section {
    top: 72px;
  }

  .header {
    padding: 12px 0 12px 0;
  }

  .header-right {
    gap: 12px;
  }

  .stats-group {
    display: none;
  }

  .right-section {
    max-height: 500px;
    padding: 20px 16px;
  }

  .order-type-btn {
    font-size: 11px;
    padding: 6px 0;
  }

  .scan-toggle-btn .toggle-label {
    display: none;
  }
}

@media (max-width: 480px) {
  .category-cards {
    grid-template-columns: 1fr 1fr;
  }

  .product-grid {
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }

  .category-cards-wrapper {
    top: 175px;
  }

  .filters-section {
    top: 115px;
  }

  .search-section {
    top: 65px;
  }

  .header {
    padding: 8px 0 10px 0;
  }

  .right-section {
    max-height: 450px;
    padding: 16px 12px;
  }

  .logo-text {
    font-size: 18px;
  }

  .logo-badge {
    font-size: 10px;
    padding: 2px 6px;
  }

  .order-item {
    padding: 10px 12px;
  }

  .item-price {
    font-size: 12px;
    min-width: 50px;
  }

  .place-order-btn {
    font-size: 13px;
    padding: 4px 16px !important;
  }

  .payment-mode-card {
    padding: 10px 12px;
  }

  .scanner-title {
    font-size: 18px;
  }

  .scanner-input {
    font-size: 13px;
    padding: 10px 8px;
  }

  .result-product {
    flex-direction: column;
    align-items: stretch;
  }

  .result-add-btn {
    width: 100%;
  }

  .variant-select-grid {
    flex-direction: column;
  }

  .variant-select-btn {
    width: 100%;
  }

  .cart-dialog-title {
    font-size: 16px;
  }

  .cart-dialog-item {
    padding: 8px 10px;
    flex-wrap: wrap;
    gap: 6px;
  }

  .item-dialog-right {
    width: 100%;
    justify-content: space-between;
  }

  .dialog-payment-options {
    flex-direction: column;
  }

  .dialog-payment-options .payment-mode-card {
    flex-direction: row;
    min-width: unset;
  }

  .amount-value {
    font-size: 24px;
  }

  .change-amount {
    font-size: 20px;
  }
}

/* ========== SCROLLBAR STYLING ========== */
.left-section::-webkit-scrollbar,
.order-list-section::-webkit-scrollbar {
  width: 6px;
}

.left-section::-webkit-scrollbar-track,
.order-list-section::-webkit-scrollbar-track {
  background: #e5e0d5;
  border-radius: 10px;
}

.left-section::-webkit-scrollbar-thumb,
.order-list-section::-webkit-scrollbar-thumb {
  background: #1b4332;
  border-radius: 10px;
}
</style>
