import json
import re

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# আপনার টেলিগ্রাম টোকেন এখানে বসান
import os

TOKEN = os.environ.get("BOT_TOKEN")

# quran.json ফাইল লোড করা
with open("quran.json", "r", encoding="utf-8") as f:
    QURAN = json.load(f)

# ১১৪টি সূরার তালিকা (ইংরেজি ও বাংলা)
SURAHS = [
    ("Al-Fatiha", "আল-ফাতিহা"),
    ("Al-Baqarah", "আল-বাকারা"),
    ("Aal-Imran", "আলে ইমরান"),
    ("An-Nisa", "আন-নিসা"),
    ("Al-Maidah", "আল-মায়িদাহ"),
    ("Al-Anam", "আল-আনআম"),
    ("Al-Araf", "আল-আরাফ"),
    ("Al-Anfal", "আল-আনফাল"),
    ("At-Tawbah", "আত-তাওবাহ"),
    ("Yunus", "ইউনুস"),
    ("Hud", "হুদ"),
    ("Yusuf", "ইউসুফ"),
    ("Ar-Rad", "আর-রাদ"),
    ("Ibrahim", "ইব্রাহিম"),
    ("Al-Hijr", "আল-হিজর"),
    ("An-Nahl", "আন-নাহল"),
    ("Al-Isra", "আল-ইসরা"),
    ("Al-Kahf", "আল-কাহফ"),
    ("Maryam", "মারইয়াম"),
    ("Ta-Ha", "ত্বা-হা"),
    ("Al-Anbiya", "আল-আম্বিয়া"),
    ("Al-Hajj", "আল-হজ্জ"),
    ("Al-Muminun", "আল-মুমিনুন"),
    ("An-Nur", "আন-নূর"),
    ("Al-Furqan", "আল-ফুরকান"),
    ("Ash-Shuara", "আশ-শুআরা"),
    ("An-Naml", "আন-নামল"),
    ("Al-Qasas", "আল-কাসাস"),
    ("Al-Ankabut", "আল-আনকাবুত"),
    ("Ar-Rum", "আর-রূম"),
    ("Luqman", "লোকমান"),
    ("As-Sajdah", "আস-সাজদাহ"),
    ("Al-Ahzab", "আল-আহযাব"),
    ("Saba", "সাবা"),
    ("Fatir", "ফাতির"),
    ("Ya-Sin", "ইয়াসিন"),
    ("As-Saffat", "আস-সাফফাত"),
    ("Sad", "সোয়াদ"),
    ("Az-Zumar", "আয-যুমার"),
    ("Ghafir", "গাফির"),
    ("Fussilat", "ফুসসিলাত"),
    ("Ash-Shura", "আশ-শূরা"),
    ("Az-Zukhruf", "আয-যুখরুফ"),
    ("Ad-Dukhan", "আদ-দুখান"),
    ("Al-Jathiyah", "আল-জাসিয়াহ"),
    ("Al-Ahqaf", "আল-আহকাফ"),
    ("Muhammad", "মুহাম্মদ"),
    ("Al-Fath", "আল-ফাতহ"),
    ("Al-Hujurat", "আল-হুজুরাত"),
    ("Qaf", "কাফ"),
    ("Adh-Dhariyat", "আয-যারিয়াত"),
    ("At-Tur", "আত-তূর"),
    ("An-Najm", "আন-নাজম"),
    ("Al-Qamar", "আল-কামার"),
    ("Ar-Rahman", "আর-রহমান"),
    ("Al-Waqiah", "আল-ওয়াকিয়াহ"),
    ("Al-Hadid", "আল-হাদীদ"),
    ("Al-Mujadila", "আল-মুজাদালাহ"),
    ("Al-Hashr", "আল-হাশর"),
    ("Al-Mumtahanah", "আল-মুমতাহিনাহ"),
    ("As-Saff", "আস-সাফ"),
    ("Al-Jumuah", "আল-জুমুআহ"),
    ("Al-Munafiqun", "আল-মুনাফিকুন"),
    ("At-Taghabun", "আত-তাগাবুন"),
    ("At-Talaq", "আত-তালাক"),
    ("At-Tahrim", "আত-তাহরীম"),
    ("Al-Mulk", "আল-মুলক"),
    ("Al-Qalam", "আল-কলম"),
    ("Al-Haqqah", "আল-হাক্কাহ"),
    ("Al-Maarij", "আল-মাআরিজ"),
    ("Nuh", "নূহ"),
    ("Al-Jinn", "আল-জিন"),
    ("Al-Muzzammil", "আল-মুযযাম্মিল"),
    ("Al-Muddaththir", "আল-মুদ্দাসসির"),
    ("Al-Qiyamah", "আল-কিয়ামাহ"),
    ("Al-Insan", "আল-ইনসান"),
    ("Al-Mursalat", "আল-মুরসালাত"),
    ("An-Naba", "আন-নাবা"),
    ("An-Naziat", "আন-নাযিআত"),
    ("Abasa", "আবাসা"),
    ("At-Takwir", "আত-তাকভীর"),
    ("Al-Infitar", "আল-ইনফিতার"),
    ("Al-Mutaffifin", "আল-মুতাফফিফিন"),
    ("Al-Inshiqaq", "আল-ইনশিকাক"),
    ("Al-Buruj", "আল-বুরুজ"),
    ("At-Tariq", "আত-তারিক"),
    ("Al-Ala", "আল-আলা"),
    ("Al-Ghashiyah", "আল-গাশিয়াহ"),
    ("Al-Fajr", "আল-ফজর"),
    ("Al-Balad", "আল-বালাদ"),
    ("Ash-Shams", "আশ-শামস"),
    ("Al-Layl", "আল-লাইল"),
    ("Ad-Duha", "আদ-দুহা"),
    ("Ash-Sharh", "আশ-শারহ"),
    ("At-Tin", "আত-তীন"),
    ("Al-Alaq", "আল-আলাক"),
    ("Al-Qadr", "আল-কদর"),
    ("Al-Bayyinah", "আল-বাইয়িনাহ"),
    ("Az-Zalzalah", "আয-যিলযাল"),
    ("Al-Adiyat", "আল-আদিয়াত"),
    ("Al-Qariah", "আল-কারিআহ"),
    ("At-Takathur", "আত-তাকাসুর"),
    ("Al-Asr", "আল-আসর"),
    ("Al-Humazah", "আল-হুমাযাহ"),
    ("Al-Fil", "আল-ফীল"),
    ("Quraysh", "কুরাইশ"),
    ("Al-Maun", "আল-মাউন"),
    ("Al-Kawthar", "আল-কাওসার"),
    ("Al-Kafirun", "আল-কাফিরুন"),
    ("An-Nasr", "আন-নাসর"),
    ("Al-Masad", "আল-মাসাদ"),
    ("Al-Ikhlas", "আল-ইখলাস"),
    ("Al-Falaq", "আল-ফালাক"),
    ("An-Nas", "আন-নাস")
]

