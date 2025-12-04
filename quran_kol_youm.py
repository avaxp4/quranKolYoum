import os
import random
import json
import sys
import requests
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)                
    ]
)

load_dotenv()
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

TOTAL_PAGES = 606
IMAGES_DIR = os.path.join("static", "images")
TRACKING_FILE = "posted_pages.json"
DUAS_FILE = "duaa.json"

def load_duas(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("duas", [])
    except FileNotFoundError:
        logging.error(f"ملف الأدعية غير موجود في المسار: {file_path}")
        return []
    except json.JSONDecodeError:
        logging.error(f"ملف الأدعية {file_path} يحتوي على تنسيق JSON غير صالح.")
        return []

def load_state():
    """تحميل حالة الصفحات المنشورة والأدعية المستخدمة"""
    if not os.path.exists(TRACKING_FILE):
        return {"posted_pages": [], "used_duas": []}
    try:
        data = json.load(open(TRACKING_FILE, "r", encoding="utf-8"))
        # دعم التوافق مع النسخة القديمة التي كانت تحتوي على posted فقط
        if "posted" in data and "posted_pages" not in data:
            return {"posted_pages": data["posted"], "used_duas": []}
        return {
            "posted_pages": data.get("posted_pages", []),
            "used_duas": data.get("used_duas", [])
        }
    except (json.JSONDecodeError, AttributeError):
        return {"posted_pages": [], "used_duas": []}

def save_state(posted_pages, used_duas):
    """حفظ الحالة الجديدة"""
    with open(TRACKING_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "posted_pages": posted_pages,
            "used_duas": used_duas
        }, f, indent=2, ensure_ascii=False)

def get_next_page_sequential(posted_pages):
    """تحديد الصفحة التالية بشكل تسلسلي (ختمة)"""
    if not posted_pages:
        return 1
    
    last_page = max(posted_pages)
    next_page = last_page + 1
    
    if next_page > TOTAL_PAGES:
        logging.info("🎉 اكتملت الختمة! سيتم إعادة البدء من الصفحة 1.")
        # ملاحظة: سنقوم بتصفير القائمة في الدالة الرئيسية عند الحفظ
        return 1
    
    return next_page

def get_unique_dua(all_duas, used_duas):
    """اختيار دعاء لم يتم استخدامه من قبل، وإعادة التعيين عند النفاذ"""
    # استخراج الأدعية المتاحة (التي لم تُستخدم)
    available_duas = [d for d in all_duas if d not in used_duas]
    
    if not available_duas:
        logging.info("🔄 تم استخدام جميع الأدعية. إعادة تعيين قائمة الأدعية.")
        used_duas = [] # تصفير القائمة محلياً
        available_duas = all_duas # إعادة ملء القائمة
    
    # اختيار دعاء عشوائي من القائمة المتاحة (للتنويع دون تكرار)
    selection = random.choice(available_duas)
    return selection, used_duas

def publish_to_facebook():
    logging.info("... بدء عملية النشر ...")
    if not PAGE_ID or not ACCESS_TOKEN:
        logging.critical("تأكد من FACEBOOK_PAGE_ID و FACEBOOK_ACCESS_TOKEN في .env")
        sys.exit(1)

    duas = load_duas(DUAS_FILE)
    if not duas:
        logging.error("لا توجد أدعية في duaa.json")
        sys.exit(1)

    # تحميل الحالة
    state = load_state()
    posted_pages = state["posted_pages"]
    used_duas_list = state["used_duas"]

    # تحديد الصفحة والدعاء
    page_number = get_next_page_sequential(posted_pages)
    
    # إذا عادت الصفحة 1 وكان هناك صفحات منشورة سابقاً، فهذا يعني بداية ختمة جديدة
    if page_number == 1 and posted_pages:
        posted_pages = [] # تصفير الصفحات

    dua_text, updated_used_duas = get_unique_dua(duas, used_duas_list)
    hashtags = "\n\n#القرآن_الكريم #ورد_يومي #تدبر #ختمة_القرآن"
    caption = f"ورد القرآن اليومي، صفحة {page_number}\n\n'{dua_text}'{hashtags}"

    image_path = os.path.join(IMAGES_DIR, f"page_{page_number}.jpg")

    if not os.path.exists(image_path):
        logging.error(f"الصورة غير موجودة: {image_path}")
        return

    logging.info(f"📖 النشر للصورة رقم: {page_number}")
    logging.info(f"📝 التعليق (جزء): {caption[:50]}...")

    url = f"https://graph.facebook.com/v24.0/{PAGE_ID}/photos"
    params = {
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }

    try:
        with open(image_path, "rb") as img:
            files = {"source": img}
            resp = requests.post(url, params=params, files=files, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            logging.info(f"رد API: {result}")

            # تحقق من مفاتيح الرد
            post_id = result.get("post_id") or result.get("id")
            if post_id:
                # تحديث القوائم والحفظ
                posted_pages.append(page_number)
                # نضيف الدعاء الحالي لقائمة المستخدم
                updated_used_duas.append(caption)
                
                save_state(posted_pages, updated_used_duas)
                logging.info(f"✅ نشر ناجح! https://facebook.com/{post_id}")
            else:
                logging.error(f"فشل: لا توجد post_id في الرد: {result}")

    except requests.exceptions.HTTPError as e:
        logging.error(f"خطأ HTTP: {resp.status_code} - {resp.text}")
    except Exception as e:
        logging.exception(f"حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    publish_to_facebook()
