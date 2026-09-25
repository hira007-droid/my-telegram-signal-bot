# texts.py
LANGUAGES = {"en": "English", "bn": "বাংলা"}

TEXT = {
    "en": {
        "choose_lang": "Choose your language / ভাষা বেছে নিন",
        "lang_set": "Language: English",
        "welcome": "Welcome! Choose a market option below:",
        "menu_signal": "📈 Real Market Signals (40 Strategies)",
        "menu_stats": "📊 My Statistics",
        "menu_lang": "🌐 Change Language",
        "menu_back": "🏠 Main Menu",
        "call": "UP (CALL)",
        "put": "DOWN (PUT)",
        "votes": "Votes",
        "up_word": "UP",
        "down_word": "DOWN",
        "confidence": "Confidence",
        "btn_win": "✅ Win",
        "btn_loss": "❌ Loss",
        "recorded_win": "✅ Recorded: WIN",
        "recorded_loss": "✅ Recorded: LOSS",
    },
    "bn": {
        "choose_lang": "Choose your language / ভাষা বেছে নিন",
        "lang_set": "ভাষা: বাংলা",
        "welcome": "স্বাগতম! নিচের অপশন থেকে যেকোনো একটি বেছে নিন:",
        "menu_signal": "📈 রিয়েল মার্কেট সিগন্যাল (৪০ স্ট্র্যাটেজি)",
        "menu_stats": "📊 আমার স্ট্যাটিস্টিক্স",
        "menu_lang": "🌐 ভাষা পরিবর্তন",
        "menu_back": "🏠 মূল মেনু",
        "call": "UP (CALL)",
        "put": "DOWN (PUT)",
        "votes": "ভোট",
        "up_word": "UP",
        "down_word": "DOWN",
        "confidence": "কনফিডেন্স",
        "btn_win": "✅ জিত",
        "btn_loss": "❌ হার",
        "recorded_win": "✅ সংরক্ষিত: জিত",
        "recorded_loss": "✅ সংরক্ষিত: হার",
    },
}

def tr(lang, key, **blanks):
    sentence = TEXT.get(lang, TEXT["en"]).get(key) or TEXT["en"][key]
    return sentence.format(**blanks) if blanks else sentence