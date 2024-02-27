from collections import OrderedDict

from ..utils.consts import KCt

class _NodesMixin:
  def __init__(self):
    super(_NodesMixin, self).__init__()
    return


  def get_all_nodes(self):
    """
    Retrieves all nodes in the cluster along with their status.

    Returns
    -------
    list
        A list of nodes and their statuses.
    """
    node_info = []
    try:
      nodes = self.v1.list_node()
      for node in nodes.items:
        memory = node.status.capacity['memory']
        cpu = node.status.capacity['cpu']
        memory_bytes = self.convert_memory_to_bytes(memory)
        conditions = {condition.type: condition.status for condition in node.status.conditions}
        node_info.append({
          'name': node.metadata.name,
          'status': 'Ready' if conditions.get('Ready') == 'True' else 'Not Ready',
          'conditions': conditions
        })
    except Exception as exc:
      self._handle_exception(exc)
      node_info = []
    return node_info


  def get_nodes_metrics(self):
    """
    Fetches metrics for all nodes and converts them to readable units.

    Returns
    -------
    list
        A list of nodes with their CPU (in millicores) and memory usage (in GiB).
    """
    node_metrics = self.custom_api.list_cluster_custom_object(
      group="metrics.k8s.io",
      version="v1beta1",
      plural="nodes"
    )
    metrics_list = []
    for node in node_metrics.get('items', []):
      cpu_usage_millicores = int(node['usage']['cpu'].rstrip('n')) / 1e6  # Convert nanocores to millicores
      memory_usage_gib = int(node['usage']['memory'].rstrip('Ki')) / (1024**2)  # Convert KiB to GiB
      metrics_list.append({
        'name': node['metadata']['name'],
        'cpu_usage_cores': round(cpu_usage_millicores / 1000, 3),
        'memory_usage_gib': round(memory_usage_gib, 2)
      })
    return metrics_list  

