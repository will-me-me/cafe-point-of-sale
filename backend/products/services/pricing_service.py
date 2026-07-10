# app/services/pricing_service.py
from decimal import Decimal
from typing import Dict, Any, Optional

from products.schemas.product import Product, ProductVariant
from products.schemas.pricing import PriceTier

class PricingService:
    """Service for calculating dynamic variant pricing"""
    
    @staticmethod
    def get_cost_per_base_unit(product: Product) -> Decimal:
        """
        Calculate cost per base unit (e.g., per kg)
        
        Args:
            product: Product with pricing and unit_conversion
        
        Returns:
            Decimal: Cost per base unit
        """
        if not product.pricing or not product.unit_conversion:
            return Decimal(0)
        
        cost_price = Decimal(str(product.pricing.cost_price))
        conversion_factor = Decimal(str(product.unit_conversion.conversion_factor))
        
        if conversion_factor <= 0:
            return Decimal(0)
        
        return cost_price / conversion_factor
    
    @staticmethod
    def get_variant_weight(variant: ProductVariant) -> Decimal:
        """
        Get variant weight in base unit (kg)
        
        Args:
            variant: Product variant with weight_kg in attributes
        
        Returns:
            Decimal: Weight in kg
        """
        if not variant.attributes or 'weight_kg' not in variant.attributes:
            return Decimal(0)
        
        return Decimal(str(variant.attributes['weight_kg']))
    
    @staticmethod
    def calculate_variant_cost(product: Product, variant: ProductVariant) -> Decimal:
        """
        Calculate cost for a variant based on weight
        
        Args:
            product: Parent product
            variant: Product variant
        
        Returns:
            Decimal: Calculated cost for the variant
        """
        if product.unit_conversion:
            cost_per_kg = PricingService.get_cost_per_base_unit(product)
            weight_kg = PricingService.get_variant_weight(variant)
            
            # If weight is 0, return 0 (could be a non-weight variant)
            if weight_kg == 0:
                return Decimal(0)
            
            return cost_per_kg * weight_kg
        else:
            # Non-bulk product: cost is the cost price
            if product.pricing:
                return Decimal(str(product.pricing.cost_price))
            return Decimal(0)
    
    @staticmethod
    def calculate_variant_margin(product: Product, variant: ProductVariant) -> Dict[str, float]:
        """
        Calculate margin and markup for a variant
        
        Args:
            product: Parent product
            variant: Product variant
        
        Returns:
            Dict: margin and markup percentages
        """
        cost = PricingService.calculate_variant_cost(product, variant)
        
        # Get selling price from variant pricing
        selling = Decimal('0')
        if variant.pricing:
            if isinstance(variant.pricing, dict):
                selling = Decimal(str(variant.pricing.get('selling_price', 0)))
            else:
                selling = Decimal(str(variant.pricing.selling_price))
        
        if selling == 0:
            return {'margin': 0, 'markup': 0}
        
        margin = ((selling - cost) / selling) * 100
        markup = ((selling - cost) / cost) * 100 if cost > 0 else 0
        
        return {
            'margin': float(margin),
            'markup': float(markup)
        }
    
    @staticmethod
    def enrich_variant_with_pricing(product: Product, variant: ProductVariant) -> Dict[str, Any]:
        """
        Enrich a variant with computed pricing information
        
        Args:
            product: Parent product
            variant: Product variant
        
        Returns:
            Dict: Variant with computed pricing
        """
        variant_dict = variant.dict() if hasattr(variant, 'dict') else dict(variant)
        
        # Calculate cost
        cost = PricingService.calculate_variant_cost(product, variant)
        variant_dict['computed_cost'] = float(cost)
        
        # Get selling price
        selling = 0
        if variant.pricing:
            if isinstance(variant.pricing, dict):
                selling = variant.pricing.get('selling_price', 0)
            else:
                selling = variant.pricing.selling_price
        
        variant_dict['computed_selling_price'] = float(selling)
        
        # Calculate margin
        margin_data = PricingService.calculate_variant_margin(product, variant)
        variant_dict['computed_margin'] = margin_data['margin']
        variant_dict['computed_markup'] = margin_data['markup']
        
        return variant_dict
    
    @staticmethod
    def get_variant_pricing(product: Product, variant: ProductVariant) -> Dict[str, Any]:
        """
        Get complete pricing for a variant including all price tiers
        
        Args:
            product: Parent product
            variant: Product variant
        
        Returns:
            Dict: Complete pricing information
        """
        cost = PricingService.calculate_variant_cost(product, variant)
        weight_kg = PricingService.get_variant_weight(variant)
        
        result = {
            'cost_price': float(cost),
            'weight_kg': float(weight_kg),
            'cost_per_kg': float(PricingService.get_cost_per_base_unit(product)),
        }
        
        # Add selling prices
        if variant.pricing:
            if isinstance(variant.pricing, dict):
                result['selling_price'] = variant.pricing.get('selling_price', 0)
                result['price_tiers'] = variant.pricing.get('price_tiers', {})
            else:
                result['selling_price'] = variant.pricing.selling_price
                result['price_tiers'] = variant.pricing.price_tiers
        
        # Calculate margins
        margin_data = PricingService.calculate_variant_margin(product, variant)
        result['margin'] = margin_data['margin']
        result['markup'] = margin_data['markup']
        
        return result