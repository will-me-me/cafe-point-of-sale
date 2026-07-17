<!-- components/products/ProductForm.vue -->
<template>
  <div class="product-form-container">
    <!-- Sticky Header -->
    <v-app-bar flat class="sticky-header" elevation="0">
      <v-container fluid class="px-2 px-sm-4">
        <div class="header-content">
          <div class="header-left">
            <v-btn
              icon
              variant="text"
              @click="handleCancel"
              size="small"
              class="d-md-none"
            >
              <v-icon>mdi-arrow-left</v-icon>
            </v-btn>
            <div>
              <div class="page-badge">
                <v-icon size="14" color="#E07A5F">
                  {{
                    mode === "edit"
                      ? "mdi-package-variant"
                      : "mdi-package-variant-plus"
                  }}
                </v-icon>
                Product Management
              </div>
              <h1 class="page-title">
                {{ mode === "edit" ? "Edit Product" : "Add New Product" }}
              </h1>
            </div>
          </div>
          <div class="header-actions">
            <v-btn
              variant="outlined"
              color="#6B7280"
              @click="handleCancel"
              size="small"
              class="d-none d-sm-flex"
            >
              Cancel
            </v-btn>
            <v-btn
              variant="outlined"
              color="#2D6A4F"
              :loading="savingDraft"
              @click="handleSaveDraft"
              size="small"
              class="d-none d-sm-flex"
            >
              Save Draft
            </v-btn>
            <v-btn
              color="#2D6A4F"
              :loading="submitting"
              @click="handleSubmit"
              size="small"
            >
              <v-icon start size="16">mdi-check</v-icon>
              <span class="d-none d-sm-inline">
                {{ mode === "edit" ? "Update Product" : "Publish Product" }}
              </span>
              <span class="d-inline d-sm-none">
                {{ mode === "edit" ? "Update" : "Publish" }}
              </span>
            </v-btn>
          </div>
        </div>
      </v-container>
    </v-app-bar>

    <!-- Main Content -->
    <v-container fluid class="main-content pa-2 pa-sm-4 pa-md-6">
      <v-row>
        <!-- Left Column - Form -->
        <v-col cols="12" lg="8">
          <v-form ref="formRef" v-model="isValid">
            <!-- Basic Information -->
            <v-card
              class="form-card mb-3 mb-md-4"
              elevation="0"
              rounded="lg rounded-xl"
            >
              <v-card-text class="pa-3 pa-sm-4 pa-md-6">
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F" size="20">mdi-information</v-icon>
                  </div>
                  <div>
                    <h3 class="section-title">Basic Information</h3>
                    <p class="section-subtitle">
                      Enter the essential details about your product
                    </p>
                  </div>
                </div>

                <v-row>
                  <v-col cols="12" sm="8">
                    <div class="form-group">
                      <label class="form-label required">Product Name</label>
                      <v-text-field
                        v-model="form.name"
                        placeholder="e.g., Kabras Sugar 2kg"
                        variant="outlined"
                        density="comfortable"
                        :rules="[rules.required]"
                        hide-details="auto"
                        @input="mode === 'create' ? generateSku : undefined"
                      />
                    </div>
                  </v-col>
                  <v-col cols="12" sm="4">
                    <div class="form-group">
                      <label class="form-label required">SKU</label>
                      <v-text-field
                        v-model="form.sku"
                        placeholder="Auto-generated"
                        variant="outlined"
                        density="comfortable"
                        :rules="[rules.required]"
                        hide-details="auto"
                      />
                      <div class="input-hint">
                        Auto-generated, can be modified
                      </div>
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6">
                    <div class="form-group">
                      <label class="form-label">Barcode</label>
                      <v-text-field
                        v-model="form.barcode"
                        placeholder="Scan or enter barcode"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      >
                        <template #append>
                          <v-btn
                            icon
                            variant="text"
                            size="small"
                            color="#2D6A4F"
                            @click="scanBarcode"
                          >
                            <v-icon size="18">mdi-barcode-scan</v-icon>
                          </v-btn>
                        </template>
                      </v-text-field>
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6">
                    <div class="form-group">
                      <label class="form-label required">Product Type</label>
                      <v-select
                        v-model="form.product_type"
                        :items="productTypes"
                        placeholder="Select type"
                        variant="outlined"
                        density="comfortable"
                        :rules="[rules.required]"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <div class="form-group">
                      <label class="form-label">Description</label>
                      <v-textarea
                        v-model="form.description"
                        placeholder="Describe your product in detail..."
                        variant="outlined"
                        rows="3"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <div class="form-group">
                      <label class="form-label">Short Description</label>
                      <v-text-field
                        v-model="form.short_description"
                        placeholder="Brief product description (max 200 chars)"
                        variant="outlined"
                        density="comfortable"
                        maxlength="200"
                        counter
                        hide-details="auto"
                      />
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Classification -->
            <v-card
              class="form-card mb-3 mb-md-4"
              elevation="0"
              rounded="lg rounded-xl"
            >
              <v-card-text class="pa-3 pa-sm-4 pa-md-6">
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F" size="20">mdi-tag</v-icon>
                  </div>
                  <div>
                    <h3 class="section-title">Classification</h3>
                    <p class="section-subtitle">
                      Categorize your product for better organization
                    </p>
                  </div>
                </div>

                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <div class="form-group">
                      <label class="form-label required">Category</label>
                      <v-autocomplete
                        v-model="form.category_id"
                        :items="categoryOptions"
                        placeholder="Search or select category"
                        variant="outlined"
                        density="comfortable"
                        :rules="[rules.required]"
                        hide-details="auto"
                        item-title="title"
                        item-value="value"
                        clearable
                      />
                      <v-btn
                        variant="text"
                        size="small"
                        color="#2D6A4F"
                        class="mt-1"
                        @click="showCategoryDialog = true"
                      >
                        <v-icon size="16">mdi-plus</v-icon>
                        Add New Category
                      </v-btn>
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <div class="form-group">
                      <label class="form-label">Brand</label>
                      <v-autocomplete
                        v-model="form.brand_id"
                        :items="brandOptions"
                        placeholder="Search or select brand"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        item-title="title"
                        item-value="value"
                        clearable
                      />
                      <v-btn
                        variant="text"
                        size="small"
                        color="#2D6A4F"
                        class="mt-1"
                        @click="showBrandDialog = true"
                      >
                        <v-icon size="16">mdi-plus</v-icon>
                        Add New Brand
                      </v-btn>
                    </div>
                  </v-col>

                  <v-col cols="12" sm="12" md="4">
                    <div class="form-group">
                      <label class="form-label">Supplier</label>
                      <v-autocomplete
                        v-model="form.supplier_id"
                        :items="supplierOptions"
                        placeholder="Search supplier"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                        item-title="title"
                        item-value="value"
                        clearable
                      />
                      <v-btn
                        variant="text"
                        size="small"
                        color="#2D6A4F"
                        class="mt-1"
                        @click="showSupplierDialog = true"
                      >
                        <v-icon size="16">mdi-plus</v-icon>
                        Add New Supplier
                      </v-btn>
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <div class="form-group">
                      <label class="form-label">Tags</label>
                      <v-combobox
                        v-model="form.tags"
                        label="Add tags..."
                        variant="outlined"
                        density="comfortable"
                        multiple
                        chips
                        deletable-chips
                        hide-details="auto"
                      />
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <!-- Pricing -->
            <v-card
              class="form-card mb-3 mb-md-4"
              elevation="0"
              rounded="lg rounded-xl"
            >
              <v-card-text class="pa-3 pa-sm-4 pa-md-6">
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F" size="20">mdi-currency-usd</v-icon>
                  </div>
                  <div>
                    <h3 class="section-title">Pricing</h3>
                    <p class="section-subtitle">
                      Set cost and selling prices with automatic margin
                      calculation
                    </p>
                  </div>
                </div>

                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <div class="form-group">
                      <label class="form-label required">Cost Price</label>
                      <v-text-field
                        v-model="form.cost_price"
                        placeholder="0.00"
                        type="number"
                        prefix="KSh"
                        variant="outlined"
                        density="comfortable"
                        :rules="[rules.required, rules.positive]"
                        hide-details="auto"
                        @input="calculatePricing"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <div class="form-group">
                      <label class="form-label required">Selling Price</label>
                      <v-text-field
                        v-model="form.selling_price"
                        placeholder="0.00"
                        type="number"
                        prefix="KSh"
                        variant="outlined"
                        density="comfortable"
                        :rules="[rules.required, rules.positive]"
                        hide-details="auto"
                        @input="calculatePricing"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <div class="form-group">
                      <label class="form-label">Margin</label>
                      <v-text-field
                        :model-value="pricingCalculations.margin"
                        readonly
                        suffix="%"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <div class="form-group">
                      <label class="form-label">Markup</label>
                      <v-text-field
                        :model-value="pricingCalculations.markup"
                        readonly
                        suffix="%"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <div class="form-group">
                      <label class="form-label">Profit per Unit</label>
                      <v-text-field
                        :model-value="pricingCalculations.profit"
                        readonly
                        prefix="KSh"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" sm="6" md="4">
                    <div class="form-group">
                      <label class="form-label">Tax Rate</label>
                      <v-select
                        v-model="form.tax_rate"
                        :items="taxRates"
                        placeholder="Select tax rate"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>
                </v-row>

                <!-- Price Tiers -->
                <div class="price-tiers-section mt-4">
                  <div class="tiers-header">
                    <span class="tiers-title">Price Tiers</span>
                    <v-btn
                      variant="text"
                      size="small"
                      color="#2D6A4F"
                      @click="showTiers = !showTiers"
                    >
                      {{ showTiers ? "Hide" : "Show" }} Advanced Pricing
                      <v-icon size="16">{{
                        showTiers ? "mdi-chevron-up" : "mdi-chevron-down"
                      }}</v-icon>
                    </v-btn>
                  </div>

                  <v-expand-transition>
                    <div v-if="showTiers">
                      <v-row>
                        <v-col cols="6" sm="3" md="3">
                          <div class="form-group">
                            <label class="form-label">Wholesale</label>
                            <v-text-field
                              v-model="form.price_tiers.wholesale"
                              placeholder="0.00"
                              type="number"
                              prefix="KSh"
                              variant="outlined"
                              density="comfortable"
                              hide-details="auto"
                            />
                          </div>
                        </v-col>

                        <v-col cols="6" sm="3" md="3">
                          <div class="form-group">
                            <label class="form-label">Dealer</label>
                            <v-text-field
                              v-model="form.price_tiers.dealer"
                              placeholder="0.00"
                              type="number"
                              prefix="KSh"
                              variant="outlined"
                              density="comfortable"
                              hide-details="auto"
                            />
                          </div>
                        </v-col>

                        <v-col cols="6" sm="3" md="3">
                          <div class="form-group">
                            <label class="form-label">VIP</label>
                            <v-text-field
                              v-model="form.price_tiers.vip"
                              placeholder="0.00"
                              type="number"
                              prefix="KSh"
                              variant="outlined"
                              density="comfortable"
                              hide-details="auto"
                            />
                          </div>
                        </v-col>

                        <v-col cols="6" sm="3" md="3">
                          <div class="form-group">
                            <label class="form-label">Member</label>
                            <v-text-field
                              v-model="form.price_tiers.member"
                              placeholder="0.00"
                              type="number"
                              prefix="KSh"
                              variant="outlined"
                              density="comfortable"
                              hide-details="auto"
                            />
                          </div>
                        </v-col>
                      </v-row>
                    </div>
                  </v-expand-transition>
                </div>
              </v-card-text>
            </v-card>

            <!-- Inventory -->
            <v-card
              class="form-card mb-3 mb-md-4"
              elevation="0"
              rounded="lg rounded-xl"
            >
              <v-card-text class="pa-3 pa-sm-4 pa-md-6">
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F" size="20">mdi-warehouse</v-icon>
                  </div>
                  <div>
                    <h3 class="section-title">Inventory</h3>
                    <p class="section-subtitle">
                      Manage stock levels and reorder points
                    </p>
                  </div>
                </div>

                <v-row>
                  <v-col cols="6" sm="3" md="3">
                    <div class="form-group">
                      <label class="form-label required">Quantity</label>
                      <v-text-field
                        v-model="form.quantity"
                        placeholder="0"
                        type="number"
                        variant="outlined"
                        density="comfortable"
                        :rules="[rules.required, rules.positive]"
                        hide-details="auto"
                        @input="checkInventoryLevel"
                      />
                    </div>
                  </v-col>

                  <v-col cols="6" sm="3" md="3">
                    <div class="form-group">
                      <label class="form-label required">Reorder Level</label>
                      <v-text-field
                        v-model="form.reorder_level"
                        placeholder="10"
                        type="number"
                        variant="outlined"
                        density="comfortable"
                        :rules="[rules.required, rules.positive]"
                        hide-details="auto"
                        @input="checkInventoryLevel"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" sm="3" md="3">
                    <div class="form-group">
                      <label class="form-label">Warehouse</label>
                      <v-select
                        v-model="form.warehouse"
                        :items="warehouseOptions"
                        placeholder="Select warehouse"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12" sm="3" md="3">
                    <div class="form-group">
                      <label class="form-label">Shelf/Rack</label>
                      <v-text-field
                        v-model="form.location"
                        placeholder="Aisle-Shelf"
                        variant="outlined"
                        density="comfortable"
                        hide-details="auto"
                      />
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <div v-if="inventoryWarning" class="inventory-warning">
                      <v-icon color="warning" size="20">mdi-alert</v-icon>
                      <span>{{ inventoryWarning }}</span>
                    </div>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col cols="12">
                    <v-switch
                      v-model="form.track_batches"
                      color="#2D6A4F"
                      hide-details
                    >
                      <template #label>
                        <div>
                          <div class="switch-label">Track Batches</div>
                          <div class="switch-hint">
                            Track products by batch numbers and expiry dates
                          </div>
                        </div>
                      </template>
                    </v-switch>
                  </v-col>
                </v-row>

                <v-expand-transition>
                  <div v-if="form.track_batches">
                    <v-row>
                      <v-col cols="12" sm="6" md="6">
                        <div class="form-group">
                          <label class="form-label">Batch Number</label>
                          <v-text-field
                            v-model="form.batch_number"
                            placeholder="Enter batch number"
                            variant="outlined"
                            density="comfortable"
                            hide-details="auto"
                          />
                        </div>
                      </v-col>
                      <v-col cols="12" sm="6" md="6">
                        <div class="form-group">
                          <label class="form-label">Expiry Date</label>
                          <v-date-picker
                            v-model="form.expiry_date"
                            placeholder="Select expiry date"
                            variant="outlined"
                            density="comfortable"
                            hide-details="auto"
                          />
                        </div>
                      </v-col>
                    </v-row>
                  </div>
                </v-expand-transition>
              </v-card-text>
            </v-card>

            <!-- Bulk Product Wizard -->
            <v-card
              class="form-card mb-3 mb-md-4"
              elevation="0"
              rounded="lg rounded-xl"
            >
              <v-card-text class="pa-3 pa-sm-4 pa-md-6">
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F" size="20"
                      >mdi-file-arrow-up-down</v-icon
                    >
                  </div>
                  <div>
                    <h3 class="section-title">Bulk Product Configuration</h3>
                    <p class="section-subtitle">
                      Configure for bulk products like rice, sugar, and flour
                    </p>
                  </div>
                </div>

                <v-row>
                  <v-col cols="12">
                    <v-switch
                      v-model="form.is_bulk_product"
                      color="#2D6A4F"
                      hide-details
                    >
                      <template #label>
                        <div>
                          <div class="switch-label">This is a Bulk Product</div>
                          <div class="switch-hint">
                            Enable for products sold in bulk with unit
                            conversion
                          </div>
                        </div>
                      </template>
                    </v-switch>
                  </v-col>
                </v-row>

                <v-expand-transition>
                  <div v-if="form.is_bulk_product">
                    <v-row>
                      <v-col cols="12" sm="4" md="4">
                        <div class="form-group">
                          <label class="form-label required"
                            >Purchase Unit</label
                          >
                          <v-text-field
                            v-model="form.purchase_unit"
                            placeholder="e.g., sack, carton"
                            variant="outlined"
                            density="comfortable"
                            :rules="
                              form.is_bulk_product ? [rules.required] : []
                            "
                            hide-details="auto"
                          />
                        </div>
                      </v-col>

                      <v-col cols="12" sm="4" md="4">
                        <div class="form-group">
                          <label class="form-label required"
                            >Selling Unit</label
                          >
                          <v-text-field
                            v-model="form.selling_unit"
                            placeholder="e.g., kg, gm"
                            variant="outlined"
                            density="comfortable"
                            :rules="
                              form.is_bulk_product ? [rules.required] : []
                            "
                            hide-details="auto"
                          />
                        </div>
                      </v-col>

                      <v-col cols="12" sm="4" md="4">
                        <div class="form-group">
                          <label class="form-label required"
                            >Conversion Factor</label
                          >
                          <v-text-field
                            v-model="form.conversion_factor"
                            placeholder="e.g., 90"
                            type="number"
                            variant="outlined"
                            density="comfortable"
                            :rules="
                              form.is_bulk_product
                                ? [rules.required, rules.positive]
                                : []
                            "
                            hide-details="auto"
                          />
                          <div class="input-hint">
                            How many selling units in one purchase unit?
                          </div>
                        </div>
                      </v-col>
                    </v-row>

                    <!-- Auto-generate variants from bulk product -->
                    <div class="bulk-variant-generator mt-4">
                      <div class="generator-header">
                        <span class="generator-title"
                          >Generate Variants Automatically</span
                        >
                        <v-btn
                          color="#2D6A4F"
                          variant="outlined"
                          size="small"
                          @click="autoGenerateVariants"
                          :disabled="!canGenerateVariants"
                        >
                          <v-icon start size="16">mdi-auto-fix</v-icon>
                          Generate
                        </v-btn>
                      </div>

                      <v-row>
                        <v-col cols="12">
                          <div class="form-group">
                            <label class="form-label">Available Sizes</label>
                            <v-combobox
                              v-model="bulkSizes"
                              label="Enter sizes (e.g., 250g, 500g, 1kg)"
                              variant="outlined"
                              density="comfortable"
                              multiple
                              chips
                              deletable-chips
                              hide-details="auto"
                            />
                          </div>
                        </v-col>
                      </v-row>

                      <div
                        v-if="generatedVariants.length > 0"
                        class="generated-variants"
                      >
                        <div class="variants-preview">
                          <h4>
                            Generated Variants ({{ generatedVariants.length }})
                          </h4>
                          <div class="table-responsive">
                            <v-table density="compact">
                              <thead>
                                <tr>
                                  <th>Size</th>
                                  <th>SKU</th>
                                  <th>Price</th>
                                  <th>Stock</th>
                                </tr>
                              </thead>
                              <tbody>
                                <tr
                                  v-for="(variant, index) in generatedVariants"
                                  :key="index"
                                >
                                  <td>
                                    {{
                                      variant.attributes?.size ||
                                      variant.variant_name
                                    }}
                                  </td>
                                  <td
                                    class="text-truncate"
                                    style="max-width: 80px"
                                  >
                                    {{ variant.sku }}
                                  </td>
                                  <td>KSh {{ variant.selling_price }}</td>
                                  <td>{{ variant.quantity }}</td>
                                </tr>
                              </tbody>
                            </v-table>
                          </div>
                          <v-btn
                            color="#2D6A4F"
                            class="mt-2"
                            @click="applyGeneratedVariants"
                            size="small"
                            block
                          >
                            Apply All Variants
                          </v-btn>
                        </div>
                      </div>
                    </div>
                  </div>
                </v-expand-transition>
              </v-card-text>
            </v-card>

            <!-- Variants -->
            <v-card
              class="form-card mb-3 mb-md-4"
              elevation="0"
              rounded="lg rounded-xl"
            >
              <v-card-text class="pa-3 pa-sm-4 pa-md-6">
                <div class="section-header">
                  <div class="section-icon">
                    <v-icon color="#2D6A4F" size="20"
                      >mdi-swap-horizontal</v-icon
                    >
                  </div>
                  <div>
                    <h3 class="section-title">Product Variants</h3>
                    <p class="section-subtitle">
                      Add variations like sizes, colors, or flavors
                    </p>
                  </div>
                  <v-btn
                    color="#2D6A4F"
                    variant="outlined"
                    size="small"
                    @click="addVariant"
                  >
                    <v-icon start size="16">mdi-plus</v-icon>
                    Add Variant
                  </v-btn>
                </div>

                <div v-if="form.variants.length === 0" class="empty-variants">
                  <v-icon size="40" color="#9CA3AF"
                    >mdi-swap-horizontal-circle-outline</v-icon
                  >
                  <h4>No variants yet</h4>
                  <p>Click "Add Variant" to create product variations</p>
                </div>

                <div v-else class="variants-list">
                  <div
                    v-for="(variant, index) in form.variants"
                    :key="index"
                    class="variant-item"
                  >
                    <div class="variant-header">
                      <div class="variant-number">#{{ index + 1 }}</div>
                      <div class="variant-actions">
                        <v-btn
                          icon
                          size="x-small"
                          variant="text"
                          color="#2D6A4F"
                          @click="editVariant(index)"
                        >
                          <v-icon size="14">mdi-pencil</v-icon>
                        </v-btn>
                        <v-btn
                          icon
                          size="x-small"
                          variant="text"
                          color="#E07A5F"
                          @click="removeVariant(index)"
                        >
                          <v-icon size="14">mdi-delete</v-icon>
                        </v-btn>
                      </div>
                    </div>
                    <div class="variant-info">
                      <div class="variant-field">
                        <span class="field-label">Name:</span>
                        <span>{{ variant.variant_name || "Not set" }}</span>
                      </div>
                      <div class="variant-field">
                        <span class="field-label">SKU:</span>
                        <span>{{ variant.sku || "Not set" }}</span>
                      </div>
                      <div class="variant-field">
                        <span class="field-label">Price:</span>
                        <span>KSh {{ variant.selling_price || "0.00" }}</span>
                      </div>
                      <div class="variant-field">
                        <span class="field-label">Stock:</span>
                        <span>{{ variant.quantity || "0" }}</span>
                      </div>
                      <div
                        class="variant-tags"
                        v-if="
                          variant.attributes &&
                          Object.keys(variant.attributes).length > 0
                        "
                      >
                        <v-chip
                          v-for="(value, key) in variant.attributes"
                          :key="key"
                          size="x-small"
                          color="#f5f3ed"
                        >
                          {{ key }}: {{ value }}
                        </v-chip>
                      </div>
                    </div>
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-form>
        </v-col>

        <!-- Right Column - Preview & Settings -->
        <v-col cols="12" lg="4">
          <!-- Live Product Preview -->
          <v-card
            class="form-card mb-3 mb-md-4"
            elevation="0"
            rounded="lg rounded-xl"
          >
            <v-card-text class="pa-3 pa-sm-4 pa-md-6">
              <div class="section-header">
                <div class="section-icon">
                  <v-icon color="#2D6A4F" size="20">mdi-eye</v-icon>
                </div>
                <div>
                  <h3 class="section-title">Live Preview</h3>
                  <p class="section-subtitle">
                    See how your product will appear
                  </p>
                </div>
              </div>

              <div class="product-preview">
                <div class="preview-image">
                  <v-img
                    v-if="imagePreview"
                    :src="imagePreview"
                    cover
                    height="120"
                    class="rounded"
                  />
                  <div v-else class="preview-placeholder">
                    <v-icon size="32" color="#9CA3AF">mdi-image</v-icon>
                    <span>No image</span>
                  </div>
                </div>

                <div class="preview-details">
                  <div class="preview-item">
                    <span class="preview-label">Name</span>
                    <span
                      class="preview-value text-truncate"
                      style="max-width: 120px"
                    >
                      {{ form.name || "Not set" }}
                    </span>
                  </div>
                  <div class="preview-item">
                    <span class="preview-label">SKU</span>
                    <span class="preview-value">{{
                      form.sku || "Not set"
                    }}</span>
                  </div>
                  <div class="preview-item">
                    <span class="preview-label">Category</span>
                    <span
                      class="preview-value text-truncate"
                      style="max-width: 120px"
                    >
                      {{ getCategoryName(form.category_id) || "Not set" }}
                    </span>
                  </div>
                  <div class="preview-item">
                    <span class="preview-label">Brand</span>
                    <span
                      class="preview-value text-truncate"
                      style="max-width: 120px"
                    >
                      {{ getBrandName(form.brand_id) || "Not set" }}
                    </span>
                  </div>
                  <div class="preview-item">
                    <span class="preview-label">Price</span>
                    <span class="preview-value"
                      >KSh {{ form.selling_price || "0.00" }}</span
                    >
                  </div>
                  <div class="preview-item">
                    <span class="preview-label">Stock</span>
                    <span class="preview-value" :class="getStockClass">
                      {{ form.quantity || "0" }} units
                      <span v-if="inventoryWarning" class="stock-warning">
                        <v-icon size="12" color="warning">mdi-alert</v-icon>
                      </span>
                    </span>
                  </div>
                  <div class="preview-item" v-if="pricingCalculations.margin">
                    <span class="preview-label">Margin</span>
                    <span class="preview-value"
                      >{{ pricingCalculations.margin }}%</span
                    >
                  </div>
                  <div class="preview-item" v-if="form.is_bulk_product">
                    <span class="preview-label">Bulk</span>
                    <span
                      class="preview-value text-truncate"
                      style="max-width: 120px"
                    >
                      {{ form.purchase_unit }} → {{ form.selling_unit }}
                    </span>
                  </div>
                  <!-- Product Info (Edit Mode Only) -->
                  <template v-if="mode === 'edit' && productData">
                    <div class="preview-item">
                      <span class="preview-label">Status</span>
                      <span class="preview-value">
                        <v-chip
                          :color="productData.is_active ? 'success' : 'error'"
                          size="x-small"
                        >
                          {{ productData.is_active ? "Active" : "Inactive" }}
                        </v-chip>
                      </span>
                    </div>
                    <div class="preview-item">
                      <span class="preview-label">Created</span>
                      <span class="preview-value">{{
                        formatDate(productData.created_at)
                      }}</span>
                    </div>
                  </template>
                </div>
              </div>
            </v-card-text>
          </v-card>

          <!-- Product Image -->
          <v-card
            class="form-card mb-3 mb-md-4"
            elevation="0"
            rounded="lg rounded-xl"
          >
            <v-card-text class="pa-3 pa-sm-4 pa-md-6">
              <div class="section-header">
                <div class="section-icon">
                  <v-icon color="#2D6A4F" size="20">mdi-image</v-icon>
                </div>
                <div>
                  <h3 class="section-title">Product Image</h3>
                  <p class="section-subtitle">Upload product images</p>
                </div>
              </div>

              <div
                class="image-upload-area"
                :class="{ 'drag-over': isDragging }"
                @click="triggerFileInput"
                @dragover.prevent="isDragging = true"
                @dragleave="isDragging = false"
                @drop.prevent="handleDrop"
              >
                <input
                  ref="fileInput"
                  type="file"
                  accept="image/*"
                  multiple
                  hidden
                  @change="handleImageUpload"
                />
                <div v-if="imagePreview" class="image-preview">
                  <img :src="imagePreview" alt="Preview" />
                  <div class="image-overlay">
                    <v-icon size="24">mdi-camera</v-icon>
                    <span>Change Image</span>
                  </div>
                </div>
                <div v-else class="upload-placeholder">
                  <v-icon size="36" color="#9CA3AF">mdi-image-plus</v-icon>
                  <p>Click to upload or drag & drop</p>
                  <span>PNG, JPG up to 5MB</span>
                </div>
              </div>

              <div v-if="imageFiles.length > 1" class="image-thumbnails">
                <div
                  v-for="(file, index) in imageFiles"
                  :key="index"
                  class="thumbnail"
                >
                  <img :src="file.preview" alt="Thumbnail" />
                </div>
              </div>
            </v-card-text>
          </v-card>

          <!-- Settings -->
          <v-card
            class="form-card mb-3 mb-md-4"
            elevation="0"
            rounded="lg rounded-xl"
          >
            <v-card-text class="pa-3 pa-sm-4 pa-md-6">
              <div class="section-header">
                <div class="section-icon">
                  <v-icon color="#2D6A4F" size="20">mdi-cog</v-icon>
                </div>
                <div>
                  <h3 class="section-title">Settings</h3>
                  <p class="section-subtitle">Configure product options</p>
                </div>
              </div>

              <div class="form-group">
                <v-switch
                  v-model="form.has_variants"
                  color="#2D6A4F"
                  hide-details
                >
                  <template #label>
                    <div>
                      <div class="switch-label">Has Variants</div>
                      <div class="switch-hint">
                        Enable for products with multiple variations
                      </div>
                    </div>
                  </template>
                </v-switch>
              </div>

              <div class="form-group mt-2">
                <v-switch
                  v-model="form.is_featured"
                  color="#2D6A4F"
                  hide-details
                >
                  <template #label>
                    <div>
                      <div class="switch-label">Featured Product</div>
                      <div class="switch-hint">
                        Highlight this product in the store
                      </div>
                    </div>
                  </template>
                </v-switch>
              </div>

              <div class="form-group mt-2">
                <v-switch v-model="form.is_active" color="#2D6A4F" hide-details>
                  <template #label>
                    <div>
                      <div class="switch-label">Active</div>
                      <div class="switch-hint">
                        Product visible in the store
                      </div>
                    </div>
                  </template>
                </v-switch>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Mobile Bottom Action Bar -->
    <v-bottom-navigation
      v-model="bottomNav"
      color="#2D6A4F"
      class="d-flex d-md-none"
      style="position: fixed; bottom: 0; left: 0; right: 0; z-index: 100"
      bg-color="white"
      elevation="8"
    >
      <v-btn @click="handleCancel" variant="text">
        <v-icon>mdi-close</v-icon>
        <span>Cancel</span>
      </v-btn>
      <v-btn @click="handleSaveDraft" :loading="savingDraft" variant="text">
        <v-icon>mdi-content-save-outline</v-icon>
        <span>Draft</span>
      </v-btn>
      <v-btn
        @click="handleSubmit"
        :loading="submitting"
        color="#2D6A4F"
        variant="flat"
      >
        <v-icon>mdi-check</v-icon>
        <span>{{ mode === "edit" ? "Update" : "Publish" }}</span>
      </v-btn>
    </v-bottom-navigation>

    <!-- Variant Dialog -->
    <v-dialog
      v-model="variantDialog.show"
      max-width="600"
      :fullscreen="$vuetify.display.smAndDown"
    >
      <v-card class="variant-dialog">
        <div class="dialog-header">
          <h3>{{ variantDialog.editing ? "Edit Variant" : "Add Variant" }}</h3>
          <v-btn icon variant="text" @click="variantDialog.show = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>

        <v-card-text>
          <v-form ref="variantFormRef" v-model="variantFormValid">
            <v-row>
              <v-col cols="12">
                <div class="form-group">
                  <label class="form-label required">Variant Name</label>
                  <v-text-field
                    v-model="variantForm.variant_name"
                    placeholder="e.g., 500ml, Size M, Red"
                    variant="outlined"
                    density="comfortable"
                    :rules="[rules.required]"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12" sm="6">
                <div class="form-group">
                  <label class="form-label required">SKU</label>
                  <v-text-field
                    v-model="variantForm.sku"
                    placeholder="e.g., RICE-500G"
                    variant="outlined"
                    density="comfortable"
                    :rules="[rules.required]"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12" sm="6">
                <div class="form-group">
                  <label class="form-label">Barcode</label>
                  <v-text-field
                    v-model="variantForm.barcode"
                    placeholder="Barcode number"
                    variant="outlined"
                    density="comfortable"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12" sm="6">
                <div class="form-group">
                  <label class="form-label required">Selling Price</label>
                  <v-text-field
                    v-model="variantForm.selling_price"
                    placeholder="0.00"
                    type="number"
                    prefix="KSh"
                    variant="outlined"
                    density="comfortable"
                    :rules="[rules.required, rules.positive]"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12" sm="6">
                <div class="form-group">
                  <label class="form-label required">Stock Quantity</label>
                  <v-text-field
                    v-model="variantForm.quantity"
                    placeholder="0"
                    type="number"
                    variant="outlined"
                    density="comfortable"
                    :rules="[rules.required, rules.positive]"
                    hide-details="auto"
                  />
                </div>
              </v-col>

              <v-col cols="12">
                <div class="form-group">
                  <label class="form-label">Attributes (JSON)</label>
                  <v-textarea
                    v-model="variantForm.attributes_json"
                    placeholder='{"size": "500ml", "flavor": "Strawberry"}'
                    variant="outlined"
                    rows="2"
                    density="comfortable"
                    hide-details="auto"
                  />
                  <div class="input-hint">
                    Enter attributes as JSON key-value pairs
                  </div>
                </div>
              </v-col>

              <v-col cols="12">
                <v-switch
                  v-model="variantForm.is_default"
                  color="#2D6A4F"
                  hide-details
                >
                  <template #label>
                    <div>
                      <div class="switch-label">Default Variant</div>
                      <div class="switch-hint">
                        This variant will be shown by default
                      </div>
                    </div>
                  </template>
                </v-switch>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="variantDialog.show = false"
            >Cancel</v-btn
          >
          <v-btn
            color="#2D6A4F"
            :disabled="!variantFormValid"
            @click="saveVariant"
          >
            {{ variantDialog.editing ? "Update" : "Add" }} Variant
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Category Dialog -->
    <v-dialog
      v-model="showCategoryDialog"
      max-width="400"
      :fullscreen="$vuetify.display.smAndDown"
    >
      <v-card class="quick-add-dialog">
        <div class="dialog-header">
          <h3>Add Category</h3>
          <v-btn icon variant="text" @click="showCategoryDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
        <v-card-text>
          <v-form ref="categoryFormRef" v-model="categoryFormValid">
            <div class="form-group">
              <label class="form-label required">Category Name</label>
              <v-text-field
                v-model="newCategory"
                placeholder="e.g., Grains, Beverages"
                variant="outlined"
                density="comfortable"
                :rules="[rules.required]"
                hide-details="auto"
              />
            </div>
          </v-form>
        </v-card-text>
        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="showCategoryDialog = false"
            >Cancel</v-btn
          >
          <v-btn
            color="#2D6A4F"
            :disabled="!categoryFormValid"
            @click="addCategory"
          >
            Add Category
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Brand Dialog -->
    <v-dialog
      v-model="showBrandDialog"
      max-width="400"
      :fullscreen="$vuetify.display.smAndDown"
    >
      <v-card class="quick-add-dialog">
        <div class="dialog-header">
          <h3>Add Brand</h3>
          <v-btn icon variant="text" @click="showBrandDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
        <v-card-text>
          <v-form ref="brandFormRef" v-model="brandFormValid">
            <div class="form-group">
              <label class="form-label required">Brand Name</label>
              <v-text-field
                v-model="newBrand"
                placeholder="e.g., Tuzo, Ajab, Sawa"
                variant="outlined"
                density="comfortable"
                :rules="[rules.required]"
                hide-details="auto"
              />
            </div>
          </v-form>
        </v-card-text>
        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="showBrandDialog = false">Cancel</v-btn>
          <v-btn color="#2D6A4F" :disabled="!brandFormValid" @click="addBrand">
            Add Brand
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Supplier Dialog -->
    <v-dialog
      v-model="showSupplierDialog"
      max-width="400"
      :fullscreen="$vuetify.display.smAndDown"
    >
      <v-card class="quick-add-dialog">
        <div class="dialog-header">
          <h3>Add Supplier</h3>
          <v-btn icon variant="text" @click="showSupplierDialog = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
        <v-card-text>
          <v-form ref="supplierFormRef" v-model="supplierFormValid">
            <div class="form-group">
              <label class="form-label required">Supplier Name</label>
              <v-text-field
                v-model="newSupplier"
                placeholder="e.g., ABC Wholesalers"
                variant="outlined"
                density="comfortable"
                :rules="[rules.required]"
                hide-details="auto"
              />
            </div>
          </v-form>
        </v-card-text>
        <v-card-actions class="dialog-actions">
          <v-btn variant="text" @click="showSupplierDialog = false"
            >Cancel</v-btn
          >
          <v-btn
            color="#2D6A4F"
            :disabled="!supplierFormValid"
            @click="addSupplier"
          >
            Add Supplier
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Success Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :timeout="3000"
      :color="snackbar.color"
      location="top"
    >
      {{ snackbar.text }}
      <template v-slot:actions>
        <v-btn variant="text" icon="mdi-close" @click="snackbar.show = false" />
      </template>
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { usePosStore } from "~/stores/pos";

