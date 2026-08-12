# 🎮 Análise do Catálogo de Jogos de PS5

Pipeline de dados completo — da extração via API ao dashboard interativo — analisando o catálogo de jogos do PlayStation 5. Projeto de portfólio construído para praticar o ciclo end-to-end de um analista de dados: **extração → transformação → modelagem → visualização**.

<img width="1081" height="602" alt="image" src="https://github.com/user-attachments/assets/9bf7f9ed-4cab-4160-9623-fe896898cfd7" />

## 📌 Sobre o projeto

O objetivo foi construir um pipeline realista, passando por cada camada que um analista de dados encontra no dia a dia — desde lidar com uma API que não entrega os dados prontos, até modelar um esquema relacional e apresentar os resultados num dashboard.

Os dados vêm da [IGDB](https://www.igdb.com/) (Internet Game Database), uma base pública de informações sobre jogos, acessada via API com autenticação OAuth.

---

## 🛠️ Stack

| Camada | Ferramenta |
|--------|-----------|
| Extração | Python (`requests`, `igdb-api-v4`) |
| Transformação | Python (`pandas`) + SQL |
| Banco de dados | SQLite |
| Modelagem e análise | SQL (esquema estrela) |
| Visualização | Power BI (modelo semântico + DAX) |

---

## 🔄 O pipeline

### 1. Extração (Python)

Os dados são puxados da API da IGDB via requisições autenticadas. Pontos técnicos tratados nesta etapa:

- **Autenticação OAuth** via Twitch (a IGDB usa as credenciais da Twitch), com geração de token a cada execução.
- **Paginação** — a API entrega no máximo 500 registros por requisição, então os dados são coletados em lotes com controle de `offset`.
- **Rate limit** — pausas entre requisições para respeitar o limite da API.
- **Filtro por plataforma** — apenas jogos com PS5 (`platform id = 167`) na lista de plataformas.

### 2. Transformação (Python + SQL)

A API retorna as relações (gêneros, plataformas, temas) como **listas de IDs** dentro de cada registro — não como valores prontos para análise. O tratamento envolveu:

- Serialização das colunas de lista em formato JSON para persistência no banco.
- Conversão dos timestamps Unix em datas legíveis.
- Normalização do modelo em SQL: as relações foram "explodidas" em tabelas de ligação usando `json_each`, transformando listas em linhas.

### 3. Modelagem (SQL — esquema estrela)

O modelo final segue um **esquema estrela**, adequado para ferramentas de BI:

```
        generos                     jogos
      (dimensão)                    (fato)
           │                          │
           └──────  jogo_genero  ─────┘
                   (tabela de ligação)
```

- **`jogos`** — tabela fato com os atributos escalares (id, nome, data de lançamento, avaliação).
- **`generos`** — dimensão (id → nome), obtida do endpoint `genres` da API.
- **`jogo_genero`** — tabela de ligação resolvendo a relação muitos-para-muitos entre jogos e gêneros.

### 4. Visualização (Power BI)

O modelo foi conectado ao Power BI, onde:

- Os **relacionamentos** foram configurados recriando o esquema estrela.
- Foram criadas **medidas DAX** (contagem distinta de jogos, ano de pico de lançamentos, gênero líder).
- O **dashboard** apresenta a distribuição de jogos por gênero e a evolução dos lançamentos ao longo dos anos, com KPIs de destaque.

---

## 📊 Principais análises

- Distribuição de jogos por gênero no catálogo de PS5.
- Evolução do número de lançamentos por ano.
- KPIs: total de jogos, número de gêneros, ano de pico e gênero mais comum.

---

## ⚠️ Nota sobre os dados

Alguns jogos aparecem com data de lançamento **anterior a 2020** (antes do lançamento do PS5). Isso **não é um erro**: a IGDB registra a data do lançamento *original* do título, não da versão de PS5 especificamente. Jogos lançados originalmente em outras plataformas e depois portados/remasterizados para PS5 mantêm a data original.

Portanto, o dashboard reflete o **catálogo disponível no PS5** por ano de lançamento original — não os lançamentos exclusivos de cada ano. Entender essa característica da fonte foi parte importante do projeto.

---

## 📁 Estrutura do repositório

```
├── request.py          # Autenticação e geração de token OAuth
├── main.py             # Extração dos jogos e carga no banco
├── jogos_ps5.db        # Banco SQLite gerado
├── normalizacao.sql    # Scripts SQL de normalização (esquema estrela)
├── docs/               # Imagens e prints do dashboard
└── README.md
```

> *Ajuste os nomes de arquivo conforme a estrutura real do seu repositório.*

---

## 🚀 Como executar

1. Crie um app na [Twitch Developer Console](https://dev.twitch.tv/console) para obter `Client ID` e `Client Secret`.
2. Crie um arquivo `.env` na raiz do projeto:
   ```
   CLIENT_ID=seu_client_id
   CLIENT_SECRET=seu_client_secret
   ```
3. Instale as dependências:
   ```bash
   pip install requests python-dotenv igdb-api-v4 pandas sqlalchemy rich
   ```
4. Rode a extração:
   ```bash
   python main.py
   ```
5. Abra o banco `jogos_ps5.db` no DBeaver e execute os scripts de `normalizacao.sql`.
6. Conecte o banco (ou os CSVs exportados) no Power BI.

---

## 📈 Próximos passos

- [ ] Expandir o modelo com novas dimensões (plataformas, temas, empresas).
- [ ] Aprofundar em medidas DAX (rumo à certificação PL-300).
- [ ] Migrar o banco para PostgreSQL para um cenário mais próximo de produção.

---

## 👤 Autor

**[Fernando Arnold Capera Gonçalves]**
[LinkedIn](https://www.linkedin.com/in/fernando-arnold-capera-gon%C3%A7alves-369785255/) · [GitHub]( https://github.com/fernandoacapera/ )

Projeto desenvolvido como parte do meu portfólio de transição para a área de dados.
