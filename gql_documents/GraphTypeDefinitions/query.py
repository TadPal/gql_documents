import strawberry

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################


@strawberry.type(description="""Type for query root""")
class Query:
    from .documentGQLmodel import documents_page

    documents_page = documents_page

    from .documentGQLmodel import document_by_id

    document_by_id = document_by_id
