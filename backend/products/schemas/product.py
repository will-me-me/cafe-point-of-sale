# app/schemas/product.py
from typing import Optional, List, Dict, Any
from pydantic import Field, field_validator, model_validator, validator, BaseModel
from datetime import datetime, date
from decimal import Decimal

from products.schemas.expiry import Expiry
from .enums import BaseSchema, ProductType, StockStatus
from .category import Category
from .brand import Brand
from .supplier import SupplierProduct
from .pricing import Pricing, PriceTier, CostHistory, PricingCreate
from .inventory import Inventory, InventoryBase, BatchDetails, SerialNumber, UnitConversion
from .tax import Tax
from .warranty import Warranty

class ProductVariantBase(BaseModel):
    """Product variants like size, color, etc."""
    sku: str = Field(..., min_length=1, max_length=50)
    barcode: Optional[str] = Field(None, max_length=50)
    variant_name: str = Field(..., min_length=1, max_length=100)
    attributes: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = True
    is_default: bool = False
    sort_order: int = 0
    pricing: Optional[Dict[str, Any]] = None 

    @field_validator('attributes')
    def validate_weights(cls, v):
        # if 'weight_kg' not in v:
        #     raise ValueError("Attribute 'weight_kg' is required for product variants")
        return v

class ProductVariantCreate(ProductVariantBase):
    pass

class ProductVariantUpdate(BaseModel):
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    barcode: Optional[str] = Field(None, max_length=50)
    variant_name: Optional[str] = Field(None, min_length=1, max_length=100)
    attributes: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    sort_order: Optional[int] = None
    pricing: Optional[PricingCreate] = None

class ProductVariant(ProductVariantBase, BaseSchema):
    inventory: Optional[Inventory] = None
    # pricing: Optional[Pricing] = None
    # images: Optional[List['ProductImage']] = []

class ProductMedia(BaseModel):
    images: Optional[List['ProductImage']] = []
    videos: Optional[List['ProductVideo']] = []
    documents: Optional[List['ProductDocument']] = []

class ProductImage(BaseModel):
    url: str
    thumbnail: Optional[str] = None
    is_primary: bool = False
    alt_text: Optional[str] = Field(None, max_length=200)
    sort_order: int = 0

class ProductVideo(BaseModel):
    url: str
    title: Optional[str] = Field(None, max_length=100)
    thumbnail: Optional[str] = None
    is_primary: bool = False

class ProductDocument(BaseModel):
    url: str
    title: str = Field(..., max_length=100)
    document_type: str
    is_public: bool = True

