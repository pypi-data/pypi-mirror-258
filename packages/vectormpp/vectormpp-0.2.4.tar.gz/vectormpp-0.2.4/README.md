# Actian VectorMPP Installer

Actian VectorMPP represents a sophisticated deployment of Actian’s Multi-node Vector Cluster within a Kubernetes environment. \
This deployment encompasses an extensive array of Kubernetes resources, accompanied by intricate configuration settings.

To facilitate a streamlined installation process, we have developed the Actian VectorMPP Installer. \
The installer is distributed as a Python package, officially registered within the Python Package Index (PyPi).

The installation process of the Actian VectorMPP Installer is straightforward:
```
pip install vectormpp
```

For assistance and command options, use: `vectormpp -h` \
This command provides usage instructions and a list of available options, including but not limited to specifying work directories, setting log levels, and executing install or uninstall commands.

## The design behind the installer

The Actian VectorMPP Installer offers a range of functionalities designed to accommodate diverse customer needs, including those with varying Kubernetes cluster configurations and pre-existing Kubernetes resources.

Central to this customization capability is [Actian VectorMPP Manifest](https://alm.actian.com/bitbucket/users/rxiao/repos/vectormpp-manifest/) — a collection of text files outlining the architecture of Actian VectorMPP. \
The `vectormpp` installer, leveraging *Manifest*, acts as a versatile tool capable of applying these Kubernetes resources and configurations to customers' Kubernetes clusters. \
This approach enables potential use cases beyond Actian VectorMPP, applicable to any Kubernetes project with *Manifest* describing its architecture.

## Examples

### Deploy Actian VectorMPP in a clean GKE cluster
Get the corresponding Manifest _clean-gke_ from our .
Clone [Actian VectorMPP Manifest repo](https://alm.actian.com/bitbucket/users/rxiao/repos/vectormpp-manifest/) to obtain the appropriate manifest file for a clean GKE cluster:
```
git clone https://alm.actian.com/bitbucket/scm/~rxiao/vectormpp-manifest.git
```

Customize your Actian VectorMPP installation by modifying the config.yaml file within the cloned repository:
```
vim vectormpp-manifest/clean-gke/config.yaml
```

Execute the installer using one of the following methods, specifying the path to your Manifest folder:
```
vectormpp --manifest vectormpp-manifest/clean-gke --install
vectormpp -m vectormpp-manifest/clean-gke -i
```
Or navigate to the Manifest directory and run:
```
cd vectormpp-manifest/clean-gke && vectormpp -i
```