const props = defineProps<{
  mode: "create" | "edit";
  productId?: string;
}>();

const emit = defineEmits<{
  (e: "success", product: any): void;
  (e: "cancel"): void;
}>();

const router = useRouter();
const store = usePosStore();

// Loading state for edit mode
const loading = ref(false);
const productData = ref(null);

// Form refs
const formRef = ref(null);
const variantFormRef = ref(null);
const categoryFormRef = ref(null);
const brandFormRef = ref(null);
const supplierFormRef = ref(null);

// Form state
const isValid = ref(false);
const variantFormValid = ref(false);
const categoryFormValid = ref(false);
const brandFormValid = ref(false);
const supplierFormValid = ref(false);
const submitting = ref(false);
const savingDraft = ref(false);
const showTiers = ref(false);
const isDragging = ref(false);
const bottomNav = ref(0);

// Image handling
const fileInput = ref(null);
const imagePreview = ref("");
const imageFiles = ref([]);

// Variant generation
const bulkSizes = ref([]);
const generatedVariants = ref([]);

// Dialogs
const showCategoryDialog = ref(false);
const showBrandDialog = ref(false);
const showSupplierDialog = ref(false);
const newCategory = ref("");
const newBrand = ref("");
const newSupplier = ref("");

// Variant dialog
const variantDialog = ref({
  show: false,
  editing: false,
  index: -1,
});

