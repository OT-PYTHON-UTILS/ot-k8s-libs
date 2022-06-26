class k8sDeploymentActions:
    def __init__(self, cli):
        self.cli = cli

    def _get_deployments_with_annotation(self, namespace, deployment_annot):
        self.namespace = namespace
        self.deployment_annot = deployment_annot

        deployments = []
        annotations = list(self.deployment_annot)
        for deployment in range(len(self.cli.list_namespaced_deployment(namespace=self.namespace).items)):
            try:
                if self.cli.list_namespaced_deployment(namespace=self.namespace).items[deployment].metadata.annotations[annotations[0]] == "true":
                    deployments.append(self.cli.list_namespaced_deployment(
                        namespace=self.namespace).items[deployment].metadata.name)
            except:
                pass
        return deployments

    def deployments_replica_change(self, properties, deployments, namespace, action):
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
            return(self.cli.patch_namespaced_deployment_scale(
                namespace=self.namespace, name=deployment, body=body))
