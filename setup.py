# -*- coding: utf-8 -*-
from setuphelpers import *
import base64

# INDIQUER UN TITRE (Exemple : INFORMATION, ALERTE, IMPORTANT...)
title = "Alerte de sécurité importante"
# INDIQUER UN SOUS-TITRE (Exemple: Perturbation des accès mails, Mise à jour applicative...)
subtile = "Changement de mot de passe recommandé"
# INDIQUER LE CORPS DU MESSAGE (Le retour à la ligne est pris en compte, par exemple, si vous passez une ligne, une ligne sera passée dans le popup)
message = """Notre système de sécurité a detecté que votre mot de passe de session Windows est répertorié dans la base de données Have I Been Pwned, un service qui identifie les mots de passe affectés par des fuites de données sur Internet.

Nous vous recommandons vivement de prendre des mesures préventives pour sécuriser votre compte en modifiant votre mot de passe en respectant les recommandations disponibles en cliquant <a href="https://www.cybermalveillance.gouv.fr/medias/2019/11/Fiche-pratique_mots-de-passe.pdf">sur le lien suivant</a>.

La sécurité de vos données est notre priorité, et nous mettons en œuvre des mesures pour renforcer la protection de votre compte.

Si vous avez des questions, n'hésitez pas à nous contacter.

Cordialement,"""
# INDIQUER LE SIGNATAIRE DU MESSAGE (Exemple La DSI, La DRH...)
signature = "La Direction des Systèmes d'Informations"
# INDIQUER LE LIEN D'UN LOGO D'ENTREPRISE
logo_link = "https://srvwapt.mydomain.lan/wapt/logo.jpg"

# INDIQUER UNE DATE DE DEPART DU POPUP, Mettre une date passée pour afficher tout de suite
popup_start_time = "2022-11-15T17:00:00"
# INDIQUER UNE DATE DE FIN DU POPUP
popup_end_time = "2024-11-15T14:00:00"

# Nom de la tâche planifiée
task_name = "WAPT-popup"
# Activer la tâche planifiée
task_enabled = True
# Afficher le popup directement après installation
popup_directly = True
# Afficher le popup après la connexion
popup_at_logon = True
# Afficher le popup après déverouillage
popup_after_unlock_session = True

# RIEN N'EST A MODIFIER DANS LA SUITE DU CODE

def install():
    uninstall()
    create_task_xml(b64_msg=convert_message_to_html_b64(msg=message))
    run(f'schtasks /create /tn "{task_name}" /xml "{task_name}.xml"')

def uninstall():

  if task_exists(task_name):
    delete_task(task_name)

def audit():

    if task_exists(task_name):
      print(f'La tâche planifiée "{task_name}" est bien présente sur le poste')
      return "OK"

    else:

        print(f"La tâche planifiée {task_name} n'existe pas")
        install()
        return "WARNING"

def convert_message_to_html_b64(msg=None):

  message_list = msg.splitlines()
  for item in range (0,len(message_list)):
    message_list.insert(item*2,"<br>")

  html_code = """<h1 class="poptitle1">
    <p style="text-align: center; color: red">%s</p>
    <div style="clear:both"></div>
    </h1>
    <h2 class="poptitle" style="text-align: center;">%s</h2>
    <br>
    %s
    <br>
    <br>
    <b>%s</b>
    <br>
    <br>
    <center>
    <img src="%s" class="logo" alt="Image" style="width:100px;height:100px;"/>
    </center>
    <br><br>""" % (title,subtile,('\n'.join(message_list)),signature,logo_link)

  sample_string_bytes = html_code.encode("utf8")
  base64_bytes = base64.b64encode(sample_string_bytes)
  base64_message = base64_bytes.decode("ascii")
  return base64_message

def create_task_xml(b64_msg=None):

  xml_data = """<?xml version="1.0" encoding="UTF-16"?>
  <Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
    <RegistrationInfo>
      <Date>2021-05-21T13:29:24.4192635</Date>
      <Author>WAPT</Author>
      <URI>\%s</URI>
    </RegistrationInfo>
    <Triggers>
      <LogonTrigger>
        <StartBoundary>%s</StartBoundary>
        <EndBoundary>%s</EndBoundary>
        <Enabled>%s</Enabled>
      </LogonTrigger>
      <SessionStateChangeTrigger>
        <StartBoundary>%s</StartBoundary>
        <EndBoundary>%s</EndBoundary>
        <Enabled>%s</Enabled>
        <StateChange>SessionUnlock</StateChange>
      </SessionStateChangeTrigger>
      <RegistrationTrigger>
        <StartBoundary>%s</StartBoundary>
        <EndBoundary>%s</EndBoundary>
        <Enabled>%s</Enabled>
      </RegistrationTrigger>
    </Triggers>
    <Principals>
      <Principal id="Author">
        <GroupId>S-1-5-21-1329495337-996673521-1290604912-513</GroupId>
        <RunLevel>LeastPrivilege</RunLevel>
      </Principal>
    </Principals>
    <Settings>
      <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
      <DisallowStartIfOnBatteries>true</DisallowStartIfOnBatteries>
      <StopIfGoingOnBatteries>true</StopIfGoingOnBatteries>
      <AllowHardTerminate>true</AllowHardTerminate>
      <StartWhenAvailable>false</StartWhenAvailable>
      <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
      <IdleSettings>
        <StopOnIdleEnd>true</StopOnIdleEnd>
        <RestartOnIdle>true</RestartOnIdle>
      </IdleSettings>
      <AllowStartOnDemand>true</AllowStartOnDemand>
      <Enabled>%s</Enabled>
      <Hidden>false</Hidden>
      <RunOnlyIfIdle>false</RunOnlyIfIdle>
      <WakeToRun>false</WakeToRun>
      <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
      <Priority>7</Priority>
    </Settings>
    <Actions Context="Author">
      <Exec>
        <Command>waptmessage</Command>
        <Arguments>-b %s -s 800X900</Arguments>
      </Exec>
    </Actions>
  </Task>""" % (task_name,
                popup_start_time,popup_end_time,str(popup_at_logon).lower(),
                popup_start_time,popup_end_time,str(popup_after_unlock_session).lower(),
                popup_start_time,popup_end_time,str(popup_directly).lower(),
                str(task_enabled).lower(),
                b64_msg)

  with open(f"{task_name}.xml", "w+") as xml:
      xml.write(xml_data)
