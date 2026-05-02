from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import config

SUPPLEMENTS = {
    "аминокислоты": {
        "аргинин": {
            "форма": "L-аргинин",
            "дозировка": "3-6 г в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/31977834/",
            "описание": "Оксид азота, пампинг, сосуды и выносливость."
        },
        "цитруллин": {
            "форма": "L-цитруллин малат",
            "дозировка": "6-8 г перед тренировкой",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/27749691/",
            "описание": "Повышает аргинин, убирает аммиак."
        },
        "креатин": {
            "форма": "Моногидрат креатина",
            "дозировка": "3-5 г в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/28615996/",
            "описание": "Сила, выносливость, поддержка мозга."
        },
        "таурин": {
            "форма": "L-таурин",
            "дозировка": "500-3000 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/23392887/",
            "описание": "Аминокислота для сердца, успокаивает нервную систему, антиоксидант."
        },
        "l-карнитин": {
            "форма": "L-карнитин тартрат / ацетил-L-карнитин",
            "дозировка": "500-2000 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/29241711/",
            "описание": "Транспорт жирных кислот в митохондрии, энергия для сердца и мышц."
        },
        "бета-аланин": {
            "форма": "Бета-аланин",
            "дозировка": "3-6 г в сутки (разделить на 2 приема)",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/26175657/",
            "описание": "Повышает карнозин в мышцах, буфер лактата, выносливость. Может вызывать покалывание."
        },
    },
    "адаптогены": {
        "ашваганда": {
            "форма": "Экстракт корня (KSM-66 / Sensoril)",
            "дозировка": "300-600 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/23439798/",
            "описание": "Адаптоген №1, снижает кортизол и тревожность."
        },
        "родиола розовая": {
            "форма": "Экстракт корня (3% розавины, 1% салидрозиды)",
            "дозировка": "200-600 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/22228673/",
            "описание": "Адаптоген, антистресс, выносливость."
        },
        "женьшень": {
            "форма": "Экстракт корня (4-7% гинзенозидов)",
            "дозировка": "200-400 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/28467172/",
            "описание": "Классический адаптоген, энергия, либидо."
        },
        "элеутерококк": {
            "форма": "Экстракт корня",
            "дозировка": "300-600 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/22155332/",
            "описание": "Сибирский женьшень, выносливость."
        },
        "бакопа монье": {
            "форма": "Экстракт листьев (50% бакозидов)",
            "дозировка": "300-600 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/25061708/",
            "описание": "Память, обучение, снижает тревогу."
        },
        "готу кола": {
            "форма": "Экстракт листьев (Centella asiatica)",
            "дозировка": "500-1000 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/28480479/",
            "описание": "Мозг, память, микроциркуляция."
        },
    },
    "грибы": {
        "кордицепс": {
            "форма": "Экстракт гриба",
            "дозировка": "1-3 г в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/30142085/",
            "описание": "Гриб-адаптоген, АТФ, энергия, либидо."
        },
        "львиная грива": {
            "форма": "Экстракт гриба (Lion's Mane)",
            "дозировка": "500-3000 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/29149849/",
            "описание": "NGF, нейрогенез, память и фокус."
        },
        "рейши": {
            "форма": "Экстракт гриба",
            "дозировка": "1-3 г в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/21617892/",
            "описание": "Иммунитет, противовоспалительное, сон."
        },
    },
    "витамины_и_минералы": {
        "витамин d3": {
            "форма": "Холекальциферол (D3)",
            "дозировка": "1000-5000 МЕ в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/30611908/",
            "описание": "Основная форма витамина D."
        },
        "цинк": {
            "форма": "Пиколинат цинка",
            "дозировка": "15-30 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/28475156/",
            "описание": "Лучшая усвояемость, иммунитет и кожа."
        },
        "магний цитрат": {
            "форма": "Цитрат магния",
            "дозировка": "200-400 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/26404370/",
            "описание": "Биодоступность, помогает при запорах."
        },
        "магний глицинат": {
            "форма": "Глицинат магния",
            "дозировка": "200-400 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/23912345/",
            "описание": "Мягкое действие, тревожность."
        },
        "витамин b12": {
            "форма": "Метилкобаламин",
            "дозировка": "500-2000 мкг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/22221769/",
            "описание": "Нервная система и энергия."
        },
        "железо": {
            "форма": "Бисглицинат железа",
            "дозировка": "18-30 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/28343152/",
            "описание": "Гемоглобин без запоров."
        },
        "витамин k2": {
            "форма": "Менахинон-7 (MK-7)",
            "дозировка": "90-180 мкг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/30917265/",
            "описание": "Кальций в кости, защита сосудов."
        },
        "селен": {
            "форма": "Селенометионин",
            "дозировка": "55-200 мкг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/28071912/",
            "описание": "Антиоксидант, щитовидная железа."
        },
    },
    "антиоксиданты": {
        "альфа-липоевая кислота": {
            "форма": "R-липоевая кислота",
            "дозировка": "300-600 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/28720509/",
            "описание": "Универсальный антиоксидант, регенерирует витамины C и E, помогает при нейропатии."
        },
        "глутатион": {
            "форма": "Липосомальный глутатион / N-ацетилцистеин (прекурсор)",
            "дозировка": "250-500 мг (глутатион) или 600-1200 мг NAC",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/25950642/",
            "описание": "Главный антиоксидант организма, детокс печени, осветляет кожу."
        },
        "астаксантин": {
            "форма": "Масляный экстракт (Haematococcus pluvialis)",
            "дозировка": "4-12 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/22214273/",
            "описание": "Мощнейший каротиноид, защита от УФ, глаза, кожа и выносливость."
        },
        "ресвератрол": {
            "форма": "Транс-ресвератрол (50%)",
            "дозировка": "150-500 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/25824342/",
            "описание": "Полифенол красного вина, сиртуины и долголетие, сердце."
        },
        "витамин c": {
            "форма": "Аскорбат натрия",
            "дозировка": "500-2000 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/23440782/",
            "описание": "Мягкая форма для желудка, поддержка иммунитета."
        },
    },
    "для_сна": {
        "мелатонин": {
            "форма": "Мелатонин",
            "дозировка": "0.3-5 мг перед сном",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/28648359/",
            "описание": "Регуляция сна, помогает при смене часовых поясов."
        },
        "5-htp": {
            "форма": "5-гидрокситриптофан (из гриффонии)",
            "дозировка": "100-300 мг перед сном",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/23341426/",
            "описание": "Прекурсор серотонина и мелатонина, улучшает засыпание."
        },
        "gaba": {
            "форма": "Гамма-аминомасляная кислота",
            "дозировка": "500-1000 мг перед сном",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/18463877/",
            "описание": "Тормозной нейромедиатор, расслабление и глубокий сон."
        },
        "глицин": {
            "форма": "Глицин",
            "дозировка": "3-5 г перед сном",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/22272660/",
            "описание": "Снижает температуру тела, улучшает качество сна."
        },
        "валериана": {
            "форма": "Экстракт корня (0.8% валереновой кислоты)",
            "дозировка": "300-600 мг перед сном",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/17145239/",
            "описание": "Классическое успокоительное, мягкое снотворное без привыкания."
        },
    },
    "спортпит": {
        "протеин": {
            "форма": "Концентрат / изолят сывороточного белка",
            "дозировка": "20-40 г после тренировки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/25169440/",
            "описание": "Белок для роста и восстановления мышц, быстрое усвоение."
        },
        "bcaa": {
            "форма": "L-лейцин + L-изолейцин + L-валин (2:1:1)",
            "дозировка": "5-10 г до/во время тренировки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/28638350/",
            "описание": "Незаменимые аминокислоты, снижают катаболизм и усталость."
        },
        "коллаген": {
            "форма": "Гидролизованный коллаген I и III типа",
            "дозировка": "5-10 г в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/23949208/",
            "описание": "Кожа, суставы, волосы и ногти."
        },
    },
    "нервы_и_стресс": {
        "зверобой": {
            "форма": "Экстракт травы (0.3% гиперицина)",
            "дозировка": "300-900 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/28064110/",
            "описание": "Природный антидепрессант, поднимает серотонин. Осторожно - взаимодействует со многими лекарствами."
        },
        "пустырник": {
            "форма": "Настойка / экстракт травы",
            "дозировка": "300-500 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/22155332/",
            "описание": "Успокаивает сердце, снижает тревожность и раздражительность."
        },
        "л-теанин": {
            "форма": "L-теанин",
            "дозировка": "100-400 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/31758301/",
            "описание": "Спокойствие без сонливости, улучшает фокус."
        },
    },
    "кости_и_суставы": {
        "глюкозамин": {
            "форма": "Глюкозамин сульфат",
            "дозировка": "1500 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/26832391/",
            "описание": "Строительный блок хряща, при остеоартрите."
        },
        "хондроитин": {
            "форма": "Хондроитин сульфат",
            "дозировка": "800-1200 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/26832391/",
            "описание": "Удерживает воду в хряще, часто комбинируют с глюкозамином."
        },
        "msm": {
            "форма": "Метилсульфонилметан",
            "дозировка": "1000-3000 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/21308063/",
            "описание": "Органическая сера, противовоспалительное для суставов, волосы и ногти."
        },
    },
    "зрение": {
        "лютеин": {
            "форма": "Лютеин + зеаксантин",
            "дозировка": "10-20 мг лютеина + 2-4 мг зеаксантина",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/25187453/",
            "описание": "Каротиноиды макулы глаза, защита от синего света и AMD."
        },
        "черника": {
            "форма": "Экстракт ягод (25% антоцианов)",
            "дозировка": "160-320 мг в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/25782234/",
            "описание": "Улучшает ночное зрение и микроциркуляцию в глазах."
        },
        "омега-3 dha": {
            "форма": "DHA из водорослей / рыбьего жира",
            "дозировка": "500-1000 мг DHA в сутки",
            "исследования": "https://pubmed.ncbi.nlm.nih.gov/31216874/",
            "описание": "Структурный компонент сетчатки, профилактика сухости глаз."
        },
    },
}

CATEGORY_NAMES = {
    "аминокислоты": "Аминокислоты",
    "адаптогены": "Адаптогены",
    "грибы": "Грибы",
    "витамины_и_минералы": "Витамины и минералы",
    "антиоксиданты": "Антиоксиданты",
    "для_сна": "Для сна",
    "спортпит": "Спортпит",
    "нервы_и_стресс": "Нервы и стресс",
    "кости_и_суставы": "Кости и суставы",
    "зрение": "Зрение",
}


async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Аминокислоты", callback_data='cat|аминокислоты')],
        [InlineKeyboardButton("Адаптогены", callback_data='cat|адаптогены')],
        [InlineKeyboardButton("Грибы", callback_data='cat|грибы')],
        [InlineKeyboardButton("Витамины и минералы", callback_data='cat|витамины_и_минералы')],
        [InlineKeyboardButton("Антиоксиданты", callback_data='cat|антиоксиданты')],
        [InlineKeyboardButton("Для сна", callback_data='cat|для_сна')],
        [InlineKeyboardButton("Спортпит", callback_data='cat|спортпит')],
        [InlineKeyboardButton("Нервы и стресс", callback_data='cat|нервы_и_стресс')],
        [InlineKeyboardButton("Кости и суставы", callback_data='cat|кости_и_суставы')],
        [InlineKeyboardButton("Зрение", callback_data='cat|зрение')],
        [InlineKeyboardButton("Поиск", callback_data='search')],
        [InlineKeyboardButton("Все исследования", callback_data='all_research')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "*База БАДов* — выберите категорию:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def show_category(update, context, category: str):
    items = SUPPLEMENTS.get(category, {})
    keyboard = []
    for name in items:
        keyboard.append([InlineKeyboardButton(name, callback_data=f'item|{category}|{name}')])
    keyboard.append([InlineKeyboardButton("Назад", callback_data='back_to_main')])

    await update.callback_query.edit_message_text(
        f"*{CATEGORY_NAMES.get(category, category)}* — выберите добавку:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )


async def show_item(update, context, category: str, item: str):
    data = SUPPLEMENTS.get(category, {}).get(item, {})
    text = (
        f"*{item}*\n\n"
        f"Форма: {data.get('форма', '-')}\n"
        f"Дозировка: {data.get('дозировка', '-')}\n"
        f"Описание: {data.get('описание', '-')}\n"
        f"[Исследование на PubMed]({data.get('исследования', '#')})\n\n"
        f"Нажмите /start для возврата в меню"
    )
    keyboard = [[InlineKeyboardButton("Назад к категории", callback_data=f'cat|{category}')]]
    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown',
        disable_web_page_preview=True
    )


async def show_all_research(update, context):
    lines = []
    for cat, items in SUPPLEMENTS.items():
        lines.append(f"*{CATEGORY_NAMES.get(cat, cat)}*")
        for name, data in items.items():
            lines.append(f"- {name}: {data['исследования']}")
        lines.append("")

    text = "\n".join(lines)

    if len(text) > 4000:
        text = text[:4000] + "\n\n_(список обрезан — слишком длинный)_"

    keyboard = [[InlineKeyboardButton("Назад", callback_data='back_to_main')]]
    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown',
        disable_web_page_preview=True
    )


