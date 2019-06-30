import telepot, time, redis
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup as markup
from telepot.namedtuple import InlineKeyboardButton as btn
import re, os, random

channel = "gpmanoto"
logs = "@gpmanoto"
token = "744193012:AAG5JzJKc8roMJuTc_xHIGaLb-Ym5joT6eE"

sudo_users = [
    603869031,
]

############################################################################################

db = redis.StrictRedis('localhost', 6379, charset='UTF-8', decode_responses=True)
bot = telepot.Bot(token=token)

############################################################################################

help = markup(inline_keyboard=[
    [
        btn(text='» راهنمای سودو', callback_data='sudohelp')
    ],
    [
        btn(text='» راهنمای مدیریتی', callback_data='modhelp'),btn(text='» راهنمای قفلی', callback_data='lockhelp')
    ],
    [
        btn(text='» راهنمای لیستی', callback_data='listhelp')
    ],
    [
        btn(text='» راهنمای سرگرمی', callback_data='funhelp'),btn(text='» راهنمای تنظیمی', callback_data='manhelp')
    ],
    [
        btn(text='•• بستن فهرست راهنما', callback_data='close')
    ]
])

pvmain = markup(inline_keyboard=[
    [
        btn(text='•• افزودن ربات به گروه', url='t.me/'+str(bot.getMe()['username'])+'?startgroup=new')
    ],
    [
        btn(text='•• راهنما', callback_data='pvhelp'),btn(text='•• کانال', url='t.me/'+channel)
    ],
    [
        btn(text='•• امکانات', callback_data='pvhelp2')
    ]
])


prvchannel = markup(inline_keyboard=[
    [
        btn(text='•• کانال', url='t.me/'+channel)
    ]
])

prvback = markup(inline_keyboard=[
    [
        btn(text='•• بازگشت', callback_data='pvmain'),btn(text='•• کانال', url='t.me/'+channel)
    ]
])

panel = markup(inline_keyboard=[
    [
        btn(text='» تنظیمات مدیا', callback_data='medialocks')
    ],
    [
        btn(text='» تنظیمات مدیریتی', callback_data='modlocks')
    ],
    [
        btn(text='» اطلاعات گروه', callback_data='gpinfo')
    ],
    [
        btn(text='» لیست‌های فعال', callback_data='lists')
    ],
    [
        btn(text='•• بستن فهرست تنظیمات', callback_data='close')
    ]
])

back = markup(inline_keyboard=[
    [
        btn(text='•• برگشت', callback_data='help'),btn(text='•• کانال', url='t.me/'+channel)
    ],
    [
        btn(text='•• بستن فهرست تنظیمات', callback_data='close')
    ]
])


back2 = markup(inline_keyboard=[
    [
        btn(text='•• برگشت', callback_data='lists'),btn(text='•• کانال', url='t.me/'+channel)
    ],
    [
        btn(text='•• بستن فهرست تنظیمات', callback_data='close')
    ]
])

back3 = markup(inline_keyboard=[
    [
        btn(text='•• برگشت', callback_data='main'),btn(text='•• کانال', url='t.me/'+channel)
    ],
    [
        btn(text='•• بستن فهرست تنظیمات', callback_data='close')
    ]
])

listspanel = markup(inline_keyboard=[
    [
        btn(text='» مدیران', callback_data='admins')
    ],
    [
        btn(text='» سکوت', callback_data='silents'),btn(text='» محروم', callback_data='bans')
    ],
    [
        btn(text='» فیلتر', callback_data='filters')
    ],
    [
        btn(text='» اعضای اضافه شده', callback_data='joins')
    ],
    [
        btn(text='•• برگشت', callback_data='main'),btn(text='•• کانال', url='t.me/'+channel)
    ],
    [
        btn(text='•• بستن فهرست تنظیمات', callback_data='close')
    ]
])

############################################################################################

def defineNewMediaLock(msg, EnName, FaName):
    text = msg['text']
    chat_id = msg['chat']['id']
    from_id = msg['from']['id']
    message_id = msg['message_id']

    if text in ['lock {}'.format(EnName), 'قفل {}'.format(FaName)]:
        bot.sendMessage(chat_id, "•• قفل {} فعال شد.\n•• حالت قفل : حذف پیام".format(FaName), reply_to_message_id=message_id)
        db.sadd("{}-delete".format(EnName), chat_id)
    elif text in ['unlock {}'.format(EnName), 'بازکردن {}'.format(FaName)]:
        bot.sendMessage(chat_id, "•• قفل {} غیرفعال شد.".format(FaName), reply_to_message_id=message_id)
        db.srem("{}-delete".format(EnName), chat_id)
        db.srem("{}-kick".format(EnName), chat_id)
        db.srem("{}-silence".format(EnName), chat_id)
    elif text in ['{} silence'.format(EnName), '{} سکوت'.format(FaName)]:
        bot.sendMessage(chat_id, "•• قفل {} بروز شد.\n•• حالت جدید :‌ سکوت کاربر".format(FaName), reply_to_message_id=message_id)
        db.srem("{}-delete".format(EnName), chat_id)
        db.srem("{}-kick".format(EnName), chat_id)
        db.sadd("{}-silence".format(EnName), chat_id)
    elif text in ['{} kick'.format(EnName), '{} اخراج'.format(FaName)]:
        bot.sendMessage(chat_id, "•• قفل {} بروز شد.\n•• حالت جدید :‌ اخراج کاربر".format(FaName), reply_to_message_id=message_id)
        db.srem("{}-delete".format(EnName), chat_id)
        db.sadd("{}-kick".format(EnName), chat_id)
        db.srem("{}-silence".format(EnName), chat_id)
    elif text in ['{} delete', '{} حذف'.format(FaName)]:
        bot.sendMessage(chat_id, "•• قفل {} بروز شد.\n•• حالت جدید :‌ حذف پیام".format(FaName), reply_to_message_id=message_id)
        db.sadd("{}-delete".format(EnName), chat_id)
        db.srem("{}-kick".format(EnName), chat_id)
        db.srem("{}-silence".format(EnName), chat_id)
############################################################################################
def startNewMediaLock(msg, EnName):
    content_type, chat_type, chat_id = telepot.glance(msg)
    message_id = msg['message_id']
    from_id = msg['from']['id']
    if content_type==EnName:
        if db.sismember('{}-delete'.format(EnName), chat_id):
            bot.deleteMessage((chat_id, message_id))
        elif db.sismember('{}-kick'.format(EnName), chat_id):
            bot.kickChatMember(chat_id, from_id)
            bot.deleteMessage((chat_id, message_id))
        elif db.sismember('{}-silence'.format(EnName), chat_id):
            db.sadd("silentlist-"+str(chat_id) , from_id)
            bot.deleteMessage((chat_id, message_id))
############################################################################################
def startBasicLock(msg, EnName):
    content_type, chat_type, chat_id = telepot.glance(msg)
    message_id = msg['message_id']
    from_id = msg['from']['id']
    if db.sismember('{}-delete'.format(EnName), chat_id):
        bot.deleteMessage((chat_id, message_id))
    elif db.sismember('{}-kick'.format(EnName), chat_id):
        bot.kickChatMember(chat_id, from_id)
        bot.deleteMessage((chat_id, message_id))
    elif db.sismember('{}-silence'.format(EnName), chat_id):
        db.sadd("silentlist-"+str(chat_id) , from_id)
        bot.deleteMessage((chat_id, message_id))
############################################################################################
def getLockStatus(msg, EnName):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if db.sismember("{}-delete".format(EnName), chat_id)==True:
        return "\[ 🗑 حذف پیام ]"
    elif db.sismember("{}-kick".format(EnName), chat_id)==True:
        return "\[ 🥾 اخراج کاربر ]"
    elif db.sismember("{}-silence".format(EnName), chat_id)==True:
        return "\[ 🔇 سکوت کاربر ]"
    else:
        return "\[ ➖ فاقد قفل ]"

def getLock(chat_id, EnName):
    if db.sismember("{}-delete".format(EnName), chat_id)==True:
        return "🗑 حذف پیام"
    elif db.sismember("{}-kick".format(EnName), chat_id)==True:
        return "🥾 اخراج کاربر"
    elif db.sismember("{}-silence".format(EnName), chat_id)==True:
        return "🔇 سکوت کاربر"
    else:
        return "➖ فاقد قفل"


def lockIt1(msg, name):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    chat_id = msg['message']['chat']['id']
    first_name = msg['from']['first_name']
    message_id = msg['message']['message_id']
    pmi = message_id-1
    is_user_panel = db.sismember('panel-{}-{}'.format(chat_id, from_id), message_id-1)

    if db.sismember(name+'-delete', chat_id):
        db.sadd( name+'-kick' ,chat_id)
        db.srem( name+'-delete' ,chat_id)
        db.srem( name+'-silence' ,chat_id)
    elif db.sismember(name+'-kick', chat_id):
        db.sadd( name+'-silence' ,chat_id)
        db.srem( name+'-kick' ,chat_id)
        db.srem( name+'-delete' ,chat_id)
    elif db.sismember(name+'-silence', chat_id):
        db.srem( name+'-kick' ,chat_id)
        db.srem( name+'-delete' ,chat_id)
        db.srem( name+'-silence' ,chat_id)
    else:
        db.srem( name+'-kick' ,chat_id)
        db.sadd( name+'-delete' ,chat_id)
        db.srem( name+'-silence' ,chat_id)
    
    firstPage = markup(inline_keyboard=[
        [
            btn(text='• عکس', callback_data='nothing'),btn(text=getLock(chat_id, 'photo'), callback_data='photo')
        ],
        [
            btn(text='• ویدیو', callback_data='nothing'),btn(text=getLock(chat_id, 'video'), callback_data='video')
        ],
        [
            btn(text='• گیف', callback_data='nothing'),btn(text=getLock(chat_id, 'gif'), callback_data='gif')
        ],
        [
            btn(text='• سلفی', callback_data='nothing'),btn(text=getLock(chat_id, 'video_note'), callback_data='video_note')
        ],
        [
            btn(text='• متن', callback_data='nothing'),btn(text=getLock(chat_id, 'text'), callback_data='text')
        ],
        [
            btn(text='• مخاطب', callback_data='nothing'),btn(text=getLock(chat_id, 'contact'), callback_data='contact')
        ],
        [
            btn(text='• موزیک', callback_data='nothing'),btn(text=getLock(chat_id, 'audio'), callback_data='audio')
        ],
        [
            btn(text='• مکان', callback_data='nothing'),btn(text=getLock(chat_id, 'location'), callback_data='location')
        ],
        [
            btn(text='• سند', callback_data='nothing'),btn(text=getLock(chat_id, 'document'), callback_data='document')
        ],
        [
            btn(text='• ویس', callback_data='nothing'),btn(text=getLock(chat_id, 'voice'), callback_data='voice')
        ],
        [
            btn(text='• استیکر', callback_data='nothing'),btn(text=getLock(chat_id, 'sticker'), callback_data='sticker')
        ],
        [
            btn(text='• بازی', callback_data='nothing'),btn(text=getLock(chat_id, 'game'), callback_data='game')
        ],
        [
            btn(text='•• بازگشت', callback_data='main'),btn(text='•• کانال', url='t.me/'+channel)
        ],
        [
            btn(text='•• بستن فهرست', callback_data='close')
        ]
    ])

    bot.editMessageText((chat_id, message_id), "» بخش قفل‌های مدیای گروه | شامل عکس ، ویدیو ، گیف ، مخاطب و . . ." ,parse_mode='HTML', reply_markup=firstPage )







