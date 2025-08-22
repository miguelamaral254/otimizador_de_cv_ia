import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends
import fitz # PyMuPDF para manipulação de PDFs

from app.models.user import User
from app.schemas.curriculum import CurriculumResponse
from app.api.dependencies import get_current_user

router = APIRouter()

@router.post("/upload")
async def upload_curriculum(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    # 1. Define o diretório e garante que ele exista
    UPLOAD_DIRECTORY = "storage_curriculum"
    Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

    # 2. Gera um nome de arquivo único e seguro
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = Path(UPLOAD_DIRECTORY) / unique_filename

    # 3. Lê o conteúdo do arquivo e salva no diretório
    contents = await file.read()
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # 4. Extrai o texto do PDF
    extracted_text = ""
    try: 
        with fitz.open(file_path) as doc:
            for page in doc:
                extracted_text += page.get_text()
    except Exception as e:
        # Lida com possíveis erros ao abrir o PDF
        return {"error": f"Erro ao processar o PDF: {e}"}

    # 5. (PRÓXIMO PASSO) SALVAR INFORMAÇÕES NO BANCO DE DADOS
    # Para esta parte, você precisará da sessão do banco de dados (db).
    # Exemplo de como seria a lógica:
    # new_curriculum = Curriculum(
    #     user_id=current_user.id,
    #     original_filename=file.filename,
    #     unique_filename=unique_filename,
    #     file_path=str(file_path),
    #     file_size=len(contents)  # Armazena o tamanho do arquivo em bytes
    # )
    # db.add(new_curriculum)
    # db.commit()
    # db.refresh(new_curriculum)

    # 6. Retorna uma resposta de sucesso
    return {
        "message": "Upload bem-sucedido",
        "original_filename": file.filename,
        "saved_as": unique_filename,
    }       
