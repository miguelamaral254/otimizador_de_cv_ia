"""
Testes unitários para o modelo User.
"""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.core.database import Base


class TestUserModel:
    """Testes para o modelo User."""
    
    def test_user_creation(self):
        """Testa criação básica de um usuário."""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password_123"
        )
        
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.hashed_password == "hashed_password_123"
        assert user.id is None  # Não foi salvo ainda
    
    def test_user_tablename(self):
        """Testa se o nome da tabela está correto."""
        assert User.__tablename__ == "users"
    
    def test_user_repr(self):
        """Testa representação string do usuário."""
        user = User(
            id=1,
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password_123"
        )
        
        expected = "<User(id=1, email='test@example.com', username='testuser')>"
        assert repr(user) == expected
    
    def test_user_attributes(self):
        """Testa atributos do modelo User."""
        user = User()
        
        # Verifica se todos os atributos necessários existem
        assert hasattr(user, 'id')
        assert hasattr(user, 'email')
        assert hasattr(user, 'username')
        assert hasattr(user, 'hashed_password')
        assert hasattr(user, 'created_at')
        assert hasattr(user, 'updated_at')
        assert hasattr(user, 'last_login')
        assert hasattr(user, 'curriculum')
    
    def test_user_table_columns(self):
        """Testa configuração das colunas da tabela."""
        # Verifica se as colunas estão configuradas corretamente
        id_column = User.__table__.columns['id']
        email_column = User.__table__.columns['email']
        username_column = User.__table__.columns['username']
        password_column = User.__table__.columns['hashed_password']
        
        # Testa propriedades das colunas
        assert id_column.primary_key is True
        assert id_column.index is True
        assert email_column.unique is True
        assert email_column.index is True
        assert email_column.nullable is False
        assert username_column.unique is True
        assert username_column.index is True
        assert username_column.nullable is False
        assert password_column.nullable is False
    
    def test_user_optional_fields(self):
        """Testa campos opcionais do usuário."""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password_123"
        )
        
        # Campos que podem ser None
        assert user.last_login is None
        assert user.created_at is None  # Será definido pelo servidor
        assert user.updated_at is None  # Será definido pelo servidor
    
    def test_user_with_timestamps(self):
        """Testa usuário com timestamps."""
        current_time = datetime.utcnow()
        
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password_123",
            created_at=current_time,
            updated_at=current_time,
            last_login=current_time
        )
        
        assert user.created_at == current_time
        assert user.updated_at == current_time
        assert user.last_login == current_time


class TestUserValidation:
    """Testes para validação do modelo User."""
    
    def test_user_email_validation(self):
        """Testa validação do email."""
        # Emails válidos
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "123@numbers.com",
            "long.email.address@very.long.domain.name.com"
        ]
        
        for email in valid_emails:
            user = User(
                email=email,
                username="testuser",
                hashed_password="password"
            )
            assert user.email == email
    
    def test_user_username_validation(self):
        """Testa validação do username."""
        # Usernames válidos
        valid_usernames = [
            "testuser",
            "user123",
            "user_name",
            "a" * 100  # Máximo de 100 caracteres
        ]
        
        for username in valid_usernames:
            user = User(
                email="test@example.com",
                username=username,
                hashed_password="password"
            )
            assert user.username == username
    
    def test_user_password_validation(self):
        """Testa validação da senha hash."""
        # Diferentes tipos de hash
        valid_passwords = [
            "simple_hash",
            "$2b$12$hash.with.bcrypt.format",
            "very_long_hash_" + "x" * 200
        ]
        
        for password in valid_passwords:
            user = User(
                email="test@example.com",
                username="testuser",
                hashed_password=password
            )
            assert user.hashed_password == password


class TestUserRelationships:
    """Testes para relacionamentos do modelo User."""
    
    def test_user_curriculum_relationship(self):
        """Testa relacionamento com Curriculum."""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="password"
        )
        
        # Verifica se o relacionamento existe
        assert hasattr(user, 'curriculum')
        
        # Verifica se é uma lista (relacionamento one-to-many)
        # Em SQLAlchemy, relacionamentos retornam InstrumentedList
        curriculum_attr = getattr(User, 'curriculum')
        assert hasattr(curriculum_attr.property, 'back_populates')
        assert curriculum_attr.property.back_populates == 'user'
    
    def test_user_curriculum_cascade(self):
        """Testa configuração de cascade."""
        curriculum_relationship = User.curriculum.property
        
        # Verifica se o cascade está configurado
        assert curriculum_relationship.cascade.delete_orphan is True
        assert 'delete' in str(curriculum_relationship.cascade)


