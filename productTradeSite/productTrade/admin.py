from django.contrib import admin
from productTrade.models import Content, Member, Comment, DropoutMember


class CommentAdmin(admin.ModelAdmin):
    # admin 사이트에서 테이블 필드 순서 변경
    #fields = ['commenter_id', 'content_id', 'text']
    
    # 각 필드 분리해서 보여주기, 튜플의 첫번째 값이 제목
    fieldsets = [
        # 데이터 필드가 많을 때 collapse를 이용해 필드 접어보기 가능
        ('ID Inforamtion', {'fields': ['commenter_id', 'content_id'], 'classes':['collapse']}),
        ('Comment', {'fields': ['text']}),
    ]
    list_display = ('id', 'content_id', 'commenter_id')
    list_filter = ['content_id'] # 정렬 사이드 바 
    search_fields = ['content_id','commenter_id'] # 검색 박스
    
# 외례키 관계 Content-Comment를 Content 화면에서 한 번에 같이 보도록 한다.    
class CommentInline(admin.TabularInline):
    model = Comment 
class ContentAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ('id', 'writer_id', 'title') # 보여지는 필드 지정
    list_filter = ['writer_id'] # 정렬 사이드 바
    search_fields = ['writer_id'] # 검색 박스
        

# admin 사이트에 테이블 반영
admin.site.register(Member)
admin.site.register(Content, ContentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(DropoutMember)

