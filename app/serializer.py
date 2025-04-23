from rest_framework import serializers
from .models import User, Admin, Exploiter, Country, Genre, Company, Actor, Film, Comment, Rating

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
        fields = ['id', 'user', 'phone_number', 'addres']  # 'addres' o'rniga 'addres'

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

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'flag_image']

    def create(self, validated_data):
        name = validated_data['name']
        country, created = Country.objects.get_or_create(
            name=name,
            defaults={'flag_image': validated_data.get('flag_image', None)}
        )
        return country

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
    genres = GenreSerializer(many=True, required=False)
    company = CompanySerializer(required=False, allow_null=True)
    actors = ActorSerializer(many=True, required=False)
    countries = CountrySerializer(many=True, required=False)

    class Meta:
        model = Film
        fields = ['id', 'name', 'views', 'video', 'genres', 'company', 'actors', 'countries']

    def create(self, validated_data):
        genres_data = validated_data.pop('genres', [])
        company_data = validated_data.pop('company', None)
        actors_data = validated_data.pop('actors', [])
        countries_data = validated_data.pop('countries', [])

        company = None
        if company_data:
            company_serializer = CompanySerializer(data=company_data)
            company_serializer.is_valid(raise_exception=True)
            company = company_serializer.save()
        elif 'company_id' in self.context.get('request', {}).data:
            company_id = self.context['request'].data.get('company_id')
            company = Company.objects.get(id=company_id) if company_id else None

        film = Film.objects.create(
            name=validated_data['name'],
            views=validated_data.get('views', 0),
            video=validated_data.get('video', None),
            company=company
        )

        genres = []
        if genres_data:
            for genre_data in genres_data:
                genre_serializer = GenreSerializer(data=genre_data)
                genre_serializer.is_valid(raise_exception=True)
                genre = genre_serializer.save()
                genres.append(genre)
            film.genres.set(genres)
        elif 'genre_ids' in self.context.get('request', {}).data:
            genre_ids = self.context['request'].data.get('genre_ids', [])
            genres = Genre.objects.filter(id__in=genre_ids)
            film.genres.set(genres)

        actors = []
        if actors_data:
            for actor_data in actors_data:
                actor_serializer = ActorSerializer(data=actor_data)
                actor_serializer.is_valid(raise_exception=True)
                actor = actor_serializer.save()
                actors.append(actor)
            film.actors.set(actors)
        elif 'actor_ids' in self.context.get('request', {}).data:
            actor_ids = self.context['request'].data.get('actor_ids', [])
            actors = Actor.objects.filter(id__in=actor_ids)
            film.actors.set(actors)

        countries = []
        if countries_data:
            for country_data in countries_data:
                country_serializer = CountrySerializer(data=country_data)
                country_serializer.is_valid(raise_exception=True)
                country = country_serializer.save()
                countries.append(country)
            film.countries.set(countries)
        elif 'country_ids' in self.context.get('request', {}).data:
            country_ids = self.context['request'].data.get('country_ids', [])
            countries = Country.objects.filter(id__in=country_ids)
            film.countries.set(countries)

        return film

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('genres', None)
        company_data = validated_data.pop('company', None)
        actors_data = validated_data.pop('actors', None)
        countries_data = validated_data.pop('countries', None)

        if genres_data:
            genres = []
            for genre_data in genres_data:
                genre_serializer = GenreSerializer(data=genre_data)
                genre_serializer.is_valid(raise_exception=True)
                genre = genre_serializer.save()
                genres.append(genre)
            instance.genres.set(genres)
        elif 'genre_ids' in self.context.get('request', {}).data:
            genre_ids = self.context['request'].data.get('genre_ids', [])
            instance.genres.set(Genre.objects.filter(id__in=genre_ids))

        if company_data:
            company_serializer = CompanySerializer(data=company_data)
            company_serializer.is_valid(raise_exception=True)
            instance.company = company_serializer.save()
        elif 'company_id' in self.context.get('request', {}).data:
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
        elif 'actor_ids' in self.context.get('request', {}).data:
            actor_ids = self.context['request'].data.get('actor_ids', [])
            instance.actors.set(Actor.objects.filter(id__in=actor_ids))

        if countries_data:
            countries = []
            for country_data in countries_data:
                country_serializer = CountrySerializer(data=country_data)
                country_serializer.is_valid(raise_exception=True)
                country = country_serializer.save()
                countries.append(country)
            instance.countries.set(countries)
        elif 'country_ids' in self.context.get('request', {}).data:
            country_ids = self.context['request'].data.get('country_ids', [])
            instance.countries.set(Country.objects.filter(id__in=country_ids))

        instance.name = validated_data.get('name', instance.name)
        instance.views = validated_data.get('views', instance.views)
        instance.video = validated_data.get('video', instance.video)
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