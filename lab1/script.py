import libvirt
import subprocess
import time


def list_vms():
    conn = libvirt.open('qemu:///system')
    if conn is None:
        print('Failed to open connection to qemu:///system')
        return

    print("List of available VMs:")
    vms = conn.listAllDomains()
    for vm in vms:
        print(vm.name())

def start_vm(vm_name):
    conn = libvirt.open('qemu:///system')
    if conn is None:
        print('Failed to open connection to qemu:///system')
        return

    try:
        vm = conn.lookupByName(vm_name)
        vm.create()
        print(f"VM {vm_name} started successfully.")
    except libvirt.libvirtError as e:
        print(f"Failed to start VM {vm_name}: {e}")

def shutdown_vm(vm_name):
    conn = libvirt.open('qemu:///system')
    if conn is None:
        print('Failed to open connection to qemu:///system')
        return

    try:
        vm = conn.lookupByName(vm_name)
        vm.shutdown()
        print(f"Shutting down VM {vm_name}...")
    except libvirt.libvirtError as e:
        print(f"Failed to shutdown VM {vm_name}: {e}")

def monitor_vm_info(vm_name):
    conn = libvirt.open('qemu:///system')
    if conn is None:
        print('Failed to open connection to qemu:///system')
        return

    try:
        vm = conn.lookupByName(vm_name)
        info = vm.info()
        info_cpu = vm.getCPUStats(True)
        memoria_vm = vm.memoryStats()
        print(f"VM Name: {vm_name}")
        print(f"State: {info[0]}")  # State is numeric, not an enum
        print(f"Max memory: {info[1]} KB")
        print(f"Number of virtual CPUs: {info[3]}")
        print(f"CPU time: {info[2]} ms")
        print(f"RAM Usage: {memoria_vm['rss'] / 1048576:.2f} MB")
    except libvirt.libvirtError as e:
        print(f"Failed to get information for VM {vm_name}: {e}")

       
def set_cpu_percentage(vm_name, user, ip, percentage):    	
    # Define the command to set CPU percentage
    cmd = ["ssh", str(user+'@'+ip), "stress-ng", "--cpu", "2", "--cpu-load", str(percentage), "--timeout", "30s"]

    try:
        # Execute the command
        result = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(15)

        print(f"CPU percentage set to {percentage}% for VM {vm_name}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set CPU percentage for VM {vm_name}: {e}")
        
def live_migrate_vm(vm_name_source, percentage):
    try:
        # Connect to the source hypervisor
        src_conn = libvirt.open('qemu:///system')
        if src_conn is None:
            print('Failed to open connection to qemu:///system')
            return

        # Connect to the destination hypervisor
        dest_conn = libvirt.open('qemu+ssh://{user}@{ip}/system')
        if dest_conn is None:
            print('Failed to open connection to qemu+ssh://{user}@{ip}/system')
            return

        # Find the source domain
        dom = src_conn.lookupByName(vm_name_source)
        if dom is None:
            print('Failed to find the domain ' + vm_name_source)
            return

        # Migrate the domain to the destination hypervisor
        new_dom = dom.migrate(dest_conn, libvirt.VIR_MIGRATE_LIVE, None, None, 0)
        if not new_dom:
            raise RuntimeError("Could not migrate to the new domain")

        print('Migration complete')

    except Exception as e:
        print('Error occurred during migration:', e)

    finally:
        # Close connections
        if src_conn is not None:
            src_conn.close()
        if dest_conn is not None:
            dest_conn.close()

def main():
    while True:
        print("================================================")
        print("\nMenu:")
        print("1. List all VMs")
        print("2. Start a VM")
        print("3. Shut down a VM")
        print("4. Monitor VM information")
        print("5. Set CPU percentage for a VM")
        print("6. Live migrate VM based on condition (e.g., CPU >= 70%)")
        print("7. Exit")

        choice = input("Enter your choice: ")
        print("==================================================\n")
        if choice == '1':
            list_vms()
        elif choice == '2':
            vm_name = input("Enter the name of the VM to start: ")
            start_vm(vm_name)
        elif choice == '3':
            vm_name = input("Enter the name of the VM to shut down: ")
            shutdown_vm(vm_name)
        elif choice == '4':
            vm_name = input("Enter the name of the VM to monitor: ")
            monitor_vm_info(vm_name)
        elif choice == '5':
            vm_name = input("Enter the name of the VM: ")
            user = input("Enter the name of the user: ")
            ip = input("Enter the IP Address: ")
            percentage = int(input("Enter the CPU percentage (1-100): "))
            if 1 <= percentage <= 100:
                set_cpu_percentage(vm_name, user, ip, percentage)
            else:
                print("Invalid CPU percentage. Please enter a value between 1 and 100.")
        elif choice == '6':
            vm_name_source = input("Enter the name of the source VM: ")
            cpu_threshold = float(input("Enter the CPU threshold percentage (e.g., 70): "))
            live_migrate_vm(vm_name_source, cpu_threshold)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

