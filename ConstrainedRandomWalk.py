import scipy.sparse as sparse
import numpy as np

class ConstrainedRandomWalk:
  def __init__(self, time_series, m, t):
    self.time_series = time_series
    self.embedding_dimension = m
    self.permutation_to_vertex = {}
    self.permutation_to_zvectors = {}
    self.vertex_to_permutation = {}
    self.lag = t
    self.z_vectors = self.generate_z_vectors(time_series, m, t)
    self.adjacency_matrix = self.build_adjacency_matrix(time_series, m, t)
    self.restored_dynamics = []

  def build_adjacency_matrix(self, time_series, m, t):
    adjacency_matrix = sparse.dok_matrix((np.math.factorial(m), np.math.factorial(m)), dtype=np.intc)

    for idx, z_vector_current in enumerate(self.z_vectors):
      if idx + 1 < self.z_vectors.shape[0]: #the last vertex in graph may be ommited, but it will be isolated in such a case
        permutation_current = self.get_permutation(z_vector_current)
        permutation_next = self.get_permutation(self.z_vectors[idx + 1])
        vertex_current_idx = self.map_permutation_to_vertex(permutation_current)
        vertex_next_idx = self.map_permutation_to_vertex(permutation_next)

        if adjacency_matrix[vertex_current_idx, vertex_next_idx] is None:
          adjacency_matrix[vertex_current_idx, vertex_next_idx] = 1
        else :
          adjacency_matrix[vertex_current_idx, vertex_next_idx] += 1

    return adjacency_matrix

  def generate_z_vectors(self, time_series, m, t):
    z_vectors = []

    for i in range(time_series.size):
      z_vector = np.empty(m, dtype=np.float)
      z_vector[0] = time_series[i]

      for j in range(1, m):
        if i + j * t < time_series.size:
          z_vector[j] = time_series[i + j * t]
        else:
          z_vector = None

      if z_vector is not None:
        z_vectors.append(z_vector)
    return np.array(z_vectors)

  def get_permutation(self, z_vector):
    indexes = np.argsort(np.argsort((-z_vector)))

    if tuple(indexes) in self.permutation_to_zvectors:
      self.permutation_to_zvectors[tuple(indexes)].append(z_vector)
    else:
      self.permutation_to_zvectors[tuple(indexes)] = [z_vector]

    return indexes

  def map_permutation_to_vertex(self, permutation):
    permutation_tuple = tuple(permutation)
    ret_val = -1

    if permutation_tuple in self.permutation_to_vertex:
      ret_val = self.permutation_to_vertex[permutation_tuple]
    else:
      ret_val = self.permutation_to_vertex[permutation_tuple] = len(self.permutation_to_vertex) + 1
      self.vertex_to_permutation[ret_val] = permutation_tuple

    if ret_val == -1:
      raise ValueError('ret_val is -1')

    return ret_val

  def constrained_random_walk(self, length = 1000):
    init_seed = np.random.randint(0, self.z_vectors.shape[0] - self.lag)
    restored_dynamics = self.init_restored_dynamics(init_seed)
    ptr = self.lag - 1
    blocked_nodes = [[]] * length

    while ptr < length:
      print(ptr)
      current_node = restored_dynamics[ptr]
      allowable_transitions = []

      for i in range(ptr+1, len(blocked_nodes)):
        blocked_nodes[i] = []

      all_possible_transitions = self.get_all_possible_transitions(current_node)

      for transition in all_possible_transitions:
        if self.is_allowable_transition(restored_dynamics[ptr - self.lag + 1], transition):
          allowable_transitions.append(transition)

      allowable_transitions = self.remove_blocked_nodes(allowable_transitions, blocked_nodes[ptr])

      if len(allowable_transitions) > 0:
        ptr += 1
        next_node = self.choose_transition(current_node, allowable_transitions)
        if ptr >= len(restored_dynamics):
          restored_dynamics.append(next_node)
        else:
          restored_dynamics[ptr] = next_node
      else:
        ptr -= 1
        blocked_nodes[ptr].append(current_node)

      if ptr < self.lag:
        raise ValueError('No path can be found from initial seed')

    self.restored_dynamics = restored_dynamics
    return restored_dynamics

  def init_restored_dynamics(self, init_seed):
    restored_dynamics = []
    for i in range(self.lag):
      restored_dynamics.append(tuple(self.get_permutation(self.z_vectors[init_seed + i])))

    return restored_dynamics

  def get_all_possible_transitions(self, current_node):
    transitions = []
    i = self.permutation_to_vertex[tuple(current_node)]
    for key in self.adjacency_matrix.keys():
      if key[0] == i:
        transitions.append(self.vertex_to_permutation[key[1]])
    return transitions

  def is_allowable_transition(self, previous_node, next_node):
    for i in range(1, len(previous_node)):
      if i + 1 == len(previous_node):
        return 1
      if (previous_node[i] - previous_node[i+1]) * (next_node[i-1] - next_node[i]) < 0:
        return 0
    return 1

  def remove_blocked_nodes(self, allowable_transitions, blocked_nodes):
    np_allowable = np.array(allowable_transitions)
    np_blocked = np.array(blocked_nodes)
    constrained_transitions = []

    for allowable in np_allowable:
      to_add = True
      for blocked in np_blocked:
        if np.array_equal(blocked, allowable):
          to_add = False
          break
      if to_add:
        constrained_transitions.append(tuple(allowable.tolist()))

    return constrained_transitions

  def choose_transition(self, current_node, allowable_transitions):
    weights = []
    current_row_idx = self.permutation_to_vertex[current_node]
    for transition in allowable_transitions:
      weights.append(self.adjacency_matrix.get((current_row_idx, self.permutation_to_vertex[transition])))

    idx = np.random.choice(len(weights), p=weights/np.sum(weights))
    return allowable_transitions[idx]

  def regenerate_time_series(self, length):
    restored_dynamics = self.constrained_random_walk(length)
    regenerated_time_series = []

    for node in restored_dynamics:
      z_vectors = self.permutation_to_zvectors[node]
      idx = np.random.randint(len(z_vectors))
      regenerated_time_series.append(z_vectors[idx][0])

    return np.array(regenerated_time_series)

