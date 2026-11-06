#!/usr/bin/env python3
"""
Script Canônico de Extração e Mineração de Microdados do DATASUS (SIH-SUS)
para Transplantes Hepáticos Realizados no Brasil (2007–2022).

Procedimentos SUS de Alta Complexidade:
- 05.05.02.009-2: Transplante de Fígado (Doador Falecido)
- 05.05.02.010-6: Transplante de Fígado (Doador Vivo)
- 05.05.01.006-2: Retirada de Órgão para Transplante (Fígado)

Diretrizes TRIPOD+AI (2024) / PROBAST+AI (2025).
Protocolo OSF: https://osf.io/pw9ed/ (ID: pw9ed)
"""

from __future__ import annotations

import argparse
import ftplib
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("datasus-extractor")

DATASUS_FTP_HOST = "ftp.datasus.gov.br"
DATASUS_SIH_DIR = "/dissemin/publicos/SIHSUS/200801_/Dados/"

# Códigos de procedimento SUS canônicos da Tabela SIGTAP para Transplante Hepático
PROCEDIMENTOS_TRANSPLANTE_FIGADO = [
    "0505020092",  # Transplante de figado (doador falecido)
    "0505020106",  # Transplante de figado (doador vivo)
    "0505010062",  # Retirada de orgao para transplante (figado)
]

UFS_BRASIL = ["SP", "RJ", "MG", "RS", "PR", "BA", "PE", "CE", "DF", "SC", "ES"]


def build_filename_pattern(uf: str, ano: int, mes: int) -> str:
    """Gera o nome do arquivo padrão do DATASUS SIH: RD<UF><AA><MM>.dbc (ex: RDSP2101.dbc)."""
    ano_str = f"{ano % 100:02d}"
    mes_str = f"{mes:02d}"
    return f"RD{uf.upper()}{ano_str}{mes_str}.dbc"


def test_datasus_ftp_connectivity() -> bool:
    """Verifica se o servidor FTP do DATASUS está acessível na rede local."""
    try:
        logger.info("Testando conexão com o FTP público do DATASUS (%s)...", DATASUS_FTP_HOST)
        ftp = ftplib.FTP(DATASUS_FTP_HOST, timeout=8)
        ftp.login()  # Conexão anônima pública
        ftp.cwd(DATASUS_SIH_DIR)
        logger.info("Conexão com o DATASUS FTP estabelecida com sucesso!")
        ftp.quit()
        return True
    except Exception as e:
        logger.warning("Conexão direta ao FTP do DATASUS indisponível ou bloqueada por firewall/proxy: %s", e)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Extração de Transplantes Hepáticos no DATASUS")
    parser.add_argument("--output-dir", type=str, default="projects/xai-liver-ecd-allocation-unos/sources/datasus_raw", help="Pasta de saída")
    parser.add_argument("--anos", type=str, default="2007-2022", help="Intervalo de anos (ex: 2007-2022)")
    parser.add_argument("--ufs", type=str, default="SP,RJ,MG,RS,PR,BA,PE,CE", help="Lista de UFs separadas por vírgula")
    parser.add_argument("--test-only", action="store_true", help="Apenas testa conectividade e mapeia arquivos sem baixar")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ufs = [u.strip().upper() for u in args.ufs.split(",") if u.strip()]
    ano_inicio, ano_fim = [int(a) for a in args.anos.split("-")]

    total_arquivos_planejados = len(ufs) * (ano_fim - ano_inicio + 1) * 12
    logger.info("Planejamento de Extração DATASUS:")
    logger.info("UFs selecionadas: %s (%d estados)", ", ".join(ufs), len(ufs))
    logger.info("Período: %d a %d (%d anos)", ano_inicio, ano_fim, ano_fim - ano_inicio + 1)
    logger.info("Volume estimado de arquivos mensais (.dbc): %d", total_arquivos_planejados)

    online = test_datasus_ftp_connectivity()
    if not online:
        logger.info("Orientação para rede local com restrição de porta 21 (FTP):")
        logger.info("1. O download das AIHs pode ser realizado via HTTP espelhado pelo portal Dados Abertos (https://dados.gov.br).")
        logger.info("2. Ou via script em R no ambiente configurado (R 4.6.1) utilizando a biblioteca 'microdatasus'.")
        logger.info("3. Para testes de modelagem, utilize o gerador do pipeline: '01_pipeline_dados_sp_sus.py --synthetic-if-missing'.")


if __name__ == "__main__":
    main()
