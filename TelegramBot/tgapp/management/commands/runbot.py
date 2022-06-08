from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from django.core.management import BaseCommand
from tgapp.views import *

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        TOKEN = '5028779716:AAEWI_822MoMa8GKg2wADRNKkTBvI0eujA4'
        updater = Updater(TOKEN)
        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(CallbackQueryHandler(inline_handler))
        updater.start_polling()
        updater.idle()