def lockIt2(msg, name):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    chat_id = msg['message']['chat']['id']
    first_name = msg['from']['first_name']
    message_id = msg['message']['message_id']
    pmi = message_id-1
    is_user_panel = db.sismember('panel-{}-{}'.format(chat_id, from_id), message_id-1)

    if db.sismember(name+'-delete', chat_id):
        db.sadd( name+'-kick' ,chat_id)
        db.srem( name+'-delete' ,chat_id)
        db.srem( name+'-silence' ,chat_id)
    elif db.sismember(name+'-kick', chat_id):
        db.sadd( name+'-silence' ,chat_id)
        db.srem( name+'-kick' ,chat_id)
        db.srem( name+'-delete' ,chat_id)
    elif db.sismember(name+'-silence', chat_id):
        db.srem( name+'-kick' ,chat_id)
        db.srem( name+'-delete' ,chat_id)
        db.srem( name+'-silence' ,chat_id)
    else:
        db.srem( name+'-kick' ,chat_id)
        db.sadd( name+'-delete' ,chat_id)
        db.srem( name+'-silence' ,chat_id)
    
    sencond_page = markup(inline_keyboard=[
        [
            btn(text='• لینک', callback_data='nothing'),btn(text=getLock(chat_id, 'link'), callback_data='link')
        ],
        [
            btn(text='• فوروارد', callback_data='nothing'),btn(text=getLock(chat_id, 'forward'), callback_data='forward')
        ],
        [
            btn(text='• پاسخ', callback_data='nothing'),btn(text=getLock(chat_id, 'reply'), callback_data='reply')
        ],
        [
            btn(text='• تگ', callback_data='nothing'),btn(text=getLock(chat_id, 'tag'), callback_data='tag')
        ],
        [
            btn(text='• هشتگ', callback_data='nothing'),btn(text=getLock(chat_id, 'hashtag'), callback_data='hashtag')
        ],
        [
            btn(text='• انگلیسی', callback_data='nothing'),btn(text=getLock(chat_id, 'english'), callback_data='english')
        ],
        [
            btn(text='• فارسی', callback_data='nothing'),btn(text=getLock(chat_id, 'persian'), callback_data='persian')
        ],
        [
            btn(text='• فحش', callback_data='nothing'),btn(text=getLock(chat_id, 'badwords'), callback_data='badwords')
        ],
        [
            btn(text='• شکلک', callback_data='nothing'),btn(text=getLock(chat_id, 'emoji'), callback_data='emoji')
        ],
        [
            btn(text='• ویرایش', callback_data='nothing'),btn(text=getLock(chat_id, 'edit'), callback_data='edit')
        ],
        [
            btn(text='• منشن', callback_data='nothing'),btn(text=getLock(chat_id, 'mention'), callback_data='mention')
        ],
        [
            btn(text='• ورود ربات', callback_data='nothing'),btn(text=getLock(chat_id, 'bot'), callback_data='bot')
        ],
        [
            btn(text='•• بازگشت', callback_data='main'),btn(text='•• کانال', url='t.me/'+channel)
        ],
        [
            btn(text='•• بستن فهرست', callback_data='close')
        ]
    ])

    bot.editMessageText((chat_id, message_id), "» بخش قفل‌های مدیریتی گروه | شامل لینک ، فحش ، فوروارد ، تگ و . . ." ,parse_mode='HTML', reply_markup=sencond_page )







ping = [
    'آنلاینم',
    'زیاد پینگ نگیر',
    'پدرمو در اوردی',
    'نمیخوای بیخیال شی؟',
    'ای بابا',
    'ول کن دیگه',
    'بسه :/',
    'جان',
    'انلاینم بخدا',
    'نوکرتم بیخیال شو'
]

############################################################################################
def chat(msg):
    print("""
-----------------------------------------------------------------------------------------------------------------------
"""+str(msg)+"""
-----------------------------------------------------------------------------------------------------------------------
""")
    content_type, chat_type, chat_id = telepot.glance(msg)
    message_id = msg['message_id']
    from_id = msg['from']['id']
    if msg.get('text'): text = msg['text'] 
    getmember = bot.getChatMember(chat_id, from_id)
    status = getmember['status']
    db.sadd('allmsgs',str(chat_id)+str(from_id)+str(message_id))
    getmemberch = bot.getChatMember("-1001408161224", from_id)
    statusch = getmemberch['status']
    print(statusch)

    if chat_type=='private':    
        if statusch in ['creator', 'administrator', 'member']:
            if text[:6] == '/start':
                bot.sendMessage(chat_id, """» سلام ، به ربات مدیریت گروه رایگان *گپای‌پلاس* خوش اومدی!
» این سرویس ، جدیدترین ربات مدیریت گروه با امکانات متنوع میباشد و از جمله امکانات مطرح این ربات میتوان به بیش از ۲۰ قفل که هرکدام دارای قابلیت شخصی سازی هستند ، اشاره کرد.
» کافیست ربات در گروه خودتون عضو کنید ، عبارت ( نصب ) یا ( add ) رو درگروه بفرستید و شاهد قدرت این ربات فوق‌العاده باشید...

» توجه داشته باشید این سرویس همانند سرویس‌های رایگان دیگر دارای تبلیغات میباشد.
» البته شما میتوانید با پرداخت تنها ۱۰ هزار تومان ، به طور نامحدود از شر تبلیغات خلاص بشید
» تنها هدف ما رضایت شماست و ما مراعات شما را نیز میکنیم ، ربات حداکثر روزانه ۱ تبلیغ که همگی طبق قوانین کشور میباشند ارسال خواهد کرد.""", reply_to_message_id=message_id,parse_mode='markdown',reply_markup=pvmain)

        else:
            bot.sendMessage(chat_id, "•• کاربر گرامی لطفا برای استفاده از خدمات ربات ابتدا در کانال ما عضو شوید ، سپس به ربات برگشته و دستور /start را مجددا ارسال کنید.", reply_to_message_id=message_id, reply_markup=prvchannel)

    if msg.get('new_chat_member') and db.sismember('wlcmsg',chat_id):
        bot.sendMessage(chat_id, reply_to_message_id=message_id, text=db.get('welcome-'+str(chat_id)))
    if msg.get('new_chat_members'):
        for i in msg.get('new_chat_members'):
            db.sadd('joinlist-'+str(chat_id), i['id'])
    if content_type in ['photo', 'video', 'sticker', 'voice', 'audio', 'contact', 'location', 'document', 'video_note', 'game']:
        db.sadd('media-'+str(chat_id), message_id)
############################################################################################
    if content_type=='text' and from_id in sudo_users:
        if msg['text']=='ارسال':
            reply_from_id = msg['reply_to_message']['message_id']
            a = db.sdiff('groups')
            b = 0
            for i in a:
                b += 1
                bot.forwardMessage(chat_id= i, from_chat_id= chat_id, message_id=reply_from_id)
            bot.sendMessage(chat_id, "•• پیام به {} گروه ارسال شد.".format(b), reply_to_message_id=message_id)
        

        if msg['text']=='همکاران':
            b = '» لیست همکاران فعال ربات مدیریت گروه گپای‌پلاس :\n\n'
            for i in sudo_users:
                a = bot.getChat(i)
                c = a['first_name']
                d = a['id']
                b += "» <a href='tg://user?id={}'>{}</a>\n".format(str(d), str(c))
            bot.sendMessage(chat_id, b, reply_to_message_id=message_id, parse_mode='HTML', disable_web_page_preview=True)

        if msg['text']=='خروج':
            bot.leaveChat(chat_id)


        if msg['text']=='امار کلی':
            bot.sendMessage(chat_id, """•••••••• آمار کل ربات ••••••••
•• تعداد کل پیام‌ها :‌ {}
•• کل اعضا :‌ {}
•• کل گروه‌ها : {}
•• کل گروه‌های دارای تبلیغات : {}
""".format(
    db.scard('allmsgs'),
    db.scard('users'),
    db.scard('groups'),
    db.scard('ads')
), reply_to_message_id=message_id)
############################################################################################
    if (status=='creator' or status=='administrator' or from_id in sudo_users or db.sismember('admins-{}'.format(chat_id), from_id)==True):
        if msg['text'] in ['ویژه']:
            db.srem('ads',chat_id)
            bot.sendMessage(chat_id, "» گروه بمدت نامحدود ویژه شد...", reply_to_message_id=message_id)
        
        if msg['text'] in ['add', 'نصب']:
            if db.sismember('groups', chat_id):
                bot.sendMessage(chat_id, "•• این گروه از قبل در لیست من ثبت شده بود.", reply_to_message_id=message_id)
            else:
                bot.sendMessage(chat_id, "•• گروه با موفقیت به لیست گروه ها اضافه شد.\n•• جهت دریافت راهنما ، عبارت ( راهنما ) رو ارسال کنین.", reply_to_message_id=message_id)
                a = bot.getChatMembersCount(chat_id)
                b = bot.getChatMember(chat_id, from_id)
                c = msg['chat']['title']
                bot.sendMessage(logs, """
•• یک گروه جدید اضافه شد...

• تعداد اعضا : {}
• توسط : {}
• آیدی گروه : {}
• نام گروه : {}
""".format(
    a,
    str(from_id)+" - @"+b['user']['username'],
    chat_id,
    c
))
                db.sadd('groups', chat_id)
                db.sadd('ads', chat_id)
