"""
Testes unitários para o módulo de dependências.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from app.core.deps import get_current_user, get_current_active_user
from app.core.security import create_access_token
from app.models.user import User


class TestGetCurrentUser:
    """Testes para a função get_current_user."""
    
    @patch('app.core.deps.decode_access_token')
    @patch('app.core.deps.get_db')
    def test_get_current_user_valid_token(self, mock_get_db, mock_decode_token):
        """Testa obtenção de usuário com token válido."""
        # Mock do banco de dados
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock do token decodificado
        mock_decode_token.return_value = {"sub": "usuario123"}
        
        # Mock do usuário no banco
        mock_user = Mock(spec=User)
        mock_user.id = "usuario123"
        mock_user.email = "usuario@exemplo.com"
        mock_user.is_active = True
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # Chama a função
        result = get_current_user(token="valid_token", db=mock_db)
        
        # Verifica resultado
        assert result is mock_user
        assert result.id == "usuario123"
        assert result.email == "usuario@exemplo.com"
        
        # Verifica se as funções foram chamadas
        mock_decode_token.assert_called_once_with("valid_token")
        mock_db.query.assert_called_once()
    
    @patch('app.core.deps.decode_access_token')
    @patch('app.core.deps.get_db')
    def test_get_current_user_invalid_token(self, mock_get_db, mock_decode_token):
        """Testa obtenção de usuário com token inválido."""
        # Mock do banco de dados
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock de erro no token
        mock_decode_token.side_effect = JWTError("Token inválido")
        
        # Deve lançar exceção
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token="invalid_token", db=mock_db)
        
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in str(exc_info.value.detail)
    
    @patch('app.core.deps.decode_access_token')
    @patch('app.core.deps.get_db')
    def test_get_current_user_user_not_found(self, mock_get_db, mock_decode_token):
        """Testa obtenção de usuário que não existe no banco."""
        # Mock do banco de dados
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock do token decodificado
        mock_decode_token.return_value = {"sub": "usuario_inexistente"}
        
        # Mock de usuário não encontrado
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Deve lançar exceção
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token="valid_token", db=mock_db)
        
        assert exc_info.value.status_code == 404
        assert "User not found" in str(exc_info.value.detail)
    
    @patch('app.core.deps.decode_access_token')
    @patch('app.core.deps.get_db')
    def test_get_current_user_missing_sub(self, mock_get_db, mock_decode_token):
        """Testa obtenção de usuário com token sem campo 'sub'."""
        # Mock do banco de dados
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock do token decodificado sem 'sub'
        mock_decode_token.return_value = {"email": "usuario@exemplo.com"}
        
        # Deve lançar exceção
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token="valid_token", db=mock_db)
        
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in str(exc_info.value.detail)
    
    @patch('app.core.deps.decode_access_token')
    @patch('app.core.deps.get_db')
    def test_get_current_user_empty_token(self, mock_get_db, mock_decode_token):
        """Testa obtenção de usuário com token vazio."""
        # Mock do banco de dados
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock de erro com token vazio
        mock_decode_token.side_effect = JWTError("Token vazio")
        
        # Deve lançar exceção
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token="", db=mock_db)
        
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in str(exc_info.value.detail)
    
    @patch('app.core.deps.decode_access_token')
    @patch('app.core.deps.get_db')
    def test_get_current_user_none_token(self, mock_get_db, mock_decode_token):
        """Testa obtenção de usuário com token None."""
        # Mock do banco de dados
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock de erro com token None
        mock_decode_token.side_effect = JWTError("Token None")
        
        # Deve lançar exceção
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token=None, db=mock_db)
        
        assert exc_info.value.status_code == 401
        assert "Could not validate credentials" in str(exc_info.value.detail)


class TestGetCurrentActiveUser:
    """Testes para a função get_current_active_user."""
    
    @patch('app.core.deps.get_current_user')
    def test_get_current_active_user_active(self, mock_get_current_user):
        """Testa obtenção de usuário ativo."""
        # Mock do usuário ativo
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        mock_user.email = "usuario@exemplo.com"
        
        mock_get_current_user.return_value = mock_user
        
        # Chama a função
        result = get_current_active_user(mock_user)
        
        # Verifica resultado
        assert result is mock_user
        assert result.is_active is True
        
        # Verifica se get_current_user foi chamada
        mock_get_current_user.assert_called_once_with(mock_user)
    
    @patch('app.core.deps.get_current_user')
    def test_get_current_active_user_inactive(self, mock_get_current_user):
        """Testa obtenção de usuário inativo."""
        # Mock do usuário inativo
        mock_user = Mock(spec=User)
        mock_user.is_active = False
        mock_user.email = "usuario@exemplo.com"
        
        mock_get_current_user.return_value = mock_user
        
        # Deve lançar exceção
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user(mock_user)
        
        assert exc_info.value.status_code == 400
        assert "Inactive user" in str(exc_info.value.detail)
    
    @patch('app.core.deps.get_current_user')
    def test_get_current_active_user_none_is_active(self, mock_get_current_user):
        """Testa obtenção de usuário com is_active None."""
        # Mock do usuário com is_active None
        mock_user = Mock(spec=User)
        mock_user.is_active = None
        mock_user.email = "usuario@exemplo.com"
        
        mock_get_current_user.return_value = mock_user
        
        # Deve lançar exceção
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user(mock_user)
        
        assert exc_info.value.status_code == 400
        assert "Inactive user" in str(exc_info.value.detail)
    
    @patch('app.core.deps.get_current_user')
    def test_get_current_active_user_false_is_active(self, mock_get_current_user):
        """Testa obtenção de usuário com is_active False."""
        # Mock do usuário com is_active False
        mock_user = Mock(spec=User)
        mock_user.is_active = False
        mock_user.email = "usuario@exemplo.com"
        
        mock_get_current_user.return_value = mock_user
        
        # Deve lançar exceção
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user(mock_user)
        
        assert exc_info.value.status_code == 400
        assert "Inactive user" in str(exc_info.value.detail)


class TestDependenciesIntegration:
    """Testes de integração das dependências."""
    
    @patch('app.core.deps.decode_access_token')
    @patch('app.core.deps.get_db')
    def test_dependencies_chain(self, mock_get_db, mock_decode_token):
        """Testa a cadeia de dependências."""
        # Mock do banco de dados
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock do token decodificado
        mock_decode_token.return_value = {"sub": "usuario123"}
        
        # Mock do usuário ativo
        mock_user = Mock(spec=User)
        mock_user.id = "usuario123"
        mock_user.email = "usuario@exemplo.com"
        mock_user.is_active = True
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # Testa get_current_user
        current_user = get_current_user(token="valid_token", db=mock_db)
        assert current_user is mock_user
        
        # Testa get_current_active_user
        active_user = get_current_active_user(current_user)
        assert active_user is mock_user
        assert active_user.is_active is True
    
    @patch('app.core.deps.decode_access_token')
    @patch('app.core.deps.get_db')
    def test_dependencies_error_handling(self, mock_get_db, mock_decode_token):
        """Testa tratamento de erros nas dependências."""
        # Mock do banco de dados
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock de erro no token
        mock_decode_token.side_effect = JWTError("Erro de token")
        
        # Deve falhar em get_current_user
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token="invalid_token", db=mock_db)
        
        assert exc_info.value.status_code == 401
        
        # Reset do mock para testar usuário inativo
        mock_decode_token.side_effect = None
        mock_decode_token.return_value = {"sub": "usuario123"}
        
        # Mock do usuário inativo
        mock_user = Mock(spec=User)
        mock_user.id = "usuario123"
        mock_user.is_active = False
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # Deve falhar em get_current_active_user
        current_user = get_current_user(token="valid_token", db=mock_db)
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user(current_user)
        
        assert exc_info.value.status_code == 400


class TestDependenciesEdgeCases:
    """Testes para casos extremos das dependências."""
    
    @patch('app.core.deps.decode_access_token')
    @patch('app.core.deps.get_db')
    def test_get_current_user_malformed_token(self, mock_get_db, mock_decode_token):
        """Testa token malformado."""
        # Mock do banco de dados
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock de erro com token malformado
        mock_decode_token.side_effect = JWTError("Token malformado")
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token="malformed.token", db=mock_db)
        
        assert exc_info.value.status_code == 401
    
    @patch('app.core.deps.decode_access_token')
    @patch('app.core.deps.get_db')
    def test_get_current_user_expired_token(self, mock_get_db, mock_decode_token):
        """Testa token expirado."""
        # Mock do banco de dados
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock de erro com token expirado
        mock_decode_token.side_effect = JWTError("Token expirado")
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(token="expired.token", db=mock_db)
        
        assert exc_info.value.status_code == 401
    
    @patch('app.core.deps.decode_access_token')
    @patch('app.core.deps.get_db')
    def test_get_current_user_database_error(self, mock_get_db, mock_decode_token):
        """Testa erro no banco de dados."""
        # Mock do banco de dados com erro
        mock_db = Mock()
        mock_get_db.return_value = mock_db
        
        # Mock do token decodificado
        mock_decode_token.return_value = {"sub": "usuario123"}
        
        # Mock de erro no banco
        mock_db.query.side_effect = Exception("Erro de banco")
        
        with pytest.raises(Exception) as exc_info:
            get_current_user(token="valid_token", db=mock_db)
        
        assert "Erro de banco" in str(exc_info.value)
    
    @patch('app.core.deps.get_current_user')
    def test_get_current_active_user_missing_attribute(self, mock_get_current_user):
        """Testa usuário sem atributo is_active."""
        # Mock do usuário sem atributo is_active
        mock_user = Mock(spec=User)
        # Não define is_active
        
        mock_get_current_user.return_value = mock_user
        
        # Deve lançar exceção ao tentar acessar is_active
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user(mock_user)
        
        assert exc_info.value.status_code == 400
        assert "Inactive user" in str(exc_info.value.detail)


class TestDependenciesMocking:
    """Testes para verificar se o mocking está funcionando corretamente."""
    
    def test_mock_dependencies_are_called(self):
        """Testa se as dependências mockadas são chamadas corretamente."""
        with patch('app.core.deps.decode_access_token') as mock_decode, \
             patch('app.core.deps.get_db') as mock_get_db:
            
            # Configura os mocks
            mock_db = Mock()
            mock_get_db.return_value = mock_db
            mock_decode.return_value = {"sub": "usuario123"}
            
            # Mock do usuário
            mock_user = Mock(spec=User)
            mock_user.id = "usuario123"
            mock_db.query.return_value.filter.return_value.first.return_value = mock_user
            
            # Chama a função
            get_current_user(token="test_token", db=mock_db)
            
            # Verifica se os mocks foram chamados
            mock_decode.assert_called_once_with("test_token")
            mock_get_db.assert_called_once()
    
    def test_mock_user_attributes(self):
        """Testa se os atributos do usuário mockado são acessíveis."""
        mock_user = Mock(spec=User)
        mock_user.id = "usuario123"
        mock_user.email = "usuario@exemplo.com"
        mock_user.is_active = True
        
        # Verifica se os atributos estão definidos
        assert mock_user.id == "usuario123"
        assert mock_user.email == "usuario@exemplo.com"
        assert mock_user.is_active is True
        
        # Verifica se o mock tem os atributos corretos
        assert hasattr(mock_user, 'id')
        assert hasattr(mock_user, 'email')
        assert hasattr(mock_user, 'is_active')
