# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "trusty64"
  config.vm.box_url = "https://vagrantcloud.com/ubuntu/boxes/trusty64/versions/14.04/providers/virtualbox.box"

  config.vm.hostname = "local.terrarium.org"
  config.vm.network "private_network", ip: "192.168.15.10"

  config.vm.provider "virtualbox" do |v|
    v.name = "terrarium"
    v.memory = "2048"
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/development.yml"
  end

  config.vm.synced_folder ".", "/home/vagrant", type: "rsync",
      rsync__exclude: ".git/",
      rsync__args: ["--verbose", "--archive", "-z", "--copy-links"]

end
