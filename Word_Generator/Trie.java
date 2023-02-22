
public class Trie<T> {
    TrieNode<T> root;

    /* Constructor that sets the root to a new node */
    public Trie() {
        root = new TrieNode<T>();
    }

    /*
     * Get Node function which find the Node accocsiated with the input. This is
     * done by traversing the tree using the getchild function on each of the string
     * chars. Doing so will yeild the correct node for the input.
     */
    private TrieNode<T> getNode(String input) {
        TrieNode<T> ret = root;
        for (int i = 0; i < input.length(); i++) {
            ret = ret.getChild(input.charAt(i));
        }

        return ret;
    }

    /*
     * Put function which populates the trie with the given data. The getNode
     * function is used to figure out if the string is in the trie or not. if not a
     * new node is created and its data is set to the input. if the string input is
     * already in the trie then the data is simply overwritten with the input data
     */
    public void put(String input, T data) {
        TrieNode<T> tracker = getNode(input);
        if (tracker == null) {
            tracker = new TrieNode<T>();
        }

        tracker.setData(data);

    }

    /*
     * Get function which takes a string and returns the data accocsiated with that
     * string in the trie. This is done by using the getNode which returns the
     * correct node for the string. Then the data at that node is returned
     */
    public T get(String input) {
        TrieNode<T> tracker = getNode(input);
        if (tracker == null) {
            return null;
        }

        return tracker.getData();

    }
}
