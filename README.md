# Infradata

Requisito: Conda (Miniconda ou Anaconda) deve estar instalado antes de criar o ambiente.

Nota: o principal motivo para recomendar Conda neste projeto é o uso de `geopandas` e suas dependências nativas. Instalar esses pacotes via Conda (conda-forge) evita builds problemáticos e reduz o risco de quebrar bibliotecas Python globais do sistema.

Este repositório fornece um arquivo `environment.yml` pronto para criar um ambiente Conda com as dependências necessárias e instalar o package local `infradata` em modo editável.

Para criar e ativar o ambiente, execute na pasta do projeto:

```bash
conda env create -f environment.yml
conda activate infradata_env
```

O `environment.yml` instala `pandas` via Conda e usa `pip` para instalar as dependências listadas em `requirements.txt`  e ainda instala o package local em modo editável (`-e .`).

Após ativar o ambiente, execute o pipeline principal:

```bash
python scripts/run_pipeline.py
```

Para notebooks, e execuções interativas selecione o kernel do ambiente conda `infradata_env`.

Observação: se você precisar de dependências nativas extras (por exemplo para `camelot-py`), instale-as no sistema conforme a documentação do seu sistema operacional.

Se precisar de ajuda, abra uma issue com a saída de `conda list` do ambiente ativo.

## Dados brutos

Os arquivos de dados brutos não estão versionados neste repositório (veja `.gitignore`). Antes de rodar o pipeline, coloque os dados sob a árvore `data/raw/` seguindo a mesma estrutura usada localmente (ex.: `data/raw/historico_infracao/`, `data/raw/hist_fluxo/`, etc.), ou execute os scripts de ingestão que baixam fontes externas — as caches são salvas em `data/external/` e `data\raw\historico_infracao`.

Resumo rápido:

- Dados brutos: `data/raw/` (não comitados)
- Caches / arquivos baixados: `data/external/` e `data\raw\historico_infracao`
- Saída processada: `data/silver/`

## Arquivo de caminhos (commitado)

Este repositório inclui `data_paths.env` com valores padrão para os caminhos de dados públicos. O projeto ainda suporta um arquivo legacy `.env`, mas `data_paths.env` é preferido para deixar claro que o arquivo contém apenas paths públicos.
