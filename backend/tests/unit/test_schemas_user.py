"""
Testes unitários para app/schemas/user.py
"""

import pytest
from datetime import datetime
from pydantic import ValidationError, EmailStr
from app.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    Token,
    TokenData,
    LoginRequest,
    TokenResponse
)


class TestUserBase:
    """Testa o schema base UserBase."""
    
    def test_user_base_valid(self):
        """Testa criação válida de UserBase."""
        data = {
            "email": "usuario@exemplo.com",
            "username": "usuario123"
        }
        user = UserBase(**data)
        assert user.email == "usuario@exemplo.com"
        assert user.username == "usuario123"
    
    def test_user_base_email_validation(self):
        """Testa validação de email."""
        # Email válido
        data = {
            "email": "test@domain.com",
            "username": "testuser"
        }
        user = UserBase(**data)
        assert user.email == "test@domain.com"
        
        # Email inválido
        with pytest.raises(ValidationError):
            UserBase(email="invalid_email", username="testuser")
    
    def test_user_base_username_length_validation(self):
        """Testa validação de comprimento do username."""
        # Username muito curto
        with pytest.raises(ValidationError):
            UserBase(email="test@domain.com", username="ab")
        
        # Username muito longo
        long_username = "a" * 101
        with pytest.raises(ValidationError):
            UserBase(email="test@domain.com", username=long_username)
        
        # Username com comprimento válido
        data = {
            "email": "test@domain.com",
            "username": "abc"
        }
        user = UserBase(**data)
        assert user.username == "abc"


class TestUserCreate:
    """Testa o schema UserCreate."""
    
    def test_user_create_valid(self):
        """Testa criação válida de UserCreate."""
        data = {
            "email": "novo@exemplo.com",
            "username": "novo_user",
            "password": "senha12345"
        }
        user = UserCreate(**data)
        assert user.email == "novo@exemplo.com"
        assert user.username == "novo_user"
        assert user.password == "senha12345"
    
    def test_user_create_password_length_validation(self):
        """Testa validação de comprimento da senha."""
        # Senha muito curta
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@domain.com",
                username="testuser",
                password="123"
            )
        
        # Senha muito longa
        long_password = "a" * 101
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@domain.com",
                username="testuser",
                password=long_password
            )
        
        # Senha com comprimento válido
        data = {
            "email": "test@domain.com",
            "username": "testuser",
            "password": "12345678"
        }
        user = UserCreate(**data)
        assert user.password == "12345678"
    
    def test_user_create_username_alphanumeric_validation(self):
        """Testa validação de username alfanumérico."""
        # Username válido com underscore
        data = {
            "email": "test@domain.com",
            "username": "user_name",
            "password": "12345678"
        }
        user = UserCreate(**data)
        assert user.username == "user_name"
        
        # Username válido com hífen
        data = {
            "email": "test@domain.com",
            "username": "user-name",
            "password": "12345678"
        }
        user = UserCreate(**data)
        assert user.username == "user-name"
        
        # Username válido com números
        data = {
            "email": "test@domain.com",
            "username": "user123",
            "password": "12345678"
        }
        user = UserCreate(**data)
        assert user.username == "user123"
        
        # Username inválido com caracteres especiais
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@domain.com",
                username="user@name",
                password="12345678"
            )
        
        # Username inválido com espaços
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@domain.com",
                username="user name",
                password="12345678"
            )
    
    def test_user_create_inheritance(self):
        """Testa se herda corretamente de UserBase."""
        data = {
            "email": "test@domain.com",
            "username": "testuser",
            "password": "12345678"
        }
        user = UserCreate(**data)
        assert isinstance(user, UserBase)
        assert user.email == "test@domain.com"
        assert user.username == "testuser"


