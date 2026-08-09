from fastapi import FastAPI

from backend.auth.router import router as auth_router

# Apenas os routers existentes são importados para estabilizar a aplicação.
from backend.routers import (
    responsaveis,
    familias,
    pessoas_tea,
    medicamentos,
    notificacoes,
    dashboard,
    receitas,
    agenda,
)

app = FastAPI(
    title="MeuTEA API",
    description="Sistema inteligente de apoio para famílias de pessoas com Transtorno do Espectro Autista.",
    version="1.0.0",
)

# Agrupamento e versionamento das rotas.
api_v1_prefix = "/api/v1"

app.include_router(auth_router, prefix=f"{api_v1_prefix}/auth", tags=["Autenticação"])
app.include_router(familias.router, prefix=f"{api_v1_prefix}/familias", tags=["Famílias"])
app.include_router(responsaveis.router, prefix=f"{api_v1_prefix}/responsaveis", tags=["Responsáveis"])
app.include_router(pessoas_tea.router, prefix=f"{api_v1_prefix}/pessoas-tea", tags=["Pessoas TEA"])
app.include_router(medicamentos.router, prefix=f"{api_v1_prefix}/medicamentos", tags=["Medicamentos"])
app.include_router(notificacoes.router, prefix=f"{api_v1_prefix}/notificacoes", tags=["Notificações"])
app.include_router(receitas.router, prefix=f"{api_v1_prefix}/receitas", tags=["Receitas Médicas"])
app.include_router(dashboard.router, prefix=f"{api_v1_prefix}/dashboard", tags=["Dashboard"])
app.include_router(agenda.router, prefix=f"{api_v1_prefix}/agenda", tags=["Agenda"])


@app.get("/")
def home():
    return {
        "sistema": "MeuTEA",
        "versao": "1.0.0",
        "documentacao": "/docs",
    }