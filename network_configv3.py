import subprocess
import re
from tabulate import tabulate
from termcolor import colored

def run_command(command):
    try:
        return subprocess.check_output(command, shell=True).decode('utf-8')
    except subprocess.CalledProcessError as e:
        return str(e)

def get_network_interfaces():
    interfaces_output = run_command('ip link show')
    interfaces = re.findall(r'\d+: ([^:]+):', interfaces_output)
    return interfaces

def get_ip_addresses():
    ip_output = run_command('ip addr')
    ips = re.findall(r'\d+: ([^:]+):.*?inet (\S+)', ip_output, re.DOTALL)
    return ips

def get_dns_settings():
    try:
        dns_output = run_command('systemd-resolve --status')
        return dns_output
    except Exception as e:
        return str(e)

def display_data(data, headers):
    print(tabulate(data, headers=headers, tablefmt="grid"))

def configure_network():
    print(colored("\nYapılandırma Seçenekleri:", 'yellow'))
    interface = input(colored("Yapılandırmak istediğiniz arayüz adını girin: ", 'green'))
    new_ip = input(colored("Yeni IP adresini girin (örn: 192.168.1.10/24): ", 'green'))
    gateway = input(colored("Varsayılan ağ geçidini girin (örn: 192.168.1.1): ", 'green'))

    ip_cmd = f"sudo ip addr add {new_ip} dev {interface}"
    gw_cmd = f"sudo ip route add default via {gateway}"

    print(colored("\nYapılandırma uygulanıyor...", 'blue'))
    print(run_command(ip_cmd))
    print(run_command(gw_cmd))
    print(colored("Yapılandırma tamamlandı.", 'green'))

def main():
    print(colored("Mevcut Ağ Arayüzleri:", 'blue'))
    interfaces = get_network_interfaces()
    display_data([(i, intf) for i, intf in enumerate(interfaces, 1)], ["Sıra No", "Arayüz"])

    print(colored("\nMevcut IP Adresleri:", 'blue'))
    ip_addresses = get_ip_addresses()
    display_data(ip_addresses, ["Arayüz", "IP Adresi"])

    print(colored("\nMevcut DNS Ayarları:", 'blue'))
    dns_settings = get_dns_settings()
    print(dns_settings)

    change_config = input(colored("\nYapılandırmayı değiştirmek istiyor musunuz? (evet/hayır): ", 'green')).strip().lower()
    if change_config == 'evet':
        configure_network()

if __name__ == "__main__":
    main()