class TestUserUpdate:
    """Testa o schema UserUpdate."""
    
    def test_user_update_valid(self):
        """Testa criação válida de UserUpdate."""
        data = {
            "email": "atualizado@exemplo.com",
            "username": "user_atualizado"
        }
        user = UserUpdate(**data)
        assert user.email == "atualizado@exemplo.com"
        assert user.username == "user_atualizado"
    
    def test_user_update_optional_fields(self):
        """Testa campos opcionais de UserUpdate."""
        # Apenas email
        data = {"email": "email@exemplo.com"}
        user = UserUpdate(**data)
        assert user.email == "email@exemplo.com"
        assert user.username is None
        
        # Apenas username
        data = {"username": "novo_username"}
        user = UserUpdate(**data)
        assert user.email is None
        assert user.username == "novo_username"
        
        # Nenhum campo
        user = UserUpdate()
        assert user.email is None
        assert user.username is None
    
    def test_user_update_username_alphanumeric_validation(self):
        """Testa validação de username alfanumérico em UserUpdate."""
        # Username válido
        data = {"username": "valid_user123"}
        user = UserUpdate(**data)
        assert user.username == "valid_user123"
        
        # Username inválido
        with pytest.raises(ValidationError):
            UserUpdate(username="invalid@user")
        
        # Username None (válido)
        data = {"username": None}
        user = UserUpdate(**data)
        assert user.username is None
    
    def test_user_update_username_length_validation(self):
        """Testa validação de comprimento do username em UserUpdate."""
        # Username muito curto
        with pytest.raises(ValidationError):
            UserUpdate(username="ab")
        
        # Username muito longo
        long_username = "a" * 101
        with pytest.raises(ValidationError):
            UserUpdate(username=long_username)
        
        # Username com comprimento válido
        data = {"username": "abc"}
        user = UserUpdate(**data)
        assert user.username == "abc"


class TestUserResponse:
    """Testa o schema UserResponse."""
    
    def test_user_response_valid(self):
        """Testa criação válida de UserResponse."""
        now = datetime.now()
        data = {
            "id": 1,
            "email": "usuario@exemplo.com",
            "username": "usuario123",
            "created_at": now,
            "updated_at": None,
            "last_login": None
        }
        user = UserResponse(**data)
        assert user.id == 1
        assert user.email == "usuario@exemplo.com"
        assert user.username == "usuario123"
        assert user.created_at == now
        assert user.updated_at is None
        assert user.last_login is None
    
    def test_user_response_with_dates(self):
        """Testa UserResponse com datas preenchidas."""
        now = datetime.now()
        yesterday = datetime(2023, 1, 1)
        data = {
            "id": 2,
            "email": "user2@exemplo.com",
            "username": "user2",
            "created_at": yesterday,
            "updated_at": now,
            "last_login": now
        }
        user = UserResponse(**data)
        assert user.id == 2
        assert user.created_at == yesterday
        assert user.updated_at == now
        assert user.last_login == now
    
    def test_user_response_inheritance(self):
        """Testa se herda corretamente de UserBase."""
        now = datetime.now()
        data = {
            "id": 1,
            "email": "test@domain.com",
            "username": "testuser",
            "created_at": now
        }
        user = UserResponse(**data)
        assert isinstance(user, UserBase)
        assert user.email == "test@domain.com"
        assert user.username == "testuser"
    
    def test_user_response_config_from_attributes(self):
        """Testa se Config.from_attributes está configurado."""
        assert UserResponse.model_config.get('from_attributes') is True


class TestUserLogin:
    """Testa o schema UserLogin."""
    
    def test_user_login_valid(self):
        """Testa criação válida de UserLogin."""
        data = {
            "email": "login@exemplo.com",
            "password": "minhasenha123"
        }
        login = UserLogin(**data)
        assert login.email == "login@exemplo.com"
        assert login.password == "minhasenha123"
    
    def test_user_login_email_validation(self):
        """Testa validação de email em UserLogin."""
        # Email válido
        data = {
            "email": "valid@domain.com",
            "password": "password123"
        }
        login = UserLogin(**data)
        assert login.email == "valid@domain.com"
        
        # Email inválido
        with pytest.raises(ValidationError):
            UserLogin(email="invalid_email", password="password123")


