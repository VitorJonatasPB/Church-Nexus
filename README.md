# Church Nexus

Church Nexus é um sistema completo de gestão para igrejas, focado em simplificar e centralizar a administração eclesiástica. Desenvolvido com **Python** e **Django**, este projeto oferece ferramentas intuitivas para controle de membresia, gestão financeira e organização de eventos.

## 🚀 Módulos Principais

*   **Secretaria**: Gestão detalhada de membros, congregações e áreas. Cadastro com informações completas (foto, cargo, endereço, etc).
*   **Tesouraria**: Controle financeiro completo, com fluxo de caixa, categorização de receitas e despesas, e visão analítica das contas.
*   **Eventos**: Organização de eventos, controle de inscritos e integração com a tesouraria (os pagamentos de eventos geram movimentos no caixa automaticamente).
*   **Relatórios e Análises**: Painéis e relatórios que facilitam a prestação de contas e dão visibilidade sobre a saúde da igreja.

## 🛠 Tecnologias Utilizadas

*   **Backend:** Python 3, Django 5
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla), Admin customizado (Jazzmin)
*   **Banco de Dados:** PostgreSQL (Produção) / SQLite (Desenvolvimento local)
*   **Hospedagem / Nuvem:** Compatível com deploy no Render (Servidor) e Supabase / Neon (Banco de Dados).

## 💻 Como Rodar Localmente

1. Clone este repositório:
```bash
git clone https://github.com/SeuUsuario/meu_projeto.git
cd meu_projeto
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r backend/requirements.txt
```

4. Execute as migrações do banco de dados (SQLite local):
```bash
cd backend
python manage.py migrate
```

5. Crie um superusuário para acessar a área administrativa:
```bash
python manage.py createsuperuser
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

Acesse o sistema no navegador em: `http://127.0.0.1:8000`

---
*Projeto desenvolvido por Vitor Paiva.*
