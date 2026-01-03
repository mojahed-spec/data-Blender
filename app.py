import streamlit as st
import pandas as pd
import io
from src.config import STANDARD_COLUMNS
from src.utils import detect_platform, normalize_dataframe

st.set_page_config(page_title="Data Blender", layout="wide")

st.title("📊 Data Blender")
st.markdown("حول ملفات منصات الإعلانات المتفرقة إلى تقرير موحد بضغطة زر.")

# 1. رفع الملفات
uploaded_files = st.file_uploader("ارفع ملفات CSV أو Excel (Facebook, TikTok, etc.)", 
                                  accept_multiple_files=True, type=['csv', 'xlsx'])

if uploaded_files:
    all_data = []
    
    st.write("---")
    st.subheader("🛠️ Processing Logs:")
    
    for file in uploaded_files:
        try:
            # قراءة الملف حسب نوعه
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            # الكشف عن المنصة
            platform = detect_platform(df.columns)
            
            if platform == "Unknown":
                st.warning(f"⚠️ لم يتم التعرف على المنصة في الملف: {file.name}")
                continue
                
            st.success(f"✅ تم اكتشاف: {platform} (الملف: {file.name})")
            
            # المعالجة والتوحيد
            clean_df = normalize_dataframe(df, platform)
            
            # التأكد من وجود الأعمدة القياسية فقط
            # (نضيف الأعمدة الناقصة ونعبئها أصفار)
            for col in STANDARD_COLUMNS:
                if col not in clean_df.columns:
                    clean_df[col] = 0
            
            # ترتيب الأعمدة حسب القالب القياسي
            final_df_slice = clean_df[STANDARD_COLUMNS]
            all_data.append(final_df_slice)
            
        except Exception as e:
            st.error(f"❌ خطأ في معالجة {file.name}: {e}")

    # التجميع النهائي
    if all_data:
        master_df = pd.concat(all_data, ignore_index=True)
        # ---------------------------------------------------------
        # ⚡ بداية قسم الحسابات التلقائية (The Calculation Engine)
        # ---------------------------------------------------------
        
        # 1. حساب ROAS (العائد على الإنفاق) = Revenue / Spend
        # نستخدم دالة للتأكد أننا لا نقسم على صفر
        master_df['ROAS'] = master_df.apply(lambda x: round(x['Revenue'] / x['Spend'], 2) if x['Spend'] > 0 else 0, axis=1)

        # 2. حساب CPA (تكلفة الشراء) = Spend / Orders
        master_df['CPA'] = master_df.apply(lambda x: round(x['Spend'] / x['Orders'], 2) if x['Orders'] > 0 else 0, axis=1)

        # 3. حساب CPC (تكلفة النقرة) = Spend / Clicks
        master_df['CPC'] = master_df.apply(lambda x: round(x['Spend'] / x['Clicks'], 2) if x['Clicks'] > 0 else 0, axis=1)

        # 4. حساب CTR (نسبة النقر) = (Clicks / Impressions) * 100
        master_df['CTR (%)'] = master_df.apply(lambda x: round((x['Clicks'] / x['Impressions']) * 100, 2) if x['Impressions'] > 0 else 0, axis=1)

        # ترتيب الأعمدة ليكون شكل التقرير احترافي
        cols_order = [
            'Date', 'Platform', 'Campaign Name', 'Ad Set Name', 'Ad Name',
            'Spend', 'Revenue', 'Orders',      # البيانات المالية
            'ROAS', 'CPA', 'CPC', 'CTR (%)',   # البيانات المحسوبة (الجديدة)
            'Impressions', 'Clicks'            # بيانات الوصول
        ]
        
        # إعادة ترتيب الجدول، وإذا كان هناك عمود ناقص لا يظهر خطأ
        existing_cols = [c for c in cols_order if c in master_df.columns]
        master_df = master_df[existing_cols]

        st.write("---")
        st.subheader("📈 النتيجة النهائية الموحدة:")
        
        # عرض سريع للأرقام
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Spend", f"${master_df['Spend'].sum():,.2f}")
        col2.metric("Total Orders", int(master_df['Orders'].sum()))
        
        # حساب ROAS الكلي
        total_roas = master_df['Revenue'].sum() / master_df['Spend'].sum() if master_df['Spend'].sum() > 0 else 0
        col3.metric("Total ROAS", f"{total_roas:.2f}")

        st.dataframe(master_df)
        
        st.write("---")
        st.markdown("### 💾 حفظ النتائج") 
        
        # إنشاء الأعمدة (Columns)
        btn_col1, btn_col2 = st.columns(2)

        # 1. زر تحميل CSV
        csv = master_df.to_csv(index=False).encode('utf-8')
        
        # ⚠️ التعديل هنا: استخدم btn_col1 بدلاً من st
        btn_col1.download_button(
            label="📥 Download Unified Report (CSV)",
            data=csv,
            file_name="Master_Ad_Report.csv",
            mime="text/csv",
            use_container_width=True, # سيأخذ الآن عرض العمود الأول فقط ✅
        )

        # 2. زر تحميل Excel
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            master_df.to_excel(writer, index=False, sheet_name='Unified_Report')
            
            workbook  = writer.book
            worksheet = writer.sheets['Unified_Report']
            header_format = workbook.add_format({'bold': True, 'bg_color': '#D7E4BC', 'border': 1})
            
            for col_num, value in enumerate(master_df.columns.values):
                worksheet.write(0, col_num, value, header_format)

        # هذا الزر صحيح لأنه مرتبط بـ btn_col2
        btn_col2.download_button(
            label="Excel Spreadsheet (.xlsx) 📗",
            data=buffer.getvalue(),
            file_name="Master_Ad_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True # سيأخذ عرض العمود الثاني فقط ✅
        )
else:
    st.info("👆 يرجى رفع الملفات للبدء.")