def get_surah_name(surah):
    return SURAHS[int(surah) - 1][1]

def get_ayah_text(surah, ayah):
    data = QURAN[str(surah)][str(ayah)]
    return (
        f"📖 সূরা {surah} | {get_surah_name(surah)}\n"
        f"আয়াত {ayah}\n\n"
        f"{data['arabic']}\n\n"
        f"🔊 বাংলা উচ্চারণ\n"
        f"{data['pronunciation']}\n\n"
        f"🇧🇩 বাংলা অর্থ\n"
        f"{data['bangla']}"
    )

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 All Surahs / সকল সূরা", callback_data="sp:0")],
        [InlineKeyboardButton("🔍 Search Surah / সূরা খুঁজুন", callback_data="search")]
    ])

def surah_keyboard(page=0):
    per_page = 10
    start = page * per_page
    end = start + per_page
    keyboard = []

    for i in range(start, min(end, 114), 2):
        row = []
        for j in range(i, min(i + 2, min(end, 114))):
            english, bangla = SURAHS[j]
            # ইংরেজি নামের বদলে এখানে শুধু বাংলা নাম বা (নম্বর + বাংলা নাম) দেওয়া হলো
            row.append(InlineKeyboardButton(f"{j+1}. {bangla}", callback_data=f"s:{j+1}"))
        keyboard.append(row)

    navigation = []
    if page > 0:
        navigation.append(InlineKeyboardButton("⬅️ পেছনের পাতা", callback_data=f"sp:{page-1}"))
    if end < 114:
        navigation.append(InlineKeyboardButton("পরের পাতা ➡️", callback_data=f"sp:{page+1}"))

    if navigation:
        keyboard.append(navigation)

    keyboard.append([InlineKeyboardButton("🏠 হোম", callback_data="home")])
    return InlineKeyboardMarkup(keyboard)

