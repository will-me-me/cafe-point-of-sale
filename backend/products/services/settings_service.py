# app/services/settings_service.py
from typing import Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
import json

from database import db
from products.schemas.settings import (
    Settings, SettingsUpdate,
    StoreSettings, POSSettings, ProductSettings,
    PaymentSettings, ReceiptSettings, PrinterSettings,
    SystemSettings
)

class SettingsService:
    def __init__(self):
        self.collection = db["settings"]
    
    def _serialize_object_id(self, obj):
        """Convert ObjectId to string for JSON serialization"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, ObjectId):
                    obj[key] = str(value)
                elif isinstance(value, datetime):
                    obj[key] = value.isoformat()
                elif isinstance(value, list):
                    obj[key] = [self._serialize_object_id(item) if isinstance(item, dict) else item for item in value]
                elif isinstance(value, dict):
                    obj[key] = self._serialize_object_id(value)
        return obj
    
    def _get_default_settings(self) -> dict:
        """Get default settings"""
        return {
            "store": {
                "name": "Babadeacon Coffee",
                "email": "info@babadeacon.com",
                "address": "123 Coffee Street, Nairobi, Kenya",
                "phone": "+254-700-123456",
                "currency": "KES",
                "timezone": "Africa/Nairobi",
                "logo": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            "pos": {
                "default_order_type": "takeaway",
                "default_payment": "cash",
                "tax_rate": 10.0,
                "receipt_footer": "Thank you for your order!",
                "auto_print_receipt": True,
                "require_customer": False,
                "allow_debt": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            "products": {
                "default_reorder": 10,
                "low_stock_threshold": 5,
                "enable_variants": True,
                "track_inventory": True,
                "require_barcode": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            "payments": {
                "payment_methods": [
                    {"id": "cash", "name": "Cash", "icon": "mdi-cash", "enabled": True},
                    {"id": "mpesa", "name": "M-Pesa", "icon": "mdi-cellphone", "enabled": True},
                    {"id": "card", "name": "Card", "icon": "mdi-credit-card", "enabled": False},
                    {"id": "debt", "name": "Debt", "icon": "mdi-account-cash", "enabled": True}
                ],
                "mpesa_paybill": None,
                "mpesa_account": None,
                "allow_partial_payment": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            "receipt": {
                "header": "☕ BABADEACON COFFEE\nPremium Coffee & Snacks",
                "footer": "Thank you for your order!\nVisit us again at Babadeacon Coffee",
                "paper_width": "80",
                "font_size": "12",
                "show_tax_breakdown": True,
                "show_item_discounts": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            "printer": {
                "connection_type": "bluetooth",
                "bluetooth_device": None,
                "usb_device": None,
                "ip_address": None,
                "port": "9100",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            "system": {
                "backup_frequency": "daily",
                "log_retention": 30,
                "auto_backup": True,
                "debug_mode": False,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            "updated_at": datetime.utcnow()
        }
    
    async def get_settings(self) -> Settings:
        """Get all settings"""
        settings = await self.collection.find_one({})
        
        if not settings:
            # Create default settings if none exist
            default_settings = self._get_default_settings()
            result = await self.collection.insert_one(default_settings)
            settings = await self.collection.find_one({"_id": result.inserted_id})
        
        # Serialize ObjectId to string
        serialized = self._serialize_object_id(settings)
        
        # Remove _id from the response
        if "_id" in serialized:
            del serialized["_id"]
        
        return Settings(**serialized)
    
    async def update_settings(self, settings_data: SettingsUpdate) -> Settings:
        """Update settings"""
        current_settings = await self.get_settings()
        
        # Convert settings_data to dict
        update_dict = settings_data.dict(exclude_unset=True)
        
        # Prepare update operations
        update_ops = {}
        
        for section, data in update_dict.items():
            if data:
                for key, value in data.items():
                    if value is not None:
                        update_ops[f"{section}.{key}"] = value
                # Update timestamp for section
                update_ops[f"{section}.updated_at"] = datetime.utcnow()
        
        update_ops["updated_at"] = datetime.utcnow()
        
        if update_ops:
            result = await self.collection.update_one(
                {},
                {"$set": update_ops}
            )
            
            if result.modified_count == 0:
                raise HTTPException(status_code=500, detail="Failed to update settings")
        
        return await self.get_settings()
    
    async def reset_settings(self) -> Settings:
        """Reset settings to default values"""
        default_settings = self._get_default_settings()
        
        # Delete existing settings
        await self.collection.delete_many({})
        
        # Insert default settings
        result = await self.collection.insert_one(default_settings)
        settings = await self.collection.find_one({"_id": result.inserted_id})
        
        serialized = self._serialize_object_id(settings)
        if "_id" in serialized:
            del serialized["_id"]
        
        return Settings(**serialized)
    
    async def update_store_settings(self, store_data: StoreSettings) -> StoreSettings:
        """Update store settings only"""
        settings = await self.get_settings()
        
        update_dict = store_data.dict(exclude_unset=True)
        update_dict["store.updated_at"] = datetime.utcnow()
        
        await self.collection.update_one(
            {},
            {"$set": update_dict}
        )
        
        updated_settings = await self.get_settings()
        return updated_settings.store
    
    async def update_pos_settings(self, pos_data: POSSettings) -> POSSettings:
        """Update POS settings only"""
        update_dict = pos_data.dict(exclude_unset=True)
        update_dict["pos.updated_at"] = datetime.utcnow()
        
        await self.collection.update_one(
            {},
            {"$set": update_dict}
        )
        
        updated_settings = await self.get_settings()
        return updated_settings.pos
    
    async def update_product_settings(self, product_data: ProductSettings) -> ProductSettings:
        """Update product settings only"""
        update_dict = product_data.dict(exclude_unset=True)
        update_dict["products.updated_at"] = datetime.utcnow()
        
        await self.collection.update_one(
            {},
            {"$set": update_dict}
        )
        
        updated_settings = await self.get_settings()
        return updated_settings.products
    
    async def update_payment_settings(self, payment_data: PaymentSettings) -> PaymentSettings:
        """Update payment settings only"""
        update_dict = payment_data.dict(exclude_unset=True)
        update_dict["payments.updated_at"] = datetime.utcnow()
        
        # Handle payment_methods list specially
        if "payment_methods" in update_dict:
            update_dict["payments.payment_methods"] = update_dict["payment_methods"]
            del update_dict["payment_methods"]
        
        await self.collection.update_one(
            {},
            {"$set": update_dict}
        )
        
        updated_settings = await self.get_settings()
        return updated_settings.payments
    
    async def update_receipt_settings(self, receipt_data: ReceiptSettings) -> ReceiptSettings:
        """Update receipt settings only"""
        update_dict = receipt_data.dict(exclude_unset=True)
        update_dict["receipt.updated_at"] = datetime.utcnow()
        
        await self.collection.update_one(
            {},
            {"$set": update_dict}
        )
        
        updated_settings = await self.get_settings()
        return updated_settings.receipt
    
    async def update_printer_settings(self, printer_data: PrinterSettings) -> PrinterSettings:
        """Update printer settings only"""
        update_dict = printer_data.dict(exclude_unset=True)
        update_dict["printer.updated_at"] = datetime.utcnow()
        
        await self.collection.update_one(
            {},
            {"$set": update_dict}
        )
        
        updated_settings = await self.get_settings()
        return updated_settings.printer
    
    async def update_system_settings(self, system_data: SystemSettings) -> SystemSettings:
        """Update system settings only"""
        update_dict = system_data.dict(exclude_unset=True)
        update_dict["system.updated_at"] = datetime.utcnow()
        
        await self.collection.update_one(
            {},
            {"$set": update_dict}
        )
        
        updated_settings = await self.get_settings()
        return updated_settings.system

# Singleton instance
settings_service = SettingsService()