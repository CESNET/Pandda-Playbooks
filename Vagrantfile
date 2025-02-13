# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  config.vm.define "collector" do |collector|
    collector.vm.box = "bento/oraclelinux-9"

    # Set a static IP
    collector.vm.network "private_network", ip: "192.168.56.10"

    # Forward ports
    collector.vm.network "forwarded_port", guest: 80, host: 8000, protocol: "tcp"
    collector.vm.network "forwarded_port", guest: 443, host: 8001, protocol: "tcp"

    collector.vm.hostname = "panddacol"
    collector.vm.provision "shell", inline: <<-SHELL
      hostnamectl set-hostname "panddacol - \(o\_o\)"
    SHELL
    collector.vm.provision "ansible" do |ansible|
      ansible.become = true
      ansible.compatibility_mode = "2.0"
      #ansible.raw_arguments = [ "-v" ]
      ansible.inventory_path = "./ansible/inventory"
      ansible.groups = {
        "collector" => ["collector"]
      }
      ansible.playbook = "./ansible/pandda.yml"
    end
  end

  config.vm.define "metering_point" do |metering_point|
    metering_point.vm.box = "bento/oraclelinux-9"

    # Set a static IP
    metering_point.vm.network "private_network", ip: "192.168.56.11"

    metering_point.vm.hostname = "panddamp"
    metering_point.vm.provision "shell", inline: <<-SHELL
      hostnamectl set-hostname "pandamp - \(o\_o\)"
    SHELL
    metering_point.vm.provision "ansible" do |ansible|
      ansible.become = true
      ansible.compatibility_mode = "2.0"
      #ansible.raw_arguments = [ "-v" ]
      ansible.inventory_path = "./ansible/inventory"
      ansible.groups = {
        "metering_point" => ["metering_point"]
      }
      ansible.playbook = "./ansible/pandda.yml"
    end
  end

end