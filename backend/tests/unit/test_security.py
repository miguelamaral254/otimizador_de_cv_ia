"""
Testes unitários para o módulo de segurança.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from jose import JWTError
from app.core.security import (
    create_access_token,
    decode_access_token,
    verify_password,
    get_password_hash
)


class TestPasswordHashing:
    """Testes para hash e verificação de senhas."""
    
    def test_get_password_hash(self):
        """Testa se a função de hash retorna uma string."""
        password = "minhasenha123"
        hashed = get_password_hash(password)
        
        assert isinstance(hashed, str)
        assert hashed != password
        assert len(hashed) > len(password)
    
    def test_verify_password_correct(self):
        """Testa verificação de senha correta."""
        password = "minhasenha123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Testa verificação de senha incorreta."""
        password = "minhasenha123"
        wrong_password = "senhaerrada456"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False
    
    def test_verify_password_empty(self):
        """Testa verificação de senha vazia."""
        password = ""
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password("qualquercoisa", hashed) is False
    
    def test_verify_password_special_chars(self):
        """Testa verificação de senha com caracteres especiais."""
        password = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password("senha_normal", hashed) is False
    
    def test_verify_password_unicode(self):
        """Testa verificação de senha com caracteres unicode."""
        password = "senha_com_çãõéíóú"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True
        assert verify_password("senha_sem_acentos", hashed) is False
    
    def test_password_hash_consistency(self):
        """Testa se o hash é consistente para a mesma senha."""
        password = "minhasenha123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hash deve ser diferente a cada vez (salt aleatório)
        assert hash1 != hash2
        
        # Mas ambos devem verificar a senha corretamente
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True


