from django.contrib import admin

# Register your models here.


from .models import Blog, Contact,Category,Tag,FeaturedBlog

# Register your models here.

admin.site.register(Blog)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(FeaturedBlog)