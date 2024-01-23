import config

USER_CMD_DESCRIPTION = "👤 Информация о пользователе"
PIG_CMD_DESCRIPTION = "🐷 Информация о хряке"
FEED_CMD_DESCRIPTION = "🐷 Покормить хряка"
NAME_CMD_DESCRIPTION = "🐷 Изменить имя хряка"
TOP_CMD_DESCRIPTION = "🐷 Топ 10 хряков по жировой массе"
REPORT_CMD_DESCRIPTION = "🐖 Жалоба на пользователя"
DATA_DELETION_CMD_DESCRIPTION = "УДАЛИТЬ ВСЕ данные, которые связаны с ВАШИМ аккаунтом дискорда (ВКЛЮЧАЯ ВЕСЬ ПРОГРЕСС)"

HELP_CMD_DATA_RETENTION_INFO = \
    (
        f"ℹ️ ВНИМАНИЕ: Если вы не использовали ни одной команды этого бота в течении "
        f"**{config.DATA_RETENTION_PERIOD_DAYS} дней** вы получите статус \"не активен\" и потеряете свой UID!\n\n"
        f"Для запроса удаления данных в любом момент - используйте команду `/delete_my_data`."
    )

NAME = "Имя"
UID = "UID"
WEIGHT = "Вес"
AGE = "Возраст"
DAYS = "дн"
KG = "кг"

TOP_10 = "🐷 ТОП 10"

PIG_PROFILE = "Профиль Хряка"

NAME_NOT_FOUND = "😢 Хряк с таким именем - не найден."
WEIGHT_CHANGE_PLUS = 'Ваш хряк пожирнел на **{} кг** 😎'
WEIGHT_CHANGE_SAME = 'Масса вашего хряка не изменилась... 🐷'
WEIGHT_CHANGE_MINUS = 'Ваш хряк похудел на **{} кг** 😢'

SAME_NAME = "🤨 Вы уже дали такое-же имя своему хряку."
NAME_ALREADY_EXISTS = "Имя `{}` уже занято 😢"
PIG_CREATED = "✅ Вы успешно создали хряка с именем `{}`"
NAME_CHANGED = "☑️ Вы успешно сменили имя своего хряка с `{0}` на `{1}`."
CHANGE_NAME_PROPOSAL = "ℹ️ Предлагаем изменить имя вашего хряка используя команду `/name <new name>`"

CONFIRMING = "✅ Подтверждаем..."
CANCELLING = "❌ Отмена."

LAST_FED = "🥕 Последний обед"
STATUS = "⌛ Статус"
STATUS_ACTIVE = "Активен"
STATUS_INACTIVE = "Не активен"

DATA_DELETION_EMBED_TITLE = "Подтвердите запрос на удаление данных!"
DATA_DELETION_EMBED_DESCRIPTION = \
    (
        "Вы собираетесь удалить **ВСЕ** свои данные. "
        "**Включая ВЕСЬ ПРОГРЕСС со ВСЕХ СЕРВЕРОВ**\n\n**ЭТОТ ПРОЦЕСС НЕВОЗМОЖНО ОБРАТИТЬ**"
    )
DATA_DELETION_NO_ASSOCIATED_DATA = "Данные ассоциированные с вашим аккаунтом - отсутствуют."
DATA_DELETION_SUCCESS = "**✅ Успешно!**\nВсе ваши данные были успешно удалены."

REPORT_SUCCESS = "☑️ Репорт успешно отправлен, спасибо!"

GUILD_CONFIG_HELP_EMBED_TITLE = "Доступные значения для настройки"
GUILD_CONFIG_HELP_INSTRUCTIONS = ("ℹ️ Это список доступных для настройки ключей для использования в "
                                  "`/config value`.\n> Пример: `/config value key:cooldown value:60`")
GUILD_CONFIG_VALUE_ERROR = "❌ Указанное значение не соответствует требованиям: `{}`"
GUILD_CONFIG_VALUE_SUCCESS = "✅ Вы успешно изменили значения `{0}` на `{1}`."

COOLDOWN_MESSAGE = "❌ Вы сможете использовать эту команду {}"
