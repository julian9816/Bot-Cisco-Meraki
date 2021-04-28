import logging
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from meraki_sdk.models.update_network_vlan_model import UpdateNetworkVlanModel
from meraki_sdk.models.dhcp_handling_enum import DhcpHandlingEnum
from meraki_sdk.models.dhcp_lease_time_enum import DhcpLeaseTimeEnum
from meraki_sdk.models import *
from meraki_sdk.models.reserved_ip_range_model import ReservedIpRangeModel
from meraki_sdk.models.dhcp_option_model import DhcpOptionModel
from meraki_sdk.exceptions.api_exception import APIException
from meraki_sdk.models.type_9_enum import Type9Enum
from meraki_sdk.meraki_sdk_client import MerakiSdkClient
from meraki_sdk.exceptions.api_exception import APIException
from meraki_sdk.models.create_network_vlan_model import CreateNetworkVlanModel
from meraki_sdk import *
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from random import randint
from meraki_sdk.models.update_network_ssid_model import UpdateNetworkSsidModel
from meraki_sdk.models.auth_mode_enum import AuthModeEnum
from meraki_sdk.models.enterprise_admin_access_enum import EnterpriseAdminAccessEnum
from meraki_sdk.models.encryption_mode_enum import EncryptionModeEnum
from meraki_sdk.models.wpa_encryption_mode_enum import WpaEncryptionModeEnum
from meraki_sdk.models.splash_page_enum import SplashPageEnum
from meraki_sdk.models.radius_server_model import RadiusServerModel
from meraki_sdk.models.radius_failover_policy_enum import RadiusFailoverPolicyEnum
from meraki_sdk.models.radius_load_balancing_policy_enum import RadiusLoadBalancingPolicyEnum
from meraki_sdk.models.radius_accounting_server_model import RadiusAccountingServerModel
from meraki_sdk.models.ap_tags_and_vlan_id_model import ApTagsAndVlanIdModel
import jsonpickle


