from pydantic import BaseModel, EmailStr, Field

class GeoSchema(BaseModel):
    lat: str
    lng: str

class AddressSchema(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoSchema

class ComapnySchema(BaseModel):
    name: str
    catchPharse: str
    bs: str

class UserSchema(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str | None = None
    website: str | None = None
    address: AddressSchema
    company: ComapnySchema

class PostSchema(BaseModel):
    id: int
    userId: int
    title: str = Field(min_length=1)
    body: str

class CommentSchema(BaseModel):
    id: int
    postId: int
    name: str
    email: EmailStr
    body: str