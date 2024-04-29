#!/bin/bash

HOME="/mnt/share/virtualpc"
DIR_TEMPLATE="$HOME/templates"
IMG_TEMPLATE="ubuntu-22.04.4-live-server-amd64.iso"
VM_NAME="something"
VM_DIR="$HOME/$VM_NAME"

mkdir -p "$VM_DIR"

export MAC_ADDR=$(printf '52:54:%02x:%02x:%02x:%02x' $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)) $((RANDOM%256)))

echo $MAC_ADDR

export INTERFACE=eth01
export IP_ADDR=192.168.122.102

cat > "$VM_DIR/network-config" <<EOF
ethernets:
  $INTERFACE:
    - $IP_ADDR/24
    dhcp4: false
    gateway: 192.168.122.1
    match:
      macaddress: $MAC_ADDR
    nameservers:
      addresses:
        - 1.1.1.1
        - 8.8.8.8
    set-name: $INTERFACE
version: 2
EOF

cat > "$VM_DIR/user-data" <<EOF
#cloud-config
hostname: $VM_NAME
manage_etc_hosts: true
users:
  - name: aljo
    sudo: ALL=(ALL) NOPASSWD:ALL
    groups: users, admin
    home: /home/aljo
    shell: /bin/bash
    lock_passwd: false
ssh_pwauth: true
disable_root: false
chpasswd:
  list: |
    aljo:password
  expire: false
EOF

touch "$VM_DIR/meta-data"

# Create the disk image file before running virt-install
qemu-img create -f qcow2 "$VM_DIR/$VM_NAME.qcow2" 10G

cloud-localds -v --network-config="$VM_DIR/network-config" "$VM_DIR/$VM_NAME-seed.qcow2" "$VM_DIR/user-data" "$VM_DIR/meta-data"

chmod -R 777 "$VM_DIR"  # Set appropriate permissions

virt-install \
    --connect qemu:///system \
    --name "$VM_NAME" \
    --ram 1024 \
    --vcpus=2 \
    --os-type linux \
    --os-variant ubuntu22.04 \
    --cdrom "$DIR_TEMPLATE/$IMG_TEMPLATE" \
    --disk path="$VM_DIR/$VM_NAME.qcow2",device=disk \
    --disk path="$VM_DIR/$VM_NAME-seed.qcow2",device=disk \
    --import --network=default,model=virtio,mac="$MAC_ADDR"

