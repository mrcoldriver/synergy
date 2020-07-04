import graphene
from graphene_django import DjangoObjectType

from backend.occupations_list.models import Occupation


class OccupationType(DjangoObjectType):
    class Meta:
        model = Occupation


class Query(graphene.ObjectType):

    get_occupation = graphene.Field(OccupationType, occupation_id=graphene.String())
    get_occupations = graphene.List(OccupationType)

    def resolve_get_occupation(self, info, occupation_id):
        return Occupation.objects.get(pk=occupation_id)

    def resolve_get_occupations(self, info):
        return Occupation.objects.all().order_by('-id')


class Mutation(graphene.ObjectType):

    add_occupation = graphene.Field(OccupationType,
                              name=graphene.String(required=True),
                              company_name =graphene.String(required=True),
                              position_name=graphene.String(required=True),
                              hire_date=graphene.Date(required=True),
                              fire_date=graphene.Date(required=False),
                              salary=graphene.Int(required=True),
                              fraction=graphene.Int(required=True),
                              base=graphene.Int(required=True),
                              advance=graphene.Int(required=True),
                              by_hours=graphene.Boolean(required=True))

    def resolve_add_occupation(self, info, **kwargs):
        return Occupation.objects.create(**kwargs)
