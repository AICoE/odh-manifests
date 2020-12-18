from kubernetes.client import V1Capabilities, V1SELinuxOptions
spawner = c.OpenShiftSpawner

def idh_apply_pod_profile(spawner, pod):
  """
  This method is responsible for modifying the final notebook pod spec before submitting it to the k8s api
  Modifying the pod based on the V1Pod and V1PodSpec avaialable in the kubernetes python API
  https://github.com/kubernetes-client/python/blob/master/kubernetes/docs
  """
  # Apply profile from singleuser-profiles
  apply_pod_profile(spawner, pod)

  # Pod container zero is the 'notebook' container with the env var we need to check
  nb_container_env = pod.spec.containers[0].env

  if spawner.gpu_mode and spawner.gpu_mode == "selinux" and \
       spawner.extra_resource_limits and "nvidia.com/gpu" in spawner.extra_resource_limits:
    # Currently a bug in RHEL Docker 1.13 whereby /dev IPC dirs get inconsistent MCS
    pod.spec.security_context.se_linux_options = V1SELinuxOptions(type='nvidia_container_t',level='s0')

  for item in nb_container_env:
    if item.name == "ENABLE_HOST_IPC":
      pod.spec.host_ipc = True

  return pod
spawner.modify_pod_hook = idh_apply_pod_profile
