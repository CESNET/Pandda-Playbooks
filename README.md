<div align="center">
<picture>
  <source srcset="https://raw.githubusercontent.com/CESNET/Pandda-Playbooks/refs/heads/main/doc/img/logo_horizontal_white.svg" media="(prefers-color-scheme: dark)">
  <img src="https://raw.githubusercontent.com/CESNET/Pandda-Playbooks/refs/heads/main/doc/img/logo_horizontal_black.svg">
</picture>
</div>


## Dependencies

The installation process is prepared as a set of configuration files and playbooks for "ansible-playbook."  
To use it, you need to have Ansible installed, with a minimum version of 2.12.2. 🌮  

The monitoring probe and collector software are downloaded from the public RPM repository maintained by CESNET at [CESNET NEMEA Stable](https://copr.fedorainfracloud.org/coprs/g/CESNET/NEMEA-stable/) 🌐  
The installed software packages also include a set of dependencies, such as DPDK from standard RPM repositories of the distribution. ⚙️  

## Configuration ⚙️  
The configuration is stored in a YAML file, which maintains settings for each installed machine. The YAML configuration file must be placed in the Ansible inventory under the name `pandda.yaml`.

### Collector with Asset Management

Example configuration:
```yaml
- collector:
    port: 4739 # <-- Port on which the IPFIX server listens
    proto: "TCP" # <-- Protocol used by the IPFIX server
    forward_targets: # <-- If you do not want to forward IPFIX data (e.g., to long-term storage), remove forward_targets and all nested items
      - { host: "host1.liberouter.org", port: 4739, proto: "TCP" } # <-- Target for forwarded IPFIX data
      - { host: "host2.liberouter.org", port: 4739, proto: "UDP" }
- adict:
    protected_prefixes:
      - 10.0.0.0/24 # <-- Your protected network for asset management
    users:
      - username: admin # <-- Initial GUI username
        password: admin # <-- Initial GUI password. Change it immediately after installation!
```

## Measurement Point  
For measurement, we use the `ipfixprobe` exporter. For detailed documentation, please refer to [ipfixprobe](https://github.com/cesnet/ipfixprobe).  

Configuration for a measurement point:
```yaml
- probes:
    - instance_name: lena_raw
      input:
        type: raw # <-- Specification of the RAW input plugin for ipfixprobe
        ifc: eno8303
        blocks: 8 # <-- Number of buffers
        pkts: 16 # <-- Input buffer size
      cache:
        size: 23 # <-- Flow cache size in format 2^size
        active_timeout: 300 # <-- Active timeout (s)
        inactive_timeout: 65 # <-- Inactive timeout (s)
      plugins:
        - basicplus
        - tls
        - vlan
        - pstats: [includezeroes, skipdup]
      output: # <-- Specification of the output plugin
        link: true
        dir: false
        host: localhost
        port: 3099
        udp: true
        template_refresh_rate: 60
```

## Installation / Configuration of Prepared Machines

1. Using the `ansible-playbook` command, the necessary packages will be installed, configuration will be created, and required services will be started automatically. 🚀  

Example execution from `path_to_this_repository/ansible/`:
```sh
ansible-playbook -i inventory pandda.yml
```
Installation and configuration can be limited to a specific server using the `-l` flag, as shown in the `ansible-playbook -h` help command.

## Modifying the Configuration of an Existing Machine

To modify the configuration of an existing machine, you need to edit the pandda configuration file located in the inventory and rerun the ansible playbook.

## Running Using a Test Vagrant Environment

1. Uncomment the line `#192.168.55.10 ansible_become=yes ansible_become_method=sudo` in `ansible/inventory/collector_vagrant_hosts` 🔧  
2. In the root directory of the repository, start Vagrant using:  
   ```sh
   vagrant up
   ```  

The PANDDA GUI with available asset management will be accessible at `http://localhost:8000` and `https://localhost:8001`.  

