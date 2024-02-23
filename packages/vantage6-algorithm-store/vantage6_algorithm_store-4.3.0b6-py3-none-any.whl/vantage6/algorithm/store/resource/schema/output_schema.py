from marshmallow import fields

from vantage6.backend.common.resource.output_schema import BaseHATEOASModelSchema
from vantage6.algorithm.store.model.algorithm import Algorithm
from vantage6.algorithm.store.model.argument import Argument
from vantage6.algorithm.store.model.database import Database
from vantage6.algorithm.store.model.function import Function
from vantage6.algorithm.store.model.vantage6_server import Vantage6Server


class HATEOASModelSchema(BaseHATEOASModelSchema):
    """
    This class is used to convert foreign-key fields to HATEOAS specification.
    """

    def __init__(self, *args, **kwargs) -> None:
        # set lambda functions to create links for one to one relationship
        # TODO check if all below are used
        setattr(self, "algorithm", lambda obj: self.create_hateoas("algorithm", obj))
        setattr(self, "function", lambda obj: self.create_hateoas("function", obj))
        setattr(self, "database", lambda obj: self.create_hateoas("database", obj))
        setattr(self, "argument", lambda obj: self.create_hateoas("argument", obj))

        # call super class. Do this after setting the attributes above, because
        # the super class initializer will call the attributes.
        super().__init__(*args, **kwargs)


class AlgorithmOutputSchema(HATEOASModelSchema):
    """Marshmallow output schema to serialize the Algorithm model"""

    class Meta:
        model = Algorithm

    functions = fields.Nested("FunctionOutputSchema", many=True, exclude=["id"])


class FunctionOutputSchema(HATEOASModelSchema):
    """Marshmallow output schema to serialize the Function model"""

    class Meta:
        model = Function
        exclude = ["type_"]

    type = fields.String(attribute="type_")

    databases = fields.Nested("DatabaseOutputSchema", many=True, exclude=["id"])
    arguments = fields.Nested("ArgumentOutputSchema", many=True, exclude=["id"])


class DatabaseOutputSchema(HATEOASModelSchema):
    """Marshmallow output schema to serialize the Database model"""

    class Meta:
        model = Database


class ArgumentOutputSchema(HATEOASModelSchema):
    """Marshmallow output schema to serialize the Argument model"""

    class Meta:
        model = Argument
        exclude = ["type_"]

    type = fields.String(attribute="type_")


class Vantage6ServerOutputSchema(HATEOASModelSchema):
    """Marshmallow output schema to serialize the Vantage6Server model"""

    class Meta:
        model = Vantage6Server
