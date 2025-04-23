from rest_framework.viewsets import ModelViewSet
from .models import User, Admin, Exploiter, Country, Genre, Company, Actor, Film, Comment, Rating
from .serializer import (
    UserSerializer, AdminSerializer, ExploiterSerializer, CountrySerializer, GenreSerializer,
    CompanySerializer, ActorSerializer, FilmSerializer, CommentSerializer, RatingSerializer
)
from .permissions import (
    IsAdmin, IsAuthenticatedOrExploiter, AllowReadOnlyForNonAdmins,
    IsAuthenticatedForComments, IsAuthenticatedForRatings
)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowReadOnlyForNonAdmins]  # GET hamma uchun, qolganlari admin uchun

class AdminViewSet(ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [AllowReadOnlyForNonAdmins]  # GET hamma uchun, qolganlari admin uchun

class ExploiterViewSet(ModelViewSet):
    queryset = Exploiter.objects.all()
    serializer_class = ExploiterSerializer
    permission_classes = [IsAuthenticatedOrExploiter]

class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowReadOnlyForNonAdmins]

class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowReadOnlyForNonAdmins]

class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [AllowReadOnlyForNonAdmins]

class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [AllowReadOnlyForNonAdmins]

class FilmViewSet(ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [AllowReadOnlyForNonAdmins]

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedForComments]

class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedForRatings]