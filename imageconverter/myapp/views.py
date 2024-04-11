from django.shortcuts import render
import csv
import urllib.request
import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import Vehicle
from .forms import CSVUploadForm

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
                    # Here you can write code to download the image and update the URL
                    # For example:
                    # urllib.request.urlretrieve(image_url, 'path_to_save_image_on_server')
                    # updated_image_url = 'new_image_url'
                    # updated_image_urls.append(updated_image_url)
                    updated_image_urls.append(
                        image_url
                    )  # For demonstration, just keeping the original URLs
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
    return render(request, "myapp/upload.html", {"form": form})