############################################################################################
        elif msg['text'] in ['rem', 'حذف']:
            if db.sismember('groups', chat_id):
                bot.sendMessage(chat_id, "•• گروه با موفقیت از لیست گروه ها حذف شد.", reply_to_message_id=message_id)
                a = bot.getChatMembersCount(chat_id)
                b = bot.getChatMember(chat_id, from_id)
                c = msg['chat']['title']
                bot.sendMessage(logs, """
•• یک گروه از لیست حذف شد...

• تعداد اعضا : {}
• توسط : {}
• آیدی گروه : {}
• نام گروه : {}
""".format(
    a,
    str(from_id)+" - @"+b['user']['username'],
    chat_id,
    c
))
                db.srem('groups', chat_id)
                db.srem('ads', chat_id)
            else:
                bot.sendMessage(chat_id, "•• این گروه در لیست من نبود...", reply_to_message_id=message_id)
############################################################################################
    
    if status=='member' and from_id not in sudo_users:
        ############################################################################################
        if msg and db.sismember("lockall", chat_id):
            bot.deleteMessage((chat_id, message_id))
        else:
            if msg.get('forward_date'):
                startBasicLock(msg, 'forward')
            if msg and db.sismember("silentlist-"+str(chat_id), from_id):
                bot.deleteMessage((chat_id, message_id))
            if db.sismember("banlist-"+str(chat_id), from_id):
                bot.kickChatMember(chat_id, from_id)
            if msg.get('new_chat_member'):
                db.sadd('joinlist-'+str(chat_id), msg['new_chat_member']['id'])
                if msg['new_chat_member']['is_bot']==True:
                    if db.sismember("bot-kick", chat_id):
                        bot.kickChatMember(chat_id, msg['new_chat_member']['id'])
                        bot.kickChatMember(chat_id, from_id)
                    elif db.sismember("bot-silence", chat_id):
                        bot.kickChatMember(chat_id, msg['new_chat_member']['id'])
                        db.sadd('silentlist-'+str(chat_id), from_id)
                    elif db.sismember("bot-delete", chat_id):
                        bot.kickChatMember(chat_id, msg['new_chat_member']['id'])
                        bot.deleteMessage((chat_id, message_id))
        ############################################################################################
            if msg.get('edit_date'):
                startBasicLock(msg, 'edit')
            if int(db.get('char-'+str(chat_id))) < len(msg['text']):
                bot.deleteMessage((chat_id, message_id))
            if msg.get('sticker'):
                startBasicLock(msg, 'sticker')
            if msg.get('animation'):
                startBasicLock(msg, 'gif')
            for i in db.smembers('filterlist-'+str(chat_id)):
                if re.search(i, msg['text']):
                    bot.deleteMessage((chat_id, message_id))
            if msg.get('entities'):
                if msg['entities'][0]['type']=='text_mention':
                    startBasicLock(msg, 'mention')
            if re.search('\@', msg['text']):
                startBasicLock(msg, 'tag')
            if re.search('\#', msg['text']):
                startBasicLock(msg, 'hashtag')
            if re.search('http', msg['text']) or re.search('t.me', msg['text']) or re.search('t . m', msg['text']) or re.search('.com', msg['text']) or re.search('www', msg['text']) or re.search('.net', msg['text']) or re.search('.org', msg['text']) or re.search('.ir', msg['text']):
                startBasicLock(msg, 'link')
            if re.search('a', str(msg['text']).lower()) or re.search('b', str(msg['text']).lower()) or re.search('c', str(msg['text']).lower()) or re.search('d', str(msg['text']).lower()) or re.search('e', str(msg['text']).lower()) or re.search('f', str(msg['text']).lower()) or re.search('g', str(msg['text']).lower()) or re.search('h', str(msg['text']).lower()) or re.search('i', str(msg['text']).lower()) or re.search('j', str(msg['text']).lower()) or re.search('k', str(msg['text']).lower()) or re.search('l', str(msg['text']).lower()) or re.search('m', str(msg['text']).lower()) or re.search('n', str(msg['text']).lower()) or re.search('o', str(msg['text']).lower()) or re.search('p', str(msg['text']).lower()) or re.search('q', str(msg['text']).lower()) or re.search('r', str(msg['text']).lower()) or re.search('s', str(msg['text']).lower()) or re.search('t', str(msg['text']).lower()) or re.search('u', str(msg['text']).lower()) or re.search('v', str(msg['text']).lower()) or re.search('w', str(msg['text']).lower()) or re.search('x', str(msg['text']).lower()) or re.search('y', str(msg['text']).lower()) or re.search('z', str(msg['text']).lower()):
                startBasicLock(msg, 'english')
            if re.search('آ', str(msg['text']).lower()) or re.search('ا', str(msg['text']).lower()) or re.search('ب', str(msg['text']).lower()) or re.search('پ', str(msg['text']).lower()) or re.search('ت', str(msg['text']).lower()) or re.search('ث', str(msg['text']).lower()) or re.search('ج', str(msg['text']).lower()) or re.search('چ', str(msg['text']).lower()) or re.search('ح', str(msg['text']).lower()) or re.search('خ', str(msg['text']).lower()) or re.search('د', str(msg['text']).lower()) or re.search('ذ', str(msg['text']).lower()) or re.search('ر', str(msg['text']).lower()) or re.search('ز', str(msg['text']).lower()) or re.search('ژ', str(msg['text']).lower()) or re.search('س', str(msg['text']).lower()) or re.search('ش', str(msg['text']).lower()) or re.search('ص', str(msg['text']).lower()) or re.search('ض', str(msg['text']).lower()) or re.search('ط', str(msg['text']).lower()) or re.search('ظ', str(msg['text']).lower()) or re.search('ع', str(msg['text']).lower()) or re.search('غ', str(msg['text']).lower()) or re.search('ف', str(msg['text']).lower()) or re.search('ق', str(msg['text']).lower()) or re.search('ک', str(msg['text']).lower()) or re.search('گ', str(msg['text']).lower()) or re.search('ل', str(msg['text']).lower()) or re.search('م', str(msg['text']).lower()) or re.search('ن', str(msg['text']).lower()) or re.search('و', str(msg['text']).lower()) or re.search('ه', str(msg['text']).lower()) or re.search('ی', str(msg['text']).lower()):
                startBasicLock(msg, 'persian')
            if re.search('کیر', msg['text']) or re.search('کوص', msg['text']) or re.search('کوس', msg['text']) or re.search('کون', msg['text']) or re.search('کس', msg['text']) or re.search('کص', msg['text']) or re.search('ننه', msg['text']):
                startBasicLock(msg, 'badwords')
            if re.search('😐', msg['text']) or re.search('😂', msg['text']) or re.search('❤️', msg['text']) or re.search('😭', msg['text']) or re.search('😁', msg['text']) or re.search('😢', msg['text']) or re.search('😍', msg['text']):
                startBasicLock(msg, 'emoji')
            # All of locks to delete here...
            startNewMediaLock(msg, 'photo')
            startNewMediaLock(msg, 'video')
            startNewMediaLock(msg, 'contact')
            startNewMediaLock(msg, 'video_note')
            startNewMediaLock(msg, 'audio')
            startNewMediaLock(msg, 'voice')
            startNewMediaLock(msg, 'gif')
            startNewMediaLock(msg, 'text')
            startNewMediaLock(msg, 'document')
            startNewMediaLock(msg, 'location')
            startNewMediaLock(msg, 'game')
############################################################################################
    if chat_type=='supergroup' and db.sismember('groups', chat_id) :
        if content_type=='text':
            text = msg['text']
            sptext = str(text).split(' ')
############################################################################################
            if msg['text'] in ['info', 'اطلاعات']:
                reply_from_id = msg['reply_to_message']['from']['id']
                reply_name = msg['reply_to_message']['from']['first_name']
                reply_username = msg['reply_to_message']['from']['username']
                bot.sendMessage(chat_id, """•• آیدی : <code>{}</code>
•• آیدی چت : <code>{}</code>
•• نام : {}
•• یوزرنیم : @{}""".format(reply_from_id , chat_id, reply_name,reply_username), reply_to_message_id=message_id, parse_mode='HTML')
############################################################################################
            elif msg['text'] in ['id', 'ایدی']:
                pic = bot.getUserProfilePhotos(from_id)['photos'][0][0]['file_id']
                print(pic)
                bot.sendPhoto(chat_id,photo=pic, caption="""•• آیدی شما : `{}`
•• آیدی چت : `{}`
•• آیدی پیام : {}
•• نام شما : {}
•• یوزرنیم شما : @{}""".format(from_id, chat_id, message_id, msg['from']['first_name'],msg['from']['username']), reply_to_message_id=message_id, parse_mode='markdown')
############################################################################################
            elif msg['text'] in ['ping', 'وضعیت', 'bot', 'online', 'انلاینی','ربات']:
                pn = random.choice(ping)
                bot.sendMessage(chat_id, pn, reply_to_message_id=message_id)
