from pydantic import BaseModel, field_validator, EmailStr


#--------INPUT SCHEMAS-------------

#Main schema for User
class User(BaseModel):
    username: str 
    age: int
    email: EmailStr

    @field_validator("username")
    @classmethod
    def username_validator(cls, value):
        if not value.strip():
            raise ValueError("Username field cant be empty")
        return value
        
    @field_validator("age")
    @classmethod
    def age_validator(cls, value):
        if value < 18:
            raise ValueError("User must have 18 years old")
        return value    

#Register input schema, inherite User Base class
class UserRegister(User):
    password: str

    @field_validator("password")
    @classmethod
    def password_validator(cls, value):
        if len(value) < 6:
            raise ValueError("Please specific a stronger password. (at least 6 digit)")
        return value    


#Login input schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_validator(cls, value):
        if len(value) < 6:
            raise ValueError("Please specific a stronger password. (at least 6 digit)")
        return value


#Edit input schema
class UserEdit(User):
    id: int

    

#------- OUTPUT SCHEMA----------------------

#User output response
class UserResponse(BaseModel):
   id: int
   username: str
   email: str
   age: int
   role: str
   image: str

#Auth output response
class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
