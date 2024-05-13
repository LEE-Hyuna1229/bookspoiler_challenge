from django.urls import path
from .views import SpoilerComment, CreateComment, UpdateComment, DeleteComment
# 일반 스포일러 댓글 가져오기, 생성, 수정, 삭제
urlpatterns = [
    path("comments/<int:spoiler_id>", SpoilerComment.as_view(), name="comments_list"),
    path("comment/create/<int:spoiler_id>",CreateComment.as_view(), name="create_comment"),
    path("comment/update/<int:comment_id>", UpdateComment.as_view(), name="update_comment"),
    path("comment/delete/<int:comment_id>", DeleteComment.as_view(), name="delete_comment"),
]