class ProductBase(BaseModel):
    """Core product schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    short_description: Optional[str] = Field(None, max_length=500)
    sku: str = Field(..., min_length=1, max_length=50)
    barcode: Optional[str] = Field(None, max_length=50)
    product_type: ProductType = ProductType.STOCK
    
    # Relationships
    category_id: Optional[str] = None
    brand_id: Optional[str] = None
    manufacturer_id: Optional[str] = None
    
    # Supplier information
    suppliers: List[SupplierProduct] = Field(default_factory=list)
    
    # Attributes and specifications
    attributes: Dict[str, Any] = Field(default_factory=dict)
    specifications: Dict[str, Any] = Field(default_factory=dict)
    
    # Inventory and pricing
    inventory: Optional[InventoryBase] = None  # Use InventoryBase instead of Inventory
    pricing: Optional[PricingCreate] = None  # Use PricingCreate instead of Pricing
    
    # Variants
    has_variants: bool = False
    variants: List[ProductVariantCreate] = Field(default_factory=list)
    
    # Additional info
    weight: Optional[float] = Field(None, ge=0)
    length: Optional[float] = Field(None, ge=0)
    width: Optional[float] = Field(None, ge=0)
    height: Optional[float] = Field(None, ge=0)
    volume: Optional[float] = Field(None, ge=0)
    unit_of_measure: str = "sack"
    minimum_order: int = Field(default=1, ge=1)
    maximum_order: Optional[int] = Field(None, ge=1)
    
    # Status
    is_active: bool = True
    is_featured: bool = False
    is_new: bool = False
    is_on_sale: bool = False
    is_rental: bool = False
    is_digital: bool = False
    is_service: bool = False
    is_composite: bool = False
    
    # Tags
    tags: List[str] = Field(default_factory=list)
    
    # Media
    media: Optional[ProductMedia] = None
    
    # SEO
    seo_title: Optional[str] = Field(None, max_length=100)
    seo_description: Optional[str] = Field(None, max_length=200)
    seo_keywords: Optional[List[str]] = None
    
    # Tax
    tax_id: Optional[str] = None
    is_taxable: bool = True
    
    # Warranty
    warranty: Optional['Warranty'] = None
    
    # Expiry
    expiry: Optional['Expiry'] = None
    
    # Batch tracking
    track_batches: bool = False
    track_serial_numbers: bool = False
    
    # Purchase and sales info
    purchase_unit: Optional[str] = None
    selling_unit: Optional[str] = None
    unit_conversion: Optional[UnitConversion] = None
    
    # Notes
    notes: Optional[str] = Field(None, max_length=1000)

    @field_validator('unit_conversion')
    def validate_unit_conversion(cls, v):
        if v is not None:
            if not v.purchase_unit or not v.selling_unit or not v.conversion_factor:

                raise ValueError("All fields in unit_conversion must be provided if unit_conversion is set")
        return v

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    short_description: Optional[str] = Field(None, max_length=500)
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    barcode: Optional[str] = Field(None, max_length=50)
    product_type: Optional[ProductType] = None
    category_id: Optional[str] = None
    brand_id: Optional[str] = None
    manufacturer_id: Optional[str] = None
    suppliers: Optional[List[SupplierProduct]] = None
    attributes: Optional[Dict[str, Any]] = None
    specifications: Optional[Dict[str, Any]] = None
    inventory: Optional[InventoryBase] = None
    pricing: Optional[PricingCreate] = None
    has_variants: Optional[bool] = None
    variants: Optional[List[ProductVariantCreate]] = None
    weight: Optional[float] = Field(None, ge=0)
    length: Optional[float] = Field(None, ge=0)
    width: Optional[float] = Field(None, ge=0)
    height: Optional[float] = Field(None, ge=0)
    volume: Optional[float] = Field(None, ge=0)
    unit_of_measure: Optional[str] = None
    minimum_order: Optional[int] = Field(None, ge=1)
    maximum_order: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_new: Optional[bool] = None
    is_on_sale: Optional[bool] = None
    is_rental: Optional[bool] = None
    is_digital: Optional[bool] = None
    is_service: Optional[bool] = None
    is_composite: Optional[bool] = None
    tags: Optional[List[str]] = None
    media: Optional[ProductMedia] = None
    seo_title: Optional[str] = Field(None, max_length=100)
    seo_description: Optional[str] = Field(None, max_length=200)
    seo_keywords: Optional[List[str]] = None
    tax_id: Optional[str] = None
    is_taxable: Optional[bool] = None
    warranty: Optional['Warranty'] = None
    expiry: Optional['Expiry'] = None
    track_batches: Optional[bool] = None
    track_serial_numbers: Optional[bool] = None
    purchase_unit: Optional[str] = None
    selling_unit: Optional[str] = None
    unit_conversion: Optional[UnitConversion] = None
    notes: Optional[str] = Field(None, max_length=1000)

    @model_validator(mode='before')
    def validate_variants(cls, values):
        """Validate variants based on product type"""
        variants = values.get('variants', [])
        has_variants = values.get('has_variants', False)
        unit_conversion = values.get('unit_conversion')
        
        if has_variants and variants:
            for variant in variants:
                # For products with unit_conversion (bulk products), weight_kg is required
                if unit_conversion and 'weight_kg' not in variant.attributes:
                    raise ValueError(
                        f"Variant '{variant.variant_name}' must have 'weight_kg' in attributes for bulk products"
                    )
                # For non-bulk products, weight_kg is optional
        return values

    # class Config:
    #     from_attributes = True

class Product(ProductBase, BaseSchema):
    """Complete product with all relationships"""
    category: Optional[Category] = None
    brand: Optional[Brand] = None
    tax: Optional[Tax] = None
    stock_status: StockStatus = StockStatus.IN_STOCK
    total_quantity: float = 0
    available_quantity: int = 0
    low_stock_alert_sent: bool = False
    last_purchase_date: Optional[datetime] = None
    last_sale_date: Optional[datetime] = None
    views_count: int = 0
    sales_count: int = 0
    rating: Optional[float] = Field(None, ge=0, le=5)
    reviews_count: int = 0

    @field_validator('available_quantity')
    def calculate_available(cls, v, values):
        if 'inventory' in values and values['inventory']:
            if hasattr(values['inventory'], 'available'):
                return values['inventory'].available
        return v

    @field_validator('stock_status')
    def determine_stock_status(cls, v, values):
        if 'inventory' in values and values['inventory']:
            if hasattr(values['inventory'], 'status'):
                return values['inventory'].status
        return StockStatus.OUT_OF_STOCK

class ProductSearch(BaseModel):
    """Product search and filter parameters"""
    query: Optional[str] = None
    category_id: Optional[str] = None
    brand_id: Optional[str] = None
    supplier_id: Optional[str] = None
    product_type: Optional[ProductType] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    in_stock: Optional[bool] = None
    is_active: Optional[bool] = None
    is_featured: Optional[bool] = None
    is_on_sale: Optional[bool] = None
    tags: Optional[List[str]] = None
    attributes: Optional[Dict[str, Any]] = None