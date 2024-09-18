from django.contrib.sites.models import Site

# If there's already a site with ID 1, update it. Otherwise, create a new one.
site, created = Site.objects.get_or_create(id=1, defaults={
    'domain': 'example.com',
    'name': 'Example Site'
})

# If the site was not created (it already existed), update it.
if not created:
    site.domain = 'example.com'
    site.name = 'Example Site'
    site.save()