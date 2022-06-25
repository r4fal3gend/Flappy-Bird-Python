import cx_Freeze

arquivo = [cx_Freeze.Executable(
    script="FlappyBird.py", icon="source/icone.ico"
)]


cx_Freeze.setup(
    name="Flappy Bird",
    options={"build_exe": {"packages": ["pygame","os","random"],
                           "include_files": ["source"]}},
    executables=arquivo
)


# python setup.py build (aqui ele vair gerar uma pasta com os arquivos dentro)
# python setup.py bdist_msi (aqui ele gera um instalador de windows)