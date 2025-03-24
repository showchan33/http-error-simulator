registry = os.getenv("TILT_DEFAULT_REGISTRY")
if registry:
  default_registry(registry)

docker_build("http-error-simulator", "./app")
k8s_yaml("k8s/deployment.yaml")
k8s_yaml("k8s/service.yaml")
k8s_yaml("k8s/ingress.yaml")
