import os
from datetime import date, timedelta
from apps.eventos.models import Evento, Participante, Pagamento

def seed_data():
    evento, created = Evento.objects.get_or_create(
        nome="Retiro Espiritual 2026",
        defaults={
            'data_inicio': date.today() + timedelta(days=30),
            'data_fim': date.today() + timedelta(days=33),
            'valor_necessario': 150.00
        }
    )

    if created:
        print(f"Evento '{evento.nome}' criado.")
    else:
        print(f"Evento '{evento.nome}' já existia.")

    participantes_data = [
        {"nome": "João Silva", "email": "joao@example.com", "telefone": "11999999999"},
        {"nome": "Maria Souza", "email": "maria@example.com", "telefone": "11988888888"},
        {"nome": "Pedro Santos", "email": "pedro@example.com", "telefone": "11977777777"},
        {"nome": "Ana Costa", "email": "ana@example.com", "telefone": "11966666666"},
    ]

    for p_data in participantes_data:
        p, p_created = Participante.objects.get_or_create(
            evento=evento,
            nome=p_data["nome"],
            defaults={
                'email': p_data["email"],
                'telefone': p_data["telefone"],
                'valor_necessario': evento.valor_necessario
            }
        )
        if p_created:
            print(f"Participante '{p.nome}' criado.")

    joao = Participante.objects.get(nome="João Silva", evento=evento)
    if not Pagamento.objects.filter(participante=joao).exists():
        Pagamento.objects.create(evento=evento, participante=joao, valor_pago=150.00, forma_pagamento='PIX', confirmado=True)
    joao.atualizar_status()

    maria = Participante.objects.get(nome="Maria Souza", evento=evento)
    if not Pagamento.objects.filter(participante=maria).exists():
        Pagamento.objects.create(evento=evento, participante=maria, valor_pago=50.00, forma_pagamento='DINHEIRO', confirmado=True)
    maria.atualizar_status()

    ana = Participante.objects.get(nome="Ana Costa", evento=evento)
    if not Pagamento.objects.filter(participante=ana).exists():
        Pagamento.objects.create(evento=evento, participante=ana, valor_pago=200.00, forma_pagamento='CARTAO', confirmado=True)
    ana.atualizar_status()

    print("Dados para teste do Relatório gerados com sucesso!")

seed_data()
