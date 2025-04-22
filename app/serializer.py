from rest_framework import serializers
from .models import User, Admin, Exploiter, Genre, Company, Actor, Film, Comment, Rating

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'exploiter')
        )
        return user

    def update(self, instance, validated_data):

        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()
        return instance

class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = ['id', 'user', 'phone_number', 'addres']

    def create(self, validated_data):

        user_data = validated_data.pop('user')

        user_data['role'] = 'admin'

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()


        admin = Admin.objects.create(
            user=user,
            phone_number=validated_data['phone_number'],
            addres=validated_data['addres']
        )
        return admin

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user', None)
        if user_data:

            user_data['role'] = 'admin'

            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()


        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.addres = validated_data.get('addres', instance.addres)
        instance.save()
        return instance

class ExploiterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Exploiter
        fields = ['id', 'user', 'phone_number']

    def create(self, validated_data):

        user_data = validated_data.pop('user')

        user_data['role'] = 'exploiter'

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()


        exploiter = Exploiter.objects.create(
            user=user,
            phone_number=validated_data['phone_number']
        )
        return exploiter

    def update(self, instance, validated_data):

        user_data = validated_data.pop('user', None)
        if user_data:

            user_data['role'] = 'exploiter'

            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()


        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

    def create(self, validated_data):

        name = validated_data['name']
        genre, created = Genre.objects.get_or_create(name=name)
        return genre

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'description']

    def create(self, validated_data):

        name = validated_data['name']
        company, created = Company.objects.get_or_create(
            name=name,
            defaults={'description': validated_data.get('description', '')}
        )
        return company

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'first_name', 'last_name', 'birth_date', 'photo']

    def create(self, validated_data):

        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        actor, created = Actor.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
            defaults={
                'birth_date': validated_data.get('birth_date'),
                'photo': validated_data.get('photo')
            }
        )
        return actor

class FilmSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(required=False, allow_null=True)
    company = CompanySerializer(required=False, allow_null=True)
    actors = ActorSerializer(many=True, required=False)

    class Meta:
        model = Film
        fields = ['id', 'name', 'views', 'genre', 'company', 'actors']

    def create(self, validated_data):

        genre_data = validated_data.pop('genre', None)
        company_data = validated_data.pop('company', None)
        actors_data = validated_data.pop('actors', [])

        genre = None
        if genre_data:
            genre_serializer = GenreSerializer(data=genre_data)
            genre_serializer.is_valid(raise_exception=True)
            genre = genre_serializer.save()
        elif 'genre_id' in self.context['request'].data:
            genre_id = self.context['request'].data.get('genre_id')
            genre = Genre.objects.get(id=genre_id)

        company = None
        if company_data:
            company_serializer = CompanySerializer(data=company_data)
            company_serializer.is_valid(raise_exception=True)
            company = company_serializer.save()
        elif 'company_id' in self.context['request'].data:
            company_id = self.context['request'].data.get('company_id')
            company = Company.objects.get(id=company_id)

        actors = []
        if actors_data:
            for actor_data in actors_data:
                actor_serializer = ActorSerializer(data=actor_data)
                actor_serializer.is_valid(raise_exception=True)
                actor = actor_serializer.save()
                actors.append(actor)
        elif 'actor_ids' in self.context['request'].data:
            actor_ids = self.context['request'].data.get('actor_ids', [])
            actors = Actor.objects.filter(id__in=actor_ids)

        film = Film.objects.create(
            name=validated_data['name'],
            views=validated_data.get('views', 0),
            genre=genre,
            company=company
        )

        if actors:
            film.actors.set(actors)

        return film

    def update(self, instance, validated_data):

        genre_data = validated_data.pop('genre', None)
        company_data = validated_data.pop('company', None)
        actors_data = validated_data.pop('actors', None)

        if genre_data:
            genre_serializer = GenreSerializer(data=genre_data)
            genre_serializer.is_valid(raise_exception=True)
            instance.genre = genre_serializer.save()
        elif 'genre_id' in self.context['request'].data:
            genre_id = self.context['request'].data.get('genre_id')
            instance.genre = Genre.objects.get(id=genre_id) if genre_id else None

        if company_data:
            company_serializer = CompanySerializer(data=company_data)
            company_serializer.is_valid(raise_exception=True)
            instance.company = company_serializer.save()
        elif 'company_id' in self.context['request'].data:
            company_id = self.context['request'].data.get('company_id')
            instance.company = Company.objects.get(id=company_id) if company_id else None

        if actors_data:
            actors = []
            for actor_data in actors_data:
                actor_serializer = ActorSerializer(data=actor_data)
                actor_serializer.is_valid(raise_exception=True)
                actor = actor_serializer.save()
                actors.append(actor)
            instance.actors.set(actors)
        elif 'actor_ids' in self.context['request'].data:
            actor_ids = self.context['request'].data.get('actor_ids', [])
            instance.actors.set(Actor.objects.filter(id__in=actor_ids))

        instance.name = validated_data.get('name', instance.name)
        instance.views = validated_data.get('views', instance.views)
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    film = FilmSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'film', 'text', 'created_at']

    def create(self, validated_data):

        user = self.context['request'].user
        film_id = self.context['request'].data.get('film_id')

        comment = Comment.objects.create(
            user=user,
            film_id=film_id,
            text=validated_data['text']
        )
        return comment

class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    film = FilmSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'film', 'score', 'created_at']

    def create(self, validated_data):

        user = self.context['request'].user
        film_id = self.context['request'].data.get('film_id')

        rating = Rating.objects.create(
            user=user,
            film_id=film_id,
            score=validated_data['score']
        )
        return rating

    def update(self, instance, validated_data):

        instance.score = validated_data.get('score', instance.score)
        instance.save()
        return instance