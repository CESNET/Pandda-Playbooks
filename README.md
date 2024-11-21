# 🐼 PANDDA Playbooks

## Závislosti

Instalační proces je připraven jako sada konfiguračních souborů a předpisy pro "ansible-playbook".
Pro použití je potřeba mít nainstalovaný software Ansible, verze alespoň 2.12.2.📦

Software monitorovací sondy se stahuje z veřejného RPM repozitáře spravovaného sdružením CESNET a to https://copr.fedorainfracloud.org/coprs/g/CESNET/NEMEA-stable/ 🌐
Instalovaným softwarovým nástrojem je balík ipfixprobe-dpdk, který zároveň instaluje i sadu závislostí, například DPDK z běžných RPM repozitářů distribuce. ⚙️

## Instalace / Konfigurace připravených strojů

1. pro přístup k měřícím bodům je potřeba mít spuštěnou VPN 🔒
2. pomocí příkazu `ansible-playbook` se automatizovaně nainstalují potřebné balíky, vytvoří se konfigurace a spustí se potřebné služby. 🚀

Příklad spuštění z umístění `cesta_k_tomuto_repozitari/ansible/`:

```
ansible-playbook -i inventory/metering_points_hosts metering-point.yml
```

Spuštění (instalaci&konfiguraci) lze limitovat na pouze vybraný server pomocí
přepínače `-l`, viz nápověda příkazu `ansible-playbook -h`.

## Změna konfigurace stávajícího stroje

Pro změnu konfigurace stávajícího stroje je potřeba upravit konfigurační soubor pro ipfixprobe, který je umístěný v cestě `ansible/inventory/host_files/ADRESA_SERVERU/ipfixprobe/instance_NAZEV_LINKY.conf`.

Z pohledu uživatelské konfigurace jsou relevantní parametry v sekci `#STORAGE` a `#OUTPUT`. Detailnější popis jednotlivých parametrů je zde: https://github.com/CESNET/ipfixprobe/blob/master/init/link0.conf.example.

Například změna konfigurace IPFIX kolektoru, na který jsou data odesílána je možná pomocí těchto parametrů:
```
HOST=novy-ftas.kr-vysocina.cz // adresa kolektoru
PORT=3600 // port na kterém kolektor poslouchá
UDP=yes // (yes/no) použití UDP protokolu, jinak TCP
```

## Spuštění pomocí testovacího Vagrantu
1. Odkomentujte řádek `#192.168.55.10 ansible_become=yes ansible_become_method=sudo` v `ansible/inventory/collector_vagrant_hosts` 🔧
2. V root složce repoziáře spusťte vagrant pomocí `vagrant up`

