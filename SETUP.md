# EduPresence - Guia de Instalação e Deployment

## 📋 Sobre o Projeto

EduPresence é um sistema de gestão de presença escolar desenvolvido com Django 5.0. O sistema permite que coordenadores, professores e administradores gerenciem alunos, turmas, frequência e monitorem alertas de evasão.

## 🚀 Instalação Local

### Pré-requisitos

- Python 3.12+
- pip (gerenciador de pacotes do Python)
- Git

### Passo 1: Clonar o repositório

```bash
git clone <repository-url>
cd Atividade-Extensionista-3
```

### Passo 2: Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### Passo 3: Instalar dependências

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Passo 4: Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
ALLOWED_HOSTS=127.0.0.1,localhost
```

### Passo 5: Executar migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### Passo 6: Criar usuários iniciais

```bash
python manage.py init_users
```

Isso criará 3 usuários de demonstração:
- **Admin**: username: `admin`, password: `admin123`, role: Administrador
- **Coordenador**: username: `coordenador`, password: `coord123`, role: Coordenador
- **Professor**: username: `professor`, password: `prof123`, role: Professor

### Passo 7: Executar servidor de desenvolvimento

```bash
python manage.py runserver
```

A aplicação estará disponível em: http://localhost:8000

Acesse a página de login em: http://localhost:8000/accounts/login/

## 📁 Estrutura do Projeto

```
edupresence/
├── config/                    # Configurações do Django
│   ├── settings.py           # Configurações principais
│   ├── urls.py               # URLs raiz
│   └── wsgi.py               # WSGI para produção
├── apps/
│   ├── accounts/             # Autenticação e usuários
│   ├── core/                 # Dashboard e home
│   ├── escola/               # Séries, turmas, disciplinas
│   ├── alunos/               # Gerenciamento de alunos
│   ├── frequencia/           # Chamada e histórico
│   ├── monitoramento/        # Alertas de evasão
│   └── relatorios/           # Relatórios e exportação
├── templates/                 # Templates HTML
├── static/                    # CSS, JS, imagens
├── assets/                    # Designs do Figma
├── manage.py                 # CLI do Django
└── requirements.txt          # Dependências Python
```

## 🔐 Autenticação e Permissões

### Papéis (Roles)

1. **Administrador (ADMIN)**
   - Acesso total ao sistema
   - Gerenciamento de usuários
   - Acesso ao painel administrativo Django

2. **Coordenador (COORD)**
   - Gerenciamento de escola (séries, turmas, disciplinas)
   - Gerenciamento de alunos e matrículas
   - Visualização de frequência e relatórios
   - Monitoramento de alunos em risco

3. **Professor (PROF)**
   - Registro de chamada (frequência)
   - Visualização de histórico de frequência
   - Relatórios de seus alunos

## 🎯 Funcionalidades Principais

### 1. Gestão Escolar
- Criar e gerenciar séries/anos
- Gerenciar turmas
- Gerenciar disciplinas
- Cadastro de professores

### 2. Gestão de Alunos
- Cadastro de alunos
- Edição de dados de alunos
- Matrículas em turmas
- Inativação de alunos

### 3. Frequência
- Chamada diária em lote (para cada turma)
- Histórico de frequência com filtros
- Cálculo automático de percentual de frequência

### 4. Monitoramento
- Alertas automáticos para alunos com frequência < 75%
- Dashboard de monitoramento
- Lista de alunos em risco

### 5. Relatórios
- Relatório individual de aluno
- Relatório de turma
- Exportação para Excel

## 🔧 Deployment em Produção

### Opção 1: Render.com (Recomendado)

1. **Criar conta em Render.com**
2. **Conectar repositório GitHub**
3. **Configurar variáveis de ambiente:**
   ```
   DEBUG=False
   SECRET_KEY=<gerar-uma-chave-segura>
   ALLOWED_HOSTS=seu-app.onrender.com,www.seu-app.onrender.com
   DATABASE_URL=postgresql://...  # Se usar PostgreSQL
   ```

4. **Criar arquivo `render.yaml`:**
   ```yaml
   services:
     - type: web
       name: edupresence
       env: python
       buildCommand: pip install -r requirements.txt && python manage.py migrate
       startCommand: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
       envVars:
         - key: PYTHON_VERSION
           value: 3.12
   ```

5. **Deploy automático**

### Opção 2: Railway.app

1. **Conectar GitHub e criar novo projeto**
2. **Adicionar plugin PostgreSQL**
3. **Configurar variáveis de ambiente**
4. **Deploy automático**

### Opção 3: PythonAnywhere

1. **Upload de código via Git**
2. **Configurar virtual environment**
3. **Configurar WSGI**
4. **Recarregar aplicação**

## 📚 API e Uso

### Acessar Django Admin

```
http://localhost:8000/admin/
```

Com credenciais de admin.

### Endpoints principais

- `GET/POST /accounts/login/` - Login
- `GET /accounts/logout/` - Logout
- `GET /` - Dashboard
- `GET /escola/series/` - Listar séries
- `GET /alunos/` - Listar alunos
- `GET /frequencia/chamada/` - Chamada diária
- `GET /frequencia/historico/` - Histórico de frequência
- `GET /monitoramento/alunos-risco/` - Alunos em risco
- `GET /relatorios/aluno/` - Relatório de aluno
- `GET /relatorios/turma/` - Relatório de turma
- `POST /relatorios/exportar-excel/` - Exportar para Excel

## 🐛 Troubleshooting

### Erro: "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Erro: Migrations não encontradas
```bash
python manage.py makemigrations
python manage.py migrate
```

### Erro: Porta 8000 já em uso
```bash
python manage.py runserver 8001
```

### Erro: Banco de dados corrompido
```bash
rm db.sqlite3
python manage.py migrate
python manage.py init_users
```

## 📝 Variáveis de Ambiente

Veja o arquivo `.env.example` para todas as variáveis disponíveis.

## 🛡️ Segurança

- Sempre use `DEBUG=False` em produção
- Mude a `SECRET_KEY` em produção
- Use HTTPS em produção
- Backup regular do banco de dados
- Mantenha dependências atualizadas

## 📞 Suporte

Para questões técnicas, consulte:
- Documentação Django: https://docs.djangoproject.com/
- Bootstrap 5: https://getbootstrap.com/docs/5.0/

## 📄 Licença

Este projeto é fornecido como parte de uma atividade de extensão.

---

**Última atualização**: Junho 2024
**Versão**: 1.0.0
