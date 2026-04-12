import sys
import importlib.util
 
 
def verificar_dependencias():
    pacotes = {
        "customtkinter": "customtkinter",
        "pandas":        "pandas",
        "openpyxl":      "openpyxl",
    }
    faltando = []
    for modulo, pip_nome in pacotes.items():
        if importlib.util.find_spec(modulo) is None:
            faltando.append(pip_nome)
 
    if faltando:
        print("=" * 50)
        print("  DEPENDÊNCIAS AUSENTES — instale com:")
        print()
        print(f"  pip install {' '.join(faltando)}")
        print("=" * 50)
        sys.exit(1)
 
 
def main():
    verificar_dependencias()
 
    # Importação adiada para só carregar após checar deps
    from interface import AppRyzen
 
    app = AppRyzen()
    app.mainloop()
 
 
if __name__ == "__main__":
    main()