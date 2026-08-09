# Alembic Migrations

Este diretório contém os scripts de migração do banco de dados gerenciados pelo Alembic.

## Comandos Essenciais

Todos os comandos devem ser executados a partir do diretório `backend/`.

### Gerar uma Nova Migração

Após fazer alterações nos modelos SQLAlchemy (em `backend/models/`), gere um novo script de migração automaticamente:

```bash
alembic revision --autogenerate -m "Descrição da alteração"
```
Exemplo:
```bash
alembic revision --autogenerate -m "Adiciona campo 'ativo' na tabela de usuários"
```
Sempre verifique o arquivo de migração gerado em `alembic/versions/` para garantir que ele reflete as alterações desejadas.

### Aplicar Migrações (Upgrade)

Para aplicar todas as migrações pendentes e atualizar o banco de dados para a versão mais recente:

```bash
alembic upgrade head
```

### Reverter Migrações (Downgrade)

Para reverter a última migração aplicada:

```bash
alembic downgrade -1
```

Para reverter todas as migrações e limpar o banco de dados (cuidado!):

```bash
alembic downgrade base
```