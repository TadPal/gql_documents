import strawberry


@strawberry.type
class Mutation:
    from .documentGQLmodel import document_insert

    document_insert = document_insert

    from .documentGQLmodel import document_update

    document_update = document_update

    from .documentGQLmodel import document_delete

    document_delete = document_delete
    
    from .documentGQLmodel import dspace_add_bitstreams
    
    dspace_add_bitstreams = dspace_add_bitstreams

    pass