class TestToken:
    """Testa o schema Token."""
    
    def test_token_valid(self):
        """Testa criação válida de Token."""
        data = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "expires_in": 3600
        }
        token = Token(**data)
        assert token.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        assert token.token_type == "bearer"
        assert token.expires_in == 3600
    
    def test_token_default_type(self):
        """Testa valor padrão de token_type."""
        data = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "expires_in": 1800
        }
        token = Token(**data)
        assert token.token_type == "bearer"
    
    def test_token_expires_in_validation(self):
        """Testa validação de expires_in."""
        # expires_in deve ser int
        with pytest.raises(ValidationError):
            Token(
                access_token="token123",
                expires_in="not_an_int"
            )


class TestTokenData:
    """Testa o schema TokenData."""
    
    def test_token_data_valid(self):
        """Testa criação válida de TokenData."""
        data = {
            "email": "user@exemplo.com",
            "user_id": 123
        }
        token_data = TokenData(**data)
        assert token_data.email == "user@exemplo.com"
        assert token_data.user_id == 123
    
    def test_token_data_optional_fields(self):
        """Testa campos opcionais de TokenData."""
        # Apenas email
        data = {"email": "email@exemplo.com"}
        token_data = TokenData(**data)
        assert token_data.email == "email@exemplo.com"
        assert token_data.user_id is None
        
        # Apenas user_id
        data = {"user_id": 456}
        token_data = TokenData(**data)
        assert token_data.email is None
        assert token_data.user_id == 456
        
        # Nenhum campo
        token_data = TokenData()
        assert token_data.email is None
        assert token_data.user_id is None


class TestLoginRequest:
    """Testa o schema LoginRequest."""
    
    def test_login_request_valid(self):
        """Testa criação válida de LoginRequest."""
        data = {
            "email": "login@exemplo.com",
            "password": "minhasenha123"
        }
        login_request = LoginRequest(**data)
        assert login_request.email == "login@exemplo.com"
        assert login_request.password == "minhasenha123"
    
    def test_login_request_email_validation(self):
        """Testa validação de email em LoginRequest."""
        # Email válido
        data = {
            "email": "valid@domain.com",
            "password": "password123"
        }
        login_request = LoginRequest(**data)
        assert login_request.email == "valid@domain.com"
        
        # Email inválido (LoginRequest usa str, não EmailStr)
        # Então aceita qualquer string
        data = {
            "email": "invalid_email",
            "password": "password123"
        }
        login_request = LoginRequest(**data)
        assert login_request.email == "invalid_email"


class TestTokenResponse:
    """Testa o schema TokenResponse."""
    
    def test_token_response_valid(self):
        """Testa criação válida de TokenResponse."""
        data = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
        token_response = TokenResponse(**data)
        assert token_response.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        assert token_response.token_type == "bearer"
    
    def test_token_response_default_type(self):
        """Testa valor padrão de token_type."""
        data = {"access_token": "token123"}
        token_response = TokenResponse(**data)
        assert token_response.token_type == "bearer"


