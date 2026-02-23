import telebot
import sqlite3
import time
import random
import json
from telebot import types
from datetime import datetime

TOKEN = '8175699315:AAH3jqml9GYgdB3HCHN7HPd97ZUD7jxDW7o'
bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

# ----- ИНИЦИАЛИЗАЦИЯ БД -----
def init_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        full_name TEXT DEFAULT 'Не указано',
        balance INTEGER DEFAULT 10000,
        bank INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        exp INTEGER DEFAULT 0,
        passport INTEGER DEFAULT 0,
        health INTEGER DEFAULT 100,
        hunger INTEGER DEFAULT 100,
        job_id INTEGER DEFAULT NULL,
        car_id INTEGER DEFAULT NULL,
        married_to INTEGER DEFAULT NULL,
        last_work_time INTEGER DEFAULT 0,
        last_walk_time INTEGER DEFAULT 0,
        last_interest INTEGER DEFAULT 0,
        house_id INTEGER DEFAULT NULL,
        army_status INTEGER DEFAULT 0,
        school_id INTEGER DEFAULT NULL,
        class_level INTEGER DEFAULT NULL,
        university_id INTEGER DEFAULT NULL,
        crypto_balance INTEGER DEFAULT 0,
        telegram_username TEXT DEFAULT NULL,
        age INTEGER DEFAULT 1,
        last_active INTEGER DEFAULT 0,
        location TEXT DEFAULT 'moscow',
        hygiene INTEGER DEFAULT 100,
        energy INTEGER DEFAULT 100,
        service_car_id INTEGER DEFAULT NULL,
        last_shot REAL DEFAULT 0
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        min_level INTEGER,
        need_passport INTEGER DEFAULT 0,
        salary INTEGER,
        exp_reward INTEGER,
        police INTEGER DEFAULT 0
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT,
        model TEXT,
        price INTEGER,
        fuel_consumption REAL,
        tuning_level INTEGER DEFAULT 0,
        fuel REAL DEFAULT 50,
        type TEXT DEFAULT 'car'
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS houses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id INTEGER UNIQUE,
        type TEXT,
        price INTEGER,
        garage_capacity INTEGER DEFAULT 1
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS schools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        type TEXT,
        min_age INTEGER,
        max_age INTEGER,
        cost_per_day INTEGER,
        exp_per_day INTEGER
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        contact_username TEXT,
        contact_name TEXT,
        contact_user_id INTEGER
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS calls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        caller_id INTEGER,
        receiver_id INTEGER,
        start_time INTEGER,
        active INTEGER DEFAULT 1
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS licenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        issued_date INTEGER
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        brand TEXT,
        price INTEGER,
        description TEXT,
        stats TEXT,
        required_level INTEGER DEFAULT 1,
        required_passport INTEGER DEFAULT 0
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_id INTEGER,
        quantity INTEGER DEFAULT 0,
        equipped INTEGER DEFAULT 0
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS equipped (
        user_id INTEGER PRIMARY KEY,
        weapon_id INTEGER,
        armor_id INTEGER,
        accessory_ids TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS marketplace_listings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seller_id INTEGER,
        item_id INTEGER,
        quantity INTEGER,
        price_per_unit INTEGER,
        marketplace TEXT,
        active INTEGER DEFAULT 1,
        created_at INTEGER
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS prison (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        arrested_by INTEGER,
        reason TEXT,
        release_time INTEGER
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS wanted (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        issued_by INTEGER,
        reason TEXT,
        issued_at INTEGER
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS handcuffs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        cuffed_by INTEGER,
        cuffed_at INTEGER
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS government (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        position TEXT UNIQUE,
        user_id INTEGER,
        username TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_job_progress (
        user_id INTEGER,
        job_id INTEGER,
        exp INTEGER DEFAULT 0,
        rank INTEGER DEFAULT 1,
        PRIMARY KEY (user_id, job_id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS effects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        effect_type TEXT,
        value INTEGER,
        expires_at INTEGER
    )''')
    conn.commit()
init_db()

# ----- НАЧАЛЬНЫЕ ДАННЫЕ -----
def populate_jobs():
    cursor.execute("SELECT COUNT(*) FROM jobs")
    if cursor.fetchone()[0] == 0:
        jobs = [
            ("Грузчик", "Таскать мешки", 1,0,500,10,0),
            ("Курьер", "Развозить заказы",2,0,800,15,0),
            ("Продавец", "Работа в магазине",3,0,1000,20,0),
            ("Водитель такси", "Нужны права",5,1,1500,25,0),
            ("Программист", "Писать код",10,1,3000,50,0),
            ("Врач", "Лечить людей",15,1,4000,60,0),
            ("Полицейский", "Охранять порядок",20,1,5000,75,1),
            ("Пожарный", "Тушить пожары",15,1,4500,70,0),
            ("Военный", "Служить в армии",25,1,6000,90,0),
            ("Учитель", "Обучать детей",18,1,3500,50,0),
            ("ОМОН", "Спецподразделение",30,1,8000,120,1),
            ("Бизнесмен", "Управлять компанией",30,1,10000,100,0)
        ]
        for j in jobs:
            cursor.execute("INSERT INTO jobs (name,description,min_level,need_passport,salary,exp_reward,police) VALUES (?,?,?,?,?,?,?)", j)
        conn.commit()
populate_jobs()

def populate_cars():
    cursor.execute("SELECT COUNT(*) FROM cars")
    if cursor.fetchone()[0] == 0:
        cars = [
            ('Lada','Granta',800000,7.0,'car'),
            ('BMW','M5 F90',9500000,12.5,'car'),
            ('Yamaha','R6',800000,5.0,'motorcycle'),
            ('Stels','Navigator',15000,0.0,'bicycle')
        ]
        for c in cars:
            cursor.execute("INSERT INTO cars (brand,model,price,fuel_consumption,type) VALUES (?,?,?,?,?)", c)
        conn.commit()
populate_cars()

def populate_schools():
    cursor.execute("SELECT COUNT(*) FROM schools")
    if cursor.fetchone()[0] == 0:
        schools = [
            ("Школа №1","school",7,17,200,10),
            ("Московский университет","university",18,25,500,20)
        ]
        for s in schools:
            cursor.execute("INSERT INTO schools (name,type,min_age,max_age,cost_per_day,exp_per_day) VALUES (?,?,?,?,?,?)", s)
        conn.commit()
populate_schools()

def populate_items():
    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        items = [
            ("Хлеб","food",None,50,"Булка хлеба",None,1,0),
            ("Пистолет Макарова","weapon",None,50000,"Стандартный пистолет",json.dumps({"damage":2,"fire_rate":3,"max_ammo":8,"silent":False}),14,1),
            ("Автомат Калашникова","weapon",None,150000,"Автомат",json.dumps({"damage":5,"fire_rate":0,"max_ammo":30,"silent":False}),18,1),
            ("Бронежилет","armor",None,50000,"Защита +100 HP",json.dumps({"armor":100}),14,0),
            ("Патроны 9мм","ammo",None,100,"Патроны для пистолета",None,1,0),
            ("Розы","flower",None,500,"Букет цветов",None,1,0),
            ("Сигареты Marlboro","cigarette",None,200,"Пачка сигарет",None,18,1),
            ("Презервативы","condom",None,150,"Средство контрацепции",None,18,0),
            ("iPhone 16","electronics",None,90000,"Смартфон",None,1,0),
            ("Диван","home",None,30000,"Удобный диван",None,1,0),
            ("Кокаин","drug",None,5000,"Порошок",json.dumps({"effect":"high","duration":3600}),18,0),
            ("Виски","alcohol",None,2000,"Бутылка",json.dumps({"effect":"drunk","duration":1800}),18,1),
            ("Глушитель","accessory",None,20000,"Делает оружие бесшумным",json.dumps({"silent":True}),14,0),
            ("Футболка Nike","clothes","Nike",2000,"Спортивная футболка",None,1,0)
        ]
        for i in items:
            cursor.execute("INSERT INTO items (name,category,brand,price,description,stats,required_level,required_passport) VALUES (?,?,?,?,?,?,?,?)", i)
        conn.commit()
populate_items()

# Президент
cursor.execute("INSERT OR IGNORE INTO government (position,user_id,username) VALUES ('president',0,'@KYNIKS')")
conn.commit()

# ----- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ -----
def check_restrictions(user_id):
    prison = cursor.execute('SELECT release_time FROM prison WHERE user_id=?', (user_id,)).fetchone()
    if prison and prison[0] > time.time():
        return f"⛔ Вы в тюрьме! Освобождение через {(prison[0]-time.time())//60} мин."
    if cursor.execute('SELECT 1 FROM handcuffs WHERE user_id=?', (user_id,)).fetchone():
        return "🔗 На вас надеты наручники!"
    return None

def update_activity(user_id):
    now = int(time.time())
    u = cursor.execute('SELECT last_active, age FROM users WHERE user_id=?', (user_id,)).fetchone()
    if u and u[0] and u[0] != 0:  # исправлено: проверяем, что last_active не 0
        hours = (now - u[0]) // 3600
        if hours > 0:
            cursor.execute('UPDATE users SET last_active=?, age=? WHERE user_id=?', (now, u[1]+hours*5, user_id))
        else:
            cursor.execute('UPDATE users SET last_active=? WHERE user_id=?', (now, user_id))
    else:
        cursor.execute('UPDATE users SET last_active=? WHERE user_id=?', (now, user_id))
    conn.commit()

def is_police(user_id):
    job = cursor.execute('SELECT job_id FROM users WHERE user_id=?', (user_id,)).fetchone()
    if job and job[0]:
        pol = cursor.execute('SELECT police FROM jobs WHERE id=?', (job[0],)).fetchone()
        return pol and pol[0] == 1
    return False

def add_job_exp(user_id, job_id, exp):
    p = cursor.execute('SELECT exp,rank FROM user_job_progress WHERE user_id=? AND job_id=?', (user_id, job_id)).fetchone()
    if not p:
        cursor.execute('INSERT INTO user_job_progress (user_id,job_id,exp,rank) VALUES (?,?,?,1)', (user_id, job_id, exp))
    else:
        cursor.execute('UPDATE user_job_progress SET exp = exp + ? WHERE user_id=? AND job_id=?', (exp, user_id, job_id))
    conn.commit()

def check_level_up(user_id):
    user = cursor.execute('SELECT level, exp FROM users WHERE user_id=?', (user_id,)).fetchone()
    if user:
        level, exp = user
        if exp >= level * 100:
            cursor.execute('UPDATE users SET level = level + 1, exp = exp - ? WHERE user_id=?', (level*100, user_id))
            conn.commit()
            bot.send_message(user_id, f"🎉 Поздравляем! Вы достигли {level+1} уровня!")

# ----- ГЛАВНОЕ МЕНЮ -----
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('👤 Профиль', '💼 Работа', '🚖 Такси')
    markup.add('🚗 Машина', '🏠 Дом', '🏛️ Мэрия')
    markup.add('🎰 Казино', '🚶 Гулять', '🏫 Школа')
    markup.add('📱 Телефон', '⚔️ Военкомат', '🏦 Банк')
    markup.add('🛒 Магазин', '📄 Паспорт', '🍔 Еда', '🏥 Больница')
    markup.add('👕 Одежда', '📦 Kyvito', '💀 Kydark', '🎒 Инвентарь')
    markup.add('Москва')
    return markup

# ----- СТАРТ -----
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    cursor.execute('UPDATE users SET telegram_username=? WHERE user_id=?', (username, user_id))
    user = cursor.execute('SELECT full_name FROM users WHERE user_id=?', (user_id,)).fetchone()
    if user and user[0] != 'Не указано':
        update_activity(user_id)
        bot.send_message(message.chat.id, f"С возвращением в Москву, {user[0]}!", reply_markup=main_menu())
    else:
        cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
        conn.commit()
        bot.send_message(message.chat.id, "Добро пожаловать! Введите ваше ФИО:")
        bot.register_next_step_handler(message, set_full_name)

def set_full_name(message):
    user_id = message.from_user.id
    name = message.text.strip()
    if len(name) < 3:
        bot.send_message(message.chat.id, "Слишком короткое имя. Попробуйте ещё раз:")
        bot.register_next_step_handler(message, set_full_name)
        return
    cursor.execute('UPDATE users SET full_name=? WHERE user_id=?', (name, user_id))
    conn.commit()
    update_activity(user_id)
    bot.send_message(message.chat.id, f"Приятно познакомиться, {name}!", reply_markup=main_menu())

# ----- ПРОФИЛЬ -----
@bot.message_handler(func=lambda m: m.text == '👤 Профиль')
def profile(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    u = cursor.execute('''SELECT full_name,balance,bank,level,exp,passport,health,hunger,
        job_id,car_id,married_to,house_id,army_status,school_id,class_level,
        university_id,crypto_balance,age,hygiene,energy,location FROM users WHERE user_id=?''', (user_id,)).fetchone()
    if not u:
        return
    (name,bal,bank,lev,exp,passp,hp,hunger,job_id,car_id,married,house_id,
     army,sch_id,cls,uni_id,crypto,age,hygiene,energy,loc) = u

    job = "Безработный"
    if job_id:
        j = cursor.execute('SELECT name FROM jobs WHERE id=?', (job_id,)).fetchone()
        if j: job = j[0]
    car = "Нет"
    if car_id:
        c = cursor.execute('SELECT brand,model FROM cars WHERE id=?', (car_id,)).fetchone()
        if c: car = f"{c[0]} {c[1]}"
    house = "Нет"
    if house_id:
        h = cursor.execute('SELECT type FROM houses WHERE id=?', (house_id,)).fetchone()
        if h: house = h[0]
    spouse = f"ID {married}" if married else "Нет"
    army_stat = ["Не служил","В армии","Отслужил"][army]
    edu = "Нет"
    if sch_id:
        s = cursor.execute('SELECT name FROM schools WHERE id=?', (sch_id,)).fetchone()
        if s: edu = f"{s[0]}, {cls} класс"
    elif uni_id:
        uu = cursor.execute('SELECT name FROM schools WHERE id=?', (uni_id,)).fetchone()
        if uu: edu = f"{uu[0]}, студент"

    text = (f"👤 {name}\n💰 Наличные: {bal} ₽\n🏦 Банк: {bank} ₽\n📊 Уровень: {lev} (опыт: {exp}/{lev*100})\n"
            f"🆔 Паспорт: {'✅' if passp else '❌'}\n❤️ Здоровье: {hp}%\n🍔 Голод: {hunger}%\n"
            f"💼 Работа: {job}\n🚗 Машина: {car}\n🏠 Дом: {house}\n💍 Супруг: {spouse}\n"
            f"⚔️ Армия: {army_stat}\n📚 Образование: {edu}\n💰 Крипта: {crypto} BTC\n"
            f"📊 Возраст: {age} лет\n🧼 Гигиена: {hygiene}%\n⚡ Энергия: {energy}%\n📍 Локация: {loc}")
    bot.send_message(message.chat.id, text)

# ----- ПАСПОРТ -----
@bot.message_handler(func=lambda m: m.text == '📄 Паспорт')
def passport_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    age = cursor.execute('SELECT age FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if age < 14:
        bot.send_message(message.chat.id, "Паспорт можно получить только с 14 лет.")
        return
    if cursor.execute('SELECT passport FROM users WHERE user_id=?', (user_id,)).fetchone()[0]:
        bot.send_message(message.chat.id, "У вас уже есть паспорт.")
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💰 Получить (1000₽)", callback_data="buy_passport"))
    bot.send_message(message.chat.id, "Стоимость оформления: 1000₽", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'buy_passport')
def buy_passport(call):
    user_id = call.from_user.id
    bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if bal < 1000:
        bot.answer_callback_query(call.id, "Недостаточно средств!")
        return
    cursor.execute('UPDATE users SET balance = balance - 1000, passport = 1 WHERE user_id=?', (user_id,))
    conn.commit()
    bot.edit_message_text("✅ Паспорт получен!", call.message.chat.id, call.message.message_id)

# ----- БАНК -----
@bot.message_handler(func=lambda m: m.text == '🏦 Банк')
def bank_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Положить", callback_data="bank_deposit"))
    markup.add(types.InlineKeyboardButton("Снять", callback_data="bank_withdraw"))
    markup.add(types.InlineKeyboardButton("Баланс", callback_data="bank_balance"))
    markup.add(types.InlineKeyboardButton("Проценты", callback_data="bank_interest"))
    bot.send_message(message.chat.id, "Банк:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('bank_'))
def bank_handler(call):
    user_id = call.from_user.id
    action = call.data.split('_')[1]
    if action == "balance":
        bank = cursor.execute('SELECT bank FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        bot.answer_callback_query(call.id, f"На счету: {bank} ₽")
    elif action == "deposit":
        bot.send_message(call.message.chat.id, "Введите сумму:")
        bot.register_next_step_handler(call.message, process_deposit)
    elif action == "withdraw":
        bot.send_message(call.message.chat.id, "Введите сумму:")
        bot.register_next_step_handler(call.message, process_withdraw)
    elif action == "interest":
        bank, last = cursor.execute('SELECT bank, last_interest FROM users WHERE user_id=?', (user_id,)).fetchone()
        today = datetime.now().date()
        if last:
            last_date = datetime.fromtimestamp(last).date()
        else:
            last_date = None
        if last_date != today:
            interest = bank // 100
            cursor.execute('UPDATE users SET bank = bank + ?, last_interest = ? WHERE user_id=?', (interest, int(time.time()), user_id))
            conn.commit()
            bot.send_message(call.message.chat.id, f"📈 Начислено процентов: +{interest} ₽")
        else:
            bot.send_message(call.message.chat.id, "Вы уже получали проценты сегодня.")

def process_deposit(message):
    try:
        am = int(message.text)
        if am <= 0: raise ValueError
        user_id = message.from_user.id
        bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        if bal < am:
            bot.send_message(message.chat.id, "Недостаточно наличных!")
            return
        cursor.execute('UPDATE users SET balance = balance - ?, bank = bank + ? WHERE user_id=?', (am, am, user_id))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Внесено {am} ₽")
    except:
        bot.send_message(message.chat.id, "Ошибка ввода.")

def process_withdraw(message):
    try:
        am = int(message.text)
        if am <= 0: raise ValueError
        user_id = message.from_user.id
        bank = cursor.execute('SELECT bank FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        if bank < am:
            bot.send_message(message.chat.id, "Недостаточно на счету!")
            return
        cursor.execute('UPDATE users SET bank = bank - ?, balance = balance + ? WHERE user_id=?', (am, am, user_id))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Снято {am} ₽")
    except:
        bot.send_message(message.chat.id, "Ошибка ввода.")

# ----- ЕДА -----
@bot.message_handler(func=lambda m: m.text == '🍔 Еда')
def food_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Пицца (200₽, +30)", callback_data="food_pizza"))
    markup.add(types.InlineKeyboardButton("Бургер (150₽, +25)", callback_data="food_burger"))
    markup.add(types.InlineKeyboardButton("Салат (100₽, +20)", callback_data="food_salad"))
    bot.send_message(message.chat.id, "Выберите еду:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('food_'))
def buy_food(call):
    food = call.data.split('_')[1]
    prices = {"pizza": (200,30), "burger": (150,25), "salad": (100,20)}
    if food not in prices:
        return
    cost, gain = prices[food]
    user_id = call.from_user.id
    bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if bal < cost:
        bot.answer_callback_query(call.id, "Недостаточно денег!")
        return
    cursor.execute('UPDATE users SET balance = balance - ?, hunger = MIN(100, hunger + ?) WHERE user_id=?', (cost, gain, user_id))
    conn.commit()
    bot.edit_message_text(f"✅ Вы поели. Голод +{gain}.", call.message.chat.id, call.message.message_id)

# ----- БОЛЬНИЦА -----
@bot.message_handler(func=lambda m: m.text == '🏥 Больница')
def hospital_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💊 Лечение (500₽, +50)", callback_data="hospital_treat"))
    bot.send_message(message.chat.id, "Больница:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'hospital_treat')
def treat(call):
    user_id = call.from_user.id
    bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if bal < 500:
        bot.answer_callback_query(call.id, "Недостаточно денег!")
        return
    cursor.execute('UPDATE users SET balance = balance - 500, health = MIN(100, health + 50) WHERE user_id=?', (user_id,))
    conn.commit()
    bot.edit_message_text("✅ Лечение завершено.", call.message.chat.id, call.message.message_id)

# ----- РАБОТА -----
@bot.message_handler(func=lambda m: m.text == '💼 Работа')
def work_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    u = cursor.execute('SELECT level, passport, job_id, last_work_time, army_status FROM users WHERE user_id=?', (user_id,)).fetchone()
    if not u: return
    level, passport, cur_job, last_work, army = u
    if army == 1:
        bot.send_message(message.chat.id, "Вы в армии, нельзя работать.")
        return
    jobs = cursor.execute('SELECT id, name, description, salary, exp_reward FROM jobs WHERE min_level <= ?', (level,)).fetchall()
    available = []
    for j in jobs:
        jid, name, desc, sal, exp = j
        need_pass = cursor.execute('SELECT need_passport FROM jobs WHERE id=?', (jid,)).fetchone()[0]
        if need_pass and not passport:
            continue
        if name == 'ОМОН' and army != 2:
            continue
        available.append(j)
    if not available:
        bot.send_message(message.chat.id, "Нет доступных работ.")
        return
    markup = types.InlineKeyboardMarkup()
    for j in available:
        jid, name, desc, sal, exp = j
        markup.add(types.InlineKeyboardButton(f"{name} (💰{sal}₽, ✨{exp} exp)", callback_data=f"job_{jid}"))
    if cur_job:
        markup.add(types.InlineKeyboardButton("📋 Моя работа", callback_data="my_job"))
    markup.add(types.InlineKeyboardButton("🔨 Работать сейчас", callback_data="work_now"))
    bot.send_message(message.chat.id, "Выберите профессию:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('job_'))
def set_job(call):
    jid = int(call.data.split('_')[1])
    user_id = call.from_user.id
    job = cursor.execute('SELECT min_level, need_passport FROM jobs WHERE id=?', (jid,)).fetchone()
    if not job:
        bot.answer_callback_query(call.id, "Ошибка")
        return
    min_lvl, need_pass = job
    u = cursor.execute('SELECT level, passport FROM users WHERE user_id=?', (user_id,)).fetchone()
    if u[0] < min_lvl or (need_pass and not u[1]):
        bot.answer_callback_query(call.id, "Эта работа вам недоступна!")
        return
    # Если была полицейская работа, убираем служебную машину
    old_job = cursor.execute('SELECT job_id FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if old_job:
        old_pol = cursor.execute('SELECT police FROM jobs WHERE id=?', (old_job,)).fetchone()
        if old_pol and old_pol[0] == 1:
            # Убираем служебную машину
            cursor.execute('UPDATE users SET car_id = NULL, service_car_id = NULL WHERE user_id=? AND service_car_id IS NOT NULL', (user_id,))
    cursor.execute('UPDATE users SET job_id=? WHERE user_id=?', (jid, user_id))
    # Если новая работа полицейская и нет своей машины, выдаём служебную
    new_pol = cursor.execute('SELECT police FROM jobs WHERE id=?', (jid,)).fetchone()[0]
    if new_pol == 1:
        if not cursor.execute('SELECT car_id FROM users WHERE user_id=?', (user_id,)).fetchone()[0]:
            # Берём первую машину из списка как служебную (можно задать конкретную)
            service_car = cursor.execute('SELECT id FROM cars WHERE type="car" LIMIT 1').fetchone()
            if service_car:
                cursor.execute('UPDATE users SET car_id=?, service_car_id=? WHERE user_id=?', (service_car[0], service_car[0], user_id))
    conn.commit()
    bot.answer_callback_query(call.id, "Профессия установлена!")
    bot.edit_message_text("✅ Профессия выбрана.", call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'my_job')
def my_job(call):
    user_id = call.from_user.id
    u = cursor.execute('SELECT job_id, last_work_time FROM users WHERE user_id=?', (user_id,)).fetchone()
    if not u or not u[0]:
        bot.answer_callback_query(call.id, "У вас нет работы!")
        return
    jid, last = u
    job = cursor.execute('SELECT name, description, salary, exp_reward FROM jobs WHERE id=?', (jid,)).fetchone()
    if not job: return
    name, desc, sal, exp = job
    now = time.time()
    if last and now - last < 3600:
        next_t = datetime.fromtimestamp(last+3600).strftime("%H:%M")
        status = f"⏳ Следующая смена после {next_t}"
    else:
        status = "✅ Можно работать"
    text = f"📋 {name}\n{desc}\n💰 Зарплата: {sal} ₽\n✨ Опыт: {exp}\n{status}"
    bot.send_message(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda call: call.data == 'work_now')
def work_now(call):
    user_id = call.from_user.id
    u = cursor.execute('SELECT job_id, last_work_time, health, hunger, army_status FROM users WHERE user_id=?', (user_id,)).fetchone()
    if not u or not u[0]:
        bot.answer_callback_query(call.id, "Сначала выберите профессию!")
        return
    jid, last, health, hunger, army = u
    if army == 1:
        bot.send_message(call.message.chat.id, "Вы в армии.")
        return
    now = time.time()
    if last and now - last < 3600:
        bot.answer_callback_query(call.id, f"Подождите {int(3600-(now-last))//60} мин.")
        return
    if health < 20 or hunger < 20:
        bot.send_message(call.message.chat.id, "Вы слишком больны или голодны!")
        return
    job = cursor.execute('SELECT salary, exp_reward FROM jobs WHERE id=?', (jid,)).fetchone()
    if not job: return
    sal, exp = job
    new_h = max(0, health - random.randint(5,15))
    new_hu = max(0, hunger - random.randint(10,20))
    cursor.execute('UPDATE users SET balance = balance + ?, exp = exp + ?, last_work_time = ?, health = ?, hunger = ? WHERE user_id=?',
                   (sal, exp, int(now), new_h, new_hu, user_id))
    conn.commit()
    add_job_exp(user_id, jid, exp)
    check_level_up(user_id)
    bot.send_message(call.message.chat.id, f"✅ Вы отработали!\n💰 +{sal} ₽\n✨ +{exp} exp\n❤️ {new_h}\n🍔 {new_hu}")

# ----- ТАКСИ -----
@bot.message_handler(func=lambda m: m.text == '🚖 Такси')
def taxi(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    car_id = cursor.execute('SELECT car_id FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if not car_id:
        bot.send_message(message.chat.id, "У вас нет машины!")
        return
    car = cursor.execute('SELECT fuel, fuel_consumption, tuning_level, type FROM cars WHERE id=?', (car_id,)).fetchone()
    if not car: return
    fuel, cons, tune, ctype = car
    if ctype == 'bicycle':
        income = 100 + tune*20
        cursor.execute('UPDATE users SET balance = balance + ?, exp = exp + 2 WHERE user_id=?', (income, user_id))
        conn.commit()
        check_level_up(user_id)
        bot.send_message(message.chat.id, f"✅ Поездка на велосипеде: +{income} ₽, +2 exp")
        return
    if fuel <= cons*0.1:
        bot.send_message(message.chat.id, "⚠️ Мало топлива!")
        return
    income = 500 + tune*100
    cursor.execute('UPDATE cars SET fuel = fuel - ? WHERE id=?', (cons, car_id))
    cursor.execute('UPDATE users SET balance = balance + ?, exp = exp + 5 WHERE user_id=?', (income, user_id))
    conn.commit()
    check_level_up(user_id)
    bot.send_message(message.chat.id, f"✅ Поездка выполнена! +{income} ₽, +5 exp")

# ----- МАШИНА -----
@bot.message_handler(func=lambda m: m.text == '🚗 Машина')
def car_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Купить", callback_data="buy_car"))
    markup.add(types.InlineKeyboardButton("Моя машина", callback_data="my_car"))
    markup.add(types.InlineKeyboardButton("Заправить", callback_data="fuel_car"))
    markup.add(types.InlineKeyboardButton("Тюнинг", callback_data="tune_car"))
    bot.send_message(message.chat.id, "Управление автомобилем:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'buy_car')
def show_cars(call):
    cars = cursor.execute('SELECT id, brand, model, price, type FROM cars').fetchall()
    text = "Доступные ТС:\n"
    for c in cars:
        text += f"{c[0]}. {c[1]} {c[2]} ({c[4]}) — {c[3]} ₽\n"
    bot.send_message(call.message.chat.id, text + "Введите ID:")
    bot.register_next_step_handler(call.message, process_buy_car)

def process_buy_car(message):
    try:
        cid = int(message.text)
        user_id = message.from_user.id
        car = cursor.execute('SELECT price FROM cars WHERE id=?', (cid,)).fetchone()
        if not car:
            bot.send_message(message.chat.id, "Не найдено.")
            return
        price = car[0]
        bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        if bal < price:
            bot.send_message(message.chat.id, "Недостаточно средств.")
            return
        if cursor.execute('SELECT car_id FROM users WHERE user_id=?', (user_id,)).fetchone()[0]:
            bot.send_message(message.chat.id, "У вас уже есть машина.")
            return
        cursor.execute('UPDATE users SET balance = balance - ?, car_id = ? WHERE user_id=?', (price, cid, user_id))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Вы купили машину за {price} ₽.")
    except:
        bot.send_message(message.chat.id, "Ошибка ввода.")

@bot.callback_query_handler(func=lambda call: call.data == 'my_car')
def my_car(call):
    user_id = call.from_user.id
    car_id = cursor.execute('SELECT car_id FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if not car_id:
        bot.answer_callback_query(call.id, "У вас нет машины.")
        return
    car = cursor.execute('SELECT brand, model, fuel, tuning_level, type FROM cars WHERE id=?', (car_id,)).fetchone()
    if not car: return
    text = f"🚗 {car[0]} {car[1]} ({car[4]})\n⛽ Топливо: {car[2]:.1f} л\n🔧 Тюнинг: {car[3]}"
    bot.send_message(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda call: call.data == 'fuel_car')
def fuel_car(call):
    user_id = call.from_user.id
    car_id = cursor.execute('SELECT car_id FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if not car_id:
        bot.answer_callback_query(call.id, "Нет машины.")
        return
    car = cursor.execute('SELECT fuel, type FROM cars WHERE id=?', (car_id,)).fetchone()
    if not car: return
    if car[1] == 'bicycle':
        bot.send_message(call.message.chat.id, "Велосипед не требует заправки.")
        return
    price_per_l = 55
    max_fuel = 80
    need = max_fuel - car[0]
    if need <= 0:
        bot.send_message(call.message.chat.id, "Бак полон.")
        return
    cost = need * price_per_l
    bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if bal >= cost:
        cursor.execute('UPDATE cars SET fuel = ? WHERE id=?', (max_fuel, car_id))
        cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id=?', (cost, user_id))
        conn.commit()
        bot.send_message(call.message.chat.id, f"⛽ Заправлено {need} л за {cost} ₽.")
    else:
        bot.send_message(call.message.chat.id, f"Не хватает денег. Нужно {cost} ₽. Сколько литров заправить?")
        bot.register_next_step_handler(call.message, partial_fuel, car_id, price_per_l)

def partial_fuel(message, car_id, price_per_l):
    try:
        lit = float(message.text)
        if lit <= 0: raise ValueError
        car = cursor.execute('SELECT fuel FROM cars WHERE id=?', (car_id,)).fetchone()
        max_fuel = 80
        new_fuel = min(max_fuel, car[0] + lit)
        real_lit = new_fuel - car[0]
        if real_lit <= 0:
            bot.send_message(message.chat.id, "Бак полон.")
            return
        cost = real_lit * price_per_l
        bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (message.from_user.id,)).fetchone()[0]
        if bal < cost:
            bot.send_message(message.chat.id, "Недостаточно средств.")
            return
        cursor.execute('UPDATE cars SET fuel = ? WHERE id=?', (new_fuel, car_id))
        cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id=?', (cost, message.from_user.id))
        conn.commit()
        bot.send_message(message.chat.id, f"⛽ Заправлено {real_lit} л за {cost} ₽.")
    except:
        bot.send_message(message.chat.id, "Ошибка ввода.")

@bot.callback_query_handler(func=lambda call: call.data == 'tune_car')
def tune_car(call):
    user_id = call.from_user.id
    car_id = cursor.execute('SELECT car_id FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if not car_id:
        bot.answer_callback_query(call.id, "Нет машины.")
        return
    tune = cursor.execute('SELECT tuning_level FROM cars WHERE id=?', (car_id,)).fetchone()[0]
    cost = (tune + 1) * 50000
    bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if bal < cost:
        bot.send_message(call.message.chat.id, "Недостаточно денег.")
        return
    cursor.execute('UPDATE cars SET tuning_level = tuning_level + 1 WHERE id=?', (car_id,))
    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id=?', (cost, user_id))
    conn.commit()
    bot.send_message(call.message.chat.id, f"✅ Тюнинг выполнен! Уровень {tune+1}, потрачено {cost} ₽.")

# ----- ДОМ -----
@bot.message_handler(func=lambda m: m.text == '🏠 Дом')
def house_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Купить дом", callback_data="buy_house"))
    markup.add(types.InlineKeyboardButton("Мой дом", callback_data="my_house"))
    markup.add(types.InlineKeyboardButton("Приготовить еду", callback_data="cook_food"))
    bot.send_message(message.chat.id, "Недвижимость:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'buy_house')
def buy_house_menu(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Квартира (1 000 000₽)", callback_data="buy_house_flat"))
    markup.add(types.InlineKeyboardButton("Дом (5 000 000₽)", callback_data="buy_house_house"))
    markup.add(types.InlineKeyboardButton("Особняк (20 000 000₽)", callback_data="buy_house_mansion"))
    bot.send_message(call.message.chat.id, "Выберите тип:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_house_'))
def process_buy_house(call):
    htype = call.data.split('_')[2]
    prices = {"flat":1000000, "house":5000000, "mansion":20000000}
    garage = {"flat":1, "house":2, "mansion":4}
    price = prices[htype]
    user_id = call.from_user.id
    if cursor.execute('SELECT id FROM houses WHERE owner_id=?', (user_id,)).fetchone():
        bot.answer_callback_query(call.id, "У вас уже есть дом!")
        return
    bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if bal < price:
        bot.answer_callback_query(call.id, "Недостаточно средств!")
        return
    cursor.execute('INSERT INTO houses (owner_id, type, price, garage_capacity) VALUES (?,?,?,?)',
                   (user_id, htype, price, garage[htype]))
    cursor.execute('UPDATE users SET balance = balance - ?, house_id = last_insert_rowid() WHERE user_id=?', (price, user_id))
    conn.commit()
    bot.edit_message_text(f"✅ Вы купили {htype}!", call.message.chat.id, call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data == 'my_house')
def my_house(call):
    user_id = call.from_user.id
    house = cursor.execute('SELECT type, garage_capacity FROM houses WHERE owner_id=?', (user_id,)).fetchone()
    if not house:
        bot.send_message(call.message.chat.id, "У вас нет дома.")
        return
    bot.send_message(call.message.chat.id, f"🏠 {house[0]}\n🚗 Мест в гараже: {house[1]}")

@bot.callback_query_handler(func=lambda call: call.data == 'cook_food')
def cook_food(call):
    user_id = call.from_user.id
    if not cursor.execute('SELECT id FROM houses WHERE owner_id=?', (user_id,)).fetchone():
        bot.answer_callback_query(call.id, "У вас нет дома.")
        return
    # Проверяем продукты в инвентаре (категория food)
    items = cursor.execute('''
        SELECT i.id, i.name, inv.quantity FROM inventory inv
        JOIN items i ON inv.item_id = i.id
        WHERE inv.user_id=? AND i.category='food'
    ''', (user_id,)).fetchall()
    if not items:
        bot.send_message(call.message.chat.id, "У вас нет продуктов.")
        return
    text = "Ваши продукты:\n"
    for it in items:
        text += f"{it[0]}. {it[1]} — {it[2]} шт.\n"
    text += "Введите ID и количество (например: 1 2):"
    bot.send_message(call.message.chat.id, text)
    bot.register_next_step_handler(call.message, process_cook)

def process_cook(message):
    try:
        parts = message.text.split()
        if len(parts) != 2: raise ValueError
        item_id = int(parts[0])
        qty = int(parts[1])
        user_id = message.from_user.id
        inv = cursor.execute('SELECT quantity FROM inventory WHERE user_id=? AND item_id=?', (user_id, item_id)).fetchone()
        if not inv or inv[0] < qty:
            bot.send_message(message.chat.id, "Недостаточно продуктов.")
            return
        new_qty = inv[0] - qty
        if new_qty == 0:
            cursor.execute('DELETE FROM inventory WHERE user_id=? AND item_id=?', (user_id, item_id))
        else:
            cursor.execute('UPDATE inventory SET quantity = ? WHERE user_id=? AND item_id=?', (new_qty, user_id, item_id))
        hunger_gain = qty * 10
        cursor.execute('UPDATE users SET hunger = MIN(100, hunger + ?) WHERE user_id=?', (hunger_gain, user_id))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Вы приготовили еду. Голод +{hunger_gain}")
    except:
        bot.send_message(message.chat.id, "Ошибка ввода.")

# ----- ШКОЛА -----
@bot.message_handler(func=lambda m: m.text == '🏫 Школа')
def school_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    age = cursor.execute('SELECT age FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    u = cursor.execute('SELECT school_id, class_level, university_id FROM users WHERE user_id=?', (user_id,)).fetchone()
    if u[0] or u[2]:
        if u[0]:
            s = cursor.execute('SELECT name FROM schools WHERE id=?', (u[0],)).fetchone()
            bot.send_message(message.chat.id, f"Вы уже учитесь в {s[0]}, {u[1]} класс.")
        else:
            uu = cursor.execute('SELECT name FROM schools WHERE id=?', (u[2],)).fetchone()
            bot.send_message(message.chat.id, f"Вы учитесь в {uu[0]}.")
        return
    schools = cursor.execute('SELECT id, name, type, cost_per_day, exp_per_day FROM schools WHERE min_age <= ? AND max_age >= ?', (age, age)).fetchall()
    if not schools:
        bot.send_message(message.chat.id, "Нет подходящих учебных заведений.")
        return
    markup = types.InlineKeyboardMarkup()
    for s in schools:
        markup.add(types.InlineKeyboardButton(f"{s[1]} ({s[3]}₽/день)", callback_data=f"enroll_{s[0]}"))
    bot.send_message(message.chat.id, "Выберите заведение:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('enroll_'))
def enroll(call):
    school_id = int(call.data.split('_')[1])
    user_id = call.from_user.id
    school = cursor.execute('SELECT type, min_age, max_age FROM schools WHERE id=?', (school_id,)).fetchone()
    age = cursor.execute('SELECT age FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if age < school[1] or age > school[2]:
        bot.answer_callback_query(call.id, "Возраст не подходит.")
        return
    if school[0] == 'school':
        bot.send_message(call.message.chat.id, "Введите класс (1-11):")
        bot.register_next_step_handler(call.message, process_school_class, school_id)
    else:
        cursor.execute('UPDATE users SET university_id=? WHERE user_id=?', (school_id, user_id))
        conn.commit()
        bot.edit_message_text("✅ Вы поступили в университет!", call.message.chat.id, call.message.message_id)

def process_school_class(message, school_id):
    try:
        cls = int(message.text)
        if cls < 1 or cls > 11: raise ValueError
        user_id = message.from_user.id
        cursor.execute('UPDATE users SET school_id=?, class_level=? WHERE user_id=?', (school_id, cls, user_id))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Вы поступили в школу, {cls} класс.")
    except:
        bot.send_message(message.chat.id, "Неверный класс.")

# ----- КАЗИНО -----
@bot.message_handler(func=lambda m: m.text == '🎰 Казино')
def casino_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Рулетка (красное/черное)", callback_data="casino_roulette"))
    bot.send_message(message.chat.id, "Казино:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'casino_roulette')
def casino_roulette(call):
    bot.send_message(call.message.chat.id, "Введите ставку и цвет (красное/черное), например: 100 красное")
    bot.register_next_step_handler(call.message, process_roulette)

def process_roulette(message):
    try:
        parts = message.text.split()
        if len(parts) != 2: raise ValueError
        bet = int(parts[0])
        color = parts[1].lower()
        if color not in ['красное','черное']: raise ValueError
        user_id = message.from_user.id
        bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        if bet <= 0 or bet > bal:
            bot.send_message(message.chat.id, "Неверная сумма.")
            return
        cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id=?', (bet, user_id))
        conn.commit()
        result = random.choice(['красное','черное'])
        if result == color:
            win = bet * 2
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id=?', (win, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"🎲 Выпало {result}! Вы выиграли {win} ₽!")
        else:
            bot.send_message(message.chat.id, f"🎲 Выпало {result}! Вы проиграли {bet} ₽.")
    except:
        bot.send_message(message.chat.id, "Ошибка ввода.")

# ----- ГУЛЯТЬ -----
@bot.message_handler(func=lambda m: m.text == '🚶 Гулять')
def walk_choice(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("По Москве", callback_data="walk_moscow"))
    markup.add(types.InlineKeyboardButton("На детской площадке", callback_data="walk_playground"))
    bot.send_message(message.chat.id, "Куда пойдём?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('walk_'))
def walk_handler(call):
    user_id = call.from_user.id
    now = int(time.time())
    last = cursor.execute('SELECT last_walk_time FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if last and now - last < 3600:
        bot.answer_callback_query(call.id, "Вы уже гуляли недавно.")
        return
    if call.data == 'walk_moscow':
        found = random.randint(100,1000)
        cursor.execute('UPDATE users SET balance = balance + ?, last_walk_time = ? WHERE user_id=?', (found, now, user_id))
        conn.commit()
        bot.send_message(call.message.chat.id, f"🚶 Вы нашли {found} ₽!")
    else:
        age = cursor.execute('SELECT age FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        if age >= 18:
            bot.answer_callback_query(call.id, "Это для детей до 18.")
            return
        hp_gain = random.randint(5,15)
        cursor.execute('UPDATE users SET health = MIN(100, health + ?), last_walk_time = ? WHERE user_id=?', (hp_gain, now, user_id))
        conn.commit()
        bot.send_message(call.message.chat.id, f"🧸 Вы погуляли, здоровье +{hp_gain}.")

# ----- ТЕЛЕФОН -----
@bot.message_handler(func=lambda m: m.text == '📱 Телефон')
def phone_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📇 Контакты", callback_data="phone_contacts"))
    markup.add(types.InlineKeyboardButton("➕ Добавить контакт", callback_data="phone_add"))
    markup.add(types.InlineKeyboardButton("📞 Позвонить", callback_data="phone_call"))
    markup.add(types.InlineKeyboardButton("💰 Крипта", callback_data="phone_crypto"))
    bot.send_message(message.chat.id, "Телефон:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'phone_contacts')
def phone_contacts(call):
    user_id = call.from_user.id
    contacts = cursor.execute('SELECT contact_name, contact_username, contact_user_id FROM contacts WHERE user_id=?', (user_id,)).fetchall()
    if not contacts:
        bot.send_message(call.message.chat.id, "Контактов нет.")
        return
    text = "📇 Ваши контакты:\n"
    for c in contacts:
        text += f"• {c[0]} (@{c[1]}, ID {c[2]})\n"
    bot.send_message(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda call: call.data == 'phone_add')
def phone_add(call):
    bot.send_message(call.message.chat.id, "Введите username (без @):")
    bot.register_next_step_handler(call.message, process_add_contact)

def process_add_contact(message):
    username = message.text.strip().lstrip('@')
    user_id = message.from_user.id
    target = cursor.execute('SELECT user_id, full_name FROM users WHERE telegram_username=?', (username,)).fetchone()
    if not target:
        bot.send_message(message.chat.id, "Пользователь не найден.")
        return
    if target[0] == user_id:
        bot.send_message(message.chat.id, "Нельзя добавить себя.")
        return
    if cursor.execute('SELECT id FROM contacts WHERE user_id=? AND contact_user_id=?', (user_id, target[0])).fetchone():
        bot.send_message(message.chat.id, "Контакт уже есть.")
        return
    cursor.execute('INSERT INTO contacts (user_id, contact_username, contact_name, contact_user_id) VALUES (?,?,?,?)',
                   (user_id, username, target[1], target[0]))
    conn.commit()
    bot.send_message(message.chat.id, f"✅ Контакт {target[1]} добавлен.")

@bot.callback_query_handler(func=lambda call: call.data == 'phone_call')
def phone_call_menu(call):
    bot.send_message(call.message.chat.id, "Введите username или ID:")
    bot.register_next_step_handler(call.message, process_call)

def process_call(message):
    target_input = message.text.strip()
    user_id = message.from_user.id
    try:
        target_id = int(target_input)
    except:
        t = cursor.execute('SELECT user_id FROM users WHERE telegram_username=?', (target_input.lstrip('@'),)).fetchone()
        if not t:
            bot.send_message(message.chat.id, "Не найден.")
            return
        target_id = t[0]
    if target_id == user_id:
        bot.send_message(message.chat.id, "Нельзя позвонить себе.")
        return
    if cursor.execute('SELECT id FROM calls WHERE (caller_id=? OR receiver_id=?) AND active=1', (target_id, target_id)).fetchone():
        bot.send_message(message.chat.id, "Пользователь занят.")
        return
    cursor.execute('INSERT INTO calls (caller_id, receiver_id, start_time, active) VALUES (?,?,?,1)',
                   (user_id, target_id, int(time.time())))
    conn.commit()
    bot.send_message(target_id, f"📞 Вам звонит {message.from_user.username}. /accept или /decline")
    bot.send_message(message.chat.id, "Звонок инициирован.")

@bot.message_handler(commands=['accept'])
def accept_call(message):
    user_id = message.from_user.id
    call = cursor.execute('SELECT id, caller_id FROM calls WHERE receiver_id=? AND active=1', (user_id,)).fetchone()
    if not call:
        bot.send_message(message.chat.id, "Нет входящих звонков.")
        return
    cursor.execute('UPDATE calls SET active=2 WHERE id=?', (call[0],))
    conn.commit()
    bot.send_message(message.chat.id, "✅ Вы приняли звонок. /off для завершения.")
    bot.send_message(call[1], f"✅ {message.from_user.username} принял звонок. /off для завершения.")

@bot.message_handler(commands=['decline'])
def decline_call(message):
    user_id = message.from_user.id
    call = cursor.execute('SELECT id, caller_id FROM calls WHERE receiver_id=? AND active=1', (user_id,)).fetchone()
    if not call:
        bot.send_message(message.chat.id, "Нет входящих звонков.")
        return
    cursor.execute('UPDATE calls SET active=0 WHERE id=?', (call[0],))
    conn.commit()
    bot.send_message(message.chat.id, "❌ Звонок отклонён.")
    bot.send_message(call[1], "❌ Пользователь отклонил звонок.")

@bot.message_handler(commands=['off'])
def end_call(message):
    user_id = message.from_user.id
    call = cursor.execute('SELECT id, caller_id, receiver_id FROM calls WHERE (caller_id=? OR receiver_id=?) AND active=2', (user_id, user_id)).fetchone()
    if not call:
        bot.send_message(message.chat.id, "Нет активного разговора.")
        return
    cursor.execute('UPDATE calls SET active=0 WHERE id=?', (call[0],))
    conn.commit()
    other = call[1] if call[2] == user_id else call[2]
    bot.send_message(message.chat.id, "🔇 Разговор завершён.")
    bot.send_message(other, "🔇 Собеседник завершил разговор.")

@bot.callback_query_handler(func=lambda call: call.data == 'phone_crypto')
def phone_crypto(call):
    user_id = call.from_user.id
    crypto = cursor.execute('SELECT crypto_balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Купить", callback_data="crypto_buy"))
    markup.add(types.InlineKeyboardButton("Продать", callback_data="crypto_sell"))
    bot.send_message(call.message.chat.id, f"💰 Крипта: {crypto} BTC (1 BTC = 1 000 000₽)", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'crypto_buy')
def crypto_buy(call):
    bot.send_message(call.message.chat.id, "Введите сумму в рублях:")
    bot.register_next_step_handler(call.message, process_crypto_buy)

def process_crypto_buy(message):
    try:
        rub = int(message.text)
        if rub <= 0: raise ValueError
        user_id = message.from_user.id
        bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        if bal < rub:
            bot.send_message(message.chat.id, "Недостаточно рублей.")
            return
        btc = rub // 1000000
        if btc == 0:
            bot.send_message(message.chat.id, "Минимум 1 000 000₽")
            return
        cursor.execute('UPDATE users SET balance = balance - ?, crypto_balance = crypto_balance + ? WHERE user_id=?', (rub, btc, user_id))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Куплено {btc} BTC.")
    except:
        bot.send_message(message.chat.id, "Ошибка.")

@bot.callback_query_handler(func=lambda call: call.data == 'crypto_sell')
def crypto_sell(call):
    bot.send_message(call.message.chat.id, "Введите количество BTC:")
    bot.register_next_step_handler(call.message, process_crypto_sell)

def process_crypto_sell(message):
    try:
        btc = int(message.text)
        if btc <= 0: raise ValueError
        user_id = message.from_user.id
        crypto = cursor.execute('SELECT crypto_balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        if crypto < btc:
            bot.send_message(message.chat.id, "Недостаточно BTC.")
            return
        rub = btc * 1000000
        cursor.execute('UPDATE users SET balance = balance + ?, crypto_balance = crypto_balance - ? WHERE user_id=?', (rub, btc, user_id))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Продано {btc} BTC за {rub}₽.")
    except:
        bot.send_message(message.chat.id, "Ошибка.")

# ----- ВОЕНКОМАТ -----
@bot.message_handler(func=lambda m: m.text == '⚔️ Военкомат')
def voenkomat(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    age = cursor.execute('SELECT age FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    army = cursor.execute('SELECT army_status FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if army == 2:
        bot.send_message(message.chat.id, "Вы уже отслужили.")
        return
    if army == 1:
        bot.send_message(message.chat.id, "Вы в армии.")
        return
    if age < 18:
        bot.send_message(message.chat.id, f"До призыва {18-age} лет.")
        return
    if cursor.execute('SELECT university_id FROM users WHERE user_id=?', (user_id,)).fetchone()[0]:
        bot.send_message(message.chat.id, "У вас отсрочка.")
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Пойти служить", callback_data="army_go"))
    bot.send_message(message.chat.id, "Военкомат:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'army_go')
def army_go(call):
    user_id = call.from_user.id
    cursor.execute('UPDATE users SET army_status=1, job_id=NULL WHERE user_id=?', (user_id,))
    # Убираем служебную машину если была
    cursor.execute('UPDATE users SET car_id = NULL, service_car_id = NULL WHERE user_id=? AND service_car_id IS NOT NULL', (user_id,))
    conn.commit()
    bot.edit_message_text("Вы призваны в армию!", call.message.chat.id, call.message.message_id)

# ----- МЭРИЯ -----
@bot.message_handler(func=lambda m: m.text == '🏛️ Мэрия')
def city_hall(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    pres = cursor.execute('SELECT username FROM government WHERE position="president"').fetchone()
    pres_text = f"\n\nПрезидент Москвы: Александр Куников {pres[0]}" if pres else ""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💍 ЗАГС", callback_data="city_zags"))
    markup.add(types.InlineKeyboardButton("🔫 Лицензия на оружие", callback_data="city_license"))
    bot.send_message(message.chat.id, f"Мэрия:{pres_text}", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'city_zags')
def zags_menu(call):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Предложить брак", callback_data="propose"))
    markup.add(types.InlineKeyboardButton("Развод", callback_data="divorce"))
    bot.send_message(call.message.chat.id, "ЗАГС:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'propose')
def propose(call):
    user_id = call.from_user.id
    if not cursor.execute('SELECT passport FROM users WHERE user_id=?', (user_id,)).fetchone()[0]:
        bot.answer_callback_query(call.id, "Нужен паспорт.")
        return
    bot.send_message(call.message.chat.id, "Введите ID пользователя:")
    bot.register_next_step_handler(call.message, process_propose)

def process_propose(message):
    try:
        target = int(message.text)
    except:
        bot.send_message(message.chat.id, "Введите число.")
        return
    user_id = message.from_user.id
    if target == user_id:
        bot.send_message(message.chat.id, "Нельзя жениться на себе.")
        return
    tpass = cursor.execute('SELECT passport FROM users WHERE user_id=?', (target,)).fetchone()
    if not tpass or not tpass[0]:
        bot.send_message(message.chat.id, "У цели нет паспорта.")
        return
    u1 = cursor.execute('SELECT married_to FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    u2 = cursor.execute('SELECT married_to FROM users WHERE user_id=?', (target,)).fetchone()[0]
    if u1 or u2:
        bot.send_message(message.chat.id, "Кто-то уже в браке.")
        return
    cursor.execute('UPDATE users SET married_to=? WHERE user_id=?', (target, user_id))
    cursor.execute('UPDATE users SET married_to=? WHERE user_id=?', (user_id, target))
    conn.commit()
    bot.send_message(message.chat.id, f"💍 Вы в браке с {target}!")

@bot.callback_query_handler(func=lambda call: call.data == 'divorce')
def divorce(call):
    user_id = call.from_user.id
    spouse = cursor.execute('SELECT married_to FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if not spouse:
        bot.answer_callback_query(call.id, "Вы не в браке.")
        return
    cursor.execute('UPDATE users SET married_to=NULL WHERE user_id IN (?,?)', (user_id, spouse))
    conn.commit()
    bot.send_message(call.message.chat.id, "Вы разведены.")

@bot.callback_query_handler(func=lambda call: call.data == 'city_license')
def weapon_license(call):
    user_id = call.from_user.id
    age = cursor.execute('SELECT age FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if age < 18:
        bot.answer_callback_query(call.id, "Только с 18 лет.")
        return
    if cursor.execute('SELECT id FROM licenses WHERE user_id=? AND type="weapon"', (user_id,)).fetchone():
        bot.send_message(call.message.chat.id, "Лицензия уже есть.")
        return
    cost = 5000
    bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if bal < cost:
        bot.send_message(call.message.chat.id, f"Недостаточно средств. Нужно {cost}₽.")
        return
    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id=?', (cost, user_id))
    cursor.execute('INSERT INTO licenses (user_id, type, issued_date) VALUES (?,?,?)', (user_id, 'weapon', int(time.time())))
    conn.commit()
    bot.send_message(call.message.chat.id, "✅ Лицензия получена!")

# ----- МАГАЗИН -----
@bot.message_handler(func=lambda m: m.text == '🛒 Магазин')
def shop_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🍎 Продукты", callback_data="shop_food"))
    markup.add(types.InlineKeyboardButton("🔫 Оружие", callback_data="shop_weapon"))
    markup.add(types.InlineKeyboardButton("📱 Электроника", callback_data="shop_elec"))
    markup.add(types.InlineKeyboardButton("🏠 Дом", callback_data="shop_home"))
    markup.add(types.InlineKeyboardButton("💊 Наркотики", callback_data="shop_drug"))
    markup.add(types.InlineKeyboardButton("🍷 Алкоголь", callback_data="shop_alcohol"))
    markup.add(types.InlineKeyboardButton("🚬 Сигареты", callback_data="shop_cigarette"))
    markup.add(types.InlineKeyboardButton("🌸 Цветы", callback_data="shop_flower"))
    markup.add(types.InlineKeyboardButton("🔧 Аксессуары", callback_data="shop_accessory"))
    bot.send_message(message.chat.id, "Категория:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('shop_'))
def shop_category(call):
    cat = call.data.split('_')[1]
    items = cursor.execute('SELECT id, name, price, description, required_level, required_passport FROM items WHERE category=?', (cat,)).fetchall()
    if not items:
        bot.answer_callback_query(call.id, "Нет товаров.")
        return
    text = f"Товары {cat}:\n"
    for i in items:
        text += f"{i[0]}. {i[1]} — {i[2]}₽\n   {i[3]}\n"
    text += "Введите ID и количество (напр. 1 2):"
    bot.send_message(call.message.chat.id, text)
    bot.register_next_step_handler(call.message, process_buy_item, cat)

def process_buy_item(message, cat):
    try:
        parts = message.text.split()
        if len(parts) != 2: raise ValueError
        item_id = int(parts[0])
        qty = int(parts[1])
        if qty <= 0: raise ValueError
        user_id = message.from_user.id
        item = cursor.execute('SELECT price, name, required_level, required_passport FROM items WHERE id=?', (item_id,)).fetchone()
        if not item:
            bot.send_message(message.chat.id, "Товар не найден.")
            return
        price, name, req_lvl, req_pass = item
        u = cursor.execute('SELECT level, age, passport FROM users WHERE user_id=?', (user_id,)).fetchone()
        if u[0] < req_lvl or u[1] < req_lvl:
            bot.send_message(message.chat.id, "Ваш уровень слишком низкий.")
            return
        if req_pass and not u[2]:
            bot.send_message(message.chat.id, "Для покупки нужен паспорт.")
            return
        total = price * qty
        bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        if bal < total:
            bot.send_message(message.chat.id, "Недостаточно средств.")
            return
        # Проверка лицензии для оружия
        if cat == 'weapon':
            lic = cursor.execute('SELECT id FROM licenses WHERE user_id=? AND type="weapon"', (user_id,)).fetchone()
            if not lic:
                bot.send_message(message.chat.id, "Нужна лицензия на оружие.")
                return
        cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id=?', (total, user_id))
        inv = cursor.execute('SELECT quantity FROM inventory WHERE user_id=? AND item_id=?', (user_id, item_id)).fetchone()
        if inv:
            cursor.execute('UPDATE inventory SET quantity = quantity + ? WHERE user_id=? AND item_id=?', (qty, user_id, item_id))
        else:
            cursor.execute('INSERT INTO inventory (user_id, item_id, quantity) VALUES (?,?,?)', (user_id, item_id, qty))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Вы купили {qty} x {name} за {total}₽.")
    except:
        bot.send_message(message.chat.id, "Ошибка ввода.")

# ----- ОДЕЖДА -----
@bot.message_handler(func=lambda m: m.text == '👕 Одежда')
def clothes_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    items = cursor.execute('SELECT id, brand, name, price FROM items WHERE category="clothes"').fetchall()
    if not items:
        bot.send_message(message.chat.id, "Одежды нет.")
        return
    text = "👕 Одежда:\n"
    for i in items:
        text += f"{i[0]}. {i[1] or ''} {i[2]} — {i[3]}₽\n"
    text += "Введите ID:"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, buy_clothes)

def buy_clothes(message):
    try:
        item_id = int(message.text)
        user_id = message.from_user.id
        item = cursor.execute('SELECT price, name FROM items WHERE id=? AND category="clothes"', (item_id,)).fetchone()
        if not item:
            bot.send_message(message.chat.id, "Не найдено.")
            return
        price, name = item
        bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        if bal < price:
            bot.send_message(message.chat.id, "Недостаточно средств.")
            return
        cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id=?', (price, user_id))
        inv = cursor.execute('SELECT quantity FROM inventory WHERE user_id=? AND item_id=?', (user_id, item_id)).fetchone()
        if inv:
            cursor.execute('UPDATE inventory SET quantity = quantity + 1 WHERE user_id=? AND item_id=?', (user_id, item_id))
        else:
            cursor.execute('INSERT INTO inventory (user_id, item_id, quantity) VALUES (?,?,1)', (user_id, item_id))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Вы купили {name}.")
    except:
        bot.send_message(message.chat.id, "Ошибка.")

# ----- МАРКЕТПЛЕЙСЫ -----
@bot.message_handler(func=lambda m: m.text == '📦 Kyvito')
def kyvito_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    listings = cursor.execute('''
        SELECT l.id, i.name, l.quantity, l.price_per_unit, u.full_name
        FROM marketplace_listings l
        JOIN items i ON l.item_id = i.id
        JOIN users u ON l.seller_id = u.user_id
        WHERE l.active=1 AND l.marketplace='kyvito'
    ''').fetchall()
    if not listings:
        bot.send_message(message.chat.id, "На Kyvito нет товаров.")
        return
    text = "📦 Kyvito:\n"
    for l in listings:
        text += f"{l[0]}. {l[1]} x{l[2]} — {l[3]}₽ (продавец {l[4]})\n"
    text += "Введите ID лота и количество (напр. 5 2):"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, process_market_buy, 'kyvito')

@bot.message_handler(func=lambda m: m.text == '💀 Kydark')
def kydark_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    listings = cursor.execute('''
        SELECT l.id, i.name, l.quantity, l.price_per_unit, u.full_name
        FROM marketplace_listings l
        JOIN items i ON l.item_id = i.id
        JOIN users u ON l.seller_id = u.user_id
        WHERE l.active=1 AND l.marketplace='kydark'
    ''').fetchall()
    if not listings:
        bot.send_message(message.chat.id, "На Kydark нет товаров.")
        return
    text = "💀 Kydark:\n"
    for l in listings:
        text += f"{l[0]}. {l[1]} x{l[2]} — {l[3]}₽ (продавец {l[4]})\n"
    text += "Введите ID лота и количество:"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, process_market_buy, 'kydark')

def process_market_buy(message, market):
    try:
        parts = message.text.split()
        if len(parts) != 2: raise ValueError
        listing_id = int(parts[0])
        qty = int(parts[1])
        user_id = message.from_user.id
        listing = cursor.execute('''
            SELECT l.seller_id, l.item_id, l.quantity, l.price_per_unit, i.name
            FROM marketplace_listings l
            JOIN items i ON l.item_id = i.id
            WHERE l.id=? AND l.active=1 AND l.marketplace=?
        ''', (listing_id, market)).fetchone()
        if not listing:
            bot.send_message(message.chat.id, "Лот не найден.")
            return
        if qty > listing[2]:
            bot.send_message(message.chat.id, "Недостаточно товара.")
            return
        total = qty * listing[3]
        bal = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        if bal < total:
            bot.send_message(message.chat.id, "Недостаточно средств.")
            return
        cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id=?', (total, user_id))
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id=?', (total, listing[0]))
        new_qty = listing[2] - qty
        if new_qty == 0:
            cursor.execute('UPDATE marketplace_listings SET active=0 WHERE id=?', (listing_id,))
        else:
            cursor.execute('UPDATE marketplace_listings SET quantity=? WHERE id=?', (new_qty, listing_id))
        inv = cursor.execute('SELECT quantity FROM inventory WHERE user_id=? AND item_id=?', (user_id, listing[1])).fetchone()
        if inv:
            cursor.execute('UPDATE inventory SET quantity = quantity + ? WHERE user_id=? AND item_id=?', (qty, user_id, listing[1]))
        else:
            cursor.execute('INSERT INTO inventory (user_id, item_id, quantity) VALUES (?,?,?)', (user_id, listing[1], qty))
        conn.commit()
        bot.send_message(message.chat.id, f"✅ Вы купили {qty} x {listing[4]} за {total}₽.")
    except:
        bot.send_message(message.chat.id, "Ошибка ввода.")

# ----- ИНВЕНТАРЬ -----
@bot.message_handler(func=lambda m: m.text == '🎒 Инвентарь')
def inventory_menu(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.send_message(message.chat.id, rest)
        return
    update_activity(user_id)
    items = cursor.execute('''
        SELECT i.id, i.name, i.category, inv.quantity, inv.equipped
        FROM inventory inv
        JOIN items i ON inv.item_id = i.id
        WHERE inv.user_id=?
    ''', (user_id,)).fetchall()
    if not items:
        bot.send_message(message.chat.id, "Инвентарь пуст.")
        return
    text = "🎒 Ваш инвентарь:\n"
    for it in items:
        eq = " [экипировано]" if it[4] else ""
        text += f"{it[0]}. {it[1]} x{it[2]}{eq}\n"
    text += "Введите ID предмета для действий:"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, inventory_action)

def inventory_action(message):
    try:
        item_id = int(message.text)
        user_id = message.from_user.id
        item = cursor.execute('''
            SELECT i.id, i.name, i.category, i.stats, inv.quantity, inv.equipped
            FROM inventory inv
            JOIN items i ON inv.item_id = i.id
            WHERE inv.user_id=? AND i.id=?
        ''', (user_id, item_id)).fetchone()
        if not item:
            bot.send_message(message.chat.id, "Предмет не найден.")
            return
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Использовать", callback_data=f"use_{item_id}"))
        if item[5] == 0:
            markup.add(types.InlineKeyboardButton("Надеть", callback_data=f"equip_{item_id}"))
        else:
            markup.add(types.InlineKeyboardButton("Снять", callback_data=f"unequip_{item_id}"))
        markup.add(types.InlineKeyboardButton("Подарить", callback_data=f"give_{item_id}"))
        bot.send_message(message.chat.id, f"Действия с {item[1]}:", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "Ошибка.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('use_'))
def use_item(call):
    item_id = int(call.data.split('_')[1])
    user_id = call.from_user.id
    item = cursor.execute('SELECT category, stats, name FROM items WHERE id=?', (item_id,)).fetchone()
    if not item:
        bot.answer_callback_query(call.id, "Ошибка")
        return
    cat, stats_json, name = item
    stats = json.loads(stats_json) if stats_json else {}
    # Использование еды, алкоголя, наркотиков, цветов и т.д.
    if cat == 'food':
        # Лечим голод
        cursor.execute('UPDATE users SET hunger = MIN(100, hunger + 20) WHERE user_id=?', (user_id,))
        cursor.execute('DELETE FROM inventory WHERE user_id=? AND item_id=? AND quantity=1', (user_id, item_id))
        cursor.execute('UPDATE inventory SET quantity = quantity - 1 WHERE user_id=? AND item_id=? AND quantity>1', (user_id, item_id))
        conn.commit()
        bot.answer_callback_query(call.id, "Вы съели еду.")
    elif cat == 'alcohol':
        # Добавляем эффект опьянения
        expires = int(time.time()) + stats.get('duration', 1800)
        cursor.execute('INSERT INTO effects (user_id, effect_type, value, expires_at) VALUES (?,?,?,?)',
                       (user_id, 'drunk', 1, expires))
        cursor.execute('DELETE FROM inventory WHERE user_id=? AND item_id=? AND quantity=1', (user_id, item_id))
        cursor.execute('UPDATE inventory SET quantity = quantity - 1 WHERE user_id=? AND item_id=? AND quantity>1', (user_id, item_id))
        conn.commit()
        bot.answer_callback_query(call.id, "Вы выпили, вы пьяны.")
    elif cat == 'drug':
        expires = int(time.time()) + stats.get('duration', 3600)
        cursor.execute('INSERT INTO effects (user_id, effect_type, value, expires_at) VALUES (?,?,?,?)',
                       (user_id, 'high', 1, expires))
        cursor.execute('DELETE FROM inventory WHERE user_id=? AND item_id=? AND quantity=1', (user_id, item_id))
        cursor.execute('UPDATE inventory SET quantity = quantity - 1 WHERE user_id=? AND item_id=? AND quantity>1', (user_id, item_id))
        conn.commit()
        bot.answer_callback_query(call.id, "Вы употребили наркотик.")
    elif cat == 'flower':
        bot.send_message(call.message.chat.id, "Введите username получателя:")
        bot.register_next_step_handler(call.message, process_give_flower, item_id)
    else:
        bot.answer_callback_query(call.id, "Этот предмет нельзя использовать.")

def process_give_flower(message, item_id):
    username = message.text.strip().lstrip('@')
    user_id = message.from_user.id
    target = cursor.execute('SELECT user_id FROM users WHERE telegram_username=?', (username,)).fetchone()
    if not target:
        bot.send_message(message.chat.id, "Пользователь не найден.")
        return
    target_id = target[0]
    # Проверить наличие цветов
    inv = cursor.execute('SELECT quantity FROM inventory WHERE user_id=? AND item_id=?', (user_id, item_id)).fetchone()
    if not inv or inv[0] < 1:
        bot.send_message(message.chat.id, "У вас нет этого цветка.")
        return
    # Передать
    cursor.execute('UPDATE inventory SET quantity = quantity - 1 WHERE user_id=? AND item_id=?', (user_id, item_id))
    inv_t = cursor.execute('SELECT quantity FROM inventory WHERE user_id=? AND item_id=?', (target_id, item_id)).fetchone()
    if inv_t:
        cursor.execute('UPDATE inventory SET quantity = quantity + 1 WHERE user_id=? AND item_id=?', (target_id, item_id))
    else:
        cursor.execute('INSERT INTO inventory (user_id, item_id, quantity) VALUES (?,?,1)', (target_id, item_id))
    conn.commit()
    bot.send_message(message.chat.id, f"✅ Вы подарили цветок {username}.")
    bot.send_message(target_id, f"🌸 {message.from_user.full_name} подарил вам цветок!")

@bot.callback_query_handler(func=lambda call: call.data.startswith('equip_'))
def equip_item(call):
    item_id = int(call.data.split('_')[1])
    user_id = call.from_user.id
    item = cursor.execute('SELECT category, stats FROM items WHERE id=?', (item_id,)).fetchone()
    if not item:
        bot.answer_callback_query(call.id, "Ошибка")
        return
    cat, stats_json = item
    stats = json.loads(stats_json) if stats_json else {}
    if cat == 'weapon':
        # Экипируем оружие
        cursor.execute('INSERT OR REPLACE INTO equipped (user_id, weapon_id, armor_id, accessory_ids) VALUES (?,?, (SELECT armor_id FROM equipped WHERE user_id=?), (SELECT accessory_ids FROM equipped WHERE user_id=?))',
                       (user_id, item_id, user_id, user_id))
        cursor.execute('UPDATE inventory SET equipped=1 WHERE user_id=? AND item_id=?', (user_id, item_id))
        conn.commit()
        bot.answer_callback_query(call.id, "Оружие экипировано.")
    elif cat == 'armor':
        cursor.execute('INSERT OR REPLACE INTO equipped (user_id, weapon_id, armor_id, accessory_ids) VALUES (?, (SELECT weapon_id FROM equipped WHERE user_id=?), ?, (SELECT accessory_ids FROM equipped WHERE user_id=?))',
                       (user_id, user_id, item_id, user_id))
        cursor.execute('UPDATE inventory SET equipped=1 WHERE user_id=? AND item_id=?', (user_id, item_id))
        conn.commit()
        bot.answer_callback_query(call.id, "Броня надета.")
    elif cat == 'accessory':
        # Просто добавим в список аксессуаров (упрощённо)
        cur = cursor.execute('SELECT accessory_ids FROM equipped WHERE user_id=?', (user_id,)).fetchone()
        acc = json.loads(cur[0]) if cur and cur[0] else []
        acc.append(item_id)
        cursor.execute('INSERT OR REPLACE INTO equipped (user_id, weapon_id, armor_id, accessory_ids) VALUES (?, (SELECT weapon_id FROM equipped WHERE user_id=?), (SELECT armor_id FROM equipped WHERE user_id=?), ?)',
                       (user_id, user_id, user_id, json.dumps(acc)))
        cursor.execute('UPDATE inventory SET equipped=1 WHERE user_id=? AND item_id=?', (user_id, item_id))
        conn.commit()
        bot.answer_callback_query(call.id, "Аксессуар экипирован.")
    else:
        bot.answer_callback_query(call.id, "Это нельзя надеть.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('unequip_'))
def unequip_item(call):
    item_id = int(call.data.split('_')[1])
    user_id = call.from_user.id
    # Упрощённо: снимаем всё
    cursor.execute('DELETE FROM equipped WHERE user_id=?', (user_id,))
    cursor.execute('UPDATE inventory SET equipped=0 WHERE user_id=?', (user_id,))
    conn.commit()
    bot.answer_callback_query(call.id, "Предмет снят.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('give_'))
def give_item(call):
    item_id = int(call.data.split('_')[1])
    bot.send_message(call.message.chat.id, "Введите username получателя:")
    bot.register_next_step_handler(call.message, process_give_item, item_id)

def process_give_item(message, item_id):
    username = message.text.strip().lstrip('@')
    user_id = message.from_user.id
    target = cursor.execute('SELECT user_id FROM users WHERE telegram_username=?', (username,)).fetchone()
    if not target:
        bot.send_message(message.chat.id, "Не найден.")
        return
    target_id = target[0]
    inv = cursor.execute('SELECT quantity FROM inventory WHERE user_id=? AND item_id=?', (user_id, item_id)).fetchone()
    if not inv or inv[0] < 1:
        bot.send_message(message.chat.id, "У вас нет этого предмета.")
        return
    cursor.execute('UPDATE inventory SET quantity = quantity - 1 WHERE user_id=? AND item_id=?', (user_id, item_id))
    inv_t = cursor.execute('SELECT quantity FROM inventory WHERE user_id=? AND item_id=?', (target_id, item_id)).fetchone()
    if inv_t:
        cursor.execute('UPDATE inventory SET quantity = quantity + 1 WHERE user_id=? AND item_id=?', (target_id, item_id))
    else:
        cursor.execute('INSERT INTO inventory (user_id, item_id, quantity) VALUES (?,?,1)', (target_id, item_id))
    conn.commit()
    bot.send_message(message.chat.id, f"✅ Предмет передан {username}.")

# ----- ПОЛИЦЕЙСКИЕ КОМАНДЫ -----
@bot.message_handler(commands=['arrest'])
def arrest_cmd(message):
    user_id = message.from_user.id
    if not is_police(user_id):
        bot.reply_to(message, "Вы не полицейский.")
        return
    try:
        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "Формат: /arrest @username минут причина")
            return
        target_name = args[1].lstrip('@')
        minutes = int(args[2])
        reason = ' '.join(args[3:])
        target = cursor.execute('SELECT user_id FROM users WHERE telegram_username=?', (target_name,)).fetchone()
        if not target:
            bot.reply_to(message, "Пользователь не найден.")
            return
        tid = target[0]
        if cursor.execute('SELECT 1 FROM prison WHERE user_id=?', (tid,)).fetchone():
            bot.reply_to(message, "Уже в тюрьме.")
            return
        release = int(time.time()) + minutes*60
        cursor.execute('INSERT INTO prison (user_id, arrested_by, reason, release_time) VALUES (?,?,?,?)',
                       (tid, user_id, reason, release))
        cursor.execute('DELETE FROM wanted WHERE user_id=?', (tid,))
        conn.commit()
        bot.send_message(tid, f"👮 Вы арестованы на {minutes} мин. Причина: {reason}")
        bot.reply_to(message, f"{target_name} арестован.")
    except:
        bot.reply_to(message, "Ошибка.")

@bot.message_handler(commands=['wanted'])
def wanted_cmd(message):
    if not is_police(message.from_user.id):
        bot.reply_to(message, "Вы не полицейский.")
        return
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "Формат: /wanted @username причина")
            return
        target_name = args[1].lstrip('@')
        reason = ' '.join(args[2:])
        target = cursor.execute('SELECT user_id FROM users WHERE telegram_username=?', (target_name,)).fetchone()
        if not target:
            bot.reply_to(message, "Не найден.")
            return
        tid = target[0]
        cursor.execute('INSERT OR REPLACE INTO wanted (user_id, issued_by, reason, issued_at) VALUES (?,?,?,?)',
                       (tid, message.from_user.id, reason, int(time.time())))
        conn.commit()
        bot.reply_to(message, f"{target_name} объявлен в розыск.")
    except:
        bot.reply_to(message, "Ошибка.")

@bot.message_handler(commands=['unwanted'])
def unwanted_cmd(message):
    if not is_police(message.from_user.id):
        bot.reply_to(message, "Вы не полицейский.")
        return
    try:
        target_name = message.text.split()[1].lstrip('@')
        target = cursor.execute('SELECT user_id FROM users WHERE telegram_username=?', (target_name,)).fetchone()
        if target:
            cursor.execute('DELETE FROM wanted WHERE user_id=?', (target[0],))
            conn.commit()
            bot.reply_to(message, f"{target_name} снят с розыска.")
    except:
        bot.reply_to(message, "Ошибка.")

@bot.message_handler(commands=['handcuff'])
def handcuff_cmd(message):
    if not is_police(message.from_user.id):
        bot.reply_to(message, "Вы не полицейский.")
        return
    try:
        target_name = message.text.split()[1].lstrip('@')
        target = cursor.execute('SELECT user_id FROM users WHERE telegram_username=?', (target_name,)).fetchone()
        if not target:
            bot.reply_to(message, "Не найден.")
            return
        tid = target[0]
        cursor.execute('INSERT OR REPLACE INTO handcuffs (user_id, cuffed_by, cuffed_at) VALUES (?,?,?)',
                       (tid, message.from_user.id, int(time.time())))
        conn.commit()
        bot.send_message(tid, "🔗 На вас надели наручники!")
        bot.reply_to(message, f"{target_name} в наручниках.")
    except:
        bot.reply_to(message, "Ошибка.")

@bot.message_handler(commands=['uncuff'])
def uncuff_cmd(message):
    if not is_police(message.from_user.id):
        bot.reply_to(message, "Вы не полицейский.")
        return
    try:
        target_name = message.text.split()[1].lstrip('@')
        target = cursor.execute('SELECT user_id FROM users WHERE telegram_username=?', (target_name,)).fetchone()
        if target:
            cursor.execute('DELETE FROM handcuffs WHERE user_id=?', (target[0],))
            conn.commit()
            bot.send_message(target[0], "🔓 Наручники сняты.")
            bot.reply_to(message, f"{target_name} освобождён.")
    except:
        bot.reply_to(message, "Ошибка.")

# ----- СТРЕЛЬБА -----
@bot.message_handler(commands=['shoot'])
def shoot_cmd(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.reply_to(message, rest)
        return
    update_activity(user_id)
    if not is_police(user_id):  # для теста разрешим всем, но можно ограничить
        pass
    try:
        target_name = message.text.split()[1].lstrip('@')
        target = cursor.execute('SELECT user_id FROM users WHERE telegram_username=?', (target_name,)).fetchone()
        if not target:
            bot.reply_to(message, "Цель не найдена.")
            return
        tid = target[0]
        # Проверить экипированное оружие
        eq = cursor.execute('SELECT weapon_id, armor_id, accessory_ids FROM equipped WHERE user_id=?', (user_id,)).fetchone()
        if not eq or not eq[0]:
            bot.reply_to(message, "У вас не экипировано оружие.")
            return
        weapon_id = eq[0]
        weapon = cursor.execute('SELECT stats FROM items WHERE id=?', (weapon_id,)).fetchone()
        if not weapon:
            return
        stats = json.loads(weapon[0])
        damage = stats.get('damage', 1)
        fire_rate = stats.get('fire_rate', 3)
        silent = stats.get('silent', False)
        # Проверка кулдауна
        last = cursor.execute('SELECT last_shot FROM users WHERE user_id=?', (user_id,)).fetchone()[0] or 0
        now = time.time()
        if now - last < fire_rate:
            bot.reply_to(message, f"Оружие перезаряжается. Подождите {fire_rate - (now - last):.1f} сек.")
            return
        # Проверка патронов (упрощённо, берём первый попавшийся тип)
        ammo = cursor.execute('SELECT id FROM items WHERE category="ammo" LIMIT 1').fetchone()
        if not ammo:
            bot.reply_to(message, "Нет патронов в игре.")
            return
        ammo_id = ammo[0]
        ammo_qty = cursor.execute('SELECT quantity FROM inventory WHERE user_id=? AND item_id=?', (user_id, ammo_id)).fetchone()
        if not ammo_qty or ammo_qty[0] < 1:
            bot.reply_to(message, "Нет патронов.")
            return
        # Расходуем патрон
        cursor.execute('UPDATE inventory SET quantity = quantity - 1 WHERE user_id=? AND item_id=?', (user_id, ammo_id))
        cursor.execute('UPDATE users SET last_shot=? WHERE user_id=?', (now, user_id))
        # Наносим урон цели
        target_armor = cursor.execute('SELECT armor_id FROM equipped WHERE user_id=?', (tid,)).fetchone()
        if target_armor and target_armor[0]:
            armor = cursor.execute('SELECT stats FROM items WHERE id=?', (target_armor[0],)).fetchone()
            if armor:
                armor_stats = json.loads(armor[0])
                armor_val = armor_stats.get('armor', 0)
                if armor_val >= damage:
                    cursor.execute('DELETE FROM equipped WHERE user_id=?', (tid,))
                    cursor.execute('UPDATE inventory SET equipped=0 WHERE user_id=?', (tid,))
                    bot.send_message(tid, "🔰 Ваша броня разрушена!")
                else:
                    remaining = damage - armor_val
                    cursor.execute('DELETE FROM equipped WHERE user_id=?', (tid,))
                    cursor.execute('UPDATE inventory SET equipped=0 WHERE user_id=?', (tid,))
                    cursor.execute('UPDATE users SET health = health - ? WHERE user_id=?', (remaining, tid))
                    bot.send_message(tid, f"🔰 Броня поглотила {armor_val} урона, вы получили {remaining}.")
            else:
                cursor.execute('UPDATE users SET health = health - ? WHERE user_id=?', (damage, tid))
        else:
            cursor.execute('UPDATE users SET health = health - ? WHERE user_id=?', (damage, tid))
        # Проверить смерть
        hp = cursor.execute('SELECT health FROM users WHERE user_id=?', (tid,)).fetchone()[0]
        if hp <= 0:
            cursor.execute('UPDATE users SET health=1 WHERE user_id=?', (tid,))
            bot.send_message(tid, "💀 Вы потеряли сознание и очнулись в больнице.")
        conn.commit()
        bot.reply_to(message, f"🔫 Вы выстрелили в {target_name}, нанеся {damage} урона.")
        bot.send_message(tid, f"🔫 {message.from_user.first_name} выстрелил в вас! Потеряно {damage} HP.")
        # Уведомление полиции, если нет глушителя
        if not silent:
            police_list = cursor.execute('SELECT user_id FROM users WHERE job_id IN (SELECT id FROM jobs WHERE police=1)').fetchall()
            for p in police_list:
                try:
                    bot.send_message(p[0], f"⚠️ Выстрел в районе Москвы! Стрелял: {message.from_user.first_name}, цель: {target_name}")
                except:
                    pass
    except:
        bot.reply_to(message, "Ошибка. Используйте /shoot @username")

# ----- 18+ КОМАНДЫ -----
@bot.message_handler(commands=['kiss'])
def kiss_cmd(message):
    if message.chat.type != 'private':
        return
    user_id = message.from_user.id
    age = cursor.execute('SELECT age FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
    if age < 18:
        bot.reply_to(message, "Вам нет 18.")
        return
    try:
        target_name = message.text.split()[1].lstrip('@')
        target = cursor.execute('SELECT user_id, age FROM users WHERE telegram_username=?', (target_name,)).fetchone()
        if not target:
            bot.reply_to(message, "Не найден.")
            return
        if target[1] < 18:
            bot.reply_to(message, "Цель младше 18.")
            return
        bot.send_message(target[0], f"💋 {message.from_user.first_name} хочет вас поцеловать! Ответьте /accept_kiss {user_id} или /decline_kiss {user_id}")
        bot.reply_to(message, "Запрос отправлен.")
    except:
        bot.reply_to(message, "Укажите @username")

@bot.message_handler(commands=['accept_kiss'])
def accept_kiss(message):
    try:
        user_id = int(message.text.split()[1])
        bot.send_message(user_id, f"💋 {message.from_user.first_name} принял ваш поцелуй!")
        bot.reply_to(message, "Вы приняли поцелуй.")
    except:
        bot.reply_to(message, "Ошибка.")

@bot.message_handler(commands=['decline_kiss'])
def decline_kiss(message):
    try:
        user_id = int(message.text.split()[1])
        bot.send_message(user_id, f"❌ {message.from_user.first_name} отклонил поцелуй.")
        bot.reply_to(message, "Вы отклонили.")
    except:
        pass

# ----- КОМАНДА ПЕРЕВОДА /pay -----
@bot.message_handler(commands=['pay'])
def pay_cmd(message):
    user_id = message.from_user.id
    rest = check_restrictions(user_id)
    if rest:
        bot.reply_to(message, rest)
        return
    update_activity(user_id)
    try:
        args = message.text.split()
        if len(args) != 3:
            bot.reply_to(message, "Формат: /pay @username сумма")
            return
        target_name = args[1].lstrip('@')
        amount = int(args[2])
        if amount <= 0:
            bot.reply_to(message, "Сумма должна быть положительной")
            return
        target = cursor.execute('SELECT user_id FROM users WHERE telegram_username=?', (target_name,)).fetchone()
        if not target:
            bot.reply_to(message, "Пользователь не найден")
            return
        target_id = target[0]
        if target_id == user_id:
            bot.reply_to(message, "Нельзя перевести самому себе")
            return
        balance = cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,)).fetchone()[0]
        if balance < amount:
            bot.reply_to(message, "Недостаточно средств")
            return
        cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id=?', (amount, user_id))
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id=?', (amount, target_id))
        conn.commit()
        bot.reply_to(message, f"✅ Переведено {amount} ₽ пользователю {target_name}")
        bot.send_message(target_id, f"💰 {message.from_user.first_name} перевёл вам {amount} ₽")
    except ValueError:
        bot.reply_to(message, "Сумма должна быть числом")
    except Exception as e:
        bot.reply_to(message, "Ошибка при переводе")

# ----- КНОПКА МОСКВА -----
@bot.message_handler(func=lambda m: m.text == 'Москва')
def moscow_chat(message):
    bot.send_message(message.chat.id, "Переходите в наш чат:\nhttps://t.me/+Gwg5L4cmThdlOWQy")

# ----- HELP -----
@bot.message_handler(commands=['help'])
def help_cmd(message):
    text = """
📱 Доступные команды и разделы:
👤 Профиль
💼 Работа
🚖 Такси
🚗 Машина
🏠 Дом
🏛️ Мэрия
🎰 Казино
🚶 Гулять
🏫 Школа
📱 Телефон
⚔️ Военкомат
🏦 Банк
🛒 Магазин
📄 Паспорт
🍔 Еда
🏥 Больница
👕 Одежда
📦 Kyvito
💀 Kydark
🎒 Инвентарь

Полицейские команды:
/arrest @user минут причина
/wanted @user причина
/unwanted @user
/handcuff @user
/uncuff @user

Другие команды:
/shoot @user
/kiss @user
/accept_kiss ID
/decline_kiss ID
/accept, /decline, /off (звонки)
/pay @user сумма
/help
    """
    bot.send_message(message.chat.id, text)

# ----- ОБРАБОТКА ВСЕГО ОСТАЛЬНОГО -----
@bot.message_handler(func=lambda m: True)
def fallback(message):
    user_id = message.from_user.id
    # Проверка на активный звонок
    call = cursor.execute('SELECT caller_id, receiver_id FROM calls WHERE (caller_id=? OR receiver_id=?) AND active=2', (user_id, user_id)).fetchone()
    if call:
        other = call[1] if call[0] == user_id else call[0]
        bot.send_message(other, f"📱 {message.from_user.first_name}: {message.text}")
        return
    bot.send_message(message.chat.id, "Используйте кнопки меню или /help")

# ----- ЗАПУСК -----
if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()