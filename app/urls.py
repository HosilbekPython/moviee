from rest_framework import routers

from .views import (
    UserViewSet, AdminViewSet, ExploiterViewSet, GenreViewSet,
    CompanyViewSet, ActorViewSet, FilmViewSet, CommentViewSet, RatingViewSet
)

router = routers.DefaultRouter()

router.register("users" , UserViewSet)
router.register("admins", AdminViewSet)
router.register("exploiter", ExploiterViewSet)
router.register("genres", GenreViewSet)
router.register("companies", CompanyViewSet)
router.register("actors", ActorViewSet)
router.register("films" , FilmViewSet)
router.register("comments", CommentViewSet)
router.register("rating", RatingViewSet)


urlpatterns = router.urls
