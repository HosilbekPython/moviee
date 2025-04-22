from rest_framework.viewsets import ModelViewSet
from .models import User, Admin, Exploiter, Genre, Company, Actor, Film, Comment, Rating
from .serializer import (
    UserSerializer, AdminSerializer, ExploiterSerializer, GenreSerializer,
    CompanySerializer, ActorSerializer, FilmSerializer, CommentSerializer, RatingSerializer
)
from .permissions import (
    IsAdmin, IsAuthenticatedOrExploiter, AllowReadOnlyForNonAdmins,
    IsAuthenticatedForComments, IsAuthenticatedForRatings
)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class AdminViewSet(ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdmin]

class ExploiterViewSet(ModelViewSet):
    queryset = Exploiter.objects.all()
    serializer_class = ExploiterSerializer
    permission_classes = [IsAuthenticatedOrExploiter]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == 'exploiter':
            return Exploiter.objects.filter(user=self.request.user)
        return Exploiter.objects.all()

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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role != 'admin':
            return Comment.objects.filter(user=self.request.user)
        return Comment.objects.all()

class RatingViewSet(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedForRatings]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role != 'admin':
            return Rating.objects.filter(user=self.request.user)
        return Rating.objects.all()