def get_main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Аминокислоты", callback_data='cat|аминокислоты')],
        [InlineKeyboardButton("Адаптогены", callback_data='cat|адаптогены')],
        [InlineKeyboardButton("Грибы", callback_data='cat|грибы')],
        [InlineKeyboardButton("Витамины и минералы", callback_data='cat|витамины_и_минералы')],
        [InlineKeyboardButton("Антиоксиданты", callback_data='cat|антиоксиданты')],
        [InlineKeyboardButton("Для сна", callback_data='cat|для_сна')],
        [InlineKeyboardButton("Спортпит", callback_data='cat|спортпит')],
        [InlineKeyboardButton("Нервы и стресс", callback_data='cat|нервы_и_стресс')],
        [InlineKeyboardButton("Кости и суставы", callback_data='cat|кости_и_суставы')],
        [InlineKeyboardButton("Зрение", callback_data='cat|зрение')],
        [InlineKeyboardButton("Поиск", callback_data='search')],
        [InlineKeyboardButton("Все исследования", callback_data='all_research')],
    ])


async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'back_to_main':
        await query.edit_message_text(
            "*База БАДов* — выберите категорию:",
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )
    elif data == 'all_research':
        await show_all_research(update, context)
    elif data == 'search':
        await query.edit_message_text(
            "Отправьте название добавки — я найду её во всех категориях.",
            parse_mode='Markdown'
        )
        context.user_data['waiting_for_search'] = True
    elif data.startswith('cat|'):
        category = data.split('|', 1)[1]
        await show_category(update, context, category)
    elif data.startswith('item|'):
        _, category, item = data.split('|', 2)
        await show_item(update, context, category, item)


async def search_handler(update: Update, context):
    if not context.user_data.get('waiting_for_search'):
        return

    query_text = update.message.text.lower().strip()
    found = []

    for cat, items in SUPPLEMENTS.items():
        for name, data in items.items():
            if query_text in name.lower():
                found.append((cat, name, data))

    if found:
        response = ""
        for cat, name, data in found:
            entry = (
                f"*{name}* ({CATEGORY_NAMES.get(cat, cat)})\n"
                f"Форма: {data['форма']}\n"
                f"Дозировка: {data['дозировка']}\n"
                f"{data['описание']}\n"
                f"{data['исследования']}\n\n"
            )
            if len(response) + len(entry) > 4000:
                break
            response += entry
    else:
        response = f"По запросу *{query_text}* ничего не найдено.\nПопробуйте другое название или /start"

    await update.message.reply_text(response, parse_mode='Markdown', disable_web_page_preview=True)
    context.user_data['waiting_for_search'] = False


def main():
    app = Application.builder().token(config.TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_handler))

    async def error_handler(update, context):
        print(f"Ошибка: {context.error}")

    app.add_error_handler(error_handler)
    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()