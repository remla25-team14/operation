WORKER_COUNT = 2

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-24.04"
  config.vm.box_version = "202502.21.0"

  config.vm.define "ctrl" do |ctrl|
    ctrl.vm.hostname = "ctrl"
    ctrl.vm.network "private_network", ip: "192.168.56.100"
    
    ctrl.vm.provider "virtualbox" do |v|
      v.memory = 4096  
      v.cpus = 1       
    end

    # provision controller node with ansible
    ctrl.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/general.yaml"
      ansible.inventory_path = "ansible/inventory.ini"
      ansible.limit = "all"
      ansible.extra_vars = {
        worker_count: WORKER_COUNT
      }
    end

    ctrl.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/ctrl.yaml"
      ansible.inventory_path = "ansible/inventory.ini"
      ansible.limit = "ctrl"
    end
  end

  (1..WORKER_COUNT).each do |i|
    config.vm.define "node-#{i}" do |node|
      node.vm.hostname = "node-#{i}"
      node.vm.network "private_network", ip: "192.168.56.#{100 + i}"
      
      node.vm.provider "virtualbox" do |v|
        v.memory = 6144  
        v.cpus = 2       
      end

      node.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "ansible/general.yaml"
        ansible.inventory_path = "ansible/inventory.ini"
        ansible.limit = "all"
        ansible.extra_vars = {
          worker_count: WORKER_COUNT
        }
      end

      if i == WORKER_COUNT
        node.vm.provision "ansible_local" do |ansible|
          ansible.playbook = "ansible/worker.yaml"
          ansible.inventory_path = "ansible/inventory.ini"
          ansible.limit = "node*"
        end
        
        # register ssh keys on the vm's (moved to after all nodes are created)
        node.vm.provision "ansible_local" do |ansible|
          ansible.playbook = "ansible/ssh_keys.yaml"
          ansible.inventory_path = "ansible/inventory.ini"
          ansible.limit = "all"
        end
      end
    end
  end

  config.vm.provider "virtualbox" do |v|
    v.gui = false
    v.linked_clone = true
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y ansible
  SHELL
end 