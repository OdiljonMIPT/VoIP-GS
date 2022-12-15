from django.db import models

catChoices = (
    ('INBOUND', 'inbound'),
    ('OUTBOUND', 'outbound')
)
statusChoices = (
    ('RUN', 'run'),
    ('STOP', 'stop')
)


class Language(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Agent(models.Model):
    name = models.CharField(max_length=50)
    cat = models.CharField(max_length=10, choices=catChoices)
    lang = models.ForeignKey(Language, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=statusChoices, default='STOP')

    def __str__(self):
        return self.name


class Voice(models.Model):
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='voices')
    lang = models.ForeignKey(Language, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
