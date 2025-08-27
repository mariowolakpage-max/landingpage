from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
import json
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def agendar_consulta_view(request):
    # Garante que a requisição é um POST
    if request.method == 'POST':
        try:
            # Pega os dados enviados pelo JavaScript
            # Nota: usamos request.POST.get() para pegar dados de um FormData
            nome = request.POST.get('name') # 'name' deve ser o atributo name="" do seu input no HTML
            phone = request.POST.get('phone')
            email = request.POST.get('email') # 'email' deve ser o atributo name=""
            mensagem = request.POST.get('message') # 'message' deve ser o atributo name=""

            # Validação simples
            if not nome or not email or not mensagem:
                return JsonResponse({'status': 'error', 'message': 'Todos os campos são obrigatórios.'}, status=400)

            # Monta o corpo do e-mail
            corpo_email = f"""
            Você recebeu uma nova mensagem de contato:

            Nome: {nome}
            Telefone: {phone}
            Email: {email}

            Mensagem:
            {mensagem}
            """

            send_mail(
                subject=f'Agendar Consulta: {nome}', # Assunto do e-mail
                message=corpo_email, # Corpo do e-mail
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['drmariowolak.atendimentos@gmail.com'], # << MUDE AQUI para o seu e-mail
                fail_silently=False,
            )

            # Retorna uma resposta de sucesso em JSON
            return JsonResponse({'status': 'success', 'message': 'Mensagem enviada com sucesso!'})

        except Exception as e:
            # Em caso de qualquer erro, retorna um erro em JSON
            return JsonResponse({'status': 'error', 'message': f'Ocorreu um erro no servidor: {e}'}, status=500)

    # Se não for POST, retorna um erro
    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)
