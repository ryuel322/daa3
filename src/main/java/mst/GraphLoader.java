package mst;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import java.io.File;
import java.io.IOException;
import java.util.*;

public class GraphLoader {
    private static final ObjectMapper mapper = new ObjectMapper();
    private static final Random random = new Random(42);

    public static Map<String, List<Graph>> loadAllGraphs() throws IOException {
        Map<String, List<Graph>> graphsByCategory = new HashMap<>();

        // Load your input file
        graphsByCategory.put("test", parseInputFile("graphs/ass3_input.json"));

        // Generate and load other categories
        generateAllGraphs();
        graphsByCategory.put("small", parseInputFile("graphs/small_graphs.json"));
        graphsByCategory.put("medium", parseInputFile("graphs/medium_graphs.json"));
        graphsByCategory.put("large", parseInputFile("graphs/large_graphs.json"));
        graphsByCategory.put("extra_large", parseInputFile("graphs/extra_large_graphs.json"));

        return graphsByCategory;
    }

    public static List<Graph> parseInputFile(String filename) throws IOException {
        List<Graph> graphs = new ArrayList<>();
        JsonNode root = mapper.readTree(new File(filename));
        JsonNode graphsNode = root.path("graphs");

        for (JsonNode graphNode : graphsNode) {
            int id = graphNode.path("id").asInt();
            JsonNode nodesNode = graphNode.path("nodes");
            JsonNode edgesNode = graphNode.path("edges");

            Map<String, Integer> nodeMap = new HashMap<>();
            int vertexCount = nodesNode.size();
            Graph graph = new Graph(vertexCount);

            for (int i = 0; i < vertexCount; i++) {
                String nodeName = nodesNode.get(i).asText();
                nodeMap.put(nodeName, i);
            }

            for (JsonNode edgeNode : edgesNode) {
                String from = edgeNode.path("from").asText();
                String to = edgeNode.path("to").asText();
                int weight = edgeNode.path("weight").asInt();

                graph.addEdge(nodeMap.get(from), nodeMap.get(to), weight);
            }

            graphs.add(graph);
        }

        return graphs;
    }

    public static void generateAllGraphs() throws IOException {
        new File("graphs").mkdirs();
        new File("results").mkdirs();

        generateCategoryGraphs("small_graphs", 5, 30, 0.4, 0.6);
        generateCategoryGraphs("medium_graphs", 10, 300, 0.2, 0.4);
        generateCategoryGraphs("large_graphs", 10, 1000, 0.1, 0.2);
        generateExtraLargeGraphs();
    }

    private static void generateCategoryGraphs(String filename, int count, int vertices,
                                               double minDensity, double maxDensity) throws IOException {
        ObjectNode root = mapper.createObjectNode();
        ArrayNode graphsArray = mapper.createArrayNode();

        for (int i = 1; i <= count; i++) {
            double density = minDensity + random.nextDouble() * (maxDensity - minDensity);
            graphsArray.add(createGraphData(i, vertices, density));
        }

        root.set("graphs", graphsArray);
        mapper.writerWithDefaultPrettyPrinter()
                .writeValue(new File("graphs/" + filename + ".json"), root);
    }

    private static void generateExtraLargeGraphs() throws IOException {
        ObjectNode root = mapper.createObjectNode();
        ArrayNode graphsArray = mapper.createArrayNode();

        graphsArray.add(createGraphData(1, 1300, 0.08));
        graphsArray.add(createGraphData(2, 1600, 0.06));
        graphsArray.add(createGraphData(3, 2000, 0.05));

        root.set("graphs", graphsArray);
        mapper.writerWithDefaultPrettyPrinter()
                .writeValue(new File("graphs/extra_large_graphs.json"), root);
    }

    private static ObjectNode createGraphData(int id, int vertices, double density) {
        ObjectNode graphNode = mapper.createObjectNode();
        graphNode.put("id", id);

        ArrayNode nodesArray = mapper.createArrayNode();
        for (int i = 0; i < vertices; i++) {
            nodesArray.add("N" + i);
        }
        graphNode.set("nodes", nodesArray);

        ArrayNode edgesArray = mapper.createArrayNode();
        Graph graph = generateConnectedGraph(vertices, density);

        for (Edge edge : graph.getEdges()) {
            ObjectNode edgeNode = mapper.createObjectNode();
            edgeNode.put("from", "N" + edge.getSource());
            edgeNode.put("to", "N" + edge.getDestination());
            edgeNode.put("weight", edge.getWeight());
            edgesArray.add(edgeNode);
        }

        graphNode.set("edges", edgesArray);
        return graphNode;
    }

    private static Graph generateConnectedGraph(int vertices, double density) {
        Graph graph = new Graph(vertices);

        for (int i = 1; i < vertices; i++) {
            int parent = random.nextInt(i);
            int weight = 1 + random.nextInt(100);
            graph.addEdge(parent, i, weight);
        }

        int maxEdges = vertices * (vertices - 1) / 2;
        int targetEdges = Math.max(vertices - 1, (int)(maxEdges * density));
        int currentEdges = vertices - 1;

        while (currentEdges < targetEdges) {
            int u = random.nextInt(vertices);
            int v = random.nextInt(vertices);
            if (u != v) {
                int weight = 1 + random.nextInt(100);
                graph.addEdge(u, v, weight);
                currentEdges++;
            }
        }

        return graph;
    }
}