class TestAccessToken:
    """Testes para criação e decodificação de tokens de acesso."""
    
    def test_create_access_token(self):
        """Testa criação de token de acesso."""
        data = {"sub": "usuario123"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
        assert "." in token  # JWT tem 3 partes separadas por pontos
    
    def test_create_access_token_with_expires_delta(self):
        """Testa criação de token com tempo de expiração personalizado."""
        data = {"sub": "usuario123"}
        expires_delta = timedelta(minutes=60)
        token = create_access_token(data, expires_delta=expires_delta)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_without_expires_delta(self):
        """Testa criação de token sem tempo de expiração personalizado."""
        data = {"sub": "usuario123"}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_empty_data(self):
        """Testa criação de token com dados vazios."""
        data = {}
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_create_access_token_complex_data(self):
        """Testa criação de token com dados complexos."""
        data = {
            "sub": "usuario123",
            "email": "usuario@exemplo.com",
            "roles": ["admin", "user"],
            "permissions": {"read": True, "write": False}
        }
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_decode_access_token_valid(self):
        """Testa decodificação de token válido."""
        data = {"sub": "usuario123"}
        token = create_access_token(data)
        
        decoded = decode_access_token(token)
        
        assert decoded is not None
        assert "sub" in decoded
        assert decoded["sub"] == "usuario123"
        assert "exp" in decoded  # Campo de expiração deve existir
    
    def test_decode_access_token_with_expires_delta(self):
        """Testa decodificação de token com expiração personalizada."""
        data = {"sub": "usuario123"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta=expires_delta)
        
        decoded = decode_access_token(token)
        
        assert decoded is not None
        assert "sub" in decoded
        assert decoded["sub"] == "usuario123"
        assert "exp" in decoded
    
    def test_decode_access_token_invalid(self):
        """Testa decodificação de token inválido."""
        invalid_token = "invalid.token.here"
        
        # decode_access_token retorna None em caso de erro, não levanta exceção
        result = decode_access_token(invalid_token)
        assert result is None
    
    def test_decode_access_token_empty(self):
        """Testa decodificação de token vazio."""
        # decode_access_token retorna None em caso de erro
        result = decode_access_token("")
        assert result is None
    
    def test_decode_access_token_none(self):
        """Testa decodificação de token None."""
        # None vai causar erro no jwt.decode mas é capturado e retorna None
        result = decode_access_token(None)
        assert result is None
    
    def test_decode_access_token_malformed(self):
        """Testa decodificação de token malformado."""
        malformed_tokens = [
            "just_one_part",
            "two.parts",
            "too.many.parts.here.and.there",
            "part1..part3",  # parte vazia no meio
            ".part2.part3",   # parte vazia no início
            "part1.part2."    # parte vazia no final
        ]
        
        for token in malformed_tokens:
            # decode_access_token retorna None em caso de erro
            result = decode_access_token(token)
            assert result is None


class TestTokenExpiration:
    """Testes para expiração de tokens."""
    
    def test_token_expiration_default(self):
        """Testa expiração padrão do token."""
        data = {"sub": "usuario123"}
        token = create_access_token(data)
        
        decoded = decode_access_token(token)
        
        # Verifica se o token foi decodificado com sucesso
        assert decoded is not None
        assert "sub" in decoded
        assert decoded["sub"] == "usuario123"
        assert "exp" in decoded
        
        # Verifica se exp é um timestamp válido
        exp_timestamp = decoded["exp"]
        assert isinstance(exp_timestamp, (int, float))
        assert exp_timestamp > 0
    
    def test_token_expiration_custom(self):
        """Testa expiração personalizada do token."""
        data = {"sub": "usuario123"}
        expires_delta = timedelta(minutes=5)
        token = create_access_token(data, expires_delta=expires_delta)
        
        decoded = decode_access_token(token)
        
        # Verifica se o token foi decodificado com sucesso
        assert decoded is not None
        assert "sub" in decoded
        assert decoded["sub"] == "usuario123"
        assert "exp" in decoded
        
        # Verifica se exp é um timestamp válido
        exp_timestamp = decoded["exp"]
        assert isinstance(exp_timestamp, (int, float))
        assert exp_timestamp > 0
    
    def test_token_expiration_very_short(self):
        """Testa expiração muito curta do token."""
        data = {"sub": "usuario123"}
        expires_delta = timedelta(seconds=1)
        token = create_access_token(data, expires_delta=expires_delta)
        
        decoded = decode_access_token(token)
        
        # Verifica se o token foi decodificado com sucesso
        assert decoded is not None
        assert "sub" in decoded
        assert decoded["sub"] == "usuario123"
        assert "exp" in decoded
        
        # Verifica se exp é um timestamp válido
        exp_timestamp = decoded["exp"]
        assert isinstance(exp_timestamp, (int, float))
        assert exp_timestamp > 0
    
    def test_token_expiration_long(self):
        """Testa expiração longa do token."""
        data = {"sub": "usuario123"}
        expires_delta = timedelta(hours=24)
        token = create_access_token(data, expires_delta=expires_delta)
        
        decoded = decode_access_token(token)
        
        # Verifica se o token foi decodificado com sucesso
        assert decoded is not None
        assert "sub" in decoded
        assert decoded["sub"] == "usuario123"
        assert "exp" in decoded
        
        # Verifica se exp é um timestamp válido
        exp_timestamp = decoded["exp"]
        assert isinstance(exp_timestamp, (int, float))
        assert exp_timestamp > 0


class TestTokenDataIntegrity:
    """Testes para integridade dos dados do token."""
    
    def test_token_data_preservation(self):
        """Testa se os dados são preservados no token."""
        original_data = {
            "sub": "usuario123",
            "email": "usuario@exemplo.com",
            "nome": "João Silva",
            "idade": 30,
            "ativo": True
        }
        
        token = create_access_token(original_data)
        decoded = decode_access_token(token)
        
        # Todos os campos originais devem estar presentes
        for key, value in original_data.items():
            assert key in decoded
            assert decoded[key] == value
    
    def test_token_data_types(self):
        """Testa se os tipos de dados são preservados."""
        data = {
            "string": "texto",
            "integer": 42,
            "float": 3.14,
            "boolean": True,
            "list": [1, 2, 3],
            "dict": {"key": "value"}
        }
        
        token = create_access_token(data)
        decoded = decode_access_token(token)
        
        # Tipos devem ser preservados
        assert isinstance(decoded["string"], str)
        assert isinstance(decoded["integer"], int)
        assert isinstance(decoded["float"], float)
        assert isinstance(decoded["boolean"], bool)
        assert isinstance(decoded["list"], list)
        assert isinstance(decoded["dict"], dict)
    
    def test_token_nested_data(self):
        """Testa dados aninhados no token."""
        data = {
            "user": {
                "id": "usuario123",
                "profile": {
                    "name": "João",
                    "preferences": {
                        "theme": "dark",
                        "language": "pt-BR"
                    }
                }
            }
        }
        
        token = create_access_token(data)
        decoded = decode_access_token(token)
        
        # Estrutura aninhada deve ser preservada
        assert "user" in decoded
        assert "id" in decoded["user"]
        assert decoded["user"]["id"] == "usuario123"
        assert "profile" in decoded["user"]
        assert "preferences" in decoded["user"]["profile"]
        assert decoded["user"]["profile"]["preferences"]["theme"] == "dark"


class TestSecurityEdgeCases:
    """Testes para casos extremos de segurança."""
    
    def test_token_with_special_characters(self):
        """Testa token com caracteres especiais nos dados."""
        data = {
            "sub": "usuário@123!",
            "email": "teste+tag@exemplo.com",
            "message": "Olá, mundo! 😊"
        }
        
        token = create_access_token(data)
        decoded = decode_access_token(token)
        
        # Caracteres especiais devem ser preservados
        assert decoded["sub"] == "usuário@123!"
        assert decoded["email"] == "teste+tag@exemplo.com"
        assert decoded["message"] == "Olá, mundo! 😊"
    
    def test_token_with_large_data(self):
        """Testa token com dados grandes."""
        large_string = "x" * 1000  # String de 1000 caracteres
        data = {
            "sub": "usuario123",
            "large_field": large_string,
            "numbers": list(range(1000))  # Lista de 1000 números
        }
        
        token = create_access_token(data)
        decoded = decode_access_token(token)
        
        # Dados grandes devem ser preservados
        assert decoded["large_field"] == large_string
        assert len(decoded["numbers"]) == 1000
        assert decoded["numbers"][0] == 0
        assert decoded["numbers"][-1] == 999
    
    def test_token_with_empty_values(self):
        """Testa token com valores vazios."""
        data = {
            "sub": "usuario123",
            "empty_string": "",
            "empty_list": [],
            "empty_dict": {},
            "none_value": None
        }
        
        token = create_access_token(data)
        decoded = decode_access_token(token)
        
        # Valores vazios devem ser preservados
        assert decoded["empty_string"] == ""
        assert decoded["empty_list"] == []
        assert decoded["empty_dict"] == {}
        assert decoded["none_value"] is None
    
    def test_token_with_unicode_data(self):
        """Testa token com dados unicode."""
        data = {
            "sub": "usuário123",
            "emoji": "🚀💻📚",
            "accented": "áéíóúâêîôûãõç",
            "special_chars": "©®™€£¥"
        }
        
        token = create_access_token(data)
        decoded = decode_access_token(token)
        
        # Dados unicode devem ser preservados
        assert decoded["emoji"] == "🚀💻📚"
        assert decoded["accented"] == "áéíóúâêîôûãõç"
        assert decoded["special_chars"] == "©®™€£¥"
