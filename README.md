
## Desafio Técnico do Time: Projeto Otimizador de Currículos com IA

**Olá, time!**

Bem-vindos ao nosso novo desafio técnico! Este projeto foi desenhado para aplicarmos e aprimorarmos nossas habilidades em desenvolvimento full-stack, criando uma ferramenta de alto impacto e relevância. Vamos construir juntos uma plataforma completa, desde o backend até o frontend, utilizando um fluxo de trabalho profissional com Git e GitHub.

### Visão Geral do Projeto

Vamos desenvolver uma plataforma de software como serviço (SaaS) chamada **"Otimizador de Currículos"**. O objetivo é que usuários possam fazer o upload de seus currículos em formato `.pdf`, receber análises detalhadas e acionáveis geradas por IA, e acompanhar a evolução da qualidade de seus currículos ao longo do tempo através de um histórico de versões.

### Objetivo Principal

O objetivo deste projeto é construir uma aplicação web funcional e robusta, que envolve manipulação de arquivos, integração com IA para análise de texto, um sistema de autenticação seguro e lógica para análise de dados históricos. O sucesso será medido pela qualidade da integração entre as tecnologias e pela entrega de uma ferramenta coesa e com valor prático para o usuário final.

---

### Processo de Desenvolvimento e Entrega via GitHub

Todo o desenvolvimento e a entrega final serão gerenciados através do GitHub para simular nosso fluxo de trabalho padrão.

1.  **Fork do Repositório:**
    * O primeiro passo é que o time realize um **fork** do repositório principal do projeto, que servirá como base.
    * **Repositório Principal:** [https://github.com/miguelamaral254/otimizador_de_cv_ia](https://github.com/miguelamaral254/otimizador_de_cv_ia)

2.  **Desenvolvimento no Fork:**
    * Após criar o fork, clonem **o fork de vocês** para suas máquinas locais. Todo o código do desafio será desenvolvido dentro deste fork.
    * Sugerimos que organizem o trabalho em branches separadas (ex: `feat/backend-setup`, `feat/frontend-auth`).
    * Mantenham uma boa prática de commits: pequenos, frequentes e com mensagens claras.

3.  **Estrutura do Projeto:**
    * Dentro do repositório, criem duas pastas principais na raiz para separar claramente as responsabilidades:
        * `/frontend`: Contendo toda a aplicação React.
        * `/backend`: Contendo toda a aplicação FastAPI (Python).

4.  **Entrega Final (Pull Request):**
    * Quando o desenvolvimento estiver concluído e testado, o time deverá abrir um **único Pull Request** a partir do seu fork para a branch `main` do repositório principal.
    * Na descrição do Pull Request, incluam um resumo do que foi feito, as decisões de arquitetura que tomaram e, se possível, um link para a aplicação funcionando (se tiverem feito o deploy em algum serviço).

---

### Requisitos e Funcionalidades da Aplicação

A plataforma que vocês construirão deverá ter as seguintes funcionalidades:

#### **1. Autenticação e Gestão de Usuários**
* Implementar rotas de cadastro e login.
* O acesso ao dashboard e às funcionalidades de análise deve ser protegido e restrito a usuários autenticados via JWT.

#### **2. Upload e Análise de Currículo (.pdf)**
* O dashboard do usuário deve permitir o **upload de um currículo em formato `.pdf`**.
* O backend será responsável por receber o arquivo, **extrair o texto** contido nele e aplicar as análises de IA para gerar feedback.
* **Lógica de Análise com IA:** O sistema deve analisar o texto extraído para fornecer, no mínimo, dois dos seguintes feedbacks:
    * **Uso de Verbos de Ação:** Identificar o uso de verbos fortes e sugerir melhorias para frases passivas.
    * **Quantificação de Resultados:** Verificar se as conquistas são apoiadas por números e métricas, sugerindo edições onde faltar essa quantificação.
    * **Análise de Palavras-Chave (Opcional):** Comparar o currículo com uma descrição de vaga e listar palavras-chave importantes que estão ausentes.

#### **3. Histórico de Versões e Resultados**
* A cada upload, a plataforma deve **salvar o arquivo `.pdf` original e o resultado da análise** associado a ele.
* O dashboard deve exibir um histórico de todos os envios, permitindo que o usuário reveja qualquer versão anterior do seu currículo e o feedback que recebeu.

#### **4. Análise de Progresso (Funcionalidade Chave)**
* A aplicação precisa **mostrar a evolução do usuário**. Para isso, cada análise deve gerar métricas (pontuações).
* No dashboard, vocês devem criar uma visualização (ex: um gráfico) que mostre a **melhora ou piora dessas métricas** ao longo do tempo, comparando as diferentes versões do currículo enviadas.

#### **(Bônus) Sugestões Avançadas com LLM**
* Como um diferencial, vocês podem integrar uma API de um Large Language Model (Google Gemini, OpenAI, etc.) para gerar um parágrafo de feedback qualitativo sobre o currículo.

---

### 📚 Documentação do Projeto

Este projeto possui documentação completa e detalhada:

### 📖 Documentação Geral
- **[DOCUMENTACAO_COMPLETA.md](./DOCUMENTACAO_COMPLETA.md)** - Visão geral completa do projeto, incluindo backend e frontend

### 🚀 Documentação do Backend
- **[Backend README.md](./backend/README.md)** - Documentação detalhada da API FastAPI, incluindo:
  - Instruções de setup e instalação
  - Visão geral da arquitetura
  - Endpoints da API
  - Configurações e variáveis de ambiente
  - Comandos úteis para desenvolvimento

### 🎨 Documentação do Frontend
- **[Frontend README.md](./frontend/README.md)** - Documentação completa do React, incluindo:
  - Setup e instalação
  - Estrutura de componentes
  - Sistema de design
  - Funcionalidades implementadas e planejadas
  - Comandos para desenvolvimento

### 📋 Instruções de Documentação

* **Backend (FastAPI):**
    * Utilize os recursos do FastAPI para gerar documentação de API interativa em `/docs`
    * Mantenha o `README.md` atualizado com instruções de setup e arquitetura
    * Documente todos os endpoints, modelos e schemas

* **Frontend (React):**
    * Documente os componentes principais, explicando responsabilidades e props
    * Mantenha o `README.md` atualizado com instruções de execução
    * Documente a estrutura de pastas e decisões de arquitetura

Bom trabalho, time! Este é um projeto desafiador e uma ótima oportunidade para construirmos algo incrível juntos.
