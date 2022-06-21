import  logging
import schedule_resource_logger
from kubernetes import client, config
from botocore.exceptions import ClientError


SCHEDULE_ACTION_ENV_KEY = "K8s_SCHEDULE_ACTION"
LOG_PATH = "/var/log/ot/aws-resource-scheduler.log"


LOGGER = schedule_resource_logger._get_logging(LOG_PATH)


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


    
