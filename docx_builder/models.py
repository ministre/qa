from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


class DocxProfile(models.Model):
    name = models.CharField(max_length=1000)
    type = models.IntegerField(default=0)
    header_subtitle = models.CharField(max_length=1000, blank=True, null=True)
    header_logo = models.FileField(upload_to="docx_builder/files/", blank=True, null=True)

    title_font_name = models.CharField(max_length=1000, blank=True, null=True, default='Calibri')
    title_font_color_red = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    title_font_color_green = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    title_font_color_blue = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    title_font_size = models.IntegerField(default=20, validators=[MinValueValidator(10), MaxValueValidator(40)])
    title_font_bold = models.BooleanField(blank=True, null=True, default=True)
    title_font_italic = models.BooleanField(blank=True, null=True, default=False)
    title_font_underline = models.BooleanField(blank=True, null=True, default=False)
    title_space_before = models.IntegerField(default=12, validators=[MinValueValidator(0), MaxValueValidator(40)])
    title_space_after = models.IntegerField(default=12, validators=[MinValueValidator(0), MaxValueValidator(40)])
    title_alignment = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])

    h1_font_name = models.CharField(max_length=1000, blank=True, null=True, default='Calibri')
    h1_font_color_red = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h1_font_color_green = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h1_font_color_blue = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h1_font_size = models.IntegerField(default=16, validators=[MinValueValidator(10), MaxValueValidator(40)])
    h1_font_bold = models.BooleanField(blank=True, null=True, default=True)
    h1_font_italic = models.BooleanField(blank=True, null=True, default=False)
    h1_font_underline = models.BooleanField(blank=True, null=True, default=False)
    h1_space_before = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    h1_space_after = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    h1_alignment = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])

    h2_font_name = models.CharField(max_length=1000, blank=True, null=True, default='Calibri')
    h2_font_color_red = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h2_font_color_green = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h2_font_color_blue = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h2_font_size = models.IntegerField(default=14, validators=[MinValueValidator(10), MaxValueValidator(40)])
    h2_font_bold = models.BooleanField(blank=True, null=True, default=True)
    h2_font_italic = models.BooleanField(blank=True, null=True, default=False)
    h2_font_underline = models.BooleanField(blank=True, null=True, default=False)
    h2_space_before = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    h2_space_after = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    h2_alignment = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])

    h3_font_name = models.CharField(max_length=1000, blank=True, null=True, default='Calibri')
    h3_font_color_red = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h3_font_color_green = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h3_font_color_blue = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    h3_font_size = models.IntegerField(default=14, validators=[MinValueValidator(10), MaxValueValidator(40)])
    h3_font_bold = models.BooleanField(blank=True, null=True, default=True)
    h3_font_italic = models.BooleanField(blank=True, null=True, default=False)
    h3_font_underline = models.BooleanField(blank=True, null=True, default=False)
    h3_space_before = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    h3_space_after = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    h3_alignment = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])

    normal_font_name = models.CharField(max_length=1000, blank=True, null=True, default='Calibri')
    normal_color_red = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    normal_color_green = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    normal_color_blue = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    normal_font_size = models.IntegerField(default=14, validators=[MinValueValidator(10), MaxValueValidator(40)])
    normal_font_bold = models.BooleanField(blank=True, null=True, default=True)
    normal_font_italic = models.BooleanField(blank=True, null=True, default=False)
    normal_font_underline = models.BooleanField(blank=True, null=True, default=False)
    normal_space_before = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    normal_space_after = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    normal_alignment = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])

    caption_font_name = models.CharField(max_length=1000, blank=True, null=True, default='Calibri')
    caption_color_red = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    caption_color_green = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    caption_color_blue = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    caption_font_size = models.IntegerField(default=11, validators=[MinValueValidator(10), MaxValueValidator(40)])
    caption_font_bold = models.BooleanField(blank=True, null=True, default=True)
    caption_font_italic = models.BooleanField(blank=True, null=True, default=False)
    caption_font_underline = models.BooleanField(blank=True, null=True, default=True)
    caption_space_before = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    caption_space_after = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    caption_alignment = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])

    quote_font_name = models.CharField(max_length=1000, blank=True, null=True, default='Calibri')
    quote_color_red = models.IntegerField(default=255, validators=[MinValueValidator(0), MaxValueValidator(255)])
    quote_color_green = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    quote_color_blue = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(255)])
    quote_font_size = models.IntegerField(default=13, validators=[MinValueValidator(10), MaxValueValidator(40)])
    quote_font_bold = models.BooleanField(blank=True, null=True, default=True)
    quote_font_italic = models.BooleanField(blank=True, null=True, default=False)
    quote_font_underline = models.BooleanField(blank=True, null=True, default=False)
    quote_space_before = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    quote_space_after = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(40)])
    quote_alignment = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])

    created_by = models.ForeignKey(User, related_name='docx_profile_c', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(User, related_name='docx_profile_u', on_delete=models.CASCADE, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

    def update_timestamp(self, user):
        self.updated_by = user
        self.updated_at = datetime.now()
        self.save()
        return True
