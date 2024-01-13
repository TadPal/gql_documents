import strawberry


###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################
@strawberry.type
class Mutation:
    from .documentGQLmodel import (
        document_insert,
        document_update,
        document_delete,
        dspace_add_bitstream,
        dspace_get_bitstream,
    )

    document_insert = document_insert
    document_update = document_update
    document_delete = document_delete
    dspace_add_bitstream = dspace_add_bitstream
    dspace_get_bitstream = dspace_get_bitstream


@strawberry.type(description="""Type for query root""")
class Query:
    from .documentGQLmodel import (
        documents_page,
        document_by_id,
    )

    documents_page = documents_page
    document_by_id = document_by_id


schema = strawberry.federation.Schema(query=Query, mutation=Mutation)
