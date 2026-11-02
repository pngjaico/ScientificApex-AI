# Atualiza, sincroniza e trava o ambiente R cientifico (R 4.6.1 / renv 1.3.1).
# Uso a partir da raiz do workspace:
#   "C:/Users/Usuario-pc/AppData/Local/Programs/R/R-4.6.1/bin/x64/Rscript.exe" --vanilla scripts/atualizar_ambiente_meta_analise.R
#
# Fluxo:
# 1. Reaproveita binarios ja presentes em modelos/estatistica_e_figuras/ambiente/biblioteca.
# 2. Instala via binarios oficiais CRAN (sem compilacao forçada) os pacotes declarados
#    em modelos/meta_analise_em_r/analysis/00_pacotes_do_ambiente.R e suas dependencias.
# 3. Sincroniza tambem a biblioteca local do R 4.6.1 para execucoes diretas via Rscript.
# 4. Atualiza modelos/meta_analise_em_r/renv.lock e modelos/meta_analise_em_r/ambiente/renv.lock
#    com snapshot.type = "all" e valida synchronized == TRUE.

options(repos = c(CRAN = "https://cloud.r-project.org"))
options(renv.consent = TRUE)

root <- normalizePath(".", winslash = "/", mustWork = TRUE)
proj_dir <- file.path(root, "modelos", "meta_analise_em_r")
est_lib <- file.path(root, "modelos", "estatistica_e_figuras", "ambiente", "biblioteca")
renv_lib <- file.path(proj_dir, "renv", "library", "windows", "R-4.6", "x86_64-w64-mingw32")
sys_lib <- .Library

dir.create(renv_lib, recursive = TRUE, showWarnings = FALSE)

# Limpa eventual diretorio temporario .renv-staging residual
staging_dir <- file.path(proj_dir, "renv", "library", ".renv-staging")
if (dir.exists(staging_dir)) {
  unlink(staging_dir, recursive = TRUE, force = TRUE)
}

# Extrai a lista de pacotes declarada em 00_pacotes_do_ambiente.R sem disparar a verificacao prematura
env_decl <- new.env(parent = baseenv())
parsed <- parse(file.path(proj_dir, "analysis", "00_pacotes_do_ambiente.R"))
for (expr in parsed) {
  if (is.call(expr) && identical(expr[[1]], as.name("<-")) && identical(expr[[2]], as.name("pacotes"))) {
    eval(expr, envir = env_decl)
  }
}
pacotes <- env_decl$pacotes
cat("Pacotes principais declarados:", length(pacotes), "\n")

db <- utils::available.packages(type = "binary")
deps <- tools::package_dependencies(
  pacotes,
  db = db,
  which = c("Depends", "Imports", "LinkingTo"),
  recursive = TRUE
)
closure <- intersect(unique(c(pacotes, unlist(deps, use.names = FALSE))), rownames(db))

installed_sys <- utils::installed.packages(lib.loc = sys_lib)
base_rec <- installed_sys[!is.na(installed_sys[, "Priority"]) &
  installed_sys[, "Priority"] %in% c("base", "recommended"), "Package"]

# 1. Reaproveita pacotes ja existentes em estatistica_e_figuras ou na biblioteca do sistema
for (src_lib in c(est_lib, sys_lib)) {
  if (dir.exists(src_lib)) {
    avail_src <- rownames(utils::installed.packages(lib.loc = src_lib))
    current_renv <- rownames(utils::installed.packages(lib.loc = renv_lib))
    to_copy <- setdiff(intersect(closure, avail_src), c(current_renv, base_rec))
    for (pkg in to_copy) {
      src_pkg <- file.path(src_lib, pkg)
      dst_pkg <- file.path(renv_lib, pkg)
      if (dir.exists(src_pkg) && !dir.exists(dst_pkg)) {
        file.copy(src_pkg, renv_lib, recursive = TRUE, copy.date = TRUE)
      }
    }
  }
}

