WORKER_COUNT = 2

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-24.04"
  config.vm.box_version = "202404.26.0"

  config.vm.define "ctrl" do |ctrl|
    ctrl.vm.hostname = "ctrl"
    ctrl.vm.network "private_network", ip: "192.168.56.100"
    
    ctrl.vm.provider "virtualbox" do |v|
      v.memory = 4096  
      v.cpus = 1       
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
    end
  end
  config.vm.provider "virtualbox" do |v|
    v.gui = false
    v.linked_clone = true
  end
end 