-- Executar numa base PostgreSQL dedicada chamada oficina_etl.
-- Pode ser repetido; não apaga resultados existentes.
BEGIN;
CREATE SCHEMA IF NOT EXISTS origem;
CREATE SCHEMA IF NOT EXISTS destino;
CREATE TABLE IF NOT EXISTS origem.servicos (
    codigo_servico varchar(3) PRIMARY KEY,
    descricao text NOT NULL,
    preco_hora numeric(10,2) NOT NULL CHECK (preco_hora > 0)
);
INSERT INTO origem.servicos VALUES
('S01','Mudança de óleo',30.00),
('S02','Substituição de travões',35.00),
('S03','Troca de pneus',25.00),
('S04','Diagnóstico eletrónico',40.00),
('S05','Revisão geral',35.00),
('S06','Substituição de bateria',25.00),
('S07','Alinhamento de direção',30.00),
('S08','Manutenção de ar condicionado',40.00)
ON CONFLICT (codigo_servico) DO UPDATE
SET descricao=EXCLUDED.descricao, preco_hora=EXCLUDED.preco_hora;
CREATE TABLE IF NOT EXISTS destino.intervencoes_integradas (
    id_intervencao integer PRIMARY KEY,
    id_veiculo integer NOT NULL,
    matricula varchar(8) NOT NULL,
    marca text NOT NULL,
    modelo text NOT NULL,
    id_cliente integer NOT NULL,
    nome_cliente text NOT NULL,
    email text,
    codigo_servico varchar(3) NOT NULL,
    descricao_servico text NOT NULL,
    data_intervencao date NOT NULL,
    horas_trabalho numeric(10,2) NOT NULL CHECK (horas_trabalho > 0),
    preco_hora numeric(10,2) NOT NULL CHECK (preco_hora > 0),
    custo_pecas numeric(10,2) NOT NULL CHECK (custo_pecas >= 0),
    custo_total numeric(12,2) NOT NULL CHECK (custo_total >= 0)
);
CREATE TABLE IF NOT EXISTS destino.rejeitados (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    execucao text NOT NULL,
    entidade text NOT NULL,
    id_origem text,
    motivo text NOT NULL,
    dados_originais text,
    registado_em timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMIT;
