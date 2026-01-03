import pandas as pd
import re
from src.config import PLATFORM_MAPPINGS

def clean_currency(value):
    """تحويل النصوص المالية مثل $1,000.00 إلى أرقام 1000.0"""
    if pd.isna(value):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    # إزالة أي شيء ليس رقماً أو نقطة
    clean_val = re.sub(r'[^\d.]', '', str(value))
    try:
        return float(clean_val)
    except ValueError:
        return 0.0

def detect_platform(df_columns):
    """تحديد المنصة بناءً على الأعمدة الموجودة"""
    for platform, config in PLATFORM_MAPPINGS.items():
        if config['signature'] in df_columns:
            return platform
    return "Unknown"

def normalize_dataframe(df, platform):
    """توحيد أسماء الأعمدة وتنظيف البيانات"""
    mapping = PLATFORM_MAPPINGS[platform]['mapping']
    
    # 1. إعادة التسمية
    df = df.rename(columns=mapping)
    
    # 2. إضافة اسم المنصة
    df['Platform'] = platform
    
    # 3. تنظيف الأرقام
    cols_to_clean = ['Spend', 'Revenue']
    for col in cols_to_clean:
        if col in df.columns:
            df[col] = df[col].apply(clean_currency)
        else:
            df[col] = 0.0 # إذا العمود غير موجود نعبئه أصفار
            
    # 4. تنظيف التاريخ (محاولة توحيد الصيغة)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
        
    return df
