# -*- coding: utf-8 -*-
from setuphelpers import *
import base64
import configparser

configfile='conf.ini'
config = configparser.ConfigParser()
config.read(configfile, encoding='utf-8')

title = config.get('common','title')
subtile = config.get('common','subtile')
message = config.get('common','message').replace(config.get('common','message')[0],"").replace(config.get('common','message')[-1],"")
signature = config.get('common','signature')
logo_link = config.get('common','logo_link')
popup_start_time = config.get('common','popup_start_time')
popup_end_time = config.get('common','popup_end_time')
popup_end_time = config.get('common','popup_end_time')
task_name = config.get('common','task_name')
task_enabled = config.getboolean('common','task_enabled')
popup_directly = config.getboolean('common','popup_directly')
popup_at_logon = config.getboolean('common','popup_at_logon')
popup_after_unlock_session = config.getboolean('common','popup_after_unlock_session')
group_objectSid_filter = config.get('common','group_objectSid_filter')

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
    messsage_list.insert(item*2,"<br>")
 
  html_code = """<h1>
    <p style="text-align: center; color: red">%s</p>
    <div style="clear:both"></div>
    </h1>
    <h2 style="text-align: center;">%s</h2>
    <br>
    %s
    <br>
    <br>
    <b>%s</b>
    <br>
    <br>
    <center>
    <img src="%s" alt="Image" style="width:100px;height:100px;"/>
    </center>
    <br><br>""" % (title,subtile,('\n'.join(message_list)),signature,logo_link) 

  return (base64.b64encode(html_code.encode("utf8"))).decode("ascii")

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
        <GroupId>%s</GroupId>
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
                group_objectSid_filter,str(task_enabled).lower(),
                b64_msg)

  with open(f"{task_name}.xml", "w+") as xml:
      xml.write(xml_data)
