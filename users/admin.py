from django.contrib import admin
from .models import*
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
import base64

class UserAdmin(BaseUserAdmin):
    list_display = ["email", "name", "phone_number",'is_admin']
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["phone_number"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["name"]
    filter_horizontal = []

class UserProfileAdminForm(forms.ModelForm):
    # Define file upload fields for images
    upload_image_1 = forms.ImageField(required=False, label="Upload Image 1")
    upload_image_2 = forms.ImageField(required=False, label="Upload Image 2")
    upload_image_3 = forms.ImageField(required=False, label="Upload Image 3")

    class Meta:
        model = UserProfile
        fields = ('user', 'upload_image_1', 'upload_image_2', 'upload_image_3')

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Convert uploaded images to binary and save them to the model fields
        if self.cleaned_data.get('upload_image_1'):
            instance.image_1 = self.cleaned_data['upload_image_1'].file.read()

        if self.cleaned_data.get('upload_image_2'):
            instance.image_2 = self.cleaned_data['upload_image_2'].file.read()

        if self.cleaned_data.get('upload_image_3'):
            instance.image_3 = self.cleaned_data['upload_image_3'].file.read()

        if commit:
            instance.save()
        return instance

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminForm
    list_display = ('user', 'display_image_1', 'display_image_2', 'display_image_3', 'updated_at')

    # Method to display the binary image in the admin list
    def display_image_1(self, obj):
        if obj.image_1:
            # Convert binary data to base64 and render image
            return f'<img src="data:image/jpeg;base64,{base64.b64encode(obj.image_1).decode("utf-8")}" height="100" />'
        return "No Image"

    def display_image_2(self, obj):
        if obj.image_2:
            # Convert binary data to base64 and render image
            return f'<img src="data:image/jpeg;base64,{base64.b64encode(obj.image_2).decode("utf-8")}" height="100" />'
        return "No Image"

    def display_image_3(self, obj):
        if obj.image_3:
            # Convert binary data to base64 and render image
            return f'<img src="data:image/jpeg;base64,{base64.b64encode(obj.image_3).decode("utf-8")}" height="100" />'
        return "No Image"

    # Allow the HTML tag for images
    display_image_1.allow_tags = True
    display_image_1.short_description = 'Image 1'

    display_image_2.allow_tags = True
    display_image_2.short_description = 'Image 2'

    display_image_3.allow_tags = True
    display_image_3.short_description = 'Image 3'

# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile,UserProfileAdmin)