from celery import shared_task

@shared_task(bind=True)
def loop(request):
        for i in range(8999):
                 print(i)