class TestUserEquality:
    """Testes para comparação de usuários."""
    
    def test_user_equality_by_id(self):
        """Testa igualdade de usuários por ID."""
        user1 = User(
            id=1,
            email="test1@example.com",
            username="user1",
            hashed_password="pass1"
        )
        
        user2 = User(
            id=1,
            email="test2@example.com",
            username="user2",
            hashed_password="pass2"
        )
        
        user3 = User(
            id=2,
            email="test1@example.com",
            username="user1",
            hashed_password="pass1"
        )
        
        # Usuários com mesmo ID devem ser considerados iguais
        # (comportamento padrão do SQLAlchemy)
        assert user1.id == user2.id
        assert user1.id != user3.id
    
    def test_user_different_instances(self):
        """Testa que instâncias diferentes são objetos diferentes."""
        user1 = User(
            email="test@example.com",
            username="testuser",
            hashed_password="password"
        )
        
        user2 = User(
            email="test@example.com",
            username="testuser",
            hashed_password="password"
        )
        
        # Mesmo dados, mas objetos diferentes
        assert user1 is not user2


class TestUserEdgeCases:
    """Testes para casos extremos do modelo User."""
    
    def test_user_empty_values(self):
        """Testa usuário com valores vazios."""
        # Strings vazias (mas não None)
        user = User(
            email="",
            username="",
            hashed_password=""
        )
        
        assert user.email == ""
        assert user.username == ""
        assert user.hashed_password == ""
    
    def test_user_long_values(self):
        """Testa usuário com valores longos."""
        long_email = "a" * 240 + "@example.com"  # ~255 chars
        long_username = "u" * 100  # 100 chars (máximo)
        long_password = "p" * 255  # 255 chars
        
        user = User(
            email=long_email,
            username=long_username,
            hashed_password=long_password
        )
        
        assert len(user.email) <= 255
        assert len(user.username) <= 100
        assert len(user.hashed_password) == 255
    
    def test_user_special_characters(self):
        """Testa usuário com caracteres especiais."""
        special_email = "test+tag@example-domain.com"
        special_username = "user_name-123"
        special_password = "pa$$w0rd!@#$%^&*()"
        
        user = User(
            email=special_email,
            username=special_username,
            hashed_password=special_password
        )
        
        assert user.email == special_email
        assert user.username == special_username
        assert user.hashed_password == special_password
    
    def test_user_unicode_characters(self):
        """Testa usuário com caracteres unicode."""
        unicode_email = "joão@domínio.com"
        unicode_username = "usuário123"
        
        user = User(
            email=unicode_email,
            username=unicode_username,
            hashed_password="password"
        )
        
        assert user.email == unicode_email
        assert user.username == unicode_username


class TestUserSerialization:
    """Testes para serialização do modelo User."""
    
    def test_user_dict_conversion(self):
        """Testa conversão do usuário para dicionário."""
        user = User(
            id=1,
            email="test@example.com",
            username="testuser",
            hashed_password="password"
        )
        
        # Verifica se pode acessar atributos como dict
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.hashed_password == "password"
    
    def test_user_attribute_access(self):
        """Testa acesso aos atributos do usuário."""
        user = User()
        
        # Testa se pode definir e acessar atributos
        user.email = "new@example.com"
        user.username = "newuser"
        
        assert user.email == "new@example.com"
        assert user.username == "newuser"
    
    def test_user_dynamic_attributes(self):
        """Testa atributos dinâmicos do usuário."""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="password"
        )
        
        # Testa se pode adicionar atributos dinâmicos
        # (não recomendado, mas tecnicamente possível)
        user.custom_field = "custom_value"
        assert user.custom_field == "custom_value"


