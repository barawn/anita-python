echo "  "
echo "  "
echo "Setting up the PCI..."
echo "  "
sudo modprobe vfio-pci
echo "  " 
sudo bash -c "echo 10ee ff01 > /sys/bus/pci/drivers/vfio-pci/new_id"
echo "10ee f01 has been assigned the uio_pci_generic driver"
sudo bash -c "echo 10ee ff00 > /sys/bus/pci/drivers/vfio-pci/new_id"
echo "10ee f00 has been assigned the uio_pci_generic driver"
sudo chown anita.anita /dev/vfio/1
echo "permission changed on /dev/vfio/1"
echo "  "
echo "  "
echo "PCI set-up complete" 
echo "  "
echo "  "
