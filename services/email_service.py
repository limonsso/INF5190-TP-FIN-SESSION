
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

from configuration.configs import get_configuration


def send_nouveaux_contrevenants(list_new_contrevenant):
    config = get_configuration('../configuration/configuration.yaml')
    email_configuration = config['email_configuration']
    smtp_configuration = config['smtp_configuration']
    msg = EmailMessage()
    msg['Subject'] = f'Les nouveaux contrevenants depuis la dernière importation de données'
    msg['From'] = email_configuration['from']
    msg['To'] = email_configuration['to']
    msg.set_content("""\
    Salut!

     De nouveaux contrevenants ont ajoutés par la ville de montréal
    
    """)
    msg.add_alternative(generate_html(list_new_contrevenant), subtype='html')
    # Send the message via our own SMTP server.
    try:
        with smtplib.SMTP(smtp_configuration['host'], smtp_configuration['port']) as s:
            s.send_message(msg)
    except:
        print("Envoi d'email a éechoué. Vérifier les configurations SMTP dans le fichier configuration.yaml")



def generate_html(list_new_contrevenant):
    rows = ''
    list_new_contrevenant.sort(key=lambda x: x.proprietaire, reverse=True)
    list_new_contrevenant = list(dict.fromkeys(list_new_contrevenant))
    for contrevenant in list_new_contrevenant:
        rows += f"""\
            <tr>
                <td scope="row">{contrevenant.proprietaire}</td>
                <td scope="row">{contrevenant.categorie}</td>
                <td scope="row">{contrevenant.etablissement}</td>
                <td scope="row">{contrevenant.adresse}</td>
                <td scope="row">{contrevenant.ville}</td>            
            </tr>
        """
    html = f"""\
        <html>
          <head>
            <link rel="stylesheet" href="https://bootswatch.com/4/yeti/bootstrap.min.css">
          </head>
          <body class="container">
            <p>Salut!</p>
            <p>
                De nouveaux contrevenants ont ajoutés par la ville de montréal
            </p>
            <table class="table">
              <thead>
                <tr class="table-dark">
                    <th scope="col">Proprietaire</th>
                    <th scope="col">Categorie</th>
                    <th scope="col">Établissement</th>
                    <th scope="col">Adresse</th>
                    <th scope="col">Ville</th>
                </tr>
              </thead>
              <tbody>
                {rows}
              <tbody>
            </table>
            </br>
            </br>
            <p>
                <strong>Ezechiel Gnepa</strong></br>
                <em>Full-Stack Programer Python</em>
            <p/>
          </body>
        </html>
        """
    return html
