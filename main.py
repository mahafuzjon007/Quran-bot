import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# Enable logging to track activity and debug easily in the console
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Main Menu Markup ---
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📖 All Surahs / সকল সুরা", callback_data="all_surahs")]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- 1. Start Command & Home Menu Handler ---
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "📖 Bangla Quran Bot\n\n"
        "আসসালামু আলাইকুম ওয়া রহমাতুল্লাহি ওয়া বারাকাতুহু।\n\n"
        "পবিত্র আল-কুরআন পড়ুন বিশুদ্ধ আরবি তিলাওয়াত, বাংলা উচ্চারণ ও অর্থসহ।\n\n"
        "⚠️ বিশেষ দ্রষ্টব্য: বাংলা অক্ষর দিয়ে তেলাওয়াত শুদ্ধ হয় না, তাই 🔊 বাংলা অডিও শুনুন"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=main_menu())
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(welcome_text, reply_markup=main_menu())

# --- 2. Surah Menu Button Handler ---
async def all_surahs_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "all_surahs" or query.data == "home":
        keyboard = [
            [InlineKeyboardButton("1. Al-Fatihah (আল-ফাতিহা)", callback_data="surah_1")],
            [InlineKeyboardButton("🔙 Back / পেছনে", callback_data="home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📖 পবিত্র আল-কুরআনের সুরা নির্বাচন করুন:",
            reply_markup=reply_markup
        )

# --- 3. Surah Selection Handler (Forward Order Buttons) ---
async def handle_surah_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data  # e.g., "surah_1"
    
    if data.startswith("surah_"):
        surah_number = int(data.split("_")[1])
        
        keyboard = []
        # Surah 1 (Al-Fatihah) has 7 ayahs; adjust for other surahs as needed
        total_ayahs = 7 if surah_number == 1 else 5 
        
        # Loop forward from Ayah 1 to total_ayahs (fixes the backwards issue)
        for i in range(1, total_ayahs + 1):
            keyboard.append([
                InlineKeyboardButton(
                    f"🔊 Ayah {i} (তিলাওয়াত শুনুন)", 
                    callback_data=f"play_{surah_number}_{i}"
                )
            ])
            
        # Add a back button to return to the surah list
        keyboard.append([InlineKeyboardButton("🔙 Back to Surahs", callback_data="all_surahs")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📖 Surah {surah_number}\n\n"
            "নিচের যেকোনো আয়াতের বোতামে স্পর্শ করে অডিও তেলাওয়াত শুনুন:",
            reply_markup=reply_markup
        )

# --- 4. On-Demand Ayah Audio Playback Handler ---
async def handle_ayah_audio_play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("অডিও লোড হচ্ছে...")
    
    data = query.data  # e.g., "play_1_1"
    
    if data.startswith("play_"):
        parts = data.split("_")
        surah_num = parts[1]
        ayah_num = parts[2]
        
        # Public audio URL for the specific Ayah (Alafasy recitation)
        audio_url = f"https://cdn.islamic.network/quran/audio/128/ar.alafasy/{ayah_num}.mp3"
        
        # Sends audio ONLY when the user clicks the specific button
        await context.bot.send_audio(
            chat_id=query.message.chat_id,
            audio=audio_url,
            caption=f"🎧 Surah {surah_num} - Ayah {ayah_num}\n⚠️ বাংলা উচ্চারণের পরিবর্তে এই খাঁটি অডিও শুনুন।"
        )

# --- 5. Main Application Entry Point ---
def main():
    # Safely loads your hidden token from the hosting panel's Environment Variables
    TOKEN = os.getenv("BOT_TOKEN")
    
    if not TOKEN:
        raise ValueError("No BOT_TOKEN found in environment variables! Please set your bot token in your hosting panel configuration.")
    
    application = Application.builder().token(TOKEN).build()
    
    # Register all handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CallbackQueryHandler(start_handler, pattern="^home$"))
    application.add_handler(CallbackQueryHandler(all_surahs_menu, pattern="^all_surahs$"))
    application.add_handler(CallbackQueryHandler(handle_surah_selection, pattern="^surah_"))
    application.add_handler(CallbackQueryHandler(handle_ayah_audio_play, pattern="^play_"))
    
    print("Bot is starting up and polling for updates...")
    application.run_polling()

if __name__ == "__main__":
    main()