############################################################################################
            if status in ['creator', 'administrator'] or from_id in sudo_users or db.sismember('admins-{}'.format(chat_id), from_id)==True:
                # All of media locks are here to code...
                defineNewMediaLock(msg, 'text', 'متن')
                defineNewMediaLock(msg, 'photo', 'عکس')
                defineNewMediaLock(msg, 'sticker', 'استیکر')
                defineNewMediaLock(msg, 'video', 'ویدیو')
                defineNewMediaLock(msg, 'contact', 'مخاطب')
                defineNewMediaLock(msg, 'audio', 'موزیک')
                defineNewMediaLock(msg, 'voice', 'ویس')
                defineNewMediaLock(msg, 'document', 'سند')
                defineNewMediaLock(msg, 'location', 'مکان')
                defineNewMediaLock(msg, 'game', 'بازی')
                defineNewMediaLock(msg, 'gif', 'گیف')
                # Other locks
                defineNewMediaLock(msg, 'link', 'لینک')
                defineNewMediaLock(msg, 'tag', 'تگ')
                defineNewMediaLock(msg, 'hashtag', 'هشتگ')
                defineNewMediaLock(msg, 'english', 'انگلیسی')
                defineNewMediaLock(msg, 'persian', 'فارسی')
                defineNewMediaLock(msg, 'reply', 'پاسخ')
                defineNewMediaLock(msg, 'badwords', 'فحش')
                defineNewMediaLock(msg, 'emoji', 'شکلک')
                defineNewMediaLock(msg, 'forward', 'فوروارد')
                defineNewMediaLock(msg, 'bot', 'ربات')
                defineNewMediaLock(msg, 'mention', 'منشن')
                defineNewMediaLock(msg, 'edit', 'ویرایش')
                
                
                if text in ['lock video note', 'قفل فیلم سلفی']:
                    bot.sendMessage(chat_id, "•• قفل فیلم سلفی فعال شد.\n•• حالت قفل : حذف پیام", reply_to_message_id=message_id)
                    db.sadd("video_note-delete", chat_id)
                elif text in ['unlock video_note', 'بازکردن فیلم سلفی']:
                    bot.sendMessage(chat_id, "•• قفل فیلم سلفی غیرفعال شد.", reply_to_message_id=message_id)
                    db.srem("video_note-delete", chat_id)
                    db.srem("video_note-kick", chat_id)
                    db.srem("video_note-silence", chat_id)
                elif text in ['video note silence', 'فیلم سلفی سکوت']:
                    bot.sendMessage(chat_id, "•• قفل فیلم سلفی بروز شد.\n•• حالت جدید :‌ سکوت کاربر", reply_to_message_id=message_id)
                    db.srem("video_note-delete", chat_id)
                    db.srem("video_note-kick", chat_id)
                    db.sadd("video_note-silence", chat_id)
                elif text in ['video note kick', 'فیلم سلفی اخراج']:
                    bot.sendMessage(chat_id, "•• قفل فیلم سلفی بروز شد.\n•• حالت جدید :‌ اخراج کاربر", reply_to_message_id=message_id)
                    db.srem("video_note-delete", chat_id)
                    db.sadd("video_note-kick", chat_id)
                    db.srem("video_note-silence", chat_id)
                elif text in ['video note delete', 'فیلم سلفی حذف']:
                    bot.sendMessage(chat_id, "•• قفل فیلم سلفی بروز شد.\n•• حالت جدید :‌ حذف پیام", reply_to_message_id=message_id)
                    db.sadd("video_note-delete", chat_id)
                    db.srem("video_note-kick", chat_id)
                    db.srem("video_note-silence", chat_id)
############################################################################################
                if sptext[0] in ['setname', 'نام']:
                    new_text = str(text).replace('setname ', '')
                    new_text = str(new_text).replace('نام ', '')
                    bot.setChatTitle(chat_id, new_text)
############################################################################################
                
############################################################################################
                elif text in ['pin','سنجاق'] and msg.get('reply_to_message'):
                    reply_message_id = msg['reply_to_message']['message_id']
                    bot.pinChatMessage(chat_id, reply_message_id)
                elif text in ['unpin','حذف سنجاق']:
                    bot.unpinChatMessage(chat_id)
                

                elif text in ['stats','امار']:
                    bot.sendMessage(chat_id, """ ••• آمار در ساعت : <b>({})</b>

•• مجموع مدیای ارسالی : {}
•• کاربران سکوت : {}
•• کاربران محروم : {}
•• کاربران عضو شده : {}
•• کل پیام‌ها :‌ {}
""".format(
    time.ctime(),
    db.scard('media-'+str(chat_id)),
    db.scard('silentlist-'+str(chat_id)),
    db.scard('banlist-'+str(chat_id)),
    db.scard('joinlist-'+str(chat_id)),
    message_id
) , reply_to_message_id=message_id, parse_mode='HTML')

############################################################################################
                elif text in ['admin list', 'لیست مدیران']:
                    admins = bot.getChatAdministrators(chat_id)
                    b = ""
                    a = ""
                    for i in admins:
                        st = bot.getChatMember(chat_id, i['user']['id'])['status']
                        if st=='creator':
                            a += "• سازنده : <a href='tg://user?id={1}'>{0}</a>\n".format(i['user']['first_name'],i['user']['id'])
                        else:
                            b += "• مدیر : <a href='tg://user?id={1}'>{0}</a>\n".format(i['user']['first_name'],i['user']['id'])
                    bot.sendMessage(chat_id, "•• لیست مدیران گروه :\n\n"+a+b, reply_to_message_id=message_id, parse_mode='HTML')
############################################################################################
                elif text in ['help', 'راهنما']:
                    db.sadd("panel-{}-{}".format(chat_id, from_id), message_id)
                    bot.sendMessage(chat_id, """••• بخش مورد نظر خود را انتخاب نمایید | قفلی ، مدیریتی و . . .""", reply_to_message_id=message_id, parse_mode='markdown', disable_web_page_preview=True, reply_markup=help)
############################################################################################
                elif sptext[0] in ['ban','محروم']:
                    if msg.get('reply_to_message')!=None:
                        reply_from_id = msg['reply_to_message']['from']['id']
                        new_status = bot.getChatMember(chat_id, reply_from_id)['status']
                        if new_status=='member' and reply_from_id not in sudo_users:
                            bot.kickChatMember(chat_id, reply_from_id)
                            db.sadd('banlist-'+str(chat_id), reply_from_id)
                            bot.sendMessage(chat_id, "•• کاربر [{0}](tg://user?id={0}) توسط [{1}](tg://user?id={1}) از گروه اخراج شد.".format(reply_from_id, from_id), reply_to_message_id=message_id, parse_mode='Markdown')
                        else:
                            bot.sendMessage(chat_id, "•• من توانایی اخراج مدیران را ندارم.", reply_to_message_id=message_id)
                    else:
                        reply_from_id = sptext[1]
                        new_status = bot.getChatMember(chat_id, reply_from_id)['status']
                        if new_status=='member' and reply_from_id not in sudo_users:
                            bot.kickChatMember(chat_id, reply_from_id)
                            db.sadd('banlist-'+str(chat_id), reply_from_id)
                            bot.sendMessage(chat_id, "•• کاربر [{0}](tg://user?id={0}) توسط [{1}](tg://user?id={1}) از گروه اخراج شد.".format(reply_from_id, from_id), reply_to_message_id=message_id, parse_mode='Markdown')
                        else:
                            bot.sendMessage(chat_id, "•• من توانایی انجام این کار را ندارم...\n••این مشکل ممکن است به دلایل زیر رخ داده باشد : \n\n• ۱. کاربر مدیر باشد\n• ۲. کاربر در گروه حضور نداشته باشد\n• ۳. آیدی کاربر نادرست باشد", reply_to_message_id=message_id)
############################################################################################
                elif text in ['lock all','قفل همه']:
                    locks = ['lockall', 'mention','edit','reply','forward','gif' ,'photo', 'video', 'sticker', 'link', 'text', 'voice', 'audio', 'contact', 'location', 'document', 'video_note', 'game', 'persian', 'english', 'tag', 'hashtag', 'badwords', 'emoji','bot']
                    for i in locks:
                        db.sadd(i+'-delete', chat_id)
                        db.srem(i+'-kick', chat_id)
                        db.srem(i+'-silence', chat_id)
                    bot.sendMessage(chat_id, "•• قفل همگانی فعال گردید.", reply_to_message_id=message_id, parse_mode='Markdown')
############################################################################################
                elif text in ['unlock all','بازکردن همه']:
                    locks = ['lockall', 'mention','edit', 'reply','forward','gif' , 'photo', 'video', 'sticker', 'link', 'text', 'voice', 'audio', 'contact', 'location', 'document', 'video_note', 'game', 'persian', 'english', 'tag', 'hashtag', 'badwords', 'emoji','bot']
                    for i in locks:
                        db.srem(i+'-delete', chat_id)
                        db.srem(i+'-kick', chat_id)
                        db.srem(i+'-silence', chat_id)
                    bot.sendMessage(chat_id, "•• قفل همگانی غیرفعال گردید.", reply_to_message_id=message_id, parse_mode='Markdown')