const variantForm = ref({
  variant_name: "",
  sku: "",
  barcode: "",
  selling_price: "",
  quantity: "",
  attributes_json: "",
  is_default: false,
});

// Form data
const form = ref({
  name: "",
  sku: "",
  barcode: "",
  description: "",
  short_description: "",
  category_id: "",
  brand_id: "",
  supplier_id: "",
  tags: [],
  cost_price: "",
  selling_price: "",
  tax_rate: 16,
  price_tiers: {
    wholesale: "",
    dealer: "",
    vip: "",
    member: "",
  },
  quantity: "",
  reorder_level: 10,
  warehouse: "main",
  location: "",
  product_type: "stock",
  has_variants: false,
  track_batches: false,
  is_featured: false,
  is_active: true,
  is_bulk_product: false,
  purchase_unit: "",
  selling_unit: "",
  conversion_factor: "",
  batch_number: "",
  expiry_date: "",
  variants: [],
  images: [],
  notes: "",
});

// Options
const productTypes = [
  { title: "Stock", value: "stock" },
  { title: "Service", value: "service" },
  { title: "Digital", value: "digital" },
  { title: "Rental", value: "rental" },
];

const taxRates = [
  { title: "0% (Zero Rated)", value: 0 },
  { title: "16% (Standard)", value: 16 },
  { title: "8% (Reduced)", value: 8 },
];

