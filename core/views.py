import logging
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from django.conf import settings

def index(request):
    return render(request, 'index.html')

# Configura o logger para este arquivo. Boa prática para ter logs mais organizados.
logger = logging.getLogger(__name__)

def agendar_consulta_view(request):
    """
    Recebe os dados de um formulário via POST, valida, envia um e-mail
    e retorna uma resposta JSON. Inclui logs para debugging.
    """
    # Garante que a requisição é um POST
    if request.method == 'POST':
        try:
            # 1. Pega os dados enviados pelo JavaScript
            nome = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            mensagem = request.POST.get('message')

            # 2. Validação simples dos dados
            if not nome or not email or not mensagem:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Nome, e-mail e mensagem são campos obrigatórios.'
                }, status=400)

            # 3. Monta o corpo do e-mail
            corpo_email = f"""
            Você recebeu uma nova mensagem de contato através do site:

            Nome: {nome}
            Telefone: {phone if phone else 'Não informado'}
            Email: {email}

            Mensagem:
            {mensagem}
            """

            # --- LOG DE DEBUG ANTES DE ENVIAR ---
            # Isso aparecerá nos seus logs do Render para confirmar que o código chegou até aqui
            print(f"Tentando enviar e-mail de '{nome}' com remetente '{settings.DEFAULT_FROM_EMAIL}'")
            logger.info(f"Tentando enviar e-mail de '{nome}' com remetente '{settings.DEFAULT_FROM_EMAIL}'")


            # 4. Envia o e-mail
            send_mail(
                subject=f'Novo agendamento pelo site: {nome}', # Assunto do e-mail
                message=corpo_email, # Corpo do e-mail
                from_email=settings.DEFAULT_FROM_EMAIL, # Remetente configurado no settings.py
                recipient_list=['drmariowolak.atendimentos@gmail.com'], # O destinatário
                fail_silently=False, # Gera um erro se o envio falhar
            )

            # 5. Retorna uma resposta de sucesso
            return JsonResponse({'status': 'success', 'message': 'Mensagem enviada com sucesso!'})

        except Exception as e:
            # --- LOG DE ERRO ---
            # Se qualquer coisa no bloco 'try' falhar, o erro exato será registrado aqui
            print(f"ERRO AO ENVIAR E-MAIL: {e}")
            logger.error(f"Falha ao processar agendamento: {e}", exc_info=True) # exc_info=True mostra o traceback completo

            # 6. Retorna uma resposta de erro genérica para o usuário
            return JsonResponse({
                'status': 'error',
                'message': 'Ocorreu um erro interno no servidor. Tente novamente mais tarde.'
            }, status=500)

    # Se a requisição não for POST, retorna um erro
    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)