############################################################################################

                elif re.search('تنظیم درباره',text):
                    text = text.replace('تنظیم درباره','')
                    bot.setChatDescription(chat_id, description=text)
                    bot.sendMessage(chat_id, "•• (درباره‌ی گروه) به : \n%s\nتنظیم شد." % (text) , reply_to_message_id=message_id, parse_mode='Markdown')

                elif re.search('تنظیم لینک',text):
                    text = text.replace('تنظیم لینک','')
                    db.set('link-'+str(chat_id), text)
                    bot.sendMessage(chat_id, "•• (لینک گروه) به : \n%s\nتنظیم شد." % (text) , reply_to_message_id=message_id, parse_mode='Markdown')

                elif re.search('تنظیم اخطار',text):
                    text = text.replace('تنظیم اخطار','')
                    db.set('warn-'+str(chat_id), text)
                    bot.sendMessage(chat_id, "•• (حساسیت اخطار گروه) به : \n%s\nتنظیم شد." % (text) , reply_to_message_id=message_id, parse_mode='Markdown')

                elif re.search('تنظیم خوشامد',text):
                    text = text.replace('تنظیم خوشامد','')
                    db.set('welcome-'+str(chat_id), text)
                    bot.sendMessage(chat_id, "•• (متن خوشامدگویی گروه) به : \n%s\nتنظیم شد." % (text) , reply_to_message_id=message_id, parse_mode='Markdown')

                elif re.search('تنظیم کاراکتر',text):
                    text = text.replace('تنظیم کاراکتر','')
                    db.set('char-'+str(chat_id), text)
                    bot.sendMessage(chat_id, "•• (حساسیت کاراکتر گروه) به : \n%s\nتنظیم شد." % (text) , reply_to_message_id=message_id, parse_mode='Markdown')

                elif text in ['خوشامدگویی روشن']:
                    if db.sismember('wlcmsg', chat_id):
                        bot.sendMessage(chat_id, "•• خوشامدگویی به اعضای جدید از قبل روشن بود." , reply_to_message_id=message_id, parse_mode='Markdown')
                    else:
                        db.sadd('wlcmsg', chat_id)
                        bot.sendMessage(chat_id, "•• خوشامدگویی به اعضای جدید روشن شد." , reply_to_message_id=message_id, parse_mode='Markdown')
                elif text in ['خوشامدگویی خاموش']:
                    if db.sismember('wlcmsg', chat_id):
                        db.srem('wlcmsg', chat_id)
                        bot.sendMessage(chat_id, "•• خوشامدگویی به اعضای جدید خاموش شد." , reply_to_message_id=message_id, parse_mode='Markdown')
                    else:
                        bot.sendMessage(chat_id, "•• خوشامدگویی به اعضای جدید از قبل خاموش بود." , reply_to_message_id=message_id, parse_mode='Markdown')


                elif sptext[0]=='حذف' and sptext[1]=='فیلتر':
                    text = text.replace('حذف فیلتر ','')
                    db.srem('filterlist-'+str(chat_id), text)
                    bot.sendMessage(chat_id, "•• عبارت \[ %s ] از لیست فیلتر حذف شد." % (text) , reply_to_message_id=message_id, parse_mode='Markdown')


                elif sptext[0]=='فیلتر':
                    text = text.replace('فیلتر ','')
                    db.sadd('filterlist-'+str(chat_id), text)
                    bot.sendMessage(chat_id, "•• عبارت \[ %s ] فیلتر شد." % (text) , reply_to_message_id=message_id, parse_mode='Markdown')
          
                
                elif text in ['link','لینک']:
                    if db.get('link-'+str(chat_id))!=None:
                        link = db.get('link-'+str(chat_id))
                        title = msg['chat']['title']
                        bot.sendMessage(chat_id, "•• لینک گروه : \n•• "+link, disable_web_page_preview=True, reply_to_message_id=message_id, parse_mode='Markdown')
                    else:
                        bot.sendMessage(chat_id, "•• لینک گروه ثبت نشده است ، به راهنما مراجعه کنید." , reply_to_message_id=message_id)

                elif text in ['link pv','لینک پیوی']:
                    if db.get('link-'+str(chat_id))!=None:
                        link = db.get('link-'+str(chat_id))
                        bot.sendMessage(from_id, "•• لینک گروه :\n•• "+link,disable_web_page_preview=True, parse_mode='html')
                        bot.sendMessage(chat_id, "•• لینک گروه به پیوی شما ارسال شد.")
                    else:
                        bot.sendMessage(chat_id, "•• لینک گروه ثبت نشده است ، به راهنما مراجعه کنید." , reply_to_message_id=message_id)

                elif text == 'لینک جدید':
                    link = bot.exportChatInviteLink(chat_id)
                    db.set('link-'+str(chat_id), link)
                    bot.sendMessage(chat_id, "•• لینک قبلی باطل و لینک جدید ساخته و ثبت شد.\n•• "+link,disable_web_page_preview=True , parse_mode='html' , reply_to_message_id=message_id)

############################################################################################
                elif text in ['clean silent list','پاکسازی لیست سکوت']:
                    db.delete('silentlist-'+str(chat_id))
                    bot.sendMessage(chat_id, "•• لیست سکوت پاکسازی شد.", reply_to_message_id=message_id, parse_mode='Markdown')
                elif text in ['silent list','لیست سکوت']:
                    members = db.smembers('silentlist-'+str(chat_id))
                    a = ""
                    if db.scard('silentlist-'+str(chat_id))==0:
                        a = "•• گروه فاقد کاربری در حالت سکوت میباشد."
                    else:
                        for i in members:
                            i = bot.getChatMember(chat_id, i)
                            a += "• کاربر :‌  <a href='tg://user?id={1}'>{0}</a> - <code>{1}</code>\n ".format(i['user']['first_name'],i['user']['id'])
                    bot.sendMessage(chat_id, "•• لیست آیدی‌های افراد بیصدا در گروه شما به شرح زیر است : \n\n"+a, reply_to_message_id=message_id, parse_mode='html')


                elif text in ['clean ban list','پاکسازی لیست محروم']:
                    db.delete('banlist-'+str(chat_id))
                    bot.sendMessage(chat_id, "•• لیست محروم پاکسازی شد.", reply_to_message_id=message_id, parse_mode='Markdown')
                elif text in ['ban list','لیست محروم']:
                    members = db.smembers('banlist-'+str(chat_id))
                    a = ""
                    if db.scard('banlist-'+str(chat_id))==0:
                        a = "•• گروه فاقد کاربری در حالت محرومیت میباشد."
                    else:
                        for i in members:
                            i = bot.getChatMember(chat_id, i)
                            a += "• کاربر :‌  <a href='tg://user?id={1}'>{0}</a> - <code>{1}</code>\n ".format(i['user']['first_name'],i['user']['id'])
                    bot.sendMessage(chat_id, "•• لیست آیدی‌های افراد محروم در گروه شما به شرح زیر است : \n\n"+a, reply_to_message_id=message_id, parse_mode='html')

                
                elif text in ['clean filter list','پاکسازی لیست فیلتر']:
                    db.delete('filterlist-'+str(chat_id))
                    bot.sendMessage(chat_id, "•• لیست فیلتر پاکسازی شد.", reply_to_message_id=message_id, parse_mode='Markdown')
                elif text in ['filter list','لیست فیلتر']:
                    members = db.smembers('filterlist-'+str(chat_id))
                    a = ""
                    if db.scard('filterlist-'+str(chat_id))==0:
                        a = "•• گروه فاقد عبارت فیلترشده میباشد."
                    else:
                        for i in members:
                            a += "• عبارت :‌ {0}\n".format(i)
                    bot.sendMessage(chat_id, "•• لیست عبارات فیلترشده در گروه شما به شرح زیر است : \n\n"+a, reply_to_message_id=message_id, parse_mode='html')

                
                elif text in ['clean join list','پاکسازی لیست جوین']:
                    db.delete('joinlist-'+str(chat_id))
                    bot.sendMessage(chat_id, "•• لیست جوین پاکسازی شد.", reply_to_message_id=message_id, parse_mode='Markdown')
                elif text in ['join list','لیست جوین']:
                    members = db.smembers('joinlist-'+str(chat_id))
                    a = ""
                    if db.scard('joinlist-'+str(chat_id))==0:
                        a = "•• گروه فاقد کاربر جدیدی میباشد."
                    else:
                        for i in members:
                            i = bot.getChatMember(chat_id, i)
                            a += "• کاربر :‌  <a href='tg://user?id={1}'>{0}</a> - <code>{1}</code>\n ".format(i['user']['first_name'],i['user']['id'])
                    bot.sendMessage(chat_id, "» لیست جدیدترین اعضای گروه شما هم اکنون به شرح زیر است :\n\n"+str(a) ,parse_mode='HTML', reply_to_message_id=message_id )


############################################################################################
                elif sptext[0] in ['unban','مجاز']:
                    if msg.get('reply_to_message'):
                        reply_from_id = msg['reply_to_message']['from']['id']
                        new_status = bot.getChatMember(chat_id, reply_from_id)['status']
                        if reply_from_id not in sudo_users:
                            bot.unbanChatMember(chat_id, reply_from_id)
                            db.srem('banlist-'+str(chat_id), reply_from_id)
                            bot.sendMessage(chat_id, "•• کاربر [{0}](tg://user?id={0}) توسط [{1}](tg://user?id={1}) لغو محرومیت شد.".format(reply_from_id, from_id), reply_to_message_id=message_id, parse_mode='Markdown')
                    else:
                        reply_from_id = sptext[1]
                        new_status = bot.getChatMember(chat_id, reply_from_id)['status']
                        if reply_from_id not in sudo_users:
                            bot.unbanChatMember(chat_id, reply_from_id)
                            db.srem('banlist-'+str(chat_id), reply_from_id)
                            bot.sendMessage(chat_id, "•• کاربر [{0}](tg://user?id={0}) توسط [{1}](tg://user?id={1}) لغو محرومیت شد.".format(reply_from_id, from_id), reply_to_message_id=message_id, parse_mode='Markdown')

############################################################################################
                elif text in ['settings', 'تنظیمات']:
                    bot.sendMessage(chat_id, """•••* تنظیمات قفل گروه:*

•• *قفل‌ها :*
• عکس : {}
• متن : {}
• ویدیو : {}
• استیکر : {}
• گیف : {}
• ویس : {}
•‌ موزیک : {}
• مخاطب : {}
• فیلم سلفی : {}
• مکان : {}
• سند : {}
•‌ بازی : {}

• لینک : {}
• فوروارد : {}
• پاسخ : {}
•‌ تگ : {}
• هشتگ : {}
• فارسی : {}
• انگلیسی : {}
• فحش : {}
• شکلک : {}
• ویرایش : {}
• منشن : {}
• ورود ربات‌ها : {}

• تعداد اعضا : {}
• تعداد پیام‌ها : {}
• لیست سکوت : {}

•• درخواست توسط [{}](tg://user?id={})""".format(
    getLockStatus(msg,'photo'),
    getLockStatus(msg,'text'),
    getLockStatus(msg,'video'),
    getLockStatus(msg,'sticker'),
    getLockStatus(msg,'gif'),
    getLockStatus(msg,'voice'),
    getLockStatus(msg,'audio'),
    getLockStatus(msg,'contact'),
    getLockStatus(msg,'video_note'),
    getLockStatus(msg,'location'),
    getLockStatus(msg,'document'),
    getLockStatus(msg,'game'),
    getLockStatus(msg,'link'),
    getLockStatus(msg,'forward'),
    getLockStatus(msg,'reply'),
    getLockStatus(msg,'tag'),
    getLockStatus(msg,'hashtag'),
    getLockStatus(msg,'persian'),
    getLockStatus(msg,'english'),
    getLockStatus(msg,'badwords'),
    getLockStatus(msg,'emoji'),
    getLockStatus(msg,'edit'),
    getLockStatus(msg,'mention'),
    getLockStatus(msg,'bot'),
    str(bot.getChatMembersCount(chat_id)),
    str(message_id),
    str(db.scard('silentlist-'+str(chat_id))),
    msg['from']['first_name'],
    from_id
), reply_to_message_id=message_id, parse_mode='Markdown')
############################################################################################
                elif re.search('حذف پیام', text) or re.search('del', text):
                    mes = text.replace('del ','')
                    mes = mes.replace('حذف پیام ', '')
                    if 0 < int(mes) <= 150:
                        bot.sendMessage(chat_id, "» در حال انجام عملیات ..." , reply_to_message_id=message_id, parse_mode='HTML')
                        for i in range(message_id-int(mes), message_id+1):
                            try:
                                bot.deleteMessage((chat_id, i))
                            except:
                                pass
                        bot.sendMessage(chat_id, "» تعداد %d پیام با موفقیت حذف شد." % int(mes), parse_mode='HTML')
                    else:
                        bot.sendMessage(chat_id, "» تعداد باید بین ۱ تا ۱۵۰ باشد." , reply_to_message_id=message_id, parse_mode='HTML')
