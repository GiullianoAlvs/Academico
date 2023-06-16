
import webview
import pandas as pd
import pyodbc
import datetime
from flask import Flask, render_template, send_file, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)
window = webview.create_window('Controle de Estoque', app)
app.config['UPLOAD_FOLDER'] = 'C:/Caminho/para/o/diretorio/uploads'

EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USERNAME = 'seu-email@exemplo.com'
EMAIL_PASSWORD = 'sua-senha'
EMAIL_FROM = 'seu-email@exemplo.com'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gerar-relatorio", methods=['GET', 'POST'])
def gerar_relatorio():
    if request.method == 'POST':
        # Recuperar a validade selecionada pelo usuário
        validade = int(request.form.get("validade"))

        # Estabelecer conexão com o banco de dados
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              'SERVER=nome-do-servidor;'
                              'DATABASE=nome-do-banco;'
                              'Trusted_Connection=yes;')

        # Consulta SQL
        sql_query = "SELECT * FROM Produtos"

        # Executar consulta e obter os resultados em um DataFrame
        df = pd.read_sql(sql_query, conn)

        # Converter a coluna 'validade' para o tipo de dados datetime
        df['validade'] = pd.to_datetime(df['validade']).dt.date

        # Calcular a data limite com base na validade escolhida
        hoje = datetime.date.today()
        data_limite = hoje + datetime.timedelta(days=validade)

        # Filtrar os produtos com base na data de validade
        produtos_validade = df[df['validade'] <= data_limite].sort_values(by='validade')

        # Gera um arquivo Excel com os produtos filtrados
        relatorio_path = app.config['UPLOAD_FOLDER'] + '/relatorio.xlsx'
        produtos_validade.to_excel(relatorio_path, index=False)

        # Fechar a conexão com o banco de dados
        conn.close()

        return render_template("relatorio_gerado.html")
    else:
        # Processar o método GET para a rota
        return "Endpoint 'gerar-relatorio' para método GET"

@app.route("/download-relatorio")
def download_relatorio():
    return send_file(app.config['UPLOAD_FOLDER'] + '/relatorio.xlsx', as_attachment=True)

@app.route("/email-form")
def email_form():
    return render_template("email_form.html")

@app.route("/enviar-email", methods=['POST'])
def enviar_email_route():
    if request.method == 'POST':
        email_destinatario = request.form.get("email")
        nome_arquivo = request.form.get("nome_arquivo")
        relatorio_path = app.config['UPLOAD_FOLDER'] + '/relatorio.xlsx'

        # Chamar a função enviar_email() para enviar o e-mail
        enviar_email(relatorio_path, email_destinatario, nome_arquivo)

        return render_template("envio_confirmado.html")


@app.route("/envio-confirmado")
def envio_confirmado():
    return render_template("envio_confirmado.html")

def enviar_email(relatorio_path, email_destinatario, nome_arquivo):
    # Criar uma instância do objeto MIMEMultipart
    msg = MIMEMultipart()

    # Configurar os detalhes do e-mail
    msg['From'] = EMAIL_FROM
    msg['To'] = email_destinatario
    msg['Subject'] = 'Relatório de Produtos'

    # Adicionar o corpo do e-mail
    mensagem = 'Segue em anexo o relatório de produtos.'
    msg.attach(MIMEText(mensagem, 'plain'))

    # Ler o conteúdo do arquivo do relatório
    with open(relatorio_path, 'rb') as arquivo:
        # Criar uma instância do objeto MIMEBase para o arquivo anexo
        anexo = MIMEBase('application', 'octet-stream')
        # Definir o conteúdo do anexo
        anexo.set_payload(arquivo.read())

    # Codificar o anexo em base64
    encoders.encode_base64(anexo)

    # Adicionar os cabeçalhos do anexo
    anexo.add_header('Content-Disposition', f'attachment; filename={nome_arquivo}')
    # Anexar o arquivo ao e-mail
    msg.attach(anexo)

    # Configurar a conexão SMTP
    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
        # Iniciar a conexão com o servidor SMTP
        smtp.ehlo()
        # Habilitar a criptografia TLS
        smtp.starttls()
        # Realizar o login no servidor SMTP
        smtp.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        # Enviar o e-mail
        smtp.send_message(msg)

    print('E-mail enviado com sucesso.')


if __name__ == '__main__':
    webview.start()
