# -*- coding: utf-8 -*-

import json
import requests
import xbmc
import xbmcaddon
import xbmcgui
from . import control

class OnlineUpdater:
    def __init__(self):
        self.addon = xbmcaddon.Addon()
        self.github_base = "https://raw.githubusercontent.com/SEU_USUARIO/vortexplay-addon/main/config/"
        self.servers_url = self.github_base + "servers.json"
        self.version_url = self.github_base + "version.json"
        
    def log(self, message):
        """Log messages para debug"""
        xbmc.log(f'[VortexPlay Online Updater] {message}', xbmc.LOGINFO)
        
    def check_for_updates(self, silent=True):
        """Verificar se há atualizações disponíveis"""
        try:
            self.log("Verificando atualizações online...")
            
            # Verificar versão atual
            current_version = self.addon.getAddonInfo('version')
            
            # Buscar versão online
            response = requests.get(self.version_url, timeout=10)
            if response.status_code == 200:
                online_data = response.json()
                online_version = online_data.get('version', '1.0.0')
                
                self.log(f"Versão atual: {current_version}, Versão online: {online_version}")
                
                # Verificar se há nova versão
                if self.compare_versions(online_version, current_version):
                    if not silent:
                        xbmcgui.Dialog().notification(
                            'VortexPlay', 
                            'Nova versão disponível!', 
                            xbmcgui.NOTIFICATION_INFO, 
                            3000
                        )
                    return True
                    
            return False
            
        except Exception as e:
            self.log(f"Erro ao verificar atualizações: {str(e)}")
            return False
    
    def update_servers(self, silent=True):
        """Atualizar lista de servidores do GitHub"""
        try:
            self.log("Atualizando servidores online...")
            
            response = requests.get(self.servers_url, timeout=10)
            if response.status_code == 200:
                servers_data = response.json()
                
                # Atualizar configurações do addon
                for i, server in enumerate(servers_data.get('servers', []), 1):
                    if i <= 10:  # Máximo 10 servidores
                        if i == 1:
                            control.setSetting('DNS', server['dns'])
                            control.setSetting('Username', server['username'])
                            control.setSetting('Password', server['password'])
                        else:
                            control.setSetting(f'DNS{i}', server['dns'])
                            control.setSetting(f'Username{i}', server['username'])
                            control.setSetting(f'Password{i}', server['password'])
                
                # Atualizar lista de opções no settings
                server_names = [f"Servidor {i+1}" for i in range(len(servers_data.get('servers', [])))]
                
                if not silent:
                    xbmcgui.Dialog().notification(
                        'VortexPlay', 
                        f'{len(servers_data.get("servers", []))} servidores atualizados!', 
                        xbmcgui.NOTIFICATION_INFO, 
                        3000
                    )
                
                self.log(f"Servidores atualizados com sucesso: {len(servers_data.get('servers', []))}")
                return True
                
        except Exception as e:
            self.log(f"Erro ao atualizar servidores: {str(e)}")
            if not silent:
                xbmcgui.Dialog().notification(
                    'VortexPlay', 
                    'Erro ao atualizar servidores', 
                    xbmcgui.NOTIFICATION_ERROR, 
                    3000
                )
            return False
    
    def get_server_status(self):
        """Obter status dos servidores"""
        try:
            response = requests.get(self.servers_url, timeout=10)
            if response.status_code == 200:
                servers_data = response.json()
                return servers_data.get('servers', [])
        except:
            pass
        return []
    
    def compare_versions(self, version1, version2):
        """Comparar versões (version1 > version2)"""
        try:
            v1_parts = [int(x) for x in version1.split('.')]
            v2_parts = [int(x) for x in version2.split('.')]
            
            # Normalizar tamanhos
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))
            
            return v1_parts > v2_parts
        except:
            return False
    
    def force_update_check(self):
        """Forçar verificação de atualizações (chamada manual)"""
        dialog = xbmcgui.DialogProgress()
        dialog.create('VortexPlay', 'Verificando atualizações...')
        
        try:
            dialog.update(25, 'Verificando versão...')
            has_update = self.check_for_updates(silent=False)
            
            dialog.update(50, 'Atualizando servidores...')
            servers_updated = self.update_servers(silent=False)
            
            dialog.update(100, 'Concluído!')
            
            if has_update or servers_updated:
                xbmcgui.Dialog().ok(
                    'VortexPlay', 
                    'Atualizações aplicadas com sucesso!\n\nReinicie o addon para aplicar todas as mudanças.'
                )
            else:
                xbmcgui.Dialog().ok(
                    'VortexPlay', 
                    'Nenhuma atualização disponível.\n\nVocê já possui a versão mais recente.'
                )
                
        except Exception as e:
            self.log(f"Erro na atualização forçada: {str(e)}")
            xbmcgui.Dialog().ok(
                'VortexPlay', 
                'Erro ao verificar atualizações.\n\nVerifique sua conexão com a internet.'
            )
        finally:
            dialog.close()
    
    def auto_update_on_startup(self):
        """Atualização automática na inicialização (silenciosa)"""
        try:
            # Verificar se deve fazer update automático
            last_check = control.setting('last_update_check')
            import time
            current_time = str(int(time.time()))
            
            # Verificar a cada 24 horas
            if not last_check or (int(current_time) - int(last_check)) > 86400:
                self.log("Executando verificação automática de atualizações...")
                self.update_servers(silent=True)
                control.setSetting('last_update_check', current_time)
                
        except Exception as e:
            self.log(f"Erro na atualização automática: {str(e)}")

