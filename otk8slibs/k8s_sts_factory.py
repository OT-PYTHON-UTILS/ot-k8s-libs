class k8sStsActions:
    def __init__(self, cli):
        self.cli = cli


    def _get_statefulsets_with_annotation(self, namespace, sts_annot):
        self.namespace = namespace
        self.sts_annot = sts_annot

        statefulsets = []
        annotations = list(self.sts_annot)
        for statefulset in range(len(self.cli.list_namespaced_stateful_set(namespace=self.namespace).items)):
            try:
                if self.cli.list_namespaced_stateful_set(namespace=self.namespace).items[statefulset].metadata.annotations[annotations[0]] == "true" :
                    statefulsets.append(self.cli.list_namespaced_stateful_set(
                        namespace=self.namespace).items[statefulset].metadata.name)
            except:
                pass
        return statefulsets


    def statefulsets_replica_change(self, properties, statefulsets, namespace, action):
        self.properties = properties
        self.statefulsets = statefulsets
        self.namespace = namespace
        self.action = action

        if self.action == "start":
            replicas = self.properties['k8s']['replicas']
        else:
            replicas = 0

        for statefulset in self.statefulsets:
            body = {"apiVersion": "apps/v1", "kind": "StatefulSet",
                    "spec": {"replicas": replicas, }}
            return(self.cli.patch_namespaced_stateful_set_scale(
                namespace=self.namespace, name=statefulset, body=body))

