from pydantic import BaseModel, ConfigDict

class BaseSchemaMixin(BaseModel):
    """
    Mix-in base para schemas Pydantic, configurando o modo 'from_attributes'
    e permitindo população por nome de campo ou alias.
    """
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)