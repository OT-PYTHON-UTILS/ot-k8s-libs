from kubernetes import client, config

class k8sActions:
    def __init__(self, cli):
        self.cli = cli

    def deployment_having_annotation(self, namespace, deployment_annot):
        self.namespace = namespace
        self.deployment_annot = deployment_annot

        deployments = []
        annotation = list(self.deployment_annot)
        for x in range(len(self.cli.list_namespaced_deployment(namespace=self.namespace).items)):
            try:
                if self.cli.list_namespaced_deployment(namespace=self.namespace).items[x].metadata.annotations[annotation[0]] == "true" :
                    deployments.append(self.cli.list_namespaced_deployment(
                        namespace=self.namespace).items[x].metadata.name)
            except:
                pass
        return deployments


    
    def deployment_replica_change(self, properties, deployments, namespace, action):
        self.properties = properties
        self.deployments = deployments
        self.namespace = namespace
        self.action = action


        if self.action == "start": 
            replicas = self.properties['k8s']['replicas']
        else:
            replicas = 0

        for deployment in self.deployments:
            body = {"apiVersion": "apps/v1", "kind": "Deployment",
                    "spec": {"replicas": replicas, }}
            print(self.cli.patch_namespaced_deployment_scale(
                namespace=self.namespace, name=deployment, body=body))


    
