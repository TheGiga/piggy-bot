import config

USER_CMD_DESCRIPTION = "👤 Information about user"
PIG_CMD_DESCRIPTION = "🐷 Information about specific pig"
FEED_CMD_DESCRIPTION = "🐷 Feed your pig"
NAME_CMD_DESCRIPTION = "🐷 Change Pig's name"
TOP_CMD_DESCRIPTION = "🐷 Top 10 pigs by weight"
REPORT_CMD_DESCRIPTION = "🐖 Report user"
DATA_DELETION_CMD_DESCRIPTION = "DELETE ALL data associated with YOUR account (YOU LOSE ALL YOUR PROGRESS)"

HELP_CMD_DATA_RETENTION_INFO = \
    (
        f"ℹ️ NOTE: If you haven't used any bot commands in "
        f"**{config.DATA_RETENTION_PERIOD_DAYS} days** your data and all the progress will be **purged**!\n\n"
        f"To request data deletion whenever you like, use `/delete_my_data` command."
    )

NAME = "Name"
UID = "UID"
WEIGHT = "Weight"
AGE = "Age"
DAYS = "d"
KG = "kg"

TOP_10 = "🐷 TOP 10"

PIG_PROFILE = "PIG PROFILE"

NAME_NOT_FOUND = "😢 Pig with such name is not found."
WEIGHT_CHANGE_PLUS = 'Your pig gained **{} kg** in weight 😎'
WEIGHT_CHANGE_SAME = "Weight of your pig didn't change... 🐷"
WEIGHT_CHANGE_MINUS = 'Your pig lost **{} kg** in weight 😢'

SAME_NAME = "🤨 You've already set the same name for your pig."
NAME_ALREADY_EXISTS = "The name `{}` is already taken 😢"
PIG_CREATED = "✅ You have successfully created a pig with name `{}`"
NAME_CHANGED = "☑️ You have successfully changed your pig's name from `{0}` to `{1}`."
CHANGE_NAME_PROPOSAL = "ℹ️ Consider changing your pigs name by using `/name <new name>`"

CONFIRMING = "✅ Confirming..."
CANCELLING = "Cancelling."

DATA_DELETION_EMBED_TITLE = "Confirm data deletion request!"
DATA_DELETION_EMBED_DESCRIPTION = \
    "You are about to delete **ALL** your data. **INCLUDING all the progress**\n\n**THIS PROCESS IS IRREVERSIBLE**"
DATA_DELETION_NO_ASSOCIATED_DATA = "There is no data associated with your account."
DATA_DELETION_SUCCESS = "**✅ Success!**\nAll your data was successfully deleted."

REPORT_SUCCESS = "☑️ Report successfully sent, thanks!"