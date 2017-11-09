#!/bin/bash

capture() {
 
build=$(curl -s http://192.168.1.234:8080/ekos/Build_Backup/ | grep deploy-offline.ga | awk '{print $6}'| grep deploy | sort -r | sed 's;.*deploy;deploy;g; s;tgz.*;tgz;g'|head -1)
 
echo "##################################"
 
echo "BUILD"
echo "#################################"
 
curl -O http://192.168.1.234:8080/ekos/Build_Backup/${build}
 
echo "################################"
}

decompression() {
 
echo ${build}
 
echo "##############################"
 
tar zxvf ${build}
 
echo "##############################"
}

bash() {
 
echo "BASH"
 
echo "#############################"
 
./deploy/deploy.sh
 
echo "#############################"

echo "complete bash"
}

ceph() {
 
echo "master"
 
ekoslet inventory init master:192.168.22.3:etcd:192.168.22.3:node:192.168.22.4
ekoslet ceph init rgw:192.168.22.3:mon:192.168.22.3:osd:192.168.22.3
 
ekoslet cluster set rgwvip:address 192.168.22.201
 
ekoslet cluster set rgwvip:port 7580
 
echo "#############################"
 
ekoslet keygen password
 
ekoslet ceph install >> /var/log/install_ceph.log
 
echo "#############################"
}

install() {
 
echo "#############################"
 
ekoslet cluster set loadbalancer_apiserver:address 192.168.22.202
ekoslet cluster set loadbalancer_apiserver:port 7443
 
ekoslet install >> /var/log/install_k8s.log
 
echo "#############################"
}

capture

decompression

bash

ceph

install
