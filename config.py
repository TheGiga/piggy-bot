import value_check_procedures

COGS = [
    'basic',
    'pigs',
    'dev',
    'data',
    'admin'
]

ADMINS = [352062534469156864]

DATA_RETENTION_PERIOD_DAYS = 30
FEED_COMMAND_COOLDOWN_MINUTES = 180

AVAILABLE_CONFIG_OPTIONS = {
    "cooldown": {
        "default_value": FEED_COMMAND_COOLDOWN_MINUTES,
        "value_check_requirements": "value: integer, 5 <= value <= 4320",
        "value_check_procedure": value_check_procedures.cooldown_value_check,
        "comment": "`/feed` command cooldown value in minutes."
    }
}

DEFAULT_GUILD_CONFIG = {x: AVAILABLE_CONFIG_OPTIONS[x]['default_value'] for x in AVAILABLE_CONFIG_OPTIONS}

EXCLUDED_HELP_CMD_GROUPS = ['dev']
