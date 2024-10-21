from django.db import models


class Vertex(models.Model):
    name = models.CharField(max_length=100)


class Edge(models.Model):
    from_vertex = models.ForeignKey(
        Vertex,
        related_name='outgoing_edges',
        on_delete=models.CASCADE)
    to_vertex = models.ForeignKey(
        Vertex,
        related_name='incoming_edges',
        on_delete=models.CASCADE)
