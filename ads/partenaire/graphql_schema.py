import graphene
from partenaire.queries import Query as MainQuery
from partenaire.mutations import Mutation as MainMutation

class Query(MainQuery, graphene.ObjectType):
    pass

class Mutation(MainMutation, graphene.ObjectType):
    pass


# Objet Schema attendu par GraphQLView
schema = graphene.Schema(query=Query, mutation=Mutation)
