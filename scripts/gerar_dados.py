"""Gera fontes sintéticas para o ETL; não executa o tratamento do Spoon."""
from pathlib import Path
import csv
import json
import random
from datetime import date, timedelta
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'dados' / 'entrada'
DATA.mkdir(parents=True, exist_ok=True)
rng = random.Random(31519)

clientes = [dict(id_cliente=i, nome=f'Cliente Fictício {i:02}',
                 email=f'cliente{i:02}@example.com', telefone=f'910{i:06}')
            for i in range(1, 31)]
clientes[2]['email'] = 'cliente03.example.com'
clientes[3]['email'] = ''
clientes[4]['nome'] = '  Cliente   Fictício 05  '
clientes[5]['email'] = ' CLIENTE06@EXAMPLE.COM '
with (DATA / 'clientes.csv').open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(clientes[0]), delimiter=';')
    writer.writeheader()
    writer.writerows(clientes + [clientes[0].copy()])

marcas = [('Renault', 'Clio'), ('Toyota', 'Yaris'), ('Peugeot', '208'),
          ('Volkswagen', 'Golf'), ('Ford', 'Fiesta')]
veiculos = []
for i in range(1, 46):
    marca, modelo = marcas[(i-1) % len(marcas)]
    veiculos.append(dict(id_veiculo=i, matricula=f'AA-{i:02}-BB', marca=marca,
                         modelo=modelo, id_cliente=(i-1) % 30 + 1))
veiculos[6]['matricula'] = ' aa-07-bb '
veiculos[7]['matricula'] = 'INVALIDA'
veiculos[8]['id_cliente'] = 999
(DATA / 'veiculos.json').write_text(json.dumps(veiculos, ensure_ascii=False, indent=2), encoding='utf-8')

root = ET.Element('intervencoes')
registos = []
for i in range(1, 151):
    registos.append(dict(id_intervencao=i, id_veiculo=rng.randint(1,45),
        data=(date(2026,1,1)+timedelta(days=rng.randint(0,272))).isoformat(),
        codigo_servico=f'S{rng.randint(1,8):02}',
        horas_trabalho=f'{rng.choice([0.5,1,1.5,2,3]):.2f}',
        custo_pecas=f'{rng.randint(0,20000)/100:.2f}'))
registos[0]['id_veiculo'] = 999
registos[1]['codigo_servico'] = 'S99'
registos[2]['horas_trabalho'] = '-1.00'
registos[3]['custo_pecas'] = '-10.00'
registos[4]['data'] = '2026-02-30'
registos[5]['data'] = '15/03/2026'
registos[6]['horas_trabalho'] = ''
registos[7]['custo_pecas'] = '12,50'
for row in registos + [registos[9].copy()]:
    node = ET.SubElement(root, 'intervencao')
    for key, value in row.items():
        ET.SubElement(node, key).text = str(value)
ET.indent(root)
ET.ElementTree(root).write(DATA / 'intervencoes.xml', encoding='utf-8', xml_declaration=True)
assert len(clientes) == 30 and len(veiculos) == 45 and len(registos) == 150
print('Fontes geradas: 31 linhas CSV (30 IDs), 45 veículos JSON, 151 intervenções XML (150 IDs).')
