# -*- mode: ruby -*-
# vi: set ft=ruby :

NODE_COUNT = 2
CONTROLLER_IP = "192.168.56.100"
WORKER_IP_START = 101
CTRL_RAM = 4096
CTRL_CPUS = 2
NODE_RAM = 4096 # for testing purposes
NODE_CPUS = 2


Vagrant.configure("2") do |config|
  # Control node configuration
  config.vm.define "ctrl" do |ctrl|
    ctrl.vm.box = "bento/ubuntu-24.04"
    ctrl.vm.hostname = "ctrl"
    ctrl.vm.network "private_network", ip: CONTROLLER_IP
    
    ctrl.vm.provider "virtualbox" do |v|
      v.memory = CTRL_RAM
      v.cpus = CTRL_CPUS
    end

    # Ansible provisioning
    ctrl.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/general.yaml"
      ansible.inventory_path = "ansible/hosts.ini"
    end
    ctrl.vm.provision "ansible" do |ansible|
     ansible.inventory_path = "ansible/hosts.ini"
     ansible.playbook = "ansible/ctrl.yaml"
    end
  end

  # Worker nodes configuration
  (1..NODE_COUNT).each do |i|
    config.vm.define "node-#{i}" do |node|
      node.vm.box = "bento/ubuntu-24.04"
      node.vm.hostname = "node-#{i}"
      node.vm.network "private_network", ip: "192.168.56.#{WORKER_IP_START + i - 1}"
      
      node.vm.provider "virtualbox" do |v|
        v.memory = NODE_RAM
        v.cpus = NODE_CPUS
      end

      # Ansible provisioning
      node.vm.provision "ansible" do |ansible|
        ansible.playbook = "ansible/general.yaml"
        ansible.inventory_path = "ansible/hosts.ini"
      end
      node.vm.provision "ansible" do |ansible|
       ansible.inventory_path = "ansible/hosts.ini"
       ansible.playbook = "ansible/node.yaml"
      end
    end
  end
end