const warehouseOptions = [
  { title: "Main Warehouse", value: "main" },
  { title: "Branch A", value: "branch_a" },
  { title: "Branch B", value: "branch_b" },
  { title: "Online Store", value: "online" },
];

const categoryOptions = ref([]);
const brandOptions = ref([]);
const supplierOptions = ref([]);

// Snackbar
const snackbar = ref({
  show: false,
  text: "",
  color: "success",
});

// Rules
const rules = {
  required: (v: any) => !!v || "This field is required",
  positive: (v: number) => v >= 0 || "Value must be positive",
};

// Computed
const pricingCalculations = computed(() => {
  const cost = parseFloat(form.value.cost_price) || 0;
  const selling = parseFloat(form.value.selling_price) || 0;

  let margin = 0;
  let markup = 0;
  let profit = 0;

  if (selling > 0) {
    margin = ((selling - cost) / selling) * 100;
    profit = selling - cost;
  }

  if (cost > 0) {
    markup = ((selling - cost) / cost) * 100;
  }

  return {
    margin: margin > 0 ? margin.toFixed(2) : "0.00",
    markup: markup > 0 ? markup.toFixed(2) : "0.00",
    profit: profit > 0 ? profit.toFixed(2) : "0.00",
  };
});

const inventoryWarning = computed(() => {
  const quantity = parseInt(form.value.quantity) || 0;
  const reorder = parseInt(form.value.reorder_level) || 0;

  if (quantity === 0 && reorder > 0) {
    return "⚠ Product is out of stock";
  }
  if (quantity > 0 && reorder > 0 && quantity <= reorder) {
    return `⚠ Product is below reorder level (${quantity} ≤ ${reorder})`;
  }
  return null;
});

