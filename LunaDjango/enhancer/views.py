from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import UploadedImage
from .psr_image_enhancer import enhance_psr_image
import os
from django.conf import settings

def upload_image(request):
    """Handle image upload and enhancement."""
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()
            input_path = os.path.join(settings.MEDIA_ROOT, str(uploaded_image.original))

            # ✅ Check if file exists before processing
            if not os.path.exists(input_path):
                form.add_error(None, "File not found. Please try uploading again.")
                return render(request, "upload.html", {"form": form})

            # Define output path
            output_folder = os.path.join(settings.MEDIA_ROOT, "enhanced")
            os.makedirs(output_folder, exist_ok=True)  # Ensure directory exists
            output_path = os.path.join(output_folder, f"enhanced_{uploaded_image.id}.png")

            # Process Image
            enhance_psr_image(input_path, output_path)

            # Save enhanced image path in the model
            uploaded_image.enhanced = f"enhanced/enhanced_{uploaded_image.id}.png"
            uploaded_image.save()

            return redirect('result', image_id=uploaded_image.id)
    else:
        form = ImageUploadForm()
    
    return render(request, "upload.html", {"form": form})

def result(request, image_id):
    """Display the original and enhanced image."""
    image = UploadedImage.objects.get(id=image_id)
    return render(request, "result.html", {"image": image})
