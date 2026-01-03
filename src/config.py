# هذا الملف يحتوي على الثوابت وقواميس الترجمة

STANDARD_COLUMNS = [
    'Date', 'Platform', 'Campaign Name', 'Ad Set Name', 'Ad Name',
    'Spend', 'Impressions', 'Clicks', 'Orders', 'Revenue'
]
PLATFORM_MAPPINGS = {
    # ==========================================
    # 1. Meta Ads (Facebook)
    # ==========================================
    'Facebook': {
        'signature': 'Amount spent (USD)',
        'mapping': {
            'Reporting Starts': 'Date',
            'Campaign name': 'Campaign Name',
            'Ad set name': 'Ad Set Name',
            'Ad name': 'Ad Name',
            'Amount spent (USD)': 'Spend',
            'Impressions': 'Impressions',
            'Link clicks': 'Clicks',
            'Purchases': 'Orders',
            'Purchases Conversion Value': 'Revenue'
        }
    },

    # ==========================================
    # 2. Instagram (Meta)
    # ==========================================
    'Instagram': {
        # غالباً نفس فيسبوك، لكن وضعناها احتياطاً
        'signature': 'Post comments', # عمود يظهر غالباً في تقارير انستجرام المخصصة
        'mapping': {
            'Reporting Starts': 'Date',
            'Campaign name': 'Campaign Name',
            'Ad set name': 'Ad Set Name',
            'Ad name': 'Ad Name',
            'Amount spent (USD)': 'Spend',
            'Impressions': 'Impressions',
            'Link clicks': 'Clicks',
            'Purchases': 'Orders',
            'Purchases Conversion Value': 'Revenue'
        }
    },

    # ==========================================
    # 3. TikTok Ads
    # ==========================================
    'TikTok': {
        'signature': 'Total Cost',
        'mapping': {
            'Stat Time': 'Date',
            'Campaign Name': 'Campaign Name',
            'Ad Group Name': 'Ad Set Name',
            'Ad Name': 'Ad Name',
            'Total Cost': 'Spend',
            'Impressions': 'Impressions',
            'Clicks': 'Clicks',
            'Total Complete Payment': 'Orders',
            'Total Complete Payment Value': 'Revenue'
        }
    },

    # ==========================================
    # 4. Snapchat Ads
    # ==========================================
    'Snapchat': {
        'signature': 'Paid Impressions',
        'mapping': {
            'Start Time': 'Date',
            'Campaign Name': 'Campaign Name',
            'Ad Set Name': 'Ad Set Name',
            'Creative Name': 'Ad Name',
            'Amount Spent': 'Spend',
            'Paid Impressions': 'Impressions',
            'Swipe Ups': 'Clicks',
            'Purchases': 'Orders',
            'Purchases Value': 'Revenue'
        }
    },

    # ==========================================
    # 5. Google Ads
    # ==========================================
    'Google': {
        'signature': 'Cost',
        'mapping': {
            'Day': 'Date',
            'Campaign': 'Campaign Name',
            'Ad group': 'Ad Set Name',
            'Ad name': 'Ad Name',
            'Cost': 'Spend',
            'Impr.': 'Impressions',
            'Clicks': 'Clicks',
            'Conversions': 'Orders',
            'Total Conv. value': 'Revenue'
        }
    },

    # ==========================================
    # 6. LinkedIn Ads
    # ==========================================
    'LinkedIn': {
        'signature': 'Total spent', # قد تكون Total spent (USD)
        'mapping': {
            'Start Date': 'Date',
            'Campaign Name': 'Campaign Name',
            'Campaign Group Name': 'Ad Set Name',
            'Creative Name': 'Ad Name',
            'Total spent': 'Spend',
            'Impressions': 'Impressions',
            'Clicks': 'Clicks',
            'Total conversions': 'Orders',
            'Total conversion value': 'Revenue'
        }
    },

    # ==========================================
    # 7. Twitter (X) Ads
    # ==========================================
    'Twitter': {
        'signature': 'Engagements', # بصمة مميزة لتويتر لتفريقها عن غيرها
        'mapping': {
            'Time': 'Date',
            'Campaign name': 'Campaign Name',
            'Ad group name': 'Ad Set Name',
            'Tweet text': 'Ad Name', # تويتر يستخدم نص التغريدة كاسم للإعلان غالباً
            'Spend': 'Spend',
            'Impressions': 'Impressions',
            'Link clicks': 'Clicks',
            'Conversions': 'Orders',
            'Conversion value': 'Revenue'
        }
    }
}