const getStockClass = computed(() => {
  const quantity = parseInt(form.value.quantity) || 0;
  const reorder = parseInt(form.value.reorder_level) || 0;
  if (quantity === 0) return "stock-out";
  if (reorder > 0 && quantity <= reorder) return "stock-low";
  return "stock-ok";
});

const canGenerateVariants = computed(() => {
  return (
    form.value.is_bulk_product &&
    form.value.purchase_unit &&
    form.value.selling_unit &&
    form.value.conversion_factor &&
    bulkSizes.value.length > 0
  );
});

// Methods
const formatDate = (date: string) => {
  if (!date) return "N/A";
  return new Date(date).toLocaleDateString("en-KE", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

const generateSku = () => {
  if (!form.value.name) return;
  if (form.value.sku) return;

  const nameParts = form.value.name.split(" ");
  const prefix = nameParts
    .slice(0, 3)
    .map((part) => part.substring(0, 3).toUpperCase())
    .join("-");

  const random = Math.floor(Math.random() * 1000)
    .toString()
    .padStart(3, "0");
  form.value.sku = `${prefix}-${random}`;
};

const calculatePricing = () => {
  // Handled by computed property
};

const checkInventoryLevel = () => {
  // Handled by computed property
};

const scanBarcode = () => {
  snackbar.value = {
    show: true,
    text: "Barcode scanner coming soon!",
    color: "info",
  };
};

// Image methods
const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleImageUpload = (event: Event) => {
  const input = event.target as HTMLInputElement;
  const files = input.files;
  if (files) {
    processFiles(files);
  }
};

const handleDrop = (event: DragEvent) => {
  isDragging.value = false;
  const files = event.dataTransfer?.files;
  if (files) {
    processFiles(files);
  }
};

const processFiles = (files: FileList) => {
  for (let i = 0; i < files.length; i++) {
    const file = files[i];
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const preview = e.target?.result as string;
        imageFiles.value.push({
          file: file,
          preview: preview,
          uploaded: false,
        });
        if (!imagePreview.value) {
          imagePreview.value = preview;
        }
      };
      reader.readAsDataURL(file);
    }
  }
};

