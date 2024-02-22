def initialize_tree_of(graph):
  """Creates a new graph that has all the vertices of input graph and none of
  its edges. The function expects the input graph in adjacency matrix form and
  returns an edgeless copy of the graph also in adjacency matrix representation.
  """
  # What the input graph uses for infinity (any diagonal element should be inf)
  _ = graph[0][0]
  return [[ _ for i in range(len(graph))] for j in range(len(graph))]


def count_and_label(graph):
  """Labels vertices in the same component with the component count. As the
  function discovers new components, it increments the count value, and assigns
  it to every vertex in that component. The function expects the input graph in
  adjacency matrix form. It returns the count of components in the input graph
  and an list with each vertices component label.
  """
  # Initialize count of components
  count = 0
  # Initialize list of visited vertices for the depth-first traversal.
  visited = []
  # Initialize list with component labels for each vertex.
  comp = [-1] * len(graph)
  # Explore every vertex in the graph
  for u in range(len(graph)):
    # But only if we have not visited it before
    if u not in visited:
      # First time at this vertex: we just found a new component
      count += 1
      # Label this and adjacent vertices with this component count
      bag = [u]
      while bag:
        v = bag.pop()
        if v not in visited:
          visited.append(v)
          comp[v] = count
          for w in range(len(graph[v])):
            if graph[v][w] < graph[0][0]:
              bag.append(w)
  return count, comp
