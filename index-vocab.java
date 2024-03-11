import java.io.*;
import java.util.*;
import java.util.regex.*;

public class Indexing {

    public static void indexCorpus(String corpusDirectory, String indexFile) throws IOException {
        Set<String> uniqueWords = new HashSet<>();
        Map<String, List<String>> postingLists = new HashMap<>();
        String specialCharactersPattern = "[!?.,;'\\[\\]{}@\\(\\)\"]";

        File[] files = new File(corpusDirectory).listFiles();
        if (files != null) {
            for (File file : files) {
                String fileName = file.getName();
                try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                    String line;
                    StringBuilder contentBuilder = new StringBuilder();
                    while ((line = reader.readLine()) != null) {
                        contentBuilder.append(line.toLowerCase()).append(" ");
                    }
                    String content = contentBuilder.toString();
                    String documentId = fileName.split("\\.")[0];
                    for (String token : content.split("\\s+")) {
                        token = token.replaceAll(specialCharactersPattern, "");
                        if (!token.isEmpty()) {
                            uniqueWords.add(token);
                            postingLists.computeIfAbsent(token, k -> new ArrayList<>()).add(documentId);
                        }
                    }
                }
            }
        }

        List<String> sortedUniqueWords = new ArrayList<>(uniqueWords);
        Collections.sort(sortedUniqueWords);

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(indexFile))) {
            for (String token : sortedUniqueWords) {
                String posting = String.join(" ", postingLists.get(token));
                writer.write(token + "\t" + posting + "\n");
            }
        }
    }

    public static List<String> search(Map<String, List<String>> index, String queryTerm) {
        return index.getOrDefault(queryTerm, new ArrayList<>());
    }

    public static List<String> searchAnd(Map<String, List<String>> index, String term1, String term2) {
        Set<String> posting1 = new HashSet<>(search(index, term1));
        Set<String> posting2 = new HashSet<>(search(index, term2));
        posting1.retainAll(posting2);
        return new ArrayList<>(posting1);
    }

    public static List<String> searchOr(Map<String, List<String>> index, String term1, String term2) {
        Set<String> posting1 = new HashSet<>(search(index, term1));
        Set<String> posting2 = new HashSet<>(search(index, term2));
        posting1.addAll(posting2);
        return new ArrayList<>(posting1);
    }

    public static List<String> searchAndNot(Map<String, List<String>> index, String term1, String term2) {
        Set<String> posting1 = new HashSet<>(search(index, term1));
        Set<String> posting2 = new HashSet<>(search(index, term2));
        posting1.removeAll(posting2);
        return new ArrayList<>(posting1);
    }

    public static List<String> searchOrNot(Map<String, List<String>> index, String term1, String term2) {
        Set<String> posting1 = new HashSet<>(search(index, term1));
        Set<String> posting2 = new HashSet<>(search(index, term2));
        posting1.addAll(posting2);
        posting1.removeAll(searchAnd(index, term1, term2));
        return new ArrayList<>(posting1);
    }

    public static void main(String[] args) throws IOException {
        String directory = "D:/data_mining"; // Thay đổi đường dẫn này thành thư mục chứa tập văn bản của bạn.
        String corpusDirectory = directory + "/reuters/test";
        String indexFile = directory + "/index.txt";

        // Index the corpus and generate the posting lists
        indexCorpus(corpusDirectory, indexFile);
        System.out.println("Indexing completed. Posting lists saved to index.txt");

        // Các dòng code sau đây không cần thay đổi.

    Map<String, List<String>> index = new HashMap<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(indexFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split("\t");
                index.put(parts[0], Arrays.asList(parts[1].split("\\s+")));
            }
        }

        // Perform searches based on different query types
        System.out.println("Single-term Query:");
        System.out.println("america: " + search(index, "america"));

        System.out.println("\nTwo-term Query with AND:");
        System.out.println("america AND oil: " + searchAnd(index, "america", "oil"));

        System.out.println("\nTwo-term Query with OR:");
        System.out.println("america OR oil: " + searchOr(index, "america", "oil"));

        System.out.println("\nTwo-term Query with AND and NOT:");
        System.out.println("america AND (NOT oil): " + searchAndNot(index, "america", "oil"));

        System.out.println("\nTwo-term Query with OR and NOT:");
        System.out.println("america OR (NOT oil): " + searchOrNot(index, "america", "oil"));
    }
}