# নতুন লজিক: পরের বা আগের আয়াতে যাওয়ার সময় সূরা পরিবর্তন হ্যান্ডেল করা
def get_next_ayah(surah, ayah):
    total = len(QURAN[str(surah)])
    if ayah < total:
        return surah, ayah + 1
    else:
        if surah < 114:
            return surah + 1, 1
        else:
            return 1, 1  # কুরআন শেষ হলে আবার ফাতিহায় ফিরে যাবে

def get_prev_ayah(surah, ayah):
    if ayah > 1:
        return surah, ayah - 1
    else:
        if surah > 1:
            prev_surah = surah - 1
            prev_total = len(QURAN[str(prev_surah)])
            return prev_surah, prev_total
        else:
            return 114, len(QURAN["114"])

def get_buttons(surah, ayah):
    next_surah, next_ayah = get_next_ayah(surah, ayah)
    prev_surah, prev_ayah = get_prev_ayah(surah, ayah)

    keyboard = [[
        InlineKeyboardButton("⬅️ Previous", callback_data=f"a:{prev_surah}:{prev_ayah}"),
        InlineKeyboardButton("Next ➡️", callback_data=f"a:{next_surah}:{next_ayah}")
    ], [
        InlineKeyboardButton("📚 All Surahs", callback_data="sp:0"),
        InlineKeyboardButton("🏠 Home", callback_data="home")
    ]]
    return InlineKeyboardMarkup(keyboard)

def normalize_name(name):
    name = name.lower().strip()
    name = re.sub(r"[^a-z0-9\u0980-\u09ff]+", " ", name)
    words = name.split()
    words = [word for word in words if word not in ("surah", "sura", "surat")]
    return " ".join(words)

def find_surahs(search):
    search = normalize_name(search)
    results = []
    for i, (english, bangla) in enumerate(SURAHS):
        names = [normalize_name(english), normalize_name(bangla)]
        if any(search == name or name.startswith(search) or search in name for name in names):
            results.append(i + 1)
    return results

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 King Fahad Bangla Quran Bot\n\n"
        "আসসালামু আলাইকুম ওয়া রহমাতুল্লাহি ওয়া বারাকাতুহু।\n\n"
        "পবিত্র আল-কুরআন পড়ুন বাংলা উচ্চারণ ও অর্থসহ।\n\n"
        "💡 আপনি যেকোনো সময় সরাসরি লিখতে পারেন:\n"
        "• `1 1` (সূরা ও আয়াত)\n"
        "• `2:255` (আয়াতুল কুরসি)\n"
        "• `Fatiha` অথবা `আল-বাকারা` (সূরার নাম)",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def surahs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 পবিত্র আল-কুরআনের ১১৪টি সূরা:", reply_markup=surah_keyboard(0))

async def ayah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        surah = int(context.args[0])
        ayah_no = int(context.args[1])
        text = get_ayah_text(surah, ayah_no)
        await update.message.reply_text(text, reply_markup=get_buttons(surah, ayah_no))
    except (IndexError, ValueError, KeyError):
        await update.message.reply_text("সঠিকভাবে লিখুন:\n/ayah 1 1")