// Variant generation
const autoGenerateVariants = () => {
  if (!canGenerateVariants.value) return;

  const baseSku =
    form.value.sku || form.value.name.substring(0, 8).toUpperCase();
  const baseSellingPrice = Number(form.value.selling_price) || 0;
  const conversionFactor = Number(form.value.conversion_factor) || 1;
  const baseStock = Number(form.value.quantity) || 0;

  generatedVariants.value = bulkSizes.value.map((size: string) => {
    const number = parseFloat(size.replace(/[^\d.]/g, ""));
    const unit = size.replace(/[\d.\s]/g, "").toLowerCase();

    let weightKg = 0;

    switch (unit) {
      case "kg":
        weightKg = number;
        break;
      case "g":
        weightKg = number / 1000;
        break;
      case "mg":
        weightKg = number / 1000000;
        break;
      default:
        weightKg = number;
    }

    const pricePerKg = baseSellingPrice / conversionFactor;

    return {
      sku: `${baseSku}-${size.replace(/\s+/g, "")}`,
      variant_name: size,
      quantity: 0,
      selling_price: Number((pricePerKg * weightKg).toFixed(2)),
      is_default: false,
      attributes: {
        size,
        unit,
        weight_kg: weightKg,
      },
    };
  });
};

const applyGeneratedVariants = () => {
  if (!generatedVariants.value.length) return;

  form.value.variants = generatedVariants.value.map((v: any) => ({
    variant_name: v.variant_name,
    sku: v.sku,
    barcode: "",
    selling_price: v.selling_price,
    quantity: v.quantity,
    is_default: v.is_default,
    attributes: v.attributes,
    attributes_json: JSON.stringify(v.attributes),
  }));

  generatedVariants.value = [];
  bulkSizes.value = [];

  snackbar.value = {
    show: true,
    text: `${form.value.variants.length} variants generated successfully!`,
    color: "success",
  };
};

// Variant CRUD
const addVariant = () => {
  variantDialog.value = {
    show: true,
    editing: false,
    index: -1,
  };
  resetVariantForm();
};

const editVariant = (index: number) => {
  const variant = form.value.variants[index];
  variantDialog.value = {
    show: true,
    editing: true,
    index: index,
  };
  variantForm.value = {
    variant_name: variant.variant_name || "",
    sku: variant.sku || "",
    barcode: variant.barcode || "",
    selling_price: variant.selling_price || "",
    quantity: variant.quantity || "",
    attributes_json: variant.attributes_json || "",
    is_default: variant.is_default || false,
  };
};

const removeVariant = (index: number) => {
  form.value.variants.splice(index, 1);
};

const resetVariantForm = () => {
  variantForm.value = {
    variant_name: "",
    sku: "",
    barcode: "",
    selling_price: "",
    quantity: "",
    attributes_json: "",
    is_default: false,
  };
};

const saveVariant = async () => {
  const { valid } = await variantFormRef.value.validate();
  if (!valid) return;

  const variantData = {
    variant_name: variantForm.value.variant_name,
    sku: variantForm.value.sku,
    barcode: variantForm.value.barcode || undefined,
    selling_price: parseFloat(variantForm.value.selling_price) || 0,
    quantity: parseInt(variantForm.value.quantity) || 0,
    attributes_json: variantForm.value.attributes_json || "",
    is_default: variantForm.value.is_default || false,
  };

  if (variantDialog.value.editing) {
    form.value.variants[variantDialog.value.index] = variantData;
  } else {
    form.value.variants.push(variantData);
  }

  variantDialog.value.show = false;
  resetVariantForm();

  snackbar.value = {
    show: true,
    text: `Variant ${
      variantDialog.value.editing ? "updated" : "added"
    } successfully!`,
    color: "success",
  };
};

// Helper methods
const getCategoryName = (id: string) => {
  const category = categoryOptions.value.find((c: any) => c.value === id);
  return category ? category.title : null;
};

const getBrandName = (id: string) => {
  const brand = brandOptions.value.find((b: any) => b.value === id);
  return brand ? brand.title : null;
};

// Dialog methods
const addCategory = () => {
  if (newCategory.value) {
    const newId = newCategory.value.toLowerCase().replace(/\s+/g, "-");
    categoryOptions.value.push({
      title: newCategory.value,
      value: newId,
    });
    form.value.category_id = newId;
    showCategoryDialog.value = false;
    newCategory.value = "";

    snackbar.value = {
      show: true,
      text: "Category added successfully!",
      color: "success",
    };
  }
};

const addBrand = () => {
  if (newBrand.value) {
    const newId = newBrand.value.toLowerCase().replace(/\s+/g, "-");
    brandOptions.value.push({
      title: newBrand.value,
      value: newId,
    });
    form.value.brand_id = newId;
    showBrandDialog.value = false;
    newBrand.value = "";

    snackbar.value = {
      show: true,
      text: "Brand added successfully!",
      color: "success",
    };
  }
};

const addSupplier = () => {
  if (newSupplier.value) {
    const newId = newSupplier.value.toLowerCase().replace(/\s+/g, "-");
    supplierOptions.value.push({
      title: newSupplier.value,
      value: newId,
    });
    form.value.supplier_id = newId;
    showSupplierDialog.value = false;
    newSupplier.value = "";

    snackbar.value = {
      show: true,
      text: "Supplier added successfully!",
      color: "success",
    };
  }
};

