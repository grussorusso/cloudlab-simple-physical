# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Only Ubuntu images supported.
imageList = [
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD', 'UBUNTU 20.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU18-64-STD', 'UBUNTU 18.04'),
]

pc.defineParameter("clientCount", "Number of Compute Nodes (1-10)",
                   portal.ParameterType.INTEGER, 1)

pc.defineParameter("osImage", "Select OS image",
                   portal.ParameterType.IMAGE,
                   imageList[0], imageList)

pc.defineParameter("phystype",  "Optional physical node type",
                   portal.ParameterType.STRING, "c6320",
                   longDescription="Specify a physical node type (pc3000,d710,etc) " +
                   "instead of letting the resource mapper choose for you.")

pc.defineParameter("localStorage", "Extra local storage in GB",
                   portal.ParameterType.INTEGER, 0)



# Always need this when using parameters
params = pc.bindParameters()

# The NFS network. All these options are required.
nfsLan = request.LAN("myLan")
nfsLan.best_effort       = True
nfsLan.vlan_tagging      = True
nfsLan.link_multiplexing = True


for i in range(1, params.clientCount+1):
    node = request.RawPC("node%d" % i)
    node.disk_image = params.osImage
    # Initialization script for the clients
    nfsLan.addInterface(node.addInterface())
    if params.phystype != "":
        node.hardware_type = params.phystype
    if params.localStorage != 0:
	    bsName="bs"+str(i)
        bs = node.Blockstore(bsName, "/mydata")
        bs.size=str(params.localStorage)+"GB"


# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
