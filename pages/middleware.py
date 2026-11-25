from django.shortcuts import render
from django.conf import settings
from .models import Page, BasePageContent


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            getattr(settings, 'MAINTENANCE_MODE', False)
            and not request.path.startswith('/admin/')
            and not request.user.is_staff
        ):
            # Fetch the About page banner image dynamically so it works on every URL
            about_page = Page.objects.filter(slug='about').first()
            image_dict = (
                {img.name: img.image.url for img in about_page.images.all()}
                if about_page
                else {}
            )

            # Include BasePageContent in case base.html relies on context variables
            base_content = BasePageContent.objects.first()

            response = render(
                request,
                'pages/maintenance.html',
                {
                    'image_dict': image_dict,
                    'base_content': base_content,
                },
                status=503,
            )
            # Tells Googlebot to keep your pages indexed and check back later
            response['Retry-After'] = '86400'
            return response

        return self.get_response(request)