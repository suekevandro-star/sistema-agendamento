from pathlib import Path

PASTA = Path(r"D:\Projeto Empresas")

# Ler o CSS atual
css_file = PASTA / "style.css"
css_content = css_file.read_text(encoding="utf-8")

# Substituir o tamanho da foto
css_content = css_content.replace(
    ".box-foto-bot {\n    width: 80px; height: 80px;",
    ".box-foto-bot {\n    width: 100px; height: 100px;"
)

# Ajustar o row para empilhar
css_content = css_content.replace(
    ".row-bot-info {\n    display: flex;\n    gap: 15px;\n    align-items: center;",
    ".row-bot-info {\n    display: flex;\n    flex-direction: column;\n    align-items: center;\n    gap: 15px;"
)

# Salvar
css_file.write_text(css_content, encoding="utf-8")
print("✅ Foto ajustada para 100px!")
print("📱 Layout otimizado para mobile!")