// Build product data for API
const buildProductData = () => {
  return {
    name: form.value.name.trim(),
    description: form.value.description || "",
    short_description: form.value.short_description || "",
    sku: form.value.sku.trim(),
    barcode: form.value.barcode || "",
    product_type: form.value.product_type || "stock",
    category_id: form.value.category_id || null,
    brand_id: form.value.brand_id || null,
    supplier_id: form.value.supplier_id || null,
    suppliers: form.value.supplier_id
      ? [
          {
            supplier_id: form.value.supplier_id,
            preferred: true,
            is_active: true,
          },
        ]
      : [],
    inventory: {
      quantity: Number(form.value.quantity) || 0,
      reserved: 0,
      reorder_level: Number(form.value.reorder_level) || 10,
      location: form.value.location || "",
      warehouse: form.value.warehouse || "main",
      status: Number(form.value.quantity) > 0 ? "in_stock" : "out_of_stock",
      batch_number: form.value.batch_number || undefined,
      expiry_date: form.value.expiry_date || undefined,
    },
    pricing: {
      cost_price: Number(form.value.cost_price) || 0,
      selling_price: Number(form.value.selling_price) || 0,

      price_tiers: {
        // REQUIRED
        retail: Number(form.value.selling_price) || 0,

        wholesale:
          form.value.price_tiers?.wholesale !== null &&
          form.value.price_tiers?.wholesale !== undefined &&
          form.value.price_tiers?.wholesale !== ""
            ? Number(form.value.price_tiers.wholesale)
            : null,

        dealer:
          form.value.price_tiers?.dealer !== null &&
          form.value.price_tiers?.dealer !== undefined &&
          form.value.price_tiers?.dealer !== ""
            ? Number(form.value.price_tiers.dealer)
            : null,

        vip:
          form.value.price_tiers?.vip !== null &&
          form.value.price_tiers?.vip !== undefined &&
          form.value.price_tiers?.vip !== ""
            ? Number(form.value.price_tiers.vip)
            : null,

        member:
          form.value.price_tiers?.member !== null &&
          form.value.price_tiers?.member !== undefined &&
          form.value.price_tiers?.member !== ""
            ? Number(form.value.price_tiers.member)
            : null,
      },

      is_taxable: true,
    },
    has_variants: form.value.has_variants,
    variants: form.value.has_variants
      ? form.value.variants.map((v: any) => ({
          sku: v.sku,
          barcode: v.barcode || "",
          variant_name: v.variant_name,
          attributes: v.attributes_json ? JSON.parse(v.attributes_json) : {},
          pricing: {
            selling_price: Number(v.selling_price) || 0,
            cost_price: Number(v.cost_price) || 0,
          },
          inventory: {
            quantity: Number(v.quantity) || 0,
            reserved: 0,
            reorder_level: Number(v.reorder_level) || 5,
          },
          is_default: v.is_default || false,
          is_active: true,
        }))
      : [],
    tags: form.value.tags || [],
    is_active: form.value.is_active,
    is_featured: form.value.is_featured,
    track_batches: form.value.track_batches,
    is_bulk_product: form.value.is_bulk_product,
    purchase_unit: form.value.purchase_unit || null,
    selling_unit: form.value.selling_unit || null,
    unit_conversion:
      form.value.is_bulk_product &&
      form.value.purchase_unit &&
      form.value.selling_unit
        ? {
            purchase_unit: form.value.purchase_unit,
            selling_unit: form.value.selling_unit,
            conversion_factor: Number(form.value.conversion_factor) || 1,
          }
        : null,
    media: {
      images: imageFiles.value.map((f: any) => f.preview),
      videos: [],
      documents: [],
    },
    notes: form.value.notes || "",
    tax_rate: form.value.tax_rate || 16,
    is_taxable: true,
  };
};

// Load product for edit mode
const loadProduct = async () => {
  if (props.mode === "create" || !props.productId) return;

  loading.value = true;
  try {
    const data = await store.getProductById(props.productId);
    if (data) {
      productData.value = data;
      populateForm(data);
    }
  } catch (error) {
    console.error("Error loading product:", error);
    snackbar.value = {
      show: true,
      text: "Failed to load product data",
      color: "error",
    };
  } finally {
    loading.value = false;
  }
};

const populateForm = (data: any) => {
  form.value = {
    name: data.name || "",
    sku: data.sku || "",
    barcode: data.barcode || "",
    description: data.description || "",
    short_description: data.short_description || "",
    category_id: data.category_id || "",
    brand_id: data.brand_id || "",
    supplier_id: data.supplier_id || "",
    tags: data.tags || [],
    cost_price: data.pricing?.cost_price || "",
    selling_price: data.pricing?.selling_price || "",
    tax_rate: data.tax_rate || 16,
    price_tiers: {
      wholesale: data.pricing?.price_tiers?.wholesale || "",
      dealer: data.pricing?.price_tiers?.dealer || "",
      vip: data.pricing?.price_tiers?.vip || "",
      member: data.pricing?.price_tiers?.member || "",
    },
    quantity: data.inventory?.quantity || "",
    reorder_level: data.inventory?.reorder_level || 10,
    warehouse: data.inventory?.warehouse || "main",
    location: data.inventory?.location || "",
    product_type: data.product_type || "stock",
    has_variants: data.has_variants || false,
    track_batches: data.track_batches || false,
    is_featured: data.is_featured || false,
    is_active: data.is_active !== false,
    is_bulk_product: data.is_bulk_product || false,
    purchase_unit: data.unit_conversion?.purchase_unit || "",
    selling_unit: data.unit_conversion?.selling_unit || "",
    conversion_factor: data.unit_conversion?.conversion_factor || "",
    batch_number: data.inventory?.batch_number || "",
    expiry_date: data.inventory?.expiry_date || "",
    variants: data.variants || [],
    images: data.images || [],
    notes: data.notes || "",
  };

  // Set image preview
  if (data.images && data.images.length > 0) {
    imagePreview.value = data.images[0];
  } else if (data.image_url) {
    imagePreview.value = data.image_url;
  }
};

// Save handlers
const handleSaveDraft = async () => {
  savingDraft.value = true;
  try {
    snackbar.value = {
      show: true,
      text: "Draft saved successfully!",
      color: "info",
    };
  } catch (error) {
    snackbar.value = {
      show: true,
      text: "Failed to save draft.",
      color: "error",
    };
  } finally {
    savingDraft.value = false;
  }
};

const handleSubmit = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) {
    snackbar.value = {
      show: true,
      text: "Please fill in all required fields",
      color: "error",
    };
    return;
  }

  submitting.value = true;
  try {
    const productData = buildProductData();
    console.log("BUILD PRODUCT");
    console.log(JSON.stringify(productData, null, 2));

    let result;
    if (props.mode === "edit" && props.productId) {
      result = await store.updateProduct(props.productId, productData);
      snackbar.value = {
        show: true,
        text: "Product updated successfully!",
        color: "success",
      };
    } else {
      result = await store.addProduct(productData);
      snackbar.value = {
        show: true,
        text: "Product created successfully!",
        color: "success",
      };
    }

    emit("success", result);

    // Navigate after 1.5 seconds
    setTimeout(() => {
      router.push("/admin/products");
    }, 1500);
  } catch (error) {
    console.error("Error saving product:", error);
    snackbar.value = {
      show: true,
      text: `Failed to ${
        props.mode === "edit" ? "update" : "create"
      } product. Please try again.`,
      color: "error",
    };
  } finally {
    submitting.value = false;
  }
};

const handleCancel = () => {
  if (form.value.name || form.value.sku) {
    if (!confirm("You have unsaved changes. Are you sure you want to leave?")) {
      return;
    }
  }
  emit("cancel");
  router.push("/admin/products");
};

// Load options
const loadOptions = async () => {
  try {
    const categoryData = await store.getAllCategories();
    categoryOptions.value = categoryData.map((category: any) => ({
      title: category.name,
      value: category.id,
    }));

    const brandData = await store.getAllBrands();
    brandOptions.value = brandData.map((brand: any) => ({
      title: brand.name,
      value: brand.id,
    }));

    const supplierData = await store.getAllSuppliers();
    supplierOptions.value = supplierData.map((supplier: any) => ({
      title: supplier.name,
      value: supplier.id,
    }));
  } catch (error) {
    console.error("Error loading options:", error);
  }
};

// Watch for name changes in create mode
watch(
  () => form.value.name,
  (newName) => {
    if (props.mode === "create" && !form.value.sku && newName) {
      generateSku();
    }
  }
);

