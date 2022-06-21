from kubernetes import client, config

class k8sActions:
    def __init__(self, cli):
        self.cli = cli


    def statefulset_having_annotation(self, namespace, sts_annot):
        self.namespace = namespace
        self.sts_annot = sts_annot

        statefulset = []
        annotation = list(self.sts_annot)
        for x in range(len(self.cli.list_namespaced_stateful_set(namespace=self.namespace).items)):
            try:
                if self.cli.list_namespaced_stateful_set(namespace=self.namespace).items[x].metadata.annotations[annotation[0]] == "true" :
                    statefulset.append(self.cli.list_namespaced_stateful_set(
                        namespace=self.namespace).items[x].metadata.name)
            except:
                pass
        return statefulset
    

    def statefulset_replica_change(self, properties, statefulset, namespace, action):
        self.properties = properties
        self.statefulset = statefulset
        self.namespace = namespace
        self.action = action

        if self.action == "start": 
            replicas = self.properties['k8s']['replicas']
        else:
            replicas = 0

        for statefulset in self.statefulset:
            body = {"apiVersion": "apps/v1", "kind": "StatefulSet",
                    "spec": {"replicas": replicas, }}
            print(self.cli.patch_namespaced_stateful_set_scale(
                namespace=self.namespace, name=statefulset, body=body))


    
