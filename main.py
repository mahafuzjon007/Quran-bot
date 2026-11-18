from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

# --- 1. Home Menu Handler ---
async def home_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "home":
        await query.edit_message_text(
            "📖 Bangla Quran Bot\n\n"
            "আসসালামু আলাইকুম ওয়া রহমাতুল্লাহি ওয়া বারাকাতুহু।\n\n"
            "পবিত্র আল-কুরআন পড়ুন বিশুদ্ধ আরবি তিলাওয়াত, বাংলা উচ্চারণ ও অর্থসহ।\n\n"
            "⚠️ বিশেষ দ্রষ্টব্য: বাংলা অক্ষর দিয়ে তেলাওয়াত শুদ্ধ হয় না, তাই 🔊 বাংলা অডিও শুনুন",
            reply_markup=main_menu() # Replace with your main menu markup function
        )
        return

# --- 2. Surah Selection Handler (Forward Order Buttons) ---
async def handle_surah_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data  # e.g., "surah_1"
    
    if data.startswith("surah_"):
        surah_number = int(data.split("_")[1])
        
        keyboard = []
        
        # Example: Define total ayahs per surah (adjust/expand based on your json data)
        # Surah 1 (Al-Fatihah) has 7 ayahs
        total_ayahs = 7 if surah_number == 1 else 5 
        
        # Loop forward from Ayah 1 to total_ayahs (fixes the backwards issue)
        for i in range(1, total_ayahs + 1):
            keyboard.append([
                InlineKeyboardButton(
                    f"🔊 Ayah {i} (তিলাওয়াত শুনুন)", 
                    callback_data=f"play_{surah_number}_{i}"
                )
            ])
            
        # Add a back button to return home
        keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="home")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"📖 Surah {surah_number}\n\n"
            "নিচের যেকোনো আয়াতের বোতামে স্পর্শ করে অডিও তেলাওয়াত শুনুন:",
            reply_markup=reply_markup
        )
        return

# --- 3. On-Demand Ayah Audio Playback Handler ---
async def handle_ayah_audio_play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer("অডিও লোড হচ্ছে...")
    
    data = query.data  # e.g., "play_1_1" (Surah 1, Ayah 1)
    
    if data.startswith("play_"):
        parts = data.split("_")
        surah_num = parts[1]
        ayah_num = parts[2]
        
        # Verified public audio URL for the specific Ayah (using Alafasy recitation API)
        audio_url = f"https://cdn.islamic.network/quran/audio/128/ar.alafasy/{ayah_num}.mp3"
        
        # Sends the audio file ONLY when the button is touched
        await context.bot.send_audio(
            chat_id=query.message.chat_id,
            audio=audio_url,
            caption=f"🎧 Surah {surah_num} - Ayah {ayah_num}\n⚠️ বাংলা উচ্চারণের পরিবর্তে এই খাঁটি অডিও শুনুন।"
        )
