# app/api/routes/settings.py
from fastapi import APIRouter, HTTPException, Depends, status
from typing import Optional

from auth.jwt_handler import check_admin_permissions, get_current_user
from products.schemas.settings import (
    Settings, SettingsUpdate,
    StoreSettingsUpdate, POSSettingsUpdate,
    ProductSettingsUpdate, PaymentSettingsUpdate,
    ReceiptSettingsUpdate, PrinterSettingsUpdate,
    SystemSettingsUpdate
)
from products.services.settings_service import settings_service


router = APIRouter()

@router.get("/", response_model=Settings)
async def get_settings(
    current_user: dict = Depends(get_current_user)
):
    """Get all system settings"""
    try:
        settings = await settings_service.get_settings()
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/", response_model=Settings)
async def update_settings(
    settings_data: SettingsUpdate,
    current_user: dict = Depends(check_admin_permissions)
):
    """Update all system settings (Admin only)"""
    try:
        settings = await settings_service.update_settings(settings_data)
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset", response_model=Settings)
async def reset_settings(
    current_user: dict = Depends(check_admin_permissions)
):
    """Reset all settings to defaults (Admin only)"""
    try:
        settings = await settings_service.reset_settings()
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ Individual Section Endpoints ============

@router.put("/store", response_model=StoreSettingsUpdate)
async def update_store_settings(
    store_data: StoreSettingsUpdate,
    current_user: dict = Depends(check_admin_permissions)
):
    """Update store settings only (Admin only)"""
    try:
        settings = await settings_service.update_store_settings(store_data)
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/pos", response_model=POSSettingsUpdate)
async def update_pos_settings(
    pos_data: POSSettingsUpdate,
    current_user: dict = Depends(check_admin_permissions)
):
    """Update POS settings only (Admin only)"""
    try:
        settings = await settings_service.update_pos_settings(pos_data)
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/products", response_model=ProductSettingsUpdate)
async def update_product_settings(
    product_data: ProductSettingsUpdate,
    current_user: dict = Depends(check_admin_permissions)
):
    """Update product settings only (Admin only)"""
    try:
        settings = await settings_service.update_product_settings(product_data)
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/payments", response_model=PaymentSettingsUpdate)
async def update_payment_settings(
    payment_data: PaymentSettingsUpdate,
    current_user: dict = Depends(check_admin_permissions)
):
    """Update payment settings only (Admin only)"""
    try:
        settings = await settings_service.update_payment_settings(payment_data)
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/receipt", response_model=ReceiptSettingsUpdate)
async def update_receipt_settings(
    receipt_data: ReceiptSettingsUpdate,
    current_user: dict = Depends(check_admin_permissions)
):
    """Update receipt settings only (Admin only)"""
    try:
        settings = await settings_service.update_receipt_settings(receipt_data)
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/printer", response_model=PrinterSettingsUpdate)
async def update_printer_settings(
    printer_data: PrinterSettingsUpdate,
    current_user: dict = Depends(check_admin_permissions)
):
    """Update printer settings only (Admin only)"""
    try:
        settings = await settings_service.update_printer_settings(printer_data)
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/system", response_model=SystemSettingsUpdate)
async def update_system_settings(
    system_data: SystemSettingsUpdate,
    current_user: dict = Depends(check_admin_permissions)
):
    """Update system settings only (Admin only)"""
    try:
        settings = await settings_service.update_system_settings(system_data)
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))