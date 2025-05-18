import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import os
from keep_alive import keep_alive
keep_alive()

# Load Bot Token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    print("Error: BOT_TOKEN environment variable not set!")
    exit()

# Load Target Chat ID from environment variable
TARGET_CHAT_ID = os.environ.get('TARGET_CHAT_ID')
if not TARGET_CHAT_ID:
    print("Error: TARGET_CHAT_ID environment variable not set!")
    exit()

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to store book data
book_data = {}
book_categories = ['Academic', 'Competitive Exam', 'Novel', 'Other']

# Star emoji variables
STAR_EMOJI = "⭐"
EMPTY_STAR_EMOJI = "☆"


# --- Start command handler ---
@bot.message_handler(commands=['start'])
def start(message):
    """Initiates the book listing process with a greeting message and instructions."""
    book_data['seller_id'] = message.from_user.id
    book_data['seller_username'] = message.from_user.username

    # Greeting message with instructions
    greeting_message = f"""
    👋 **Hello {message.from_user.first_name}!** 👋
    **Welcome to Miblio, **

    I'm here to help you list your books. Please follow these instructions:

    1. **Upload a clear cover photo of your book.**
    2. **Provide accurate details about the book (title, author, category, etc.).**
    3. **Be honest about the book's condition.**
    4. **Set a reasonable selling price.**
    5. **Confirm your details before submitting.**

    Let's get started!
    """
    bot.send_message(message.chat.id, greeting_message, parse_mode='Markdown')

    # Proceed with listing process
    bot.send_message(message.chat.id, "Please upload the cover photo of your book:")
    bot.register_next_step_handler(message, process_cover_photo)


# --- Cover Photo ---
def process_cover_photo(message):
    """Handles the cover photo upload."""
    if message.content_type == 'photo':
        book_data['cover_photo'] = message.photo[-1].file_id
        bot.send_message(message.chat.id, "Enter the title of the book:")
        bot.register_next_step_handler(message, process_title)
    else:
        bot.reply_to(message, "Please upload a photo of the book cover.")
        bot.register_next_step_handler(message, process_cover_photo)


# --- Title ---
def process_title(message):
    """Handles the book title input."""
    book_data['title'] = message.text
    bot.send_message(message.chat.id, "Enter the author/publication of the book:")
    bot.register_next_step_handler(message, process_author)


# --- Author ---
def process_author(message):
    """Handles the book author/publication input."""
    book_data['author'] = message.text
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    for category in book_categories:
        markup.add(KeyboardButton(category))
    bot.send_message(message.chat.id, "Select the category of the book:", reply_markup=markup)
    bot.register_next_step_handler(message, process_category)


# --- Category ---
def process_category(message):
    """Handles the category selection and asks for condition or examination name or institution name or details for 'Other'."""
    book_data['category'] = message.text
    if message.text == 'Competitive Exam':
        bot.send_message(message.chat.id, "Enter Examination Name:")
        bot.register_next_step_handler(message, process_exam_name)
    elif message.text == 'Academic':
        bot.send_message(message.chat.id, "Enter School/College/University Name:")
        bot.register_next_step_handler(message, process_institution_name)
    elif message.text == 'Other':  # Check for 'Other' category
        bot.send_message(message.chat.id, "Write some details about the book:")
        bot.register_next_step_handler(message, process_other_details)  # New function call
    else:
        # Create keyboard markup with star rating buttons (for other categories)
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=5)
        for i in range(1, 6):
            markup.add(KeyboardButton(STAR_EMOJI * i + EMPTY_STAR_EMOJI * (5 - i)))
        bot.send_message(message.chat.id, "Rate the book's condition (1-5 stars):", reply_markup=markup)
        bot.register_next_step_handler(message, process_star_rating)


# --- Institution Name (for Academic) ---
def process_institution_name(message):
    """Handles the institution name input for 'Academic' category and asks for condition."""
    book_data['institution_name'] = message.text
    # Create keyboard markup with star rating buttons
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=5)
    for i in range(1, 6):
        markup.add(KeyboardButton(STAR_EMOJI * i + EMPTY_STAR_EMOJI * (5 - i)))
    bot.send_message(message.chat.id, "Rate the book's condition (1-5 stars):", reply_markup=markup)
    bot.register_next_step_handler(message, process_star_rating)


# --- Exam Name (for Competitive Exam) ---
def process_exam_name(message):
    """Handles the examination name input for 'Competitive Exam' category and asks for condition."""
    book_data['exam_name'] = message.text
    # Create keyboard markup with star rating buttons
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=5)
    for i in range(1, 6):
        markup.add(KeyboardButton(STAR_EMOJI * i + EMPTY_STAR_EMOJI * (5 - i)))
    bot.send_message(message.chat.id, "Rate the book's condition (1-5 stars):", reply_markup=markup)
    bot.register_next_step_handler(message, process_star_rating)


# --- Other Details (for 'Other' category) ---
def process_other_details(message):
    """Handles the details input for 'Other' category and asks for condition."""
    book_data['other_details'] = message.text  # Store the details
    # Create keyboard markup with star rating buttons
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, row_width=5)
    for i in range(1, 6):
        markup.add(KeyboardButton(STAR_EMOJI * i + EMPTY_STAR_EMOJI * (5 - i)))
    bot.send_message(message.chat.id, "Rate the book's condition (1-5 stars):", reply_markup=markup)
    bot.register_next_step_handler(message, process_star_rating)


# --- Star Rating (Condition) ---
def process_star_rating(message):
    """Handles the book condition input (star rating)."""
    book_data['condition'] = message.text
    bot.send_message(message.chat.id, "Enter your location (e.g., City, State):")
    bot.register_next_step_handler(message, process_location)


# --- Location ---
def process_location(message):
    """Handles the location input."""
    book_data['location'] = message.text
    bot.send_message(message.chat.id, "Enter the selling price (in
