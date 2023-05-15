from django.shortcuts import redirect

from megano.celery_task import app


@app.task
def confirm_payment(card_num, pk):
    last_num = int(card_num[-1])
    if last_num != 0 and last_num % 2 == 0:
        print('ok')
        return 1
    else:
        return 0