class TestUserTableStructure:
    """Testes para estrutura da tabela User."""
    
    def test_user_table_exists(self):
        """Testa se a tabela User está definida."""
        assert hasattr(User, '__table__')
        assert User.__table__.name == "users"
    
    def test_user_primary_key(self):
        """Testa chave primária da tabela."""
        pk_columns = [col for col in User.__table__.columns if col.primary_key]
        
        assert len(pk_columns) == 1
        assert pk_columns[0].name == 'id'
        assert pk_columns[0].type.python_type == int
    
    def test_user_indexes(self):
        """Testa índices da tabela."""
        indexed_columns = [
            col.name for col in User.__table__.columns 
            if col.index or col.unique
        ]
        
        # Colunas que devem ter índice
        expected_indexed = ['id', 'email', 'username']
        
        for column in expected_indexed:
            assert column in indexed_columns
    
    def test_user_unique_constraints(self):
        """Testa restrições de unicidade."""
        unique_columns = [
            col.name for col in User.__table__.columns 
            if col.unique
        ]
        
        # Colunas que devem ser únicas
        expected_unique = ['email', 'username']
        
        for column in expected_unique:
            assert column in unique_columns
    
    def test_user_nullable_constraints(self):
        """Testa restrições de nulidade."""
        non_nullable = [
            col.name for col in User.__table__.columns 
            if not col.nullable
        ]
        
        nullable = [
            col.name for col in User.__table__.columns 
            if col.nullable
        ]
        
        # Colunas obrigatórias
        expected_non_nullable = ['email', 'username', 'hashed_password']
        for column in expected_non_nullable:
            assert column in non_nullable
        
        # Colunas opcionais
        expected_nullable = ['last_login']
        for column in expected_nullable:
            assert column in nullable


class TestUserModelIntegration:
    """Testes de integração para o modelo User."""
    
    def test_user_base_inheritance(self):
        """Testa se User herda de Base."""
        assert issubclass(User, Base)
    
    def test_user_sqlalchemy_integration(self):
        """Testa integração com SQLAlchemy."""
        # Verifica se tem metadados do SQLAlchemy
        assert hasattr(User, '__table__')
        assert hasattr(User, '__mapper__')
        assert hasattr(User, 'metadata')
    
    def test_user_column_types(self):
        """Testa tipos das colunas."""
        from sqlalchemy import Integer, String, Boolean, DateTime
        
        # Verifica tipos das principais colunas
        columns = User.__table__.columns
        
        assert str(columns['id'].type) == 'INTEGER'
        assert 'VARCHAR' in str(columns['email'].type)
        assert 'VARCHAR' in str(columns['username'].type)
        assert 'VARCHAR' in str(columns['hashed_password'].type)
        assert 'DATETIME' in str(columns['created_at'].type)


class TestUserMockData:
    """Testes com dados mock para User."""
    
    def test_user_factory(self):
        """Testa criação de usuários com factory pattern."""
        def create_user(email=None, username=None, password=None):
            return User(
                email=email or "default@example.com",
                username=username or "defaultuser",
                hashed_password=password or "defaultpass"
            )
        
        # Usuário padrão
        user1 = create_user()
        assert user1.email == "default@example.com"
        
        # Usuário customizado
        user2 = create_user(email="custom@example.com")
        assert user2.email == "custom@example.com"
        assert user2.username == "defaultuser"
    
    def test_user_bulk_creation(self):
        """Testa criação em massa de usuários."""
        users = []
        
        for i in range(10):
            user = User(
                email=f"user{i}@example.com",
                username=f"user{i}",
                hashed_password=f"password{i}"
            )
            users.append(user)
        
        assert len(users) == 10
        assert users[0].email == "user0@example.com"
        assert users[9].username == "user9"
    
    def test_user_data_variations(self):
        """Testa diferentes variações de dados de usuário."""
        test_cases = [
            {
                'email': 'simple@test.com',
                'username': 'simple',
                'password': 'pass123'
            },
            {
                'email': 'complex.email+tag@subdomain.domain.co.uk',
                'username': 'complex_user_123',
                'password': '$2b$12$very.long.bcrypt.hash.here'
            },
            {
                'email': 'números123@domínio.com.br',
                'username': 'usuário_especial',
                'password': 'sênha_cõmplèxa!@#$'
            }
        ]
        
        for case in test_cases:
            user = User(
                email=case['email'],
                username=case['username'],
                hashed_password=case['password']
            )
            
            assert user.email == case['email']
            assert user.username == case['username']
            assert user.hashed_password == case['password']