# স্মার্ট এবং ইন্টারেক্টিভ টেক্সট হ্যান্ডলার
async def smart_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    match = re.match(r"^(\d{1,3})[\s:\.]+(\d{1,3})$", text)
    if match:
        surah = int(match.group(1))
        ayah_no = int(match.group(2))
        try:
            if str(surah) in QURAN and str(ayah_no) in QURAN[str(surah)]:
                msg_text = get_ayah_text(surah, ayah_no)
                await update.message.reply_text(msg_text, reply_markup=get_buttons(surah, ayah_no))
                return
            else:
                await update.message.reply_text("❌ এই সূরা বা আয়াতটি ডাটাবেসে পাওয়া যায়নি। সঠিক নম্বর দিন (যেমন: 1 1)")
                return
        except Exception:
            pass

    if text.isdigit():
        surah = int(text)
        if 1 <= surah <= 114:
            if str(surah) in QURAN:
                msg_text = get_ayah_text(surah, 1)
                await update.message.reply_text(msg_text, reply_markup=get_buttons(surah, 1))
                return
        else:
            await update.message.reply_text("❌ অনুগ্রহ করে ১ থেকে ১১৪ এর মধ্যে একটি সূরা নম্বর দিন।")
            return

    results = find_surahs(text)
    if len(results) == 1:
        surah = results[0]
        msg_text = get_ayah_text(surah, 1)
        await update.message.reply_text(msg_text, reply_markup=get_buttons(surah, 1))
        return
    elif len(results) > 1:
        keyboard = []
        for number in results:
            english, bangla = SURAHS[number - 1]
            keyboard.append([
                InlineKeyboardButton(
                    f"{number}. {english} | {bangla}",
                    callback_data=f"s:{number}"
                )
            ])
        keyboard.append([InlineKeyboardButton("📚 All Surahs", callback_data="sp:0")])
        await update.message.reply_text("🔍 আপনার অনুসন্ধানের একাধিক ফলাফল পাওয়া গেছে:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    await update.message.reply_text(
        "দুঃখিত! আপনার লেখা বুঝতে পারিনি।\n\n"
        "আপনি যেভাবে লিখতে পারেন:\n"
        "• সরাসরি আয়াত দেখতে: `1 1` অথবা `2:255`\n"
        "• সূরার নম্বর দিয়ে: `1`\n"
        "• সূরার নাম লিখে: `Fatiha` অথবা `আল-বাকারা`",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# বোতামের কাজ হ্যান্ডেল করার ফাংশন
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "home":
        await query.edit_message_text(
            "📖 King Fahad Bangla Quran Bot\n\n"
            "আসসালামু আলাইকুম ওয়া রহমাতুল্লাহি ওয়া বারাকাতুহু।\n\n"
            "পবিত্র আল-কুরআন পড়ুন বাংলা উচ্চারণ ও অর্থসহ।",
            reply_markup=main_menu()
        )
        return

    if data == "search":
        await query.edit_message_text(
            "🔍 আপনি কোন সূরা বা আয়াত খুঁজছেন?\n\n"
            "চ্যাট বক্সে সরাসরি লিখে পাঠান:\n"
            "• `1 1` (সূরা ১, আয়াত ১)\n"
            "• `Baqarah` বা `আল-বাকারা`",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
        return

    if data.startswith("sp:"):
        page = int(data.split(":")[1])
        await query.edit_message_text(
            f"📚 পবিত্র আল-কুরআনের সূরা নির্বাচন করুন:\n\nপৃষ্ঠা {page+1} / 12",
            reply_markup=surah_keyboard(page)
        )
        return

    if data.startswith("s:"):
        surah = int(data.split(":")[1])
        if str(surah) not in QURAN:
            await query.edit_message_text("এই সূরার তথ্য ডাটাবেসে পাওয়া যায়নি।")
            return
        text = get_ayah_text(surah, 1)
        await query.edit_message_text(text, reply_markup=get_buttons(surah, 1))
        return

    if data.startswith("a:"):
        _, surah, ayah_no = data.split(":")
        surah = int(surah)
        ayah_no = int(ayah_no)
        try:
            text = get_ayah_text(surah, ayah_no)
            await query.edit_message_text(text, reply_markup=get_buttons(surah, ayah_no))
        except (KeyError, ValueError):
            await query.answer("এই আয়াতটি পাওয়া যায়নি।", show_alert=True)

# বট রান করার সেটআপ
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("surahs", surahs_command))
app.add_handler(CommandHandler("ayah", ayah))

app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, smart_message_handler))

print("✅ King Fahad Bangla Quran Bot Running")
app.run_polling()