# 2. Baixa e instala binarios CRAN ausentes na biblioteca renv do modelo
current_renv <- rownames(utils::installed.packages(lib.loc = c(renv_lib, sys_lib)))
to_install <- setdiff(closure, current_renv)
cat("Total na fecho transitivo CRAN:", length(closure),
    "| Novas instalacoes binarias:", length(to_install), "\n")
if (length(to_install) > 0) {
  utils::install.packages(to_install, lib = renv_lib, dependencies = FALSE, type = "binary")
}

# 3. Garante que qualquer pacote do fecho presente em sys_lib (exceto base/recommended)
#    tambem esteja materializado em renv_lib para que o lockfile do projeto fique completo
current_renv_only <- rownames(utils::installed.packages(lib.loc = renv_lib))
from_sys <- setdiff(intersect(closure, rownames(installed_sys)), c(current_renv_only, base_rec))
for (pkg in from_sys) {
  src_pkg <- file.path(sys_lib, pkg)
  dst_pkg <- file.path(renv_lib, pkg)
  if (dir.exists(src_pkg) && !dir.exists(dst_pkg)) {
    file.copy(src_pkg, renv_lib, recursive = TRUE, copy.date = TRUE)
  }
}

# 4. Espelha pacotes novos para sys_lib para que Rscript direto em outros projetos funcione
current_sys <- rownames(utils::installed.packages(lib.loc = sys_lib))
current_renv_only <- rownames(utils::installed.packages(lib.loc = renv_lib))
to_sys <- setdiff(current_renv_only, current_sys)
for (pkg in to_sys) {
  src_pkg <- file.path(renv_lib, pkg)
  dst_pkg <- file.path(sys_lib, pkg)
  if (dir.exists(src_pkg) && !dir.exists(dst_pkg)) {
    file.copy(src_pkg, sys_lib, recursive = TRUE, copy.date = TRUE)
  }
}

# 5. Ativa o projeto renv, grava o snapshot e sincroniza ambiente/renv.lock e modelos correlatos
old_wd <- setwd(proj_dir)
on.exit(setwd(old_wd), add = TRUE)
source(".Rprofile")
renv::settings$snapshot.type("all")
renv::snapshot(project = proj_dir, library = c(renv_lib, sys_lib), lockfile = file.path(proj_dir, "renv.lock"), prompt = FALSE, force = TRUE)
dir.create(file.path(proj_dir, "ambiente"), recursive = TRUE, showWarnings = FALSE)
file.copy(file.path(proj_dir, "renv.lock"), file.path(proj_dir, "ambiente", "renv.lock"), overwrite = TRUE)

# Sincroniza os locks de modelos/estatistica_e_figuras e modelos/manuscrito com o lock consolidado
for (target_lock in c(
  file.path(root, "modelos", "estatistica_e_figuras", "ambiente", "renv.lock"),
  file.path(root, "modelos", "manuscrito", "renv.lock"),
  file.path(root, "modelos", "manuscrito", "ambiente", "renv.lock")
)) {
  dir.create(dirname(target_lock), recursive = TRUE, showWarnings = FALSE)
  file.copy(file.path(proj_dir, "renv.lock"), target_lock, overwrite = TRUE)
}

# 6. Executa o validador 00_pacotes_do_ambiente.R e confere renv::status()
source(file.path(proj_dir, "analysis", "00_pacotes_do_ambiente.R"))
st <- renv::status(project = proj_dir, library = c(renv_lib, sys_lib), lockfile = file.path(proj_dir, "renv.lock"))
cat("renv synchronized:", isTRUE(st$synchronized), "\n")
if (!isTRUE(st$synchronized)) {
  stop("renv nao ficou sincronizado apos snapshot.")
}
writeLines(
  utils::capture.output(utils::sessionInfo()),
  file.path(proj_dir, "ambiente", "sessao_r_2026-11-02.txt"),
  useBytes = TRUE
)
cat("PASS: Ambiente R 4.6.1 atualizado, sincronizado e travado em renv.lock.\n")
