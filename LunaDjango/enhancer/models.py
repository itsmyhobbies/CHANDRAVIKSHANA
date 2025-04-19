from django.db import models

class UploadedImage(models.Model):
    original = models.ImageField(upload_to="uploads/")
    enhanced = models.ImageField(upload_to="enhanced/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"
