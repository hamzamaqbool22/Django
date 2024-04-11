import csv
import urllib.request
from django.shortcuts import render
from django.http import HttpResponse
from .forms import CSVUploadForm
from .models import Vehicle
import json


def download_image(url):
    # Function to download image from given URL
    try:
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
            return image_data
    except Exception as e:
        print(f"Failed to download image from URL: {url}. Error: {e}")
        return None


def index(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["csv_file"]
            decoded_file = csv_file.read().decode("utf-8").splitlines()
            csv_reader = csv.DictReader(decoded_file)
            updated_rows = []
            for row in csv_reader:
                # Download images and update URLs here
                image_urls = json.loads(row["image"])
                updated_image_urls = []
                for image_url in image_urls:
                    # Download image
                    image_data = download_image(image_url)
                    if image_data:
                        # Save the image to your desired location and get the new URL
                        new_image_url = "http://new-image-url.com"
                    else:
                        new_image_url = image_url
                        
                        updated_image_urls.append(new_image_url)
                row["image"] = json.dumps(updated_image_urls)
                updated_rows.append(row)
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                'attachment; filename="updated_vehicles.csv"'
            )
            writer = csv.DictWriter(response, fieldnames=updated_rows[0].keys())
            writer.writeheader()
            for row in updated_rows:
                writer.writerow(row)
            return response
    else:
        form = CSVUploadForm()

    return render(request, 'myapp/upload.html', {'form': form})
