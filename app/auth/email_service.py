from flask_mail import Message
from app.extensions import mail
from flask import current_app


def send_password_reset_email(email: str, token: str, full_name: str = None):
    """
    Envía un email con el token de recuperación de contraseña

    Args:
        email: Email del destinatario
        token: Token de recuperación generado
        full_name: Nombre completo del usuario (opcional)

    Returns:
        bool: True si el email se envió correctamente, False en caso contrario
    """
    try:
        # Construir URL de reset (ajustar según tu frontend)
        # En producción esto debería apuntar a tu frontend
        reset_url = f"{current_app.config.get('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={token}"

        # Nombre del destinatario
        recipient_name = full_name if full_name else "Usuario"

        # Crear el mensaje
        msg = Message(
            subject="Recuperación de Contraseña - Biblioteca",
            recipients=[email],
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )

        # Cuerpo del email en HTML
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .content {{ background-color: #f9f9f9; padding: 20px; margin: 20px 0; }}
                .button {{
                    display: inline-block;
                    padding: 12px 24px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    margin: 20px 0;
                }}
                .footer {{ color: #777; font-size: 12px; text-align: center; margin-top: 20px; }}
                .warning {{ color: #d32f2f; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Recuperación de Contraseña</h1>
                </div>
                <div class="content">
                    <p>Hola {recipient_name},</p>
                    <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta.</p>
                    <p>Haz clic en el botón de abajo para crear una nueva contraseña:</p>
                    <div style="text-align: center;">
                        <a href="{reset_url}" class="button">Restablecer Contraseña</a>
                    </div>
                    <p>O copia y pega este enlace en tu navegador:</p>
                    <p style="background-color: #e0e0e0; padding: 10px; word-break: break-all;">
                        {reset_url}
                    </p>
                    <p class="warning">⚠️ Este enlace expirará en 1 hora.</p>
                    <p>Si no solicitaste restablecer tu contraseña, puedes ignorar este correo de forma segura.</p>
                </div>
                <div class="footer">
                    <p>Este es un correo automático, por favor no respondas.</p>
                    <p>&copy; 2025 Sistema de Biblioteca. Todos los derechos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Cuerpo del email en texto plano (fallback)
        msg.body = f"""
        Hola {recipient_name},

        Recibimos una solicitud para restablecer la contraseña de tu cuenta.

        Para crear una nueva contraseña, visita el siguiente enlace:
        {reset_url}

        ⚠️ Este enlace expirará en 1 hora.

        Si no solicitaste restablecer tu contraseña, puedes ignorar este correo de forma segura.

        ---
        Este es un correo automático, por favor no respondas.
        Sistema de Biblioteca © 2025
        """

        # Enviar el email
        mail.send(msg)
        return True

    except Exception as e:
        # Log del error (en producción usar logging)
        print(f"Error al enviar email: {str(e)}")
        return False
