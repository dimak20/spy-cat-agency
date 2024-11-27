from drf_spectacular.openapi import OpenApiParameter

cat_filter_parameters = [
    OpenApiParameter(
        name="name",
        type=str,
        description="Search cat by name. Case insensitive",
        required=False,
    ),
    OpenApiParameter(
        name="breed",
        type=str,
        description="Search cat by breed. Case insensitive",
        required=False,
    ),
    OpenApiParameter(
        name="salary_more_than",
        type=int,
        description="""
            Search cat by salary. 
            Result list will show cats 
            with salary greater than number
            """,
        required=False,
    ),
    OpenApiParameter(
        name="salary_less_than",
        type=int,
        description="""
            Search cat by salary. 
            Result list will show cats 
            with salary less than number
            """,
        required=False,
    ),
]

mission_filter_parameters = [
    OpenApiParameter(
        name="is_complete",
        type=str,
        description="Search mission by complete status.",
        required=False,
    )
]

