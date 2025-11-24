from django.db import models


class Lead(models.Model):
    STATUS_CHOICES = [
        ('unused', 'Unused'),
        ('sent', 'Sent'),
        ('bad', 'Bad'),
        ('bounced', 'Bounced'),
        ('opened', 'Opened'),
        ('replied', 'Replied'),
        ('demoed', 'Demoed'),
    ]

    Email = models.EmailField(db_column='email', db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unused', db_index=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    assigned_to = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    linkedin = models.URLField(blank=True)
    website = models.URLField(blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leads'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['Email']),
            models.Index(fields=['status']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.Email

