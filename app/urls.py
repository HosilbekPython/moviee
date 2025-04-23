from rest_framework import routers

from .views import (
    UserViewSet, AdminViewSet, ExploiterViewSet, CountryViewSet, GenreViewSet,
    CompanyViewSet, ActorViewSet, FilmViewSet, CommentViewSet, RatingViewSet
)

router = routers.DefaultRouter()
router.register("users", UserViewSet)
router.register("admins", AdminViewSet)
router.register("exploiters", ExploiterViewSet)
router.register("countries", CountryViewSet)
router.register("genres", GenreViewSet)
router.register("companies", CompanyViewSet)
router.register("actors", ActorViewSet)
router.register("films", FilmViewSet)
router.register("comments", CommentViewSet)
router.register("ratings", RatingViewSet)

urlpatterns = router.urls