class botCisco():
    # Enable logging
    def setUp(self):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)
    # Iniciar la conversacion

    def start(self, update, context):
        if update.message.text == "/start" or update.message.text == "1":
            self.seg_code = randint(1000, 9999)
            enviado = self.enviarCorreo("xxx@uxxxo")
            if enviado:
                update.message.reply_text(
                    "Se ha enviado un codigo de verificacion a su correo")
                update.message.reply_text("Por favor digite este codigo")
            return self.verificacion
        else:
            return ConversationHandler.END

    # Verificacion

    def enviarCorreo(self, correo):
        msg = MIMEMultipart()
        message = "Su codigo de seguridad es: "+str(self.seg_code)
        password = "xxxx"
        msg['From'] = "botmerakitelegram@gmail.com"
        msg['To'] = correo
        msg['Subject'] = "Codigo de seguridad BOT Cisco Meraki"
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("successfully sent email to %s:" % (msg['To']))
        return True
    # Menu Principal

    def inicio1(self, update, context):
        if int(update.message.text) == self.seg_code:
            self.num_intentos = 0
            self.organizations=self.meraki.organizations.get_organizations()
            org_text = 'Number'+'|'+'ID    '+'|'+'NAME  '+'|'+'\n'
            i=1
            for x in self.organizations:
                org_text = org_text + \
                    str(i)+'      |'+format(x["id"])+'|'+format(x["name"]) + '\n'
                x["number"]=i
                i+=1
            print(self.organizations)
            update.message.reply_text(org_text)
            update.message.reply_text("""
            Digite el numero de la organizacion.
            """)
        else:
            if self.num_intentos == 3:
                update.message.reply_text(
                    "Se ha agotado el numero de intentos")
                update.message.reply_text("""
                Opciones
                1. Para volver a enviar el codigo de verificacion
                2. Para salir
                """)
                return self.intentos_agotados
            else:
                update.message.reply_text(
                    "El codigo ingresado es erroneo, por favor vuelva a ingresar el codigo")
                text = "Le quedan "+str(3-self.num_intentos)+" intentos"
                update.message.reply_text(text)
                self.num_intentos += 1
                return self.verificacion
        return self.op_sel_org
    # Funciones MENUS
    def sel_network(self, update, context):
        self.organizacion=int(update.message.text)
        for x in self.organizations:
            if x["number"]==self.organizacion:
                self.organizacion=x["id"]
                break
        controller=self.meraki.networks
        self.networks=controller.get_organization_networks({"organization_id":self.organizacion})
        net_text = 'Number'+'|'+'ID    '+'|'+'NAME  '+'|'+'\n'
        i=1
        for x in self.networks:
            net_text = net_text + \
                str(i)+'      |'+format(x["id"])+'|'+format(x["name"]) + '\n'
            x["number"]=i
            i+=1
        update.message.reply_text(net_text)
        update.message.reply_text("""
            Digite el numero de la red
            """)
        return self.op_sel_net
    # Menu Principal
    def menu(self, update, context):
        for x in self.networks:
            if x["number"]==int(update.message.text):
                self.networkid=x["id"]
                break
        print(self.networkid)
        update.message.reply_text("""
            Bot Cisco Meraki
            Opciones:
            1. Administrar Redes
            2. Monitoreo
            """)
        return self.op_menu
    # Menu monitoreo
    def menu_monit(self, update, context):
        update.message.reply_text("""
            Bot Cisco Meraki
            Opciones:
            1. Monitoreo trafico clientes
            2. Monitoreo Location Analytics
            """)
        return self.op_monitoreo
    def monitor_client(self, update, context):
        collect = {}
        collect["network_id"] = self.networkid
        try:
            self.clients_controller.get_network_clients(collect)
        except APIException as e:
            print(e)
        return self.nose
    # Menu configuracion
    def menu_conf(self, update, context):
        update.message.reply_text("""
            Bot Cisco Meraki
            Opciones:
            1. Administrar VLANS
            2. Administrar Redes WIFI
            3. Salir
            """)
        return self.OPCION
    def menu_vlan(self, update, context):
        update.message.reply_text("Menu VLANS"
                                  'Opciones''\n'
                                  '1. Añadir VLAN''\n'
                                  '2. Ver VLANS existentes''\n'
                                  '3. Eliminar una VLAN'
                                  "4. Volver al menu principal")
        return self.OPCION_MENU_VLAN

    def menu_WIFI(self, update, context):
        update.message.reply_text("""
            Menu Redes WIFI
            Opciones
            1. Ver Redes WIFI activas
            2. Configurar una nueva Red WIFI
            3. Desactivar una Red WIFI
            4. Volver al menu principal""")
        return self.OPCION_MENU_WIFI

    # Funciones Menu Vlans

    def recoleccionDatosVlan(self, update, context):
        update.message.reply_text('Añadir VLAN')
        update.message.reply_text('Digite la direccion de la subnet')
        update.message.reply_text('Formato: xxx.xxx.xxx.xxx/xx')
        return self.DATOS

    def recoleccionDatosEliminarVlan(self, update, context):
        update.message.reply_text('Digite el id de la VLAN a eliminar')
        return self.ELIMINARVLAN

    def eliminarVlan(self, update, context):
        vlan_id = update.message.text
        collect = {}
        network_id = self.networkid
        collect['network_id'] = network_id
        collect['vlan_id'] = vlan_id
        try:
            self.vlans_controller.delete_network_vlan(collect)
        except APIException as e:
            print(e)
        update.message.reply_text(
            'Se ha eliminado la VLAN: '+str(vlan_id)+' Con exito')
        update.message.reply_text('Para volver al menu anterior digite Si')
        update.message.reply_text('Para Salir digite /cancel')
        return self.START

    def verVlans(self, update, context):
        update.message.reply_text('VLANS')
        vlans = self.vlans_controller.get_network_vlans(self.networkid)
        vlansText = 'VLAN ID'+'|'+'VLAN NAME'+'|'+'VLAN subnet'+'\n'
        for x in vlans:
            vlansText = vlansText + \
                format(x["id"])+'|'+format(x["name"]) + \
                '|'+format(x["subnet"])+'\n'

        update.message.reply_text(vlansText)
        update.message.reply_text('Para volver al menu anterior digite Si')
        update.message.reply_text('Para Salir digite /cancel')
        return self.START

    def subnet(self, update, context):
        update.message.reply_text('Digite la direccion del gateway')
        update.message.reply_text('Formato: xxx.xxx.xxx.xxx')
        self.subnetDir = update.message.text
        return self.GATEWAY

    def gateway(self, update, context):
        update.message.reply_text('Digite el ID de la VLAN a crear')
        self.gatewayDir = update.message.text
        return self.VLANID

    def vlanid_func(self, update, context):
        update.message.reply_text('Digite el nombre de la VLAN')
        self.vlanid = update.message.text
        return self.VLANAME

    def vlaname(self, update, context):
        self.vlanNameValor = update.message.text
        update.message.reply_text('Nueva VLAN''\n'
                                  'Nombre VLAN: '+self.vlanNameValor+'\n'
                                  'ID VLAN: '+str(self.vlanid)+'\n'
                                  'Direccion Subnet: '+str(self.subnetDir)+'\n'
                                  'Direccion GateWay: ' +
                                  str(self.gatewayDir)+'\n'
                                  'Para confirmar los valores por favor digite Si'+'\n'
                                  'Para cambiar los valores por favor digite No'
                                  )
        return self.CREARVLAN

    def crearVlan(self, update, context):

        if update.message.text == 'Si':
            network_id = self.networkid
            collect = {}
            collect['network_id'] = network_id
            create_network_vlan = CreateNetworkVlanModel()
            create_network_vlan.id = self.vlanid
            create_network_vlan.name = self.vlanNameValor
            create_network_vlan.subnet = self.subnetDir
            create_network_vlan.appliance_ip = self.gatewayDir
            collect['create_network_vlan'] = create_network_vlan
            try:
                self.vlans_controller.create_network_vlan(collect)
            except APIException as e:
                print(e)
            update.message.reply_text(
                'La VLAN: '+str(self.vlanid)+'\n'+'Ha sido creada con exito')
            update.message.reply_text('Para volver al menu anterior digite Si')
            update.message.reply_text('Para Salir digite /cancel')
        return self.START

