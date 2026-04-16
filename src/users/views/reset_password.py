from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password

from ..models.auth import User
from rest_framework.views import APIView
from rest_framework.response import Response

class RequestPasswordResetView(APIView):
    def post(self, request):
        email = request.data.get("email")

        try:
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"

            send_mail(
                "Reset de senha",
                f"Clique no link: {reset_link}",
                "no-reply@seusistema.com",
                [email],
            )

        except User.DoesNotExist:
            pass

        return Response({"message": "Se o email existir, você receberá instruções."})
    

class ConfirmPasswordResetView(APIView):
    def post(self, request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=user_id)

            if not default_token_generator.check_token(user, token):
                return Response({"error": "Token inválido"}, status=400)

            user.password = make_password(password)
            user.save()

            return Response({"message": "Senha redefinida com sucesso"})

        except Exception:
            return Response({"error": "Erro ao redefinir senha"}, status=400)