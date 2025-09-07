import argparse
def bar(count: int, scale: int = 1, char: str = "█") -> str:
n = max(1, count // max(1, scale))
return char * n




def top_n(counter_dict: dict, n: int = 10) -> list[tuple[str, int]]:
return sorted(counter_dict.items(), key=lambda x: (-x[1], x[0]))[:n]




def fmt_money(v):
return "-" if v is None else f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")




def make_report(res: dict, out_path: Path):
lines = []
lines.append("# 📊 Relatório de Mercado — TI Júnior\n")
lines.append("Baseado no CSV fornecido.\n")


# Hard skills
lines.append("## 🔧 Hard Skills mais citadas (por categoria)\n")
for bucket, counts in res["hard"].items():
lines.append(f"### {bucket}\n")
for skill, c in top_n(counts, 10):
lines.append(f"- {skill}: {c} {bar(c)}")
lines.append("")


# Soft skills
lines.append("## 🤝 Soft Skills mais citadas\n")
for skill, c in top_n(res["soft"], 10):
lines.append(f"- {skill}: {c} {bar(c)}")
lines.append("")


# Salários
lines.append("## 💰 Faixa Salarial por Papel\n")
for role, stats in res["salaries"].items():
lines.append(f"- **{role}** → min: {fmt_money(stats['min'])} | mediana: {fmt_money(stats['median'])} | máx: {fmt_money(stats['max'])}")
lines.append("")


# Plano de estudos sugerido (6 meses)
lines.append("## 🚀 Plano de Estudos (6 meses)\n")
lines.append("**Foco técnico**: Python (dados/automação) + React.js (front-end).\n")
lines.append("**Foco comportamental**: Resolução de problemas.\n")
lines.append("\n### Trilha sugerida\n")
lines.append("1. **Mês 1–2 (Fundação)**: Python básico/avançado, pandas, SQL; JS moderno; Git/GitHub.\n")
lines.append("2. **Mês 3 (Dados/Automação)**: automações com Python, APIs REST, ETL leve.\n")
lines.append("3. **Mês 4 (Front)**: React.js + TypeScript; consumo de APIs; roteamento.\n")
lines.append("4. **Mês 5 (Full)**: projeto full stack simples (API Node ou mock) + React.\n")
lines.append("5. **Mês 6 (DevOps/Cloud)**: Linux básico, deploy em nuvem grátis, CI/CD GitHub Actions.\n")


out_path.write_text("\n".join(lines), encoding="utf-8")




# ------------------------------
# CLI
# ------------------------------


def main():
ap = argparse.ArgumentParser(description="Analisador de mercado TI Júnior")
ap.add_argument("--csv", required=True, help="Caminho do CSV de vagas")
ap.add_argument("--skills", default="skills.yaml", help="Arquivo YAML de termos")
ap.add_argument("--out", default="Relatorio_Carreira.md", help="Saída Markdown")
args = ap.parse_args()


df = read_csv(Path(args.csv))
cfg = load_yaml(Path(args.skills))
res = analyze(df, cfg)
make_report(res, Path(args.out))
print(f"Relatório gerado em: {args.out}")




if __name__ == "__main__":
main()
