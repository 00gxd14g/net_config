#!/bin/bash

# Ağ bilgilerini ve yapılandırmayı gösteren script

echo "Mevcut Ağ Arayüzleri:"
ip link show
echo ""

echo "Mevcut IP Adresleri:"
ip addr show
echo ""

echo "Mevcut DNS Ayarları:"
cat /etc/resolv.conf
echo ""

# Ağ arayüzünü al
read -p "Yapılandırmak istediğiniz ağ arayüzünü girin: " interface

# IP adresini ve alt ağ maskesini al
read -p "IP adresini ve alt ağ maskesini girin (CIDR notasyonunda): " ip_address

# Ağ geçidini al
read -p "Varsayılan ağ geçidini girin: " gateway

# DNS sunucusunu al
read -p "DNS sunucusunu girin: " dns

# Yerel web uygulaması için hostname al
read -p "Yerel web uygulaması için kullanılacak hostname girin (örn. localwebapp): " app_hostname

# Netplan yapılandırma dosyasını oluştur
sudo bash -c "cat > /etc/netplan/01-netcfg.yaml" << EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    $interface:
      dhcp4: no
      addresses: [$ip_address]
      gateway4: $gateway
      nameservers:
          addresses: [$dns]
EOF

# Netplan ile yapılandırmayı uygula
sudo netplan apply

# /etc/hosts dosyasına yerel DNS kaydını ekle
sudo bash -c "echo '${ip_address%/*} $app_hostname' >> /etc/hosts"

echo "Ağ ve yerel DNS yapılandırması tamamlandı."