############################################################################################
                elif text in ['menu', 'فهرست']:
                    if statusch in ['creator', 'administrator', 'member']:
                        db.sadd("panel-{}-{}".format(chat_id, from_id), message_id)
                        bot.sendMessage(chat_id, """» فهرست مدیریت آسان‌ | جهت دسترسی به هربخش کافیست روی آن کلیک کنید.
•• درخواست توسط <a href='tg://user?id={1}'>{0}</a>""".format(msg['from']['first_name'],from_id), reply_to_message_id=message_id, parse_mode='HTML',reply_markup=panel)
                    else:
                        bot.sendMessage(chat_id, '» مدیریت محترم جهت استفاده از فهرست شما باید در کانال ما عضو شده باشید.', reply_to_message_id=message_id,reply_markup=prvchannel)
############################################################################################
                elif sptext[0] in ['mute', 'بیصدا']:
                    if msg.get('reply_to_message'):
                        reply_from_id = msg['reply_to_message']['from']['id']
                        new_status = bot.getChatMember(chat_id, reply_from_id)['status']
                        if new_status=='member' and reply_from_id not in sudo_users:
                            db.sadd('silentlist-'+str(chat_id), reply_from_id)
                            bot.sendMessage(chat_id, "•• کاربر [{0}](tg://user?id={0}) توسط [{1}](tg://user?id={1}) به حالت سکوت وارد شد.".format(reply_from_id, from_id), reply_to_message_id=message_id, parse_mode='Markdown')
                        else:
                            bot.sendMessage(chat_id, "•• •• من توانایی انجام این کار را ندارم...\n••این مشکل ممکن است به دلایل زیر رخ داده باشد : \n\n• ۱. کاربر مدیر باشد\n• ۲. کاربر در گروه حضور نداشته باشد\n• ۳. آیدی کاربر نادرست باشد", reply_to_message_id=message_id)
                    else:
                        reply_from_id = sptext[1]
                        try:
                            new_status = bot.getChatMember(chat_id, reply_from_id)['status']
                            if new_status=='member' and reply_from_id not in sudo_users:
                                db.sadd('silentlist-'+str(chat_id), reply_from_id)
                                bot.sendMessage(chat_id, "•• کاربر [{0}](tg://user?id={0}) توسط [{1}](tg://user?id={1}) به حالت سکوت وارد شد.".format(reply_from_id, from_id), reply_to_message_id=message_id, parse_mode='Markdown')
                            else:
                                bot.sendMessage(chat_id, "•• •• من توانایی انجام این کار را ندارم...\n••این مشکل ممکن است به دلایل زیر رخ داده باشد : \n\n• ۱. کاربر مدیر باشد\n• ۲. کاربر در گروه حضور نداشته باشد\n• ۳. آیدی کاربر نادرست باشد", reply_to_message_id=message_id)
                        except:
                            bot.sendMessage(chat_id, "•• این کاربر در سیستم یا در گروه وجود ندارد.", reply_to_message_id=message_id)
############################################################################################
                elif sptext[0] in ['unmute', 'باصدا'] and msg['reply_to_message']:
                    if msg.get('reply_to_message'):
                        reply_from_id = msg['reply_to_message']['from']['id']
                        new_status = bot.getChatMember(chat_id, reply_from_id)['status']
                        if new_status=='member' and reply_from_id not in sudo_users:
                            db.srem('silentlist-'+str(chat_id), reply_from_id)
                            bot.sendMessage(chat_id, "•• کاربر [{0}](tg://user?id={0}) توسط [{1}](tg://user?id={1}) از حالت سکوت خارج شد.".format(reply_from_id, from_id), reply_to_message_id=message_id, parse_mode='Markdown')
                        else:
                            bot.sendMessage(chat_id, "•• •• من توانایی انجام این کار را ندارم...\n••این مشکل ممکن است به دلایل زیر رخ داده باشد : \n\n• ۱. کاربر مدیر باشد\n• ۲. کاربر در گروه حضور نداشته باشد\n• ۳. آیدی کاربر نادرست باشد", reply_to_message_id=message_id)
                    else:
                        reply_from_id = sptext[1]
                        try:
                            new_status = bot.getChatMember(chat_id, reply_from_id)['status']
                            if new_status=='member' and reply_from_id not in sudo_users:
                                db.srem('silentlist-'+str(chat_id), reply_from_id)
                                bot.sendMessage(chat_id, "•• کاربر [{0}](tg://user?id={0}) توسط [{1}](tg://user?id={1}) از حالت سکوت خارج شد.".format(reply_from_id, from_id), reply_to_message_id=message_id, parse_mode='Markdown')
                            else:
                                bot.sendMessage(chat_id, "•• •• من توانایی انجام این کار را ندارم...\n••این مشکل ممکن است به دلایل زیر رخ داده باشد : \n\n• ۱. کاربر مدیر باشد\n• ۲. کاربر در گروه حضور نداشته باشد\n• ۳. آیدی کاربر نادرست باشد", reply_to_message_id=message_id)
                        except:
                            bot.sendMessage(chat_id, "•• این کاربر در سیستم یا در گروه وجود ندارد.", reply_to_message_id=message_id)
############################################################################################

