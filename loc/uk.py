import config

USER_CMD_DESCRIPTION = "👤 Інформація щодо користувача"
PIG_CMD_DESCRIPTION = "🐷 Інформація про конкретного хряка"
FEED_CMD_DESCRIPTION = "🐷 Покормити хряка"
NAME_CMD_DESCRIPTION = "🐷 Змінити ім'я хряка"
TOP_CMD_DESCRIPTION = "🐷 Топ 10 хряків за сальною масою"
REPORT_CMD_DESCRIPTION = "🐖 Скарга на користувача"
DATA_DELETION_CMD_DESCRIPTION = "ВИДАЛИТИ УСІ дані пов'язані з ВАШИМ аккаунтом діскорда (у тому числі і ВЕСЬ ПРОГРЕСС)"


HELP_CMD_DATA_RETENTION_INFO = \
    (
        f"ℹ️ УВАГА: Якщо ви не користувалися командами цього бота у період більший за "
        f"**{config.DATA_RETENTION_PERIOD_DAYS} днів** ваші дані (і прогресс на всіх серверах) буде **видалено**!\n\n"
        f"Щоб запросити видалення даних в будь який момент - використайте команду `/delete_my_data`."
    )

NAME = "Ім'я"
UID = "UID"
WEIGHT = "Вага"
AGE = "Вік"
DAYS = "дн"
KG = "кг"

TOP_10 = "🐷 ТОП 10"

PIG_PROFILE = "Профіль Хряка"

NAME_NOT_FOUND = "😢 Хряка з таким іменем - не знайдено."
WEIGHT_CHANGE_PLUS = 'Ваш хряк нагнав салової маси на **{} кг** 😎'
WEIGHT_CHANGE_SAME = 'Маса вашого хряка не змінилася... 🐷'
WEIGHT_CHANGE_MINUS = 'Ваш хряк скинув салової маси на **{} кг** 😢'

SAME_NAME = "🤨 Ви вже дали таке саме ім'я свому хряку."
NAME_ALREADY_EXISTS = "Ім'я `{}` вже зайняте 😢"
PIG_CREATED = "✅ Ви успішно створили хряка з іменем `{}`"
NAME_CHANGED = "☑️ Ви успішно змінили ім'я свого хряка з `{0}` на `{1}`."
CHANGE_NAME_PROPOSAL = "ℹ️ Пропонуємо змінити ім'я вашого хряка використовуючи `/name <нове ім'я>`"

CONFIRMING = "✅ Підтверджуємо..."
CANCELLING = "❌ Відміна."

LAST_FED = "🥕 Останній перекус"
STATUS = "⌛ Статус"
STATUS_ACTIVE = "Активний"
STATUS_INACTIVE = "Не активний"

DATA_DELETION_EMBED_TITLE = "Підтверідть запрос на видалення даних!"
DATA_DELETION_EMBED_DESCRIPTION = \
    (
        "Ви збираєтесь видалити **УСІ** свої дані. "
        "**У тому числі і ВЕСЬ ПРГОГРЕСС зі ВСІХ СЕРВЕРІВ**\n\n**ЦЕЙ ПРОЦЕС Є НЕЗВОРОТНИМ**"
    )
DATA_DELETION_NO_ASSOCIATED_DATA = "Дані асоційовані з вашим аккаунтом - відсутні."
DATA_DELETION_SUCCESS = "**✅ Успішно!**\nУсі ваші дані були успішно видалено."

REPORT_SUCCESS = "☑️ Репорт успішно відправлено, дякуємо!"