// Lifecycle
onMounted(async () => {
  await loadOptions();
  await loadProduct();
});
</script>

<style scoped>
/* All the styles from your original add page */
.product-form-container {
  background: #f8f6f2;
  min-height: 100vh;
  padding-bottom: 64px;
}

.sticky-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: white !important;
  border-bottom: 1px solid #e5e7eb;
  padding: 4px 0;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-badge {
  font-size: 10px;
  font-weight: 600;
  color: #e07a5f;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.page-title {
  font-family: "Playfair Display", serif;
  font-size: 18px;
  font-weight: 800;
  color: #1b4332;
  margin: 0;
  line-height: 1.2;
}

.header-actions {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.main-content {
  padding: 16px 8px 80px;
  max-width: 1400px;
  margin: 0 auto;
}

/* Form Cards */
.form-card {
  background: white;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.form-card:hover {
  border-color: #2d6a4f;
}

.section-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
}

.section-icon {
  width: 32px;
  height: 32px;
  background: rgba(45, 106, 79, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.section-title {
  font-size: 15px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 1px;
}

.section-subtitle {
  font-size: 12px;
  color: #6b7280;
}

/* Form Groups */
.form-group {
  margin-bottom: 12px;
}

.form-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 4px;
}

.form-label.required::after {
  content: " *";
  color: #e07a5f;
}

.input-hint {
  font-size: 10px;
  color: #9ca3af;
  margin-top: 2px;
}

/* Price Tiers */
.price-tiers-section {
  background: #f8f6f2;
  border-radius: 8px;
  padding: 12px;
}

.tiers-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.tiers-title {
  font-weight: 600;
  color: #1b4332;
  font-size: 13px;
}

/* Inventory Warning */
.inventory-warning {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: #fef3c7;
  border-radius: 6px;
  border-left: 3px solid #f59e0b;
  color: #92400e;
  font-weight: 500;
  font-size: 13px;
}

/* Image Upload */
.image-upload-area {
  border: 2px dashed #e5e7eb;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.image-upload-area:hover,
.image-upload-area.drag-over {
  border-color: #2d6a4f;
  background: rgba(45, 106, 79, 0.05);
}

.image-preview {
  position: relative;
  height: 160px;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.3s ease;
  font-size: 13px;
}

.image-preview:hover .image-overlay {
  opacity: 1;
}

.upload-placeholder {
  padding: 24px;
  text-align: center;
}

.upload-placeholder p {
  margin-top: 8px;
  color: #374151;
  font-size: 14px;
}

.upload-placeholder span {
  font-size: 11px;
  color: #9ca3af;
}

.image-thumbnails {
  display: flex;
  gap: 6px;
  margin-top: 8px;
  flex-wrap: wrap;
}

.thumbnail {
  width: 48px;
  height: 48px;
  border-radius: 6px;
  overflow: hidden;
  border: 2px solid #e5e7eb;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Product Preview */
.product-preview {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.preview-image {
  width: 100%;
  height: 120px;
  border-radius: 6px;
  overflow: hidden;
  background: #f8f6f2;
}

.preview-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #9ca3af;
}

.preview-placeholder span {
  font-size: 11px;
  margin-top: 2px;
}

.preview-details {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.preview-item {
  display: flex;
  justify-content: space-between;
  padding: 3px 6px;
  background: #f8f6f2;
  border-radius: 4px;
  gap: 8px;
}

.preview-label {
  color: #6b7280;
  font-size: 11px;
  flex-shrink: 0;
}

.preview-value {
  font-weight: 600;
  color: #1b4332;
  font-size: 11px;
  text-align: right;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.preview-value.stock-ok {
  color: #2d6a4f;
}

.preview-value.stock-low {
  color: #f59e0b;
}

.preview-value.stock-out {
  color: #e07a5f;
}

.stock-warning {
  margin-left: 2px;
}

/* Bulk Variant Generator */
.bulk-variant-generator {
  background: #f8f6f2;
  border-radius: 8px;
  padding: 12px;
}

.generator-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.generator-title {
  font-weight: 600;
  color: #1b4332;
  font-size: 13px;
}

.generated-variants {
  margin-top: 12px;
}

.variants-preview h4 {
  margin-bottom: 8px;
  color: #1b4332;
  font-size: 14px;
}

.table-responsive {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* Variants */
.variants-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.variant-item {
  background: #f8f6f2;
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.variant-item:hover {
  border-color: #2d6a4f;
}

.variant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.variant-number {
  font-weight: 700;
  color: #2d6a4f;
  font-size: 13px;
}

.variant-actions {
  display: flex;
  gap: 2px;
}

.variant-info {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 4px;
}

.variant-field {
  font-size: 12px;
}

.variant-field .field-label {
  color: #6b7280;
  margin-right: 2px;
}

.variant-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 3px;
  margin-top: 4px;
}

.empty-variants {
  text-align: center;
  padding: 24px 16px;
}

.empty-variants h4 {
  margin-top: 8px;
  color: #1b4332;
  font-size: 15px;
}

.empty-variants p {
  color: #6b7280;
  font-size: 13px;
}

/* Switches */
.switch-label {
  font-weight: 500;
  color: #1b4332;
  font-size: 13px;
}

.switch-hint {
  font-size: 11px;
  color: #6b7280;
}

/* Dialogs */
.variant-dialog,
.quick-add-dialog {
  border-radius: 16px !important;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px 0;
}

.dialog-header h3 {
  font-size: 17px;
  font-weight: 700;
  color: #1b4332;
}

.dialog-actions {
  padding: 12px 20px 20px;
  gap: 8px;
}

/* Bottom Navigation */
.v-bottom-navigation {
  border-top: 1px solid #e5e7eb;
}

/* Mobile Responsive */
@media (min-width: 600px) {
  .main-content {
    padding: 20px 24px 80px;
  }

  .page-title {
    font-size: 22px;
  }

  .section-title {
    font-size: 16px;
  }

  .section-subtitle {
    font-size: 13px;
  }

  .form-card .pa-3.pa-sm-4.pa-md-6 {
    padding: 16px !important;
  }
}

@media (min-width: 960px) {
  .main-content {
    padding: 24px 32px 40px;
  }

  .page-title {
    font-size: 28px;
  }

  .form-card .pa-3.pa-sm-4.pa-md-6 {
    padding: 24px !important;
  }

  .section-icon {
    width: 40px;
    height: 40px;
  }

  .section-icon .v-icon {
    font-size: 20px !important;
  }

  .preview-image {
    height: 150px;
  }
}

@media (max-width: 599px) {
  .v-btn {
    min-height: 40px;
  }

  .v-text-field,
  .v-select,
  .v-autocomplete,
  .v-combobox {
    font-size: 16px !important;
  }

  .form-group {
    margin-bottom: 10px;
  }

  .section-header {
    gap: 10px;
    margin-bottom: 12px;
  }

  .section-icon {
    width: 28px;
    height: 28px;
  }

  .section-icon .v-icon {
    font-size: 16px !important;
  }

  .price-tiers-section {
    padding: 10px;
  }

  .bulk-variant-generator {
    padding: 10px;
  }

  .variant-item {
    padding: 10px;
  }

  .variant-info {
    grid-template-columns: 1fr 1fr;
  }

  .image-preview {
    height: 120px;
  }

  .upload-placeholder {
    padding: 16px;
  }

  .dialog-header {
    padding: 12px 16px 0;
  }

  .dialog-header h3 {
    font-size: 16px;
  }

  .dialog-actions {
    flex-direction: column;
  }

  .dialog-actions .v-btn {
    width: 100%;
  }

  .inventory-warning {
    font-size: 12px;
    padding: 8px 12px;
  }
}

@media (max-width: 400px) {
  .page-title {
    font-size: 15px;
  }

  .page-badge {
    font-size: 9px;
  }

  .header-actions .v-btn {
    font-size: 11px;
    padding: 0 8px;
  }

  .header-actions .v-btn .v-icon {
    font-size: 14px !important;
  }

  .variant-info {
    grid-template-columns: 1fr;
  }

  .variant-field {
    font-size: 11px;
  }

  .preview-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0;
  }

  .preview-value {
    text-align: left;
  }
}
</style>
