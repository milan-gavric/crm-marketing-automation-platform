from django.db import models


class MessageTemplate(models.Model):
    content = models.TextField()
    industry = models.CharField(max_length=255, blank=True, db_index=True)
    skills = models.JSONField(default=list, blank=True)
    used = models.IntegerField(default=0)
    replied = models.IntegerField(default=0)
    succeeded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'message_templates'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['industry']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"Message Template {self.id}"


class SubjectTemplate(models.Model):
    content = models.CharField(max_length=500)
    used = models.IntegerField(default=0)
    replied = models.IntegerField(default=0)
    succeeded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subject_templates'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.content

