from kubernetes import  config

def _create_k8s_session(k8s_context=None):

    if k8s_context:
        config.load_kube_config(context=k8s_context)
    else:
        config.load_kube_config(context="minikube")

