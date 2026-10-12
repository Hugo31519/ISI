# Integração e validação de dados de uma oficina automóvel

Trabalho individual de ISI 2026/27. Plataforma: Pentaho Kettle (Spoon) + PostgreSQL.
Todos os dados são fictícios e foram gerados para demonstrar integração e qualidade de dados.
Não representam pessoas, contactos, veículos ou preços reais. Os custos são simulados em EUR, sem IVA.

## Material preparado

- `dados/entrada/clientes.csv`: UTF-8, separador ponto e vírgula, cabeçalho, 31 registos (30 clientes distintos e um duplicado).
- `dados/entrada/veiculos.json`: array na raiz, 45 veículos.
- `dados/entrada/intervencoes.xml`: raiz `intervencoes`, elemento repetido `intervencao`, 151 registos (150 IDs e um duplicado).
- `sql/01_preparar_bd.sql`: schemas origem/destino, 8 serviços e tabelas de destino.
- `scripts/gerar_dados.py`: geração determinística das fontes, sem executar o ETL.

O ETL será construído no Spoon; ainda não existem transformações `.ktr` ou jobs `.kjb`.
Os ficheiros representam exportações de três sistemas legados. PostgreSQL é uma quarta origem,
com os preços dos serviços, e também o destino, em schemas separados.

## Preparação

1. Criar uma base PostgreSQL chamada `oficina_etl`.
2. Executar `sql/01_preparar_bd.sql` nessa base, por exemplo no editor SQL do pgAdmin.
3. Configurar a ligação PostgreSQL no Spoon com as credenciais locais, sem as colocar no Git.
4. Criar os fluxos abaixo por etapas e observar os resultados na pré-visualização.

## Transformações a construir

1. Clientes: ler CSV, aparar espaços, reduzir espaços repetidos no nome, converter email para minúsculas, validar email e remover duplicados por ID.
2. Veículos: ler JSON, aparar espaços e converter matrícula para maiúsculas, validar formato e procurar o cliente.
3. Intervenções: ler XML, remover duplicados por ID, tratar números e datas, validar valores, procurar veículo/cliente/serviço e calcular custo.
4. Carregamento e resumos: inserir/atualizar intervenções por ID, exportar totais por mês e serviço e registos rejeitados com motivo.
5. Job principal: executar as transformações na ordem, parar em falha e registar início, fim e contagens.

Usar `${Internal.Entry.Current.Directory}`/parâmetros para evitar caminhos absolutos dependentes do computador.
Guardar ficheiros `.ktr` em `transformacoes/`, `.kjb` em `jobs/`, exportações em `dados/saida/` e logs em `logs/`.

## Regras de negócio

- ID é a chave de deduplicação; os duplicados preparados são idênticos, conservar apenas um.
- Nome é obrigatório. Email vazio ou inválido: manter cliente, definir email como nulo e emitir aviso de qualidade.
- Matrículas: o cenário usa exclusivamente o formato fictício `AA-00-AA`; regex `^[A-Z]{2}-[0-9]{2}-[A-Z]{2}$`. Não é uma validação de todos os formatos portugueses.
- Email: regex didática `^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$`, após normalização; não valida existência nem todas as possibilidades do padrão de email.
- Veículo com matrícula inválida ou cliente inexistente: rejeitar veículo; rejeitar intervenções que dependam dele.
- Datas: aceitar `yyyy-MM-dd` e `dd/MM/yyyy`, converter para data e rejeitar datas impossíveis.
- Números: aceitar ponto ou vírgula decimal nos exemplos preparados; campos vazios não viram zero.
- Horas devem ser maiores que zero; custo de peças maior ou igual a zero.
- Veículo e serviço devem existir nos dados válidos de referência.
- Custo total = horas de trabalho × preço por hora + custo das peças, com arredondamento a 2 casas.
- Cada intervenção válida representa um serviço executado. Totais são custos simulados dos serviços, não prova de pagamentos recebidos.
- Reexecução: atualizar/inserir por ID, sem multiplicar os resultados; identificar execução nos rejeitados e logs.

## Casos preparados para a defesa

| Entidade/ID | Caso | Resultado esperado |
|---|---|---|
| Cliente 1 | Linha duplicada | Conservar uma |
| Cliente 3 | Email sem @ | Aviso; email nulo |
| Cliente 4 | Email vazio | Aviso; email nulo |
| Cliente 5 | Espaços no nome | Normalizar |
| Cliente 6 | Email com espaços e maiúsculas | Normalizar |
| Veículo 7 | Matrícula com espaços e minúsculas | Normalizar |
| Veículo 8 | Matrícula inválida | Rejeitar |
| Veículo 9 | Cliente 999 inexistente | Rejeitar |
| Intervenção 1 | Veículo 999 inexistente | Rejeitar |
| Intervenção 2 | Serviço S99 inexistente | Rejeitar |
| Intervenção 3 | Horas negativas | Rejeitar |
| Intervenção 4 | Peças com custo negativo | Rejeitar |
| Intervenção 5 | Data impossível | Rejeitar |
| Intervenção 6 | Data em formato alternativo | Converter, se outras regras passarem |
| Intervenção 7 | Horas vazias | Rejeitar |
| Intervenção 8 | Vírgula decimal | Converter, se outras regras passarem |
| Intervenção 10 | Linha duplicada | Conservar uma |

Há também intervenções que apontam aos veículos 8 e 9; devem ser rejeitadas pela dependência inválida.
Uma linha pode conter mais de um problema: documentar a ordem de validação e conservar os motivos.

## Entrega

Adicionar transformações, job, scripts SQL, dados sintéticos, instruções, relatório e vídeo/QR Code ao material da entrega.
Relatório: enquadramento, problema, estratégia, diagramas/explicações das transformações e job, vídeo, conclusão e referências.
Entrega indicada no enunciado: 22 de outubro de 2026. Defesa individual.