# Funciones menu WIFI

    def ssids_activas(self, update, context):
        try:
            ssids = self.ssid_controller.get_network_ssids(self.networkid)
            ssid_text = 'ID'+'|'+'NAME'+'|'+'VLAN'+'\n'
            for red in ssids:
                if red["enabled"]:
                    ssid_text += str(red["number"])+"|"+red['name'] + \
                        "|"+str(red["defaultVlanId"])+'\n'
                else:
                    continue
            update.message.reply_text(ssid_text)
        except APIException as e:
            print(e)
        update.message.reply_text("""1. Para volver al menu de redes WIFI
        2. Para volver al menu principal""")
        return self.volver_menu_wifi

    def ssids_conf(self, update, context):
        try:
            ssids = self.ssid_controller.get_network_ssids(self.networkid)
            ssid_text = 'ID'+'|'+'NAME'+'|'+'Activa'+'\n'
            for red in ssids:
                if red["enabled"]:
                    ssid_text += str(red["number"])+"|" + \
                        red['name']+"|"+"Si"+'\n'
                else:
                    ssid_text += str(red["number"])+"|" + \
                        red['name']+"|"+"No"+'\n'
        except APIException as e:
            print(e)
        update.message.reply_text(ssid_text)
        update.message.reply_text("Digite el numero del id a configurar.")
        return self.id_wifi

    def confirmar_wifi(self, update, context):
        collect = {}
        collect['network_id'] = self.networkid
        self.number_ssid = update.message.text
        collect['number'] = self.number_ssid
        try:
            ssid = self.ssid_controller.get_network_ssid(collect)
            ssid_text = 'ID'+'|'+'NAME'+'|'+'Activa'+'\n'
            if ssid["enabled"]:
                ssid_text += str(ssid["number"])+"|"+ssid['name']+"|"+"Si"+'\n'
            else:
                ssid_text += str(ssid["number"])+"|"+ssid['name']+"|"+"No"+'\n'
            update.message.reply_text(ssid_text)
            update.message.reply_text("""Digite SI para configurar esta SSID
        Digite NO para cambiar de SSID""")
        except APIException as e:
            print(e)

        return self.confirmacion

    # Configuracion WIfi

    def conf_nombre_wifi(self, update, context):
        update.message.reply_text("Digite el nombre para la red WIFI")
        return self.op_nombre_wifi

    def conf_auth(self, update, context):
        self.nombre_wifi = update.message.text
        update.message.reply_text("Tipo de autenticacion para la red WIFI")
        update.message.reply_text("Digite una de las siguientes opciones")
        update.message.reply_text("""
        1. 'open'
        2. 'psk',
        3.'open-with-radius'
        4.'8021x-meraki'
        5.'8021x-radius'
        6.'ipsk-with-radius'
        7.'ipsk-without-radius'
        """)
        return self.op_tipo_auth

    def conf_clave(self, update, context):
        self.tipo_auth = int(update.message.text)
        if self.tipo_auth == 1:
            self.tipo_auth = AuthModeEnum.OPEN
            update.message.reply_text("Open")
            update.message.reply_text("Modo de Asignacion IP")
            update.message.reply_text("Digite una de las siguientes opciones")
            update.message.reply_text("""
            1.'NAT mode'
            2.'Bridge mode'
            3.'Layer 3 roaming',
            4.'Layer 3 roaming with a concentrator'
            5.'VPN'
            """)
            return self.op_mode_assigmentip
        elif self.tipo_auth == 2:
            self.tipo_auth = AuthModeEnum.PSK
            update.message.reply_text("Psk")
            update.message.reply_text("Digite la clave para la red WIFI")
        elif self.tipo_auth == 3:
            self.tipo_auth = AuthModeEnum.OPENWITHRADIUS
            update.message.reply_text("Open with radius") ##Corregir-revisar servidor
            update.message.reply_text("Digite la direccion ip del servidor")
            return self.op_conf_serv
        elif self.tipo_auth == 4:
            self.tipo_auth = AuthModeEnum.ENUM_8021XMERAKI
            update.message.reply_text('8021x-meraki') ##Corregir-revisar servidor
            self.mode_encrip = "wpa-eap"
            update.message.reply_text("RADIUS attribute specifying group policy name")
            update.message.reply_text("Digite una de las siguientes opciones")
            update.message.reply_text("""
            1.'Filter-Id'
            2.'Reply-Message'
            3.'Airespace-ACL-Name'
            4.'Aruba-User-Role'
                """)
            return self.op_radius_attribute
        elif self.tipo_auth == 5:
            self.tipo_auth = AuthModeEnum.ENUM_8021XRADIUS
            update.message.reply_text('8021x-radius') ##Corregir-revisar servidor
            update.message.reply_text("Digite la direccion ip del servidor")
            return self.op_conf_serv
        elif self.tipo_auth == 6:
            self.tipo_auth = 'ipsk-with-radius'
            update.message.reply_text('ipsk-with-radius') ##Corregir-revisar servidor
            update.message.reply_text("Digite la direccion ip del servidor")
            return self.op_conf_serv
        elif self.tipo_auth == 7:
            self.tipo_auth = "ipsk-without-radius"
            update.message.reply_text('ipsk-without-radius') ##Corregir-revisar servidor
            update.message.reply_text("Digite la direccion ip del servidor")
            return self.op_conf_serv
        else:
            update.message.reply_text("Digite una opcion valida")
            return self.op_tipo_auth
        return self.op_clave_wifi

    def conf_serv_radius(self, update, context):
        self.mode_encrip = "wpa-eap"
        update.message.reply_text("Digite el puerto del servidor")
        self.serv_radius = update.message.text
        return self.op_conf_port

    def conf_port_radius(self, update, context):
        self.port_radius = update.message.text
        update.message.reply_text("RADIUS attribute specifying group policy name")
        update.message.reply_text("Digite una de las siguientes opciones")
        update.message.reply_text("""
        1.'Filter-Id'
        2.'Reply-Message'
        3.'Airespace-ACL-Name'
        4.'Aruba-User-Role'
            """)
        return self.op_radius_attribute

    def conf_radius_attribute(self, update, context):
        opcion = int(update.message.text)
        if opcion == 1:
            self.radius_attribute = 'Filter-Id'
            update.message.reply_text("Modo de Asignacion IP")
            update.message.reply_text("Digite una de las siguientes opciones")
            update.message.reply_text("""
            1.'NAT mode'
            2.'Bridge mode'
            3.'Layer 3 roaming',
            4.'Layer 3 roaming with a concentrator'
            5.'VPN'
            """)
            return self.op_mode_assigmentip
        elif opcion == 2:
            self.radius_attribute = 'Reply-Message'
            update.message.reply_text("Modo de Asignacion IP")
            update.message.reply_text("Digite una de las siguientes opciones")
            update.message.reply_text("""
            1.'NAT mode'
            2.'Bridge mode'
            3.'Layer 3 roaming',
            4.'Layer 3 roaming with a concentrator'
            5.'VPN'
            """)
            return self.op_mode_assigmentip
        elif opcion == 3:
            self.radius_attribute = 'Airespace-ACL-Name'
            update.message.reply_text("Modo de Asignacion IP")
            update.message.reply_text("Digite una de las siguientes opciones")
            update.message.reply_text("""
            1.'NAT mode'
            2.'Bridge mode'
            3.'Layer 3 roaming',
            4.'Layer 3 roaming with a concentrator'
            5.'VPN'
            """)
            return self.op_mode_assigmentip
        elif opcion == 4:
            self.radius_attribute = 'Aruba-User-Role'
            update.message.reply_text("Modo de Asignacion IP")
            update.message.reply_text("Digite una de las siguientes opciones")
            update.message.reply_text("""
            1.'NAT mode'
            2.'Bridge mode'
            3.'Layer 3 roaming',
            4.'Layer 3 roaming with a concentrator'
            5.'VPN'
            """)
            return self.op_mode_assigmentip
        else:
            update.message.reply_text("Digite una opcion valida")
            return self.op_mode_encrip

    def conf_mode_encriptacion(self, update, context):
        self.clave_wifi = update.message.text
        update.message.reply_text(
            "Modo de encriptacion para la contraseña de la red WIFI")
        update.message.reply_text("Digite una de las siguientes opciones")
        update.message.reply_text("""
        1. WEP
        2. WPA
        """)
        return self.op_mode_encrip

    def conf_mode_wpaencriptacion(self, update, context):
        self.mode_encrip = int(update.message.text)
        if self.mode_encrip == 1:
            self.mode_encrip = EncryptionModeEnum.WEP
            update.message.reply_text("WEP")
            update.message.reply_text("Modo de Asignacion IP")
            update.message.reply_text("Digite una de las siguientes opciones")
            update.message.reply_text("""
            1.'NAT mode'
            2.'Bridge mode'
            3.'Layer 3 roaming',
            4.'Layer 3 roaming with a concentrator'
            5.'VPN'
            """)
            return self.op_mode_assigmentip
        elif self.mode_encrip == 2:
            self.mode_encrip = EncryptionModeEnum.WPA
            update.message.reply_text("WPA")
            update.message.reply_text("Modo de encriptacion WPA")
            update.message.reply_text("Digite una de las siguientes opciones")
            update.message.reply_text("""
            1.'WPA1 and WPA2'
            2.'WPA2 only'
            """)
        else:
            update.message.reply_text("Digite una opcion valida")
            return self.op_mode_encrip
        return self.op_mode_wpaencrip

    def conf_mode_assigmentip(self, update, context):
        self.mode_wpaencrip = int(update.message.text)
        if self.mode_wpaencrip == 1:
            self.mode_wpaencrip = WpaEncryptionModeEnum.ENUM_WPA1_AND_WPA2
            update.message.reply_text("WPA1 and WPA2")
            update.message.reply_text("Modo de Asignacion IP")
            update.message.reply_text("Digite una de las siguientes opciones")
            update.message.reply_text("""
                1.'NAT mode'
                2.'Bridge mode'
                3.'Layer 3 roaming',
                4.'Layer 3 roaming with a concentrator'
                5.'VPN'
                """)
        elif self.mode_wpaencrip == 2:
            self.mode_wpaencrip = WpaEncryptionModeEnum.ENUM_WPA2_ONLY
            update.message.reply_text("WPA2 ONLY")
            update.message.reply_text("Modo de Asignacion IP")
            update.message.reply_text("Digite una de las siguientes opciones")
            update.message.reply_text("""
                1.'NAT mode'
                2.'Bridge mode'
                3.'Layer 3 roaming'
                4.'Layer 3 roaming with a concentrator'
                5.'VPN'
                """)
        else:
            update.message.reply_text("Digite una opcion valida")
            return self.op_mode_wpaencrip
        return self.op_mode_assigmentip

    def conf_wvlan_id(self, update, context):
        self.mode_assigmentip = int(update.message.text)
        if self.mode_assigmentip == 1:
            self.mode_assigmentip = 'NAT mode'
            update.message.reply_text("Bandas para la red Wifi")
            update.message.reply_text("Digite una de las siguientes opciones")
            update.message.reply_text("""
            1.'Dual band operation'
            2.'5 GHz band only'
            3.'Dual band operation with Band Steering'
            """)
            return self.op_band_selection
        elif self.mode_assigmentip == 2:
            self.mode_assigmentip = 'Bridge mode'
            update.message.reply_text('Bridge mode')
            vlans = self.vlans_controller.get_network_vlans(self.networkid)
            vlansText = 'VLAN ID'+'|'+'VLAN NAME'+'|'+'VLAN subnet'+'\n'
            for x in vlans:
                vlansText = vlansText + \
                    format(x["id"])+'|'+format(x["name"]) + \
                    '|'+format(x["subnet"])+'\n'
            update.message.reply_text(vlansText)
            update.message.reply_text("Digite el id de la VLAN a asignar")
        elif self.mode_assigmentip == 3:
            self.mode_assigmentip = 'Layer 3 roaming'
            update.message.reply_text('Layer 3 roaming')
            update.message.reply_text('VLANS')
            vlans = self.vlans_controller.get_network_vlans(self.networkid)
            vlansText = 'VLAN ID'+'|'+'VLAN NAME'+'|'+'VLAN subnet'+'\n'
            for x in vlans:
                vlansText = vlansText + \
                    format(x["id"])+'|'+format(x["name"]) + \
                    '|'+format(x["subnet"])+'\n'
            update.message.reply_text(vlansText)
            update.message.reply_text("Digite el id de la VLAN a asignar")
        elif self.mode_assigmentip == 4:
            self.mode_assigmentip = 'Layer 3 roaming with a concentrator'
            update.message.reply_text('Layer 3 roaming with a concentrator')
            vlans = self.vlans_controller.get_network_vlans(self.networkid)
            vlansText = 'VLAN ID'+'|'+'VLAN NAME'+'|'+'VLAN subnet'+'\n'
            for x in vlans:
                vlansText = vlansText + \
                    format(x["id"])+'|'+format(x["name"]) + \
                    '|'+format(x["subnet"])+'\n'
            update.message.reply_text(vlansText)
            update.message.reply_text("Digite el id de la VLAN a asignar")
        elif self.mode_assigmentip == 5:
            self.mode_assigmentip = 'VPN'
            update.message.reply_text("Bandas para la red Wifi")
            update.message.reply_text("Digite una de las siguientes opciones")
            update.message.reply_text("""
            1.'Dual band operation'
            2.'5 GHz band only'
            3.'Dual band operation with Band Steering'
            """)
            return self.op_band_selection
        else:
            update.message.reply_text("Digite una opcion valida")
            return self.op_mode_assigmentip
        return self.op_wvlan_id

    def conf_band_selection(self, update, context):
        self.wvlan_id = int(update.message.text)
        update.message.reply_text("Bandas para la red Wifi")
        update.message.reply_text("Digite una de las siguientes opciones")
        update.message.reply_text("""
        1.'Dual band operation'
        2.'5 GHz band only'
        3.'Dual band operation with Band Steering'
        """)
        return self.op_band_selection

    def conf_client_limitup(self, update, context):
        self.band_selection = int(update.message.text)
        if self.band_selection == 1:
            self.band_selection = 'Dual band operation'
            update.message.reply_text('Dual band operation')
            update.message.reply_text(
                "Digite el límite de ancho de banda de carga en Kbps. (0 representa sin límite)")
        elif self.band_selection == 2:
            self.band_selection = '5 GHz band only'
            update.message.reply_text('5 GHz band only')
            update.message.reply_text(
                "Digite el límite de ancho de banda de carga en Kbps. (0 representa sin límite)")
        elif self.band_selection == 3:
            self.band_selection = 'Dual band operation with Band Steering'
            update.message.reply_text('Dual band operation with Band Steering')
            update.message.reply_text(
                "Digite el límite de ancho de banda de carga en Kbps. (0 representa sin límite)")
        else:
            update.message.reply_text("Digite una opcion valida")
            return self.op_band_selection
        return self.op_client_limitup

    def conf_client_limitdown(self, update, context):
        self.client_limitup = int(update.message.text)
        update.message.reply_text(
            "Digite el límite de ancho de banda de bajada en Kbps. (0 representa sin límite)")
        return self.op_client_limitdown

    def conf_wifi(self, update, context):
        self.client_limitdown = int(update.message.text)
        self.allow_ap = True
        self.update_network_ssid = {}
        self.update_network_ssid['name'] = self.nombre_wifi
        self.update_network_ssid['enabled'] = True
        if self.tipo_auth == "open":
            self.update_network_ssid['authMode'] = self.tipo_auth

        elif self.mode_encrip == "wpa":
            self.update_network_ssid['authMode'] = self.tipo_auth
            self.update_network_ssid['psk'] = self.clave_wifi
            self.update_network_ssid['encryptionMode'] = self.mode_encrip
            self.update_network_ssid['wpaEncryptionMode'] = self.mode_wpaencrip

        elif self.mode_encrip == "web":
            self.update_network_ssid['authMode'] = self.tipo_auth
            self.update_network_ssid['encryptionMode'] = self.mode_encrip

        else:
            if self.tipo_auth == "8021x-meraki" :
                self.update_network_ssid['radiusEnabled'] = True
                self.update_network_ssid['radiusAttributeForGroupPolicies'] = self.radius_attribute
                self.update_network_ssid['authMode'] = self.tipo_auth
                self.update_network_ssid['encryptionMode'] = "wpa"
                self.update_network_ssid['wpaEncryptionMode'] = "WPA2 only"
            else :
                radius_server={}
                radius_server["host"] = self.serv_radius
                radius_server["port"] = self.port_radius
                radius_server["secret"] = "null"
                self.update_network_ssid['authMode'] = self.tipo_auth
                self.update_network_ssid['encryptionMode'] = "wpa"
                self.update_network_ssid['wpaEncryptionMode'] = "WPA2 only"
                self.update_network_ssid['radiusServers'] = [radius_server]
                self.update_network_ssid['radiusEnabled'] = True
                self.update_network_ssid['radiusAttributeForGroupPolicies'] = self.radius_attribute
        if self.mode_assigmentip == "NAT mode" or self.mode_assigmentip == "VPN":
            self.update_network_ssid['ipAssignmentMode'] = self.mode_assigmentip
        else :
            self.update_network_ssid['ipAssignmentMode'] = self.mode_assigmentip
            self.update_network_ssid['useVlanTagging'] = True
            self.update_network_ssid['defaultVlanId'] = self.wvlan_id
            self.update_network_ssid['lanIsolationEnabled'] = False
        self.update_network_ssid['minBitrate'] = 11
        self.update_network_ssid['bandSelection'] = self.band_selection
        self.update_network_ssid['perClientBandwidthLimitUp'] = self.client_limitup
        self.update_network_ssid['perClientBandwidthLimitDown'] = self.client_limitdown
        self.update_network_ssid['availableOnAllAps'] = self.allow_ap
        self.update_network_ssid['visible'] = True
        self.update_network_ssid['splashPage'] = SplashPageEnum.ENUM_NONE
        print(self.update_network_ssid)
        collect = {}
        number = self.number_ssid
        collect['network_id'] = self.networkid
        collect['number'] = number
        collect['update_network_ssid'] = self.update_network_ssid
        try:
            self.ssid_controller.update_network_ssid(collect)
            update.message.reply_text("La Red se ha configurado con exito")
            update.message.reply_text("""1. Para volver al menu de redes WIFI
            2. Para volver al menu principal""")
            del self.update_network_ssid
            return self.volver_menu_wifi
        except APIException as e:
            print(e)
            update.message.reply_text("""
            Ha ocurrido un error por favor digite las siguientes opciones
            1. Para volver a configurar la red wifi
            2. Para volver al menu wifi""")
            del self.update_network_ssid
            return self.error_update_wifi

    # Funciones para cancelar y cerrar la conversacion

    def cancel(self, update, context):
        user = update.message.from_user
        self.logger.info(
            "El usuario %s ha salido de la conversacion.", user.first_name)
        update.message.reply_text('Adios, que tenga un buen día.',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    def error(self, update, context):
        """Log Errors caused by Updates."""
        self.logger.warning('Update "%s" caused error "%s"',
                            update, context.error)

    def main(self):
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        self.num_intentos = 0
        updater = Updater(
            "xxxx", use_context=True)
        # mibot = telegram.Bot("1018036620:AAEEdlklWQYxFm5MM8UDj9JF-VTAb2iKaFo")
        # Get the dispatcher to register handlers
        dp = updater.dispatcher
        # Variables menu principal
        (self.OPCION, self.OPCION_MENU_WIFI, self.OPCION_MENU_VLAN, self.DATOS,
         self.SUBNET, self.VLANID, self.VLANAME, self.GATEWAY, self.CREARVLAN,
         self.START, self.ELIMINARVLAN, self.volver_menu_wifi, self.id_wifi,
         self.confirmacion, self.verificacion, self.op_nombre_wifi, self.op_tipo_auth,
         self.intentos_agotados, self.op_clave_wifi, self.op_mode_encrip,
         self.op_mode_wpaencrip, self.op_mode_assigmentip, self.op_mode_assigmentip,
         self.op_wvlan_id, self.op_band_selection, self.op_client_limitup,
         self.op_client_limitdown, self.op_conf_serv, self.error_update_wifi,
         self.op_conf_port, self.op_radius_attribute, self.op_sel_org,
         self.op_sel_net, self.op_menu, self.op_monitoreo) = range(35)
        # conexion meraki
        x_cisco_meraki_api_key = 'xxx'
        self.meraki = MerakiSdkClient(x_cisco_meraki_api_key)
        # controladores
        self.vlans_controller = self.meraki.vlans
        self.ssid_controller = self.meraki.ssids
        self.clients_controller = self.meraki.clients
        # Menu
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],

            states={
                # Verificacion
                self.verificacion: [MessageHandler(Filters.text, self.inicio1)],
                self.intentos_agotados: [MessageHandler(Filters.text, self.start)],
                # Seleccion network y organizacion
                self.op_sel_org: [MessageHandler(Filters.text, self.sel_network)],
                self.op_sel_net: [MessageHandler(Filters.text, self.menu)],
                # Menu principal
                self.op_menu: [MessageHandler(Filters.regex('^(1)$'), self.menu_conf),
                               MessageHandler(Filters.regex('^(1)$'), self.menu_monit)],
                # Menu Monitoreo
                self.op_monitoreo: [MessageHandler(Filters.regex('^(1)$'), self.monitor_client),
                                    MessageHandler(Filters.regex('^(1)$'), self.location_analytics)],
                # Menu Configuracion
                self.OPCION: [MessageHandler(Filters.regex('^(1)$'), self.menu_vlan),
                              MessageHandler(Filters.regex( '^(2)$'), self.menu_WIFI),
                              MessageHandler(Filters.regex('^(3)$'), self.cancel)],
                # ADMINISTRAR VLANS
                self.OPCION_MENU_VLAN: [MessageHandler(Filters.regex('^(1)$'), self.recoleccionDatosVlan),
                                        MessageHandler(Filters.regex('^(2)$'), self.verVlans),
                                        MessageHandler(Filters.regex('^(3)$'), self.recoleccionDatosEliminarVlan),
                                        MessageHandler(Filters.regex('^(4)$'), self.menu)],
                self.DATOS: [MessageHandler(Filters.text, self.subnet)],
                self.GATEWAY: [MessageHandler(Filters.text, self.gateway)],
                self.VLANAME: [MessageHandler(Filters.text, self.vlaname)],
                self.VLANID: [MessageHandler(Filters.text, self.vlanid_func)],
                self.CREARVLAN: [MessageHandler(Filters.regex('^(Si)$'), self.crearVlan),
                                 MessageHandler(Filters.regex('^(No)$'), self.recoleccionDatosVlan)],
                self.START: [MessageHandler(Filters.regex('^(Si)$'), self.menu_vlan)],

                self.ELIMINARVLAN: [MessageHandler(Filters.text, self.eliminarVlan)],

                # Administrar Redes WIFI

                self.OPCION_MENU_WIFI: [MessageHandler(Filters.regex('^(1)$'), self.ssids_activas),
                                        MessageHandler(Filters.regex('^(2)$'), self.ssids_conf),
                                        MessageHandler(Filters.regex('^(4)$'), self.menu)],
                self.volver_menu_wifi: [MessageHandler(Filters.regex('^(1)$'), self.menu_WIFI),
                                        MessageHandler(Filters.regex('^(2)$'), self.menu)],
                self.id_wifi: [MessageHandler(Filters.text, self.confirmar_wifi)],
                self.confirmacion: [MessageHandler(Filters.regex('^(SI)$'), self.conf_nombre_wifi),
                                    MessageHandler(Filters.regex('^(NO)$'), self.ssids_conf)],
                self.op_nombre_wifi: [MessageHandler(Filters.text, self.conf_auth)],
                self.op_tipo_auth: [MessageHandler(Filters.text, self.conf_clave)],
                self.op_conf_serv: [MessageHandler(Filters.text, self.conf_serv_radius)],
                self.op_conf_port: [MessageHandler(Filters.text, self.conf_port_radius)],
                self.op_radius_attribute: [MessageHandler(Filters.text, self.conf_radius_attribute)],
                self.op_clave_wifi: [MessageHandler(Filters.text, self.conf_mode_encriptacion)],
                self.op_mode_encrip: [MessageHandler(Filters.text, self.conf_mode_wpaencriptacion)],
                self.op_mode_wpaencrip: [MessageHandler(Filters.text, self.conf_mode_assigmentip)],
                self.op_mode_assigmentip: [MessageHandler(Filters.text, self.conf_wvlan_id)],
                self.op_wvlan_id: [MessageHandler(Filters.text, self.conf_band_selection)],
                self.op_band_selection: [MessageHandler(Filters.text, self.conf_client_limitup)],
                self.op_client_limitup: [MessageHandler(Filters.text, self.conf_client_limitdown)],
                self.op_client_limitdown: [MessageHandler(Filters.text, self.conf_wifi)],
                self.error_update_wifi: [MessageHandler(Filters.regex('^(1)$'), self.confirmar_wifi),
                                         MessageHandler(Filters.regex('^(2)$'), self.menu_WIFI)]
            },

            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

        dp.add_handler(conv_handler)

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()


if __name__ == '__main__':
    botCiscoA = botCisco()
    botCiscoA.setUp()
    botCisco.main(botCiscoA)
