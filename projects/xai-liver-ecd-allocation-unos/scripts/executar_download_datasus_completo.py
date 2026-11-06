#!/usr/bin/env python3
"""
Download e minerador contínuo em background para procedimentos de Transplante Hepático no DATASUS (SIH/SUS).
Processa arquivo a arquivo (.dbc -> .dbf -> filtragem rápida -> remoção de temporários),
mantendo em disco apenas o CSV consolidado com os registros reais de transplante.
"""

from __future__ import annotations

import ftplib
import logging
import os
import sys
import time
from pathlib import Path
import dbfread
import pandas as pd
import pyreaddbc

log_file = Path("projects/xai-liver-ecd-allocation-unos/sources/datasus_raw/download.log")
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(str(log_file), mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("datasus-miner")

DATASUS_FTP_HOST = "ftp.datasus.gov.br"
DATASUS_SIH_DIR = "/dissemin/publicos/SIHSUS/200801_/Dados/"

# Procedimentos de Transplante Hepático
PROCEDIMENTOS_FIGADO = {"0505020092", "0505020106", "0505010062"}

# Começando pelos estados líderes: São Paulo (maior centro), seguido por RJ, RS, PR, MG
UFS = ["SP", "RJ", "RS", "PR", "MG", "PE", "CE", "BA", "DF"]
ANOS = list(range(2023, 2017, -1))  # Dos mais recentes (2023) até 2018


def extrair_mes(ftp: ftplib.FTP, uf: str, ano: int, mes: int, temp_dir: Path, output_csv: Path) -> int:
    filename = f"RD{uf.upper()}{ano % 100:02d}{mes:02d}.dbc"
    dbc_file = temp_dir / filename
    dbf_file = temp_dir / filename.replace(".dbc", ".dbf")

    try:
        with open(dbc_file, "wb") as f:
            ftp.retrbinary(f"RETR {filename}", f.write)
    except Exception as e:
        logger.debug(f"Arquivo {filename} indisponível no FTP: {e}")
        return 0

    try:
        pyreaddbc.dbc2dbf(str(dbc_file), str(dbf_file))
        table = dbfread.DBF(str(dbf_file), encoding="latin1", load=False)
        
        matches = []
        for record in table:
            p_rea = str(record.get("PROC_REA", "")).strip()
            p_sol = str(record.get("PROC_SOL", "")).strip()
            if p_rea in PROCEDIMENTOS_FIGADO or p_sol in PROCEDIMENTOS_FIGADO:
                rec_dict = dict(record)
                rec_dict["UF_ORIGEM"] = uf
                rec_dict["ANO_ARQUIVO"] = ano
                rec_dict["MES_ARQUIVO"] = mes
                matches.append(rec_dict)

        if matches:
            df_matches = pd.DataFrame(matches)
            hdr = not output_csv.exists()
            df_matches.to_csv(output_csv, mode="a", index=False, header=hdr, encoding="utf-8")
            count = len(matches)
            logger.info(f"==> [{uf}] {ano}/{mes:02d}: {count} transplantes hepáticos extraídos e salvos!")
            return count
        else:
            logger.info(f"[{uf}] {ano}/{mes:02d}: 0 transplantes hepáticos.")
            return 0
    except Exception as e:
        logger.error(f"Erro ao processar {filename}: {e}")
        return 0
    finally:
        if dbc_file.exists():
            try: dbc_file.unlink()
            except Exception: pass
        if dbf_file.exists():
            try: dbf_file.unlink()
            except Exception: pass


def main():
    base_dir = Path("projects/xai-liver-ecd-allocation-unos")
    temp_dir = base_dir / "sources" / "datasus_raw"
    temp_dir.mkdir(parents=True, exist_ok=True)
    out_csv = base_dir / "evidence" / "sp_sus" / "transplantes_sih_sus_reais.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    logger.info("================================================================================")
    logger.info("Iniciando mineração em background do DATASUS SIH/SUS para Transplante Hepático...")
    logger.info(f"UFs: {UFS} | Anos: {ANOS}")
    logger.info(f"Destino consolidado: {out_csv}")
    logger.info("================================================================================")

    total_extraidos = 0
    for uf in UFS:
        logger.info(f">>> Processando Estado: {uf} <<<")
        for ano in ANOS:
            for mes in range(12, 0, -1):
                connected = False
                for attempt in range(3):
                    try:
                        ftp = ftplib.FTP(DATASUS_FTP_HOST, timeout=30)
                        ftp.login()
                        ftp.cwd(DATASUS_SIH_DIR)
                        connected = True
                        break
                    except Exception as e:
                        time.sleep(2)
                
                if not connected:
                    logger.warning(f"Não foi possível conectar ao FTP para {uf} {ano}/{mes:02d}")
                    continue

                try:
                    c = extrair_mes(ftp, uf, ano, mes, temp_dir, out_csv)
                    total_extraidos += c
                finally:
                    try:
                        ftp.quit()
                    except Exception:
                        pass

    logger.info(f"Mineração DATASUS finalizada! Total acumulado de transplantes reais: {total_extraidos}")


if __name__ == "__main__":
    main()
