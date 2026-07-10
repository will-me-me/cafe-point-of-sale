<!-- pages/admin/product/add/index.vue -->
<template>
  <div class="add-product-container">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <div class="page-badge">
          <v-icon size="16" color="#E07A5F">mdi-package-variant-plus</v-icon>
          Product Management
        </div>
        <h1 class="page-title">Add New Product</h1>
        <p class="page-subtitle">
          Create a new product with variants, pricing, and inventory details
        </p>
      </div>
      <div class="header-actions">
        <v-btn variant="outlined" color="#6B7280" @click="handleCancel">
          <v-icon start>mdi-close</v-icon>
          Cancel
        </v-btn>
        <v-btn color="#2D6A4F" :loading="submitting" @click="handleSubmit">
          <v-icon start>mdi-check</v-icon>
          Save Product
        </v-btn>
      </div>
    </div>

    <!-- Main Form -->
    <v-form ref="formRef" v-model="isValid">
      <v-row class="form-row" no-gutters>
        <!-- Left Column - Basic Info -->
        <v-col cols="12" lg="8" class="pr-lg-4">
          <v-card class="form-card" elevation="0" rounded="xl">
            <v-card-text class="pa-4 pa-md-6">
              <!-- Basic Information -->
              <div class="section-header">
                <div class="section-icon">
                  <v-icon color="#2D6A4F">mdi-information</v-icon>
                </div>
                <div>
                  <h3 class="section-title">Basic Information</h3>
                  <p class="section-subtitle">
                    Enter the essential details about your product
                  </p>
                </div>
              </div>

              <v-row>
                <v-col cols="12">
                  <div class="form-group">
                    <label class="form-label required">Product Name</label>
                    <v-text-field
                      v-model="form.name"
                      placeholder="e.g., Pishori Rice 90kg Sack"
                      variant="outlined"
                      density="comfortable"
                      :rules="[rules.required]"
                      hide-details="auto"
                    />
                  </div>
                </v-col>

                <v-col cols="12" md="6">
                  <div class="form-group">
                    <label class="form-label required">SKU</label>
                    <v-text-field
                      v-model="form.sku"
                      placeholder="e.g., RICE-PISHORI-90KG"
                      variant="outlined"
                      density="comfortable"
                      :rules="[rules.required]"
                      hide-details="auto"
                    />
                  </div>
                </v-col>

                <v-col cols="12" md="6">
                  <div class="form-group">
                    <label class="form-label">Barcode</label>
                    <v-text-field
                      v-model="form.barcode"
                      placeholder="e.g., 6161234567800"
                      variant="outlined"
                      density="comfortable"
                      hide-details="auto"
                    />
                  </div>
                </v-col>

                <v-col cols="12">
                  <div class="form-group">
                    <label class="form-label">Description</label>
                    <v-textarea
                      v-model="form.description"
                      placeholder="Describe your product..."
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

              <!-- Category & Brand -->
              <div class="section-header mt-6">
                <div class="section-icon">
                  <v-icon color="#2D6A4F">mdi-tag</v-icon>
                </div>
                <div>
                  <h3 class="section-title">Classification</h3>
                  <p class="section-subtitle">
                    Categorize your product for better organization
                  </p>
                </div>
              </div>

              <v-row>
                <v-col cols="12" md="6">
                  <div class="form-group">
                    <label class="form-label">Category</label>
                    <v-select
                      v-model="form.category_id"
                      :items="categoryOptions"
                      placeholder="Select category"
                      variant="outlined"
                      density="comfortable"
                      hide-details="auto"
                    />
                    <v-btn
                      variant="text"
                      size="small"
                      color="#2D6A4F"
                      class="mt-2"
                      @click="showCategoryDialog = true"
                    >
                      <v-icon size="16">mdi-plus</v-icon>
                      Add New Category
                    </v-btn>
                  </div>
                </v-col>

                <v-col cols="12" md="6">
                  <div class="form-group">
                    <label class="form-label">Brand</label>
                    <v-select
                      v-model="form.brand_id"
                      :items="brandOptions"
                      placeholder="Select brand"
                      variant="outlined"
                      density="comfortable"
                      hide-details="auto"
                    />
                    <v-btn
                      variant="text"
                      size="small"
                      color="#2D6A4F"
                      class="mt-2"
                      @click="showBrandDialog = true"
                    >
                      <v-icon size="16">mdi-plus</v-icon>
                      Add New Brand
                    </v-btn>
                  </div>
                </v-col>
              </v-row>

              <!-- Tags -->
              <div class="section-header mt-6">
                <div class="section-icon">
                  <v-icon color="#2D6A4F">mdi-tag-multiple</v-icon>
                </div>
                <div>
                  <h3 class="section-title">Tags</h3>
                  <p class="section-subtitle">
                    Add keywords to help customers find your product
                  </p>
                </div>
              </div>

              <v-row>
                <v-col cols="12">
                  <div class="form-group">
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

              <!-- Pricing -->
              <div class="section-header mt-6">
                <div class="section-icon">
                  <v-icon color="#2D6A4F">mdi-currency-usd</v-icon>
                </div>
                <div>
                  <h3 class="section-title">Pricing</h3>
                  <p class="section-subtitle">
                    Set cost and selling prices for your product
                  </p>
                </div>
              </div>

              <v-row>
                <v-col cols="12" md="4">
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
                    />
                  </div>
                </v-col>

                <v-col cols="12" md="4">
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
                    />
                  </div>
                </v-col>

                <v-col cols="12" md="4">
                  <div class="form-group">
                    <label class="form-label">Margin</label>
                    <v-text-field
                      :model-value="calculatedMargin"
                      readonly
                      suffix="%"
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
                    <v-icon>{{
                      showTiers ? "mdi-chevron-up" : "mdi-chevron-down"
                    }}</v-icon>
                  </v-btn>
                </div>

                <v-expand-transition>
                  <div v-if="showTiers">
                    <v-row>
                      <v-col cols="12" sm="6" md="4">
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

                      <v-col cols="12" sm="6" md="4">
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

                      <v-col cols="12" sm="6" md="4">
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

                      <v-col cols="12" sm="6" md="4">
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

              <!-- Inventory -->
              <div class="section-header mt-6">
                <div class="section-icon">
                  <v-icon color="#2D6A4F">mdi-warehouse</v-icon>
                </div>
                <div>
                  <h3 class="section-title">Inventory</h3>
                  <p class="section-subtitle">
                    Manage stock levels and reorder points
                  </p>
                </div>
              </div>

              <v-row>
                <v-col cols="12" md="4">
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
                    />
                  </div>
                </v-col>

                <v-col cols="12" md="4">
                  <div class="form-group">
                    <label class="form-label">Reorder Level</label>
                    <v-text-field
                      v-model="form.reorder_level"
                      placeholder="10"
                      type="number"
                      variant="outlined"
                      density="comfortable"
                      hide-details="auto"
                    />
                  </div>
                </v-col>

                <v-col cols="12" md="4">
                  <div class="form-group">
                    <label class="form-label">Location</label>
                    <v-text-field
                      v-model="form.location"
                      placeholder="Warehouse A, Section 1"
                      variant="outlined"
                      density="comfortable"
                      hide-details="auto"
                    />
                  </div>
                </v-col>
              </v-row>

              <!-- Unit Conversion (for bulk products) -->
              <div class="section-header mt-6">
                <div class="section-icon">
                  <v-icon color="#2D6A4F">mdi-file-arrow-up-down</v-icon>
                </div>
                <div>
                  <h3 class="section-title">Unit Conversion</h3>
                  <p class="section-subtitle">
                    Configure for bulk products (e.g., 1 sack = 90kg)
                  </p>
                </div>
              </div>

              <v-row>
                <v-col cols="12" md="4">
                  <div class="form-group">
                    <label class="form-label">Purchase Unit</label>
                    <v-text-field
                      v-model="form.purchase_unit"
                      placeholder="sack"
                      variant="outlined"
                      density="comfortable"
                      hide-details="auto"
                    />
                  </div>
                </v-col>

                <v-col cols="12" md="4">
                  <div class="form-group">
                    <label class="form-label">Selling Unit</label>
                    <v-text-field
                      v-model="form.selling_unit"
                      placeholder="kg"
                      variant="outlined"
                      density="comfortable"
                      hide-details="auto"
                    />
                  </div>
                </v-col>

                <v-col cols="12" md="4">
                  <div class="form-group">
                    <label class="form-label">Conversion Factor</label>
                    <v-text-field
                      v-model="form.conversion_factor"
                      placeholder="90"
                      type="number"
                      variant="outlined"
                      density="comfortable"
                      hide-details="auto"
                    />
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Right Column - Media & Settings -->
        <v-col cols="12" lg="4" class="pl-lg-4">
          <!-- Product Image -->
          <v-card class="form-card" elevation="0" rounded="xl">
            <v-card-text class="pa-4 pa-md-6">
              <div class="section-header">
                <div class="section-icon">
                  <v-icon color="#2D6A4F">mdi-image</v-icon>
                </div>
                <div>
                  <h3 class="section-title">Product Image</h3>
                  <p class="section-subtitle">Upload a product image</p>
                </div>
              </div>

              <div class="image-upload-area" @click="triggerFileInput">
                <input
                  ref="fileInput"
                  type="file"
                  accept="image/*"
                  hidden
                  @change="handleImageUpload"
                />
                <div v-if="imagePreview" class="image-preview">
                  <img :src="imagePreview" alt="Preview" />
                  <div class="image-overlay">
                    <v-icon size="30">mdi-camera</v-icon>
                    <span>Change Image</span>
                  </div>
                </div>
                <div v-else class="upload-placeholder">
                  <v-icon size="48" color="#9CA3AF">mdi-image-plus</v-icon>
                  <p>Click to upload product image</p>
                  <span>PNG, JPG up to 5MB</span>
                </div>
              </div>
            </v-card-text>
          </v-card>

          <!-- Product Type & Settings -->
          <v-card class="form-card mt-4" elevation="0" rounded="xl">
            <v-card-text class="pa-4 pa-md-6">
              <div class="section-header">
                <div class="section-icon">
                  <v-icon color="#2D6A4F">mdi-cog</v-icon>
                </div>
                <div>
                  <h3 class="section-title">Settings</h3>
                  <p class="section-subtitle">Configure product options</p>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Product Type</label>
                <v-select
                  v-model="form.product_type"
                  :items="productTypes"
                  placeholder="Select type"
                  variant="outlined"
                  density="comfortable"
                  hide-details="auto"
                />
              </div>

              <div class="form-group mt-4">
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

              <div class="form-group mt-4">
                <v-switch
                  v-model="form.track_batches"
                  color="#2D6A4F"
                  hide-details
                >
                  <template #label>
                    <div>
                      <div class="switch-label">Track Batches</div>
                      <div class="switch-hint">
                        Track products by batch numbers
                      </div>
                    </div>
                  </template>
                </v-switch>
              </div>

              <div class="form-group mt-4">
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

              <div class="form-group mt-4">
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

          <!-- Product Stats Preview -->
          <v-card class="form-card mt-4" elevation="0" rounded="xl">
            <v-card-text class="pa-4 pa-md-6">
              <div class="section-header">
                <div class="section-icon">
                  <v-icon color="#2D6A4F">mdi-chart-box</v-icon>
                </div>
                <div>
                  <h3 class="section-title">Quick Stats</h3>
                  <p class="section-subtitle">Product summary</p>
                </div>
              </div>

              <div class="stats-preview">
                <div class="stat-item">
                  <span class="stat-label">Product Name</span>
                  <span class="stat-value">{{ form.name || "Not set" }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">SKU</span>
                  <span class="stat-value">{{ form.sku || "Not set" }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Price</span>
                  <span class="stat-value"
                    >KSh {{ form.selling_price || "0.00" }}</span
                  >
                </div>
                <div class="stat-item">
                  <span class="stat-label">Stock</span>
                  <span class="stat-value"
                    >{{ form.quantity || "0" }} units</span
                  >
                </div>
                <div class="stat-item" v-if="calculatedMargin">
                  <span class="stat-label">Margin</span>
                  <span class="stat-value">{{ calculatedMargin }}%</span>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-form>

    <!-- Variants Section -->
    <v-row v-if="form.has_variants" class="mt-4" no-gutters>
      <v-col cols="12">
        <v-card class="form-card" elevation="0" rounded="xl">
          <v-card-text class="pa-4 pa-md-6">
            <div class="section-header">
              <div class="section-icon">
                <v-icon color="#2D6A4F">mdi-swap-horizontal</v-icon>
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
                <v-icon start>mdi-plus</v-icon>
                Add Variant
              </v-btn>
            </div>

            <div v-if="form.variants.length === 0" class="empty-variants">
              <v-icon size="48" color="#9CA3AF"
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
                      <v-icon size="16">mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      size="x-small"
                      variant="text"
                      color="#E07A5F"
                      @click="removeVariant(index)"
                    >
                      <v-icon size="16">mdi-delete</v-icon>
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
      </v-col>
    </v-row>

    <!-- Variant Dialog -->
    <v-dialog v-model="variantDialog.show" max-width="600">
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

              <v-col cols="12" md="6">
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

              <v-col cols="12" md="6">
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

              <v-col cols="12" md="6">
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

              <v-col cols="12" md="6">
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
    <v-dialog v-model="showCategoryDialog" max-width="400">
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
    <v-dialog v-model="showBrandDialog" max-width="400">
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
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { usePosStore } from "~/stores/pos";

definePageMeta({
  layout: "default",
  middleware: "auth",
});

const router = useRouter();

// Form state
const posStore = usePosStore();
const formRef = ref(null);
const variantFormRef = ref(null);
const categoryFormRef = ref(null);
const brandFormRef = ref(null);
const isValid = ref(false);
const variantFormValid = ref(false);
const categoryFormValid = ref(false);
const brandFormValid = ref(false);
const submitting = ref(false);
const showTiers = ref(false);

const form = ref({
  name: "",
  sku: "",
  barcode: "",
  description: "",
  short_description: "",
  category_id: "",
  brand_id: "",
  tags: [],
  cost_price: "",
  selling_price: "",
  price_tiers: {
    wholesale: "",
    dealer: "",
    vip: "",
    member: "",
  },
  quantity: "",
  reorder_level: 10,
  location: "",
  product_type: "stock",
  has_variants: false,
  track_batches: false,
  is_featured: false,
  is_active: true,
  purchase_unit: "",
  selling_unit: "",
  conversion_factor: "",
  variants: [],
});

// Product types
const productTypes = [
  { title: "Stock", value: "stock" },
  { title: "Service", value: "service" },
  { title: "Digital", value: "digital" },
  { title: "Rental", value: "rental" },
];

// Options (to be populated from API)
const categoryOptions = ref([]);
const brandOptions = ref([]);

// Image handling
const fileInput = ref(null);
const imagePreview = ref("");
const imageFile = ref(null);

// Dialogs
const showCategoryDialog = ref(false);
const showBrandDialog = ref(false);
const newCategory = ref("");
const newBrand = ref("");

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
const calculatedMargin = computed(() => {
  const cost = parseFloat(form.value.cost_price);
  const selling = parseFloat(form.value.selling_price);
  if (cost > 0 && selling > 0 && selling > cost) {
    return (((selling - cost) / selling) * 100).toFixed(2);
  }
  return 0;
});

// Methods
const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleImageUpload = (event: Event) => {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (file) {
    imageFile.value = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
};

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

const addCategory = () => {
  if (newCategory.value) {
    categoryOptions.value.push({
      title: newCategory.value,
      value: newCategory.value.toLowerCase().replace(/\s+/g, "-"),
    });
    form.value.category_id = newCategory.value
      .toLowerCase()
      .replace(/\s+/g, "-");
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
    brandOptions.value.push({
      title: newBrand.value,
      value: newBrand.value.toLowerCase().replace(/\s+/g, "-"),
    });
    form.value.brand_id = newBrand.value.toLowerCase().replace(/\s+/g, "-");
    showBrandDialog.value = false;
    newBrand.value = "";

    snackbar.value = {
      show: true,
      text: "Brand added successfully!",
      color: "success",
    };
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
    // Build product data
    const productData = {
      name: form.value.name,
      sku: form.value.sku,
      barcode: form.value.barcode || undefined,
      description: form.value.description || undefined,
      short_description: form.value.short_description || undefined,
      category_id: form.value.category_id || undefined,
      brand_id: form.value.brand_id || undefined,
      tags: form.value.tags || [],
      product_type: form.value.product_type || "stock",
      has_variants: form.value.has_variants,
      track_batches: form.value.track_batches,
      is_featured: form.value.is_featured,
      is_active: form.value.is_active,
      pricing: {
        cost_price: parseFloat(form.value.cost_price) || 0,
        selling_price: parseFloat(form.value.selling_price) || 0,
        price_tiers: {
          wholesale: parseFloat(form.value.price_tiers.wholesale) || undefined,
          dealer: parseFloat(form.value.price_tiers.dealer) || undefined,
          vip: parseFloat(form.value.price_tiers.vip) || undefined,
          member: parseFloat(form.value.price_tiers.member) || undefined,
        },
        is_taxable: true,
      },
      inventory: {
        quantity: parseInt(form.value.quantity) || 0,
        reorder_level: parseInt(form.value.reorder_level) || 10,
        location: form.value.location || undefined,
        status: parseInt(form.value.quantity) > 0 ? "in_stock" : "out_of_stock",
      },
      unit_conversion:
        form.value.purchase_unit &&
        form.value.selling_unit &&
        form.value.conversion_factor
          ? {
              purchase_unit: form.value.purchase_unit,
              selling_unit: form.value.selling_unit,
              conversion_factor: parseFloat(form.value.conversion_factor),
            }
          : undefined,
      variants: form.value.has_variants
        ? form.value.variants.map((v) => ({
            variant_name: v.variant_name,
            sku: v.sku,
            barcode: v.barcode || undefined,
            pricing: {
              selling_price: v.selling_price,
            },
            inventory: {
              quantity: v.quantity,
            },
            attributes: v.attributes_json ? JSON.parse(v.attributes_json) : {},
            is_default: v.is_default || false,
            is_active: true,
          }))
        : [],
    };

    await posStore.addProduct(productData);

    console.log("Product data:", productData);

    snackbar.value = {
      show: true,
      text: "Product created successfully!",
      color: "success",
    };

    // Navigate to product list after 2 seconds
    setTimeout(() => {
      router.push("/admin/products");
    }, 2000);
  } catch (error) {
    console.error("Error saving product:", error);
    snackbar.value = {
      show: true,
      text: "Failed to create product. Please try again.",
      color: "error",
    };
  } finally {
    submitting.value = false;
  }
};

const handleCancel = () => {
  router.push("/admin/products");
};

// Load categories and brands on mount
onMounted(async () => {
  let categorydataOptions = await posStore.getAllCategories();
  categoryOptions.value = categorydataOptions.map((category) => ({
    title: category.name,
    value: category.id,
  }));

  let branddataOptions = await posStore.getAllBrands();
  brandOptions.value = branddataOptions.map((brand) => ({
    title: brand.name,
    value: brand.id,
  }));
});
</script>

<style scoped>
.add-product-container {
  padding: 24px;
  background: #f8f6f2;
  min-height: calc(100vh - 64px);
}

/* Page Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
}

.page-badge {
  font-size: 12px;
  font-weight: 600;
  color: #e07a5f;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.page-title {
  font-family: "Playfair Display", serif;
  font-size: 28px;
  font-weight: 800;
  color: #1b4332;
  margin-bottom: 4px;
}

.page-subtitle {
  color: #6b7280;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
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
  gap: 16px;
  margin-bottom: 24px;
}

.section-icon {
  width: 40px;
  height: 40px;
  background: rgba(45, 106, 79, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: #1b4332;
  margin-bottom: 2px;
}

.section-subtitle {
  font-size: 13px;
  color: #6b7280;
}

/* Form Groups */
.form-group {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
}

.form-label.required::after {
  content: " *";
  color: #e07a5f;
}

.input-hint {
  font-size: 11px;
  color: #9ca3af;
  margin-top: 4px;
}

/* Price Tiers */
.price-tiers-section {
  background: #f8f6f2;
  border-radius: 12px;
  padding: 16px;
}

.tiers-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

.tiers-title {
  font-weight: 600;
  color: #1b4332;
}

/* Image Upload */
.image-upload-area {
  border: 2px dashed #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.image-upload-area:hover {
  border-color: #2d6a4f;
  background: rgba(45, 106, 79, 0.05);
}

.image-preview {
  position: relative;
  height: 200px;
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
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.image-preview:hover .image-overlay {
  opacity: 1;
}

.upload-placeholder {
  padding: 40px;
  text-align: center;
}

.upload-placeholder p {
  margin-top: 12px;
  color: #374151;
}

.upload-placeholder span {
  font-size: 12px;
  color: #9ca3af;
}

/* Stats Preview */
.stats-preview {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  background: #f8f6f2;
  border-radius: 8px;
}

.stat-label {
  color: #6b7280;
  font-size: 13px;
}

.stat-value {
  font-weight: 600;
  color: #1b4332;
}

/* Switches */
.switch-label {
  font-weight: 500;
  color: #1b4332;
}

.switch-hint {
  font-size: 12px;
  color: #6b7280;
}

/* Variants */
.variants-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.variant-item {
  background: #f8f6f2;
  border-radius: 12px;
  padding: 16px;
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
  margin-bottom: 12px;
}

.variant-number {
  font-weight: 700;
  color: #2d6a4f;
}

.variant-actions {
  display: flex;
  gap: 4px;
}

.variant-info {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 8px;
}

.variant-field {
  font-size: 13px;
}

.variant-field .field-label {
  color: #6b7280;
  margin-right: 4px;
}

.variant-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 8px;
}

.empty-variants {
  text-align: center;
  padding: 40px 20px;
}

.empty-variants h4 {
  margin-top: 12px;
  color: #1b4332;
}

.empty-variants p {
  color: #6b7280;
  font-size: 14px;
}

/* Dialogs */
.variant-dialog,
.quick-add-dialog {
  border-radius: 24px !important;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px 0;
}

.dialog-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #1b4332;
}

.dialog-actions {
  padding: 16px 24px 24px;
  gap: 12px;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .add-product-container {
    padding: 16px;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .page-title {
    font-size: 24px;
  }

  .header-actions {
    flex-direction: column;
  }

  .header-actions .v-btn {
    width: 100%;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .section-icon {
    width: 32px;
    height: 32px;
  }

  .section-icon .v-icon {
    font-size: 20px !important;
  }

  .section-title {
    font-size: 15px;
  }

  .section-subtitle {
    font-size: 12px;
  }

  .form-card .pa-4.pa-md-6 {
    padding: 16px !important;
  }

  .tiers-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .variant-info {
    grid-template-columns: 1fr;
  }

  .variant-item {
    padding: 12px;
  }

  .variant-header {
    flex-wrap: wrap;
    gap: 8px;
  }

  .stats-preview {
    gap: 6px;
  }

  .stat-item {
    padding: 6px 10px;
    font-size: 12px;
  }

  .image-preview {
    height: 150px;
  }

  .upload-placeholder {
    padding: 24px;
  }

  .upload-placeholder p {
    font-size: 14px;
  }

  .upload-placeholder span {
    font-size: 11px;
  }

  .dialog-header {
    padding: 16px 20px 0;
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

  .form-row {
    margin: 0 !important;
  }

  .form-row > .v-col {
    padding: 0 !important;
  }

  .v-col-lg-8,
  .v-col-lg-4 {
    padding-left: 0 !important;
    padding-right: 0 !important;
  }

  .form-card {
    margin-bottom: 16px;
  }

  .mt-4 {
    margin-top: 16px !important;
  }
}

@media (max-width: 480px) {
  .add-product-container {
    padding: 12px;
  }

  .page-title {
    font-size: 20px;
  }

  .page-subtitle {
    font-size: 12px;
  }

  .form-card .pa-4.pa-md-6 {
    padding: 12px !important;
  }

  .form-group {
    margin-bottom: 12px;
  }

  .form-label {
    font-size: 12px;
  }

  .v-text-field,
  .v-select,
  .v-textarea {
    font-size: 14px;
  }

  .variant-item {
    padding: 10px;
  }

  .variant-field {
    font-size: 12px;
  }

  .stats-preview .stat-item {
    font-size: 11px;
    padding: 4px 8px;
  }

  .section-header {
    gap: 12px;
  }

  .section-title {
    font-size: 14px;
  }

  .empty-variants {
    padding: 24px 16px;
  }

  .empty-variants h4 {
    font-size: 16px;
  }
}

/* Transitions */
.variant-item-enter-active,
.variant-item-leave-active {
  transition: all 0.3s ease;
}

.variant-item-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.variant-item-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