def inlines(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    chat_id = msg['message']['chat']['id']
    chat_type = msg['message']['chat']['type']
    first_name = msg['from']['first_name']
    message_id = msg['message']['message_id']
    pmi = message_id-1
    is_user_panel = db.sismember('panel-{}-{}'.format(chat_id, from_id), message_id-1)

    firstPage = markup(inline_keyboard=[
        [
            btn(text='• عکس', callback_data='nothing'),btn(text=getLock(chat_id, 'photo'), callback_data='photo')
        ],
        [
            btn(text='• ویدیو', callback_data='nothing'),btn(text=getLock(chat_id, 'video'), callback_data='video')
        ],
        [
            btn(text='• گیف', callback_data='nothing'),btn(text=getLock(chat_id, 'gif'), callback_data='gif')
        ],
        [
            btn(text='• سلفی', callback_data='nothing'),btn(text=getLock(chat_id, 'video_note'), callback_data='video_note')
        ],
        [
            btn(text='• متن', callback_data='nothing'),btn(text=getLock(chat_id, 'text'), callback_data='text')
        ],
        [
            btn(text='• مخاطب', callback_data='nothing'),btn(text=getLock(chat_id, 'contact'), callback_data='contact')
        ],
        [
            btn(text='• موزیک', callback_data='nothing'),btn(text=getLock(chat_id, 'audio'), callback_data='audio')
        ],
        [
            btn(text='• مکان', callback_data='nothing'),btn(text=getLock(chat_id, 'location'), callback_data='location')
        ],
        [
            btn(text='• سند', callback_data='nothing'),btn(text=getLock(chat_id, 'document'), callback_data='document')
        ],
        [
            btn(text='• ویس', callback_data='nothing'),btn(text=getLock(chat_id, 'voice'), callback_data='voice')
        ],
        [
            btn(text='• استیکر', callback_data='nothing'),btn(text=getLock(chat_id, 'sticker'), callback_data='sticker')
        ],
        [
            btn(text='• بازی', callback_data='nothing'),btn(text=getLock(chat_id, 'game'), callback_data='game')
        ],
        [
            btn(text='•• بازگشت', callback_data='main'),btn(text='•• کانال', url='t.me/'+channel)
        ],
        [
            btn(text='•• بستن فهرست', callback_data='close')
        ]
    ])

    sencond_page = markup(inline_keyboard=[
        [
            btn(text='• لینک', callback_data='nothing'),btn(text=getLock(chat_id, 'link'), callback_data='link')
        ],
        [
            btn(text='• فوروارد', callback_data='nothing'),btn(text=getLock(chat_id, 'forward'), callback_data='forward')
        ],
        [
            btn(text='• پاسخ', callback_data='nothing'),btn(text=getLock(chat_id, 'reply'), callback_data='reply')
        ],
        [
            btn(text='• تگ', callback_data='nothing'),btn(text=getLock(chat_id, 'tag'), callback_data='tag')
        ],
        [
            btn(text='• هشتگ', callback_data='nothing'),btn(text=getLock(chat_id, 'hashtag'), callback_data='hashtag')
        ],
        [
            btn(text='• انگلیسی', callback_data='nothing'),btn(text=getLock(chat_id, 'english'), callback_data='english')
        ],
        [
            btn(text='• فارسی', callback_data='nothing'),btn(text=getLock(chat_id, 'persian'), callback_data='persian')
        ],
        [
            btn(text='• فحش', callback_data='nothing'),btn(text=getLock(chat_id, 'badwords'), callback_data='badwords')
        ],
        [
            btn(text='• شکلک', callback_data='nothing'),btn(text=getLock(chat_id, 'emoji'), callback_data='emoji')
        ],
        [
            btn(text='• ویرایش', callback_data='nothing'),btn(text=getLock(chat_id, 'edit'), callback_data='edit')
        ],
        [
            btn(text='• منشن', callback_data='nothing'),btn(text=getLock(chat_id, 'mention'), callback_data='mention')
        ],
        [
            btn(text='• ورود ربات', callback_data='nothing'),btn(text=getLock(chat_id, 'bot'), callback_data='bot')
        ],
        [
            btn(text='•• بازگشت', callback_data='main'),btn(text='•• کانال', url='t.me/'+channel)
        ],
        [
            btn(text='•• بستن فهرست', callback_data='close')
        ]
    ])

    if chat_type=='private':

        if query_data=='pvmain':
            bot.editMessageText((chat_id, message_id), """» سلام ، به ربات مدیریت گروه رایگان *گپای‌پلاس* خوش اومدی!
» این سرویس ، جدیدترین ربات مدیریت گروه با امکانات متنوع میباشد و از جمله امکانات مطرح این ربات میتوان به بیش از ۲۰ قفل که هرکدام دارای قابلیت شخصی سازی هستند ، اشاره کرد.
» کافیست ربات در گروه خودتون عضو کنید ، عبارت ( نصب ) یا ( add ) رو درگروه بفرستید و شاهد قدرت این ربات فوق‌العاده باشید...

» توجه داشته باشید این سرویس همانند سرویس‌های رایگان دیگر دارای تبلیغات میباشد.
» البته شما میتوانید با پرداخت تنها ۱۰ هزار تومان ، به طور نامحدود از شر تبلیغات خلاص بشید
» تنها هدف ما رضایت شماست و ما مراعات شما را نیز میکنیم ، ربات حداکثر روزانه ۱ تبلیغ که همگی طبق قوانین کشور میباشند ارسال خواهد کرد.""",parse_mode='markdown',reply_markup=pvmain)

        elif query_data=='pvhelp':
            bot.editMessageText((chat_id, message_id), """» این بخش یک راهنمای خلاصه وار از کل ربات میباشد که بسیار ساده و قابل فهم است , لطفا قبل از هرگونه انتقاد و اعتراض مطالعه کنید !

*نصب*
» تایید گروه به عنوان گروه فعال ( اگر این دستور را در گروه و هنگامی که ربات ادمین است ارسال نکنید ربات کار نخواهد کرد. )

*راهنما*
» دریافت راهنمای  بخش های اصلی ربات در گروه , توجه داشته باشید در گروه دستور بالا را وارد نمایید.

*فهرست*
» دریافت فهرست تنظیمات شیشه ای ربات با دستور بالا در گروه , توجه داشته باشید که از طریق فهرست میتوانید به تمامی تنظیمان مربوط به گروه خود دسترسی داشته باشید.


- متاسفانه هیچ ربات رایگانی (Api) قادر به پاک کردن پیام ربات دیگری نمیباشد , از جمله : پیام ادد شدن  ربات - لینکی که ربات میفرستد - فایلی که ربات میفرستد.

- ربات های رایگان دسترسی و توانایی پاکسازی کلی یا بیش از حد گروه را ندارند , یعنی نمیتوانند پیام زیادی را پاک کنند !

-  ربات ما کمترین تبلیغات ممکن را در گروه ها ارسال میکند که کوچکترین دروغ یا غیراخلاقی بودنی در آن وجود ندارد که باعث رنجش کاربران گروه ها شود (برعکس ربات های دیگر)

- تمامی آپدیت ها و توضیحات امکانات جدید ربات ما در کانال @EvinCo موجود میباشد

- ربات ما دارای قابلیت ویژه سازی میباشد که پس از پرداخت هزینه ی بسیار اندک میتوانید از شر تبلیغات ما نیز راحت شوید.""",parse_mode='markdown',reply_markup=prvback)

        elif query_data=='pvhelp2':
            bot.editMessageText((chat_id, message_id), """» این ربات متعلق به مجموعه ی رباتسازی اِوین میباشد.

» مشخصات :
» نوشته شده به زبان Python3.7
» سرور قدرتمند با 4 هسته cpu و ram
» پایداری و آنلاین بودن 99.999 درصد


» امکانات  :

» دارای بیش از 20 قفل ساده و حرفه ای ؛
» دارای انواع دستورات فان و جذاب ؛
» دارای فهرست شیشه‌ای حرفه ای و شیک بدون زدن دستورات خسته کننده ؛
» دارای تیم پشتیبانی مجرب ؛
» نصب بسیار راحت ؛
» با کمترین تبلیغات ممکن ؛""",parse_mode='markdown', reply_markup=prvback)


    elif not is_user_panel:
        bot.answerCallbackQuery(query_id, '» شما این فهرست را درخواست نکرده‌اید.', show_alert=True)

    elif query_data=='close' and is_user_panel:
        bot.editMessageText((chat_id, message_id), "•• فهرست توسط <a href='tg://user?id={1}'>{0}</a> بسته شد.".format(first_name,from_id),parse_mode='HTML')

    elif query_data=='medialocks' and is_user_panel:
        bot.editMessageText((chat_id, message_id), "» بخش قفل‌های مدیای گروه | شامل عکس ، ویدیو ، گیف ، مخاطب و . . ." ,parse_mode='HTML', reply_markup=firstPage )

    elif query_data=='modlocks' and is_user_panel:
        bot.editMessageText((chat_id, message_id), "» بخش قفل‌های مدیریتی گروه | شامل لینک ، فحش ، فوروارد ، تگ و . . ." ,parse_mode='HTML', reply_markup=sencond_page )

    elif query_data=='otherlocks' and is_user_panel:
        bot.answerCallbackQuery(query_id, '» درحال تکمیل...', show_alert=True)

    elif query_data=='lists' and is_user_panel:
        bot.editMessageText((chat_id, message_id), "» لیست‌های موجود جهت مدیریت | اعضای لیست سکوت ، محروم‌ها و . . ." ,parse_mode='HTML', reply_markup=listspanel )

    elif query_data=='admins' and is_user_panel:
        admins = bot.getChatAdministrators(chat_id)
        b = ""
        a = ""
        for i in admins:
            st = bot.getChatMember(chat_id, i['user']['id'])['status']
            if st=='creator':
                a += "• سازنده : <a href='tg://user?id={1}'>{0}</a>\n".format(i['user']['first_name'],i['user']['id'])
            else:
                b += "• مدیر : <a href='tg://user?id={1}'>{0}</a>\n".format(i['user']['first_name'],i['user']['id'])
        bot.editMessageText((chat_id, message_id), "» لیست سازنده و مدیران گروه شما هم اکنون به شرح زیر است :\n\n"+str(a)+str(b) ,parse_mode='HTML', reply_markup=back2 )

    elif query_data=='silents' and is_user_panel:
        members = db.smembers('silentlist-'+str(chat_id))
        a = ""
        if db.scard('silentlist-'+str(chat_id))==0:
            a = "•• گروه فاقد کاربری در حالت سکوت میباشد."
        else:
            for i in members:
                i = bot.getChatMember(chat_id, i)
                a += "• کاربر :‌  <a href='tg://user?id={1}'>{0}</a> - <code>{1}</code>\n ".format(i['user']['first_name'],i['user']['id'])
        bot.editMessageText((chat_id, message_id), "» لیست کاربران تحت سکوت گروه شما هم اکنون به شرح زیر است :\n\n"+str(a) ,parse_mode='HTML', reply_markup=back2 )

    elif query_data=='bans' and is_user_panel:
        members = db.smembers('banlist-'+str(chat_id))
        a = ""
        if db.scard('banlist-'+str(chat_id))==0:
            a = "•• گروه فاقد کاربری در حالت محرومیت میباشد."
        else:
            for i in members:
                i = bot.getChatMember(chat_id, i)
                a += "• کاربر :‌  <a href='tg://user?id={1}'>{0}</a> - <code>{1}</code>\n ".format(i['user']['first_name'],i['user']['id'])
        bot.editMessageText((chat_id, message_id), "» لیست کاربران تحت محرومیت گروه شما هم اکنون به شرح زیر است :\n\n"+str(a) ,parse_mode='HTML', reply_markup=back2 )

    elif query_data=='joins' and is_user_panel:
        members = db.smembers('joinlist-'+str(chat_id))
        a = ""
        if db.scard('joinlist-'+str(chat_id))==0:
            a = "•• گروه فاقد کاربر جدیدی میباشد."
        else:
            for i in members:
                i = bot.getChatMember(chat_id, i)
                a += "• کاربر :‌  <a href='tg://user?id={1}'>{0}</a> - <code>{1}</code>\n ".format(i['user']['first_name'],i['user']['id'])
        bot.editMessageText((chat_id, message_id), "» لیست جدیدترین اعضای گروه شما هم اکنون به شرح زیر است :\n\n"+str(a) ,parse_mode='HTML', reply_markup=back2 )


    elif query_data=='filters' and is_user_panel:
        members = db.smembers('filterlist-'+str(chat_id))
        a = ""
        if db.scard('filterlist-'+str(chat_id))==0:
            a = "•• گروه فاقد عبارات فیلترشده میباشد."
        else:
            for i in members:
                a += "• عبارت :‌ <code>{}</code>\n".format(i)
        bot.editMessageText((chat_id, message_id), "» لیست عبارات فیلترشده‌ی گروه شما هم اکنون به شرح زیر است :\n\n"+str(a) ,parse_mode='HTML', reply_markup=back2 )

    elif query_data=='gpinfo' and is_user_panel:
        a = """» تعداد اعضا : {}
» تعداد بیصدا : {}
» تعداد محروم : {}
» تعداد جوین : {}
» تعداد مدیا : {}
» تعداد فیلتر : {}
» تعداد پیام‌ها : {}""".format(
    bot.getChatMembersCount(chat_id),
    db.scard('silentlist-'+str(chat_id)),
    db.scard('banlist-'+str(chat_id)),
    db.scard('joinlist-'+str(chat_id)),
    db.scard('media-'+str(chat_id)),
    db.scard('filterlist-'+str(chat_id)),
    message_id
)
        bot.editMessageText((chat_id, message_id), a ,parse_mode='HTML', reply_markup=back3)

    elif query_data=='sudohelp' and is_user_panel and from_id not in sudo_users:
        bot.answerCallbackQuery(query_id, '» شما سودوی ربات نیستید.', show_alert=True)
    elif query_data=='sudohelp' and is_user_panel and from_id in sudo_users:
        bot.editMessageText((chat_id, message_id), """*راهنمای سودوهای ربات مدیریت گروه رایگان گپای‌پلاس :*


*ویژه* ( ایدی‌گروه )
`جهت ویژه کردن گروه ( گروه‌های ویژه فاقد تبلیغات خواهند بود... )`

*امار کلی*
`فهرستی از اطلاعات کلی ربات`

*ارسال* ( پاسخ )
`ارسال پیام ریپلای‌ ( پاسخ ) شده به عنوان تبلیغ در گروه‌هایی که ویژه نیستند`

*همکاران*
`دریافت لیست تمام سودوها`

*خروج* ( ارسال در گروه)
`خارج شدن ربات از گروه مورد نظر`""" , reply_markup=back , parse_mode='markdown')
    
    elif query_data=='manhelp' and is_user_panel:
        bot.editMessageText((chat_id, message_id), """*راهنمای تنظیمی ربات مدیریت گروه رایگان گپای‌پلاس :*


*تنظیمات*
`دریافت اطلاعات تنظیمات گروه`

*نام* ( متن )
`تغییر نام گروه به متن شما`
مثال : نام گروه دورهمی

*تنظیم درباره* ( متن )
`تنظیم متن مورد نظر به Description گروه`
مثال : تنظیم درباره به گروه ما خوش اومدید ، قوانین را رعایت کنید

*تنظیم لینک* ( لینک گروه )
`تنظیم لینک گروه`

*لینک جدید*
`ساخت لینک جدید توسط ربات و تنظیم آن`

*لینک*
`دریافت لینک گروه`

*لینک پیوی*
`دریافت لینک گروه در پیوی `

*تنظیم اخطار* ( عدد )
`تنظیم حساسیت اخطار`
مثال :‌ تنظیم اخطار 3

*تنظیم کاراکتر* ( عدد )
`تنظیم حساسیت تعداد کاراکتر`
مثال : تنظیم کاراکتر 2048

*تنظیم خوشامد* ( متن )
`تنظیم متن خوشامدگویی`
مثال : تنظیم خوشامد سلام به گروه ما خوش اومدی...

*خوشامدگویی* { روشن | خاموش }
`تنظیم حالت خوشامدگویی به اعضای جدید`

*فیلتر* ( متن )
`حذف کردن کلمه درخواستی درصورتی که در گروه ارسال شود`
مثال :‌ فیلتر بای

*حذف فیلتر* ( متن )
`حذف کلمه از لیست فیلتر`
مثال : حذف فیلتر بای""" , reply_markup=back , parse_mode='markdown')
    
    elif query_data=='listhelp' and is_user_panel:
        bot.editMessageText((chat_id, message_id), """*راهنمای لیستی ربات مدیریت گروه رایگان گپای‌پلاس :*

*لیست مدیران*
`دریافت لیست مدیران`

*لیست سکوت*
`دریافت لیست افراد بیصدا`

*پاکسازی لیست سکوت*
`پاکسازی کامل افراد از لیست سکوت`

*لیست محروم*
`دریافت لیست افراد محروم شده از گروه`

*پاکسازی لیست محروم*
`پاکسازی کامل افراد از لیست محرومین`

*لیست فیلتر*
`دریافت لیست عبارات فیلتر شده`

*پاکسازی لیست فیلتر*
`پاکسازی کامل عبارت موجود در لیست فیلتر`

*لیست جوین*
`دریافت لیست اعضای جدید`

*پاکسازی لیست جوین*
`پاکسازی کامل (لیست) اعضای جدید (اعضا حذف نمیشوند.)`

*امار*
`دریافت لیست کلی اطلاعات گروه`""" , reply_markup=back , parse_mode='markdown')
    
    elif query_data=='modhelp' and is_user_panel:
        bot.editMessageText((chat_id, message_id), """*راهنمای مدیریتی ربات مدیریت گروه رایگان گپای‌پلاس :*


*فهرست*
`دریافت فهرست با دکمه‌ی اینلاین ( شیشه‌ای ) جهت مدیریت راحت‌تر برای مدیران گروه`

*نصب*
`افزودن گروه خود به فهرست گروه‌های تحت پشتیبانی ربات`

*حذف*
`حذف گروه خود از فهرست گروه‌های تحت پشتیبانی ربات`

*ترفیع* ( پاسخ | يوزرآیدی ) - \[ متاسفانه این قابلیت فعال نمیباشد ]
`ارتقای رتبه‌ی یک کاربر به مدیریت ربات`

*تنزل* ( پاسخ | یوزرآیدی ) - \[ متاسفانه این قابلیت فعال نمیباشد ]
`تنزل رتبه‌ی مدیر به کاربر`

*سنجاق* ( پاسخ به یک پیام )
‍`پیامی را که روی آن ریپلای ( پاسخ ) کرده‌اید را سنجاق میکند`

*حذف سنجاق*
`پیام سنجاق شده را حذف میکند`

*محروم* ( پاسخ | یوزرآیدی )
`اخراج کاربر با ریپلای کردن روی پیام ایشان یا با استفاده از آیدی عددی کاربر`
مثال :‌ محروم 123456789

*ازاد*‌ ( پاسخ |‌ یوزرآیدی )
`حذف کاربر از لیست اعضای محروم گروه`
مثال : ازاد 123456789

*بیصدا* ( پاسخ | یوزرآیدی )
`کاربری که بیصدا شود توانایی ارسال هیچ پیامی را در گروه نخواهد داشت`
مثال :‌ بیصدا 123456789

*باصدا* ( پاسخ | یوزرآیدی )
`حذف کاربر از لیست افراد بیصدا`
مثال : بیصدا 123456789

*قفل همه*
`فعالسازی تمامی قفل‌های ربات به صورت همزمان ( حالت قفل : حذف ) `

*بازکردن همه*
`غیرفعالسازی تمامی قفل‌های ربات`

*حذف پیام* ( عدد )
`پاکسازی پیام‌های گروه به تعداد ذکر شده ( بین ۱ تا ۱۵۰ پیام )`""" , reply_markup=back , parse_mode='markdown')
    
    elif query_data=='lockhelp' and is_user_panel:
        bot.editMessageText((chat_id, message_id), """*» راهنمای قفل‌های ربات مدیریت گروه رایگان گپای‌پلاس :*


*قفل + نام*
جهت قفل کردن یک فرآیند در حالت پیشفرض میشود ( حالت پیشفرض :‌ حذف پیام )
مثال :‌ قفل عکس
`در این صورت اگر شخصی در گروه عکس ارسال کند ، آن عکس توسط ربات پاک میشود`

*بازکردن + نام*
جهت غیرفعالسازی قفل موردنظر میشود
مثال : بازکردن عکس
`در این صورت اگر شخصی در گروه عکس ارسال کند ، آن عکس توسط ربات پاک نمیشود`

*نام + حالت*
جهت شخصی‌سازی کارکرد قفل‌های ربات ( حالت‌ها : اخراج | سکوت | حذف )
مثال :‌ عکس سکوت
`در این صورت قفل عکس از حالت پیشفرض ( حذف ) به ( سکوت ) تغییر میکند.`


*نام قفل‌های مدیا :*
_عکس | ویدیو |‌ ویس | موزیک | گیف | استیکر | مکان | مخاطب | فیلم سلفی | سند | بازی | متن_

*نام قفل‌های دیگر :*
_لینک | فوروارد | پاسخ | تگ | هشتگ |‌ انگلیسی | فارسی | فحش | شکلک | ویرایش | منشن | ورود ربات_""" , reply_markup=back , parse_mode='markdown')
    
    elif query_data=='funhelp' and is_user_panel:
        bot.editMessageText((chat_id, message_id), """*راهنمای سرگرمی ربات مدیریت گروه رایگان گپای‌پلاس‌ :*

*ایدی*
`دریافت اطلاعات شخصی`

*اطلاعات* ( پاسخ )
`دریافت اطلاعات شخص مورد نظر`

*ربات | وضعیت*
`اطلاع از انلاین بودن ربات`""" , reply_markup=back , parse_mode='markdown')


    elif query_data=='main' and is_user_panel:
        bot.editMessageText((chat_id, message_id), """» فهرست مدیریت آسان‌ | جهت دسترسی به هربخش کافیست روی آن کلیک کنید.
•• درخواست توسط [{}](tg://user?id={})""".format(msg['from']['first_name'],from_id) , reply_markup=panel , parse_mode='markdown')

    elif query_data=='help' and is_user_panel:
        bot.editMessageText((chat_id, message_id), "••• بخش مورد نظر خود را انتخاب نمایید | قفلی ، مدیریتی و . . ." , reply_markup=help , parse_mode='markdown')


    elif query_data=='photo' and is_user_panel:
        lockIt1(msg, 'photo')
    elif query_data=='video' and is_user_panel:
        lockIt1(msg, 'video')
    elif query_data=='gif' and is_user_panel:
        lockIt1(msg, 'gif')
    elif query_data=='video_note' and is_user_panel:
        lockIt1(msg, 'video_note')
    elif query_data=='sticker' and is_user_panel:
        lockIt1(msg, 'sticker')
    elif query_data=='audio' and is_user_panel:
        lockIt1(msg, 'audio')
    elif query_data=='location' and is_user_panel:
        lockIt1(msg, 'location')
    elif query_data=='document' and is_user_panel:
        lockIt1(msg, 'document')
    elif query_data=='game' and is_user_panel:
        lockIt1(msg, 'game')
    elif query_data=='contact' and is_user_panel:
        lockIt1(msg, 'contact')
    elif query_data=='text' and is_user_panel:
        lockIt1(msg, 'text')
    elif query_data=='voice' and is_user_panel:
        lockIt1(msg, 'voice')
    
    elif query_data=='edit' and is_user_panel:
        lockIt2(msg, 'edit')
    elif query_data=='emoji' and is_user_panel:
        lockIt2(msg, 'emoji')
    elif query_data=='english' and is_user_panel:
        lockIt2(msg, 'english')
    elif query_data=='persian' and is_user_panel:
        lockIt2(msg, 'persian')
    elif query_data=='link' and is_user_panel:
        lockIt2(msg, 'link')
    elif query_data=='hashtag' and is_user_panel:
        lockIt2(msg, 'hashtag')
    elif query_data=='tag' and is_user_panel:
        lockIt2(msg, 'tag')
    elif query_data=='badwords' and is_user_panel:
        lockIt2(msg, 'badwords')
    elif query_data=='forward' and is_user_panel:
        lockIt2(msg, 'forward')
    elif query_data=='mention' and is_user_panel:
        lockIt2(msg, 'mention')
    elif query_data=='bot' and is_user_panel:
        lockIt2(msg, 'bot')
    elif query_data=='reply' and is_user_panel:
        lockIt2(msg, 'reply')

MessageLoop(bot, {'chat': chat, 'callback_query': inlines}).run_as_thread()
while True:
    time.sleep(10)