from django.contrib import admin
from .models import Tag, News, Category

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TagFilter(admin.SimpleListFilter):
    title = 'Тэги'
    parameter_name = 'tags'
    def lookups(self, request, model_admin):
        return [(tag.id, tag.name) for tag in Tag.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tags__id=self.value())
        return queryset


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content','actual', 'category', 'brief_info', 'person_info')
    list_display_links = ('id', 'title')
    ordering = ['title']
    list_editable = ('actual','category', 'content')
    actions = ['set_actuality','set_deactuality']
    search_fields = ['content','category__name']
    list_filter = [TagFilter, 'actual']


    @admin.display(description="Краткое описание")
    def brief_info(self, news: News):
        return f"Описание {len(news.content)} символов."

    @admin.display(description="Персоналии")
    def person_info(self, news: News):
        return f"Все, кто отмечены в новости"

    @admin.action(description="Актуализировать выбранные записи")
    def set_actuality(self, request, queryset):
        count = queryset.update(actual=True)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Деактуализировать выбранные записи")
    def set_deactuality(self, request, queryset):
        count = queryset.update(actual=False)
        self.message_user(request, f"Изменено {count} записи(ей).")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

