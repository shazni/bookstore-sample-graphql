import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db.models import Q

from .models import Book

class BookType(DjangoObjectType):
    class Meta:
        model = Book

class Query(graphene.ObjectType):
    books = graphene.List(BookType, search=graphene.String())

    def resolve_books(self, info, search=None):
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(description__icontains=search) |
                Q(publisher_book_url__icontains=search) 
            )
            return Book.objects.filter(filter)

        return Book.objects.all()

class CreateBook(graphene.Mutation):
    book = graphene.Field(BookType)

    class Arguments:
        title = graphene.String()
        author = graphene.String()
        description = graphene.String()
        publisher_book_url = graphene.String()

    def mutate(self, info, **kwargs):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError("user must logged in to create a book")

        book = Book(title=kwargs.get('title'), author=kwargs.get('author'), 
                    description=kwargs.get('description'), publisher_book_url=kwargs.get('publisher_book_url'))

        book.save()
        return CreateBook(book=book)

class UpdateBook(graphene.Mutation):
    book = graphene.Field(BookType)

    class Arguments:
        book_id = graphene.Int(required=True)
        title = graphene.String()
        author = graphene.String()
        description = graphene.String()
        publisher_book_url = graphene.String()

    def mutate(self, info, book_id, title=None, author=None, description=None, publisher_book_url=None):
        user = info.context.user
        book = Book.objects.get(id=book_id)

        if user.is_anonymous:
            raise GraphQLError("user must logged in to update a book. Also user must be the creator")

        book.title = title if title != None and title != "" else book.title
        book.author = author if author != None and author != "" else book.author
        book.description = description if description != None and description != "" else book.description
        book.publisher_book_url = publisher_book_url \
            if publisher_book_url != None and publisher_book_url != "" else book.publisher_book_url

        book.save()

        return UpdateBook(book=book)

class DeleteBook(graphene.Mutation):
    book_id = graphene.Int()

    class Arguments:
        book_id = graphene.Int(required=True)

    def mutate(self, info, book_id):
        user = info.context.user
        book = Book.objects.get(id=book_id)

        if user.is_anonymous:
            raise GraphQLError("user must logged in to update a book. Also user must be the creator")

        book.delete()

        return DeleteBook(book_id=book_id)


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()