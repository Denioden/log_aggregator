from django.db import models


class Log(models.Model):
    remote_host = models.GenericIPAddressField(
        db_index=True,
        blank=False,
        null=False,
    )

    remote_logname = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    remote_user = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    request_time = models.DateTimeField(
        blank=False,
        null=False,
    )

    request_line = models.TextField(
        blank=True,
        null=True,
    )

    final_status = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    bytes_sent = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    referer = models.TextField(
        blank=True,
        null=True,
    )

    user_agent = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['request_time', 'remote_host']

    def __str__(self):
        return self.remote_host()


class LogFile(models.Model):
    date_time = models.DateTimeField(auto_now=True)

    file_path = models.TextField()

    last_line = models.TextField(blank=True)

    class Meta:
        ordering = ['date_time']

    def __str__(self):
        return self.last_line