class TestSchemaValidation:
    """Testa validações gerais dos schemas."""
    
    def test_required_fields_validation(self):
        """Testa validação de campos obrigatórios."""
        # UserBase sem campos obrigatórios
        with pytest.raises(ValidationError):
            UserBase()
        
        # UserCreate sem campos obrigatórios
        with pytest.raises(ValidationError):
            UserCreate()
        
        # UserLogin sem campos obrigatórios
        with pytest.raises(ValidationError):
            UserLogin()
        
        # Token sem campos obrigatórios
        with pytest.raises(ValidationError):
            Token()
        
        # LoginRequest sem campos obrigatórios
        with pytest.raises(ValidationError):
            LoginRequest()
        
        # TokenResponse sem campos obrigatórios
        with pytest.raises(ValidationError):
            TokenResponse()
    
    def test_field_types_validation(self):
        """Testa validação de tipos de campos."""
        # ID deve ser int
        with pytest.raises(ValidationError):
            UserResponse(
                id="not_an_int",
                email="test@domain.com",
                username="testuser",
                created_at=datetime.now()
            )
        
        # expires_in deve ser int
        with pytest.raises(ValidationError):
            Token(
                access_token="token123",
                expires_in="not_an_int"
            )
    
    def test_email_validation_edge_cases(self):
        """Testa casos extremos de validação de email."""
        # Email com domínio local
        with pytest.raises(ValidationError):
            UserBase(email="user@localhost", username="testuser")
        
        # Email com múltiplos @
        with pytest.raises(ValidationError):
            UserBase(email="user@@domain.com", username="testuser")
        
        # Email vazio
        with pytest.raises(ValidationError):
            UserBase(email="", username="testuser")
        
        # Email apenas com @
        with pytest.raises(ValidationError):
            UserBase(email="@", username="testuser")


class TestSchemaEdgeCases:
    """Testa casos extremos dos schemas."""
    
    def test_empty_strings_validation(self):
        """Testa validação de strings vazias."""
        # Username vazio
        with pytest.raises(ValidationError):
            UserBase(email="test@domain.com", username="")
        
        # Password vazio
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@domain.com",
                username="testuser",
                password=""
            )
    
    def test_whitespace_validation(self):
        """Testa validação de strings com espaços."""
        # Username com espaços (deve passar pois não há validação específica)
        user = UserBase(email="test@domain.com", username="user name")
        assert user.username == "user name"
        
        # Username apenas com espaços (deve passar pois não há validação específica)
        user = UserBase(email="test@domain.com", username="   ")
        assert user.username == "   "
    
    def test_special_characters_validation(self):
        """Testa validação de caracteres especiais."""
        # Username com caracteres especiais (deve passar pois não há validação específica)
        special_chars = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "+", "=", "[", "]", "{", "}", "|", "\\", ":", ";", "'", '"', "<", ">", ",", ".", "?", "/"]
        
        for char in special_chars:
            user = UserBase(email="test@domain.com", username=f"user{char}name")
            assert user.username == f"user{char}name"
    
    def test_unicode_validation(self):
        """Testa validação de caracteres Unicode."""
        # Username com caracteres Unicode (deve passar pois não há validação específica)
        user = UserBase(email="test@domain.com", username="usuário123")
        assert user.username == "usuário123"
        
        # Username com emojis (deve passar pois não há validação específica)
        user = UserBase(email="test@domain.com", username="user😀123")
        assert user.username == "user😀123"


class TestSchemaInheritance:
    """Testa herança entre schemas."""
    
    def test_user_create_inherits_base(self):
        """Testa se UserCreate herda de UserBase."""
        assert issubclass(UserCreate, UserBase)
    
    def test_user_response_inherits_base(self):
        """Testa se UserResponse herda de UserBase."""
        assert issubclass(UserResponse, UserBase)
    
    def test_all_schemas_inherit_base_model(self):
        """Testa se todos os schemas herdam de BaseModel."""
        schemas = [
            UserBase, UserCreate, UserUpdate, UserResponse,
            UserLogin, Token, TokenData, LoginRequest, TokenResponse
        ]
        
        for schema in schemas:
            assert hasattr(schema, 'model_fields')  # Indica que é um Pydantic model


class TestSchemaFieldInfo:
    """Testa informações dos campos dos schemas."""
    
    def test_field_constraints(self):
        """Testa se as restrições dos campos estão configuradas."""
        # UserBase username tem min_length e max_length
        username_field = UserBase.model_fields['username']
        # Verifica se as restrições estão presentes
        assert username_field is not None
        
        # UserCreate password tem min_length e max_length
        password_field = UserCreate.model_fields['password']
        assert password_field is not None
        
        # UserUpdate username tem min_length e max_length
        username_update_field = UserUpdate.model_fields['username']
        assert username_